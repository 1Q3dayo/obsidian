---
title: "AWS DevOps Agent (Preview)のEKSアクセス設定をやってみた #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/aws-devops-agent-preview-eks-access/"
author: ""
published: "2025-12-06"
created: "2025-12-09"
description: ""
tags:
  - ""
  - "raw"
---

こんにちは。たかやまです。

AWS DevOps Agentは、エージェントの機能を最大化させるために以下の機能（Capabilitie）が追加できます。  
各機能を紹介しているブログのリンクを貼っているのでこちらも参考にしてください。

| 機能カテゴリ | 説明 | 参考ブログ |
| --- | --- | --- |
| AWS EKS アクセス設定 | パブリックとプライベート両方の EKS 環境で、Kubernetes クラスター、ポッドログ、クラスターイベントの検査を有効化する | こちらのブログ |
| CI/CD パイプライン統合 | GitHub と GitLab パイプラインを接続してデプロイメントをインシデントと関連付け、調査中のコード変更を追跡する | [AWS DevOps AgentがどこまでCDKの設定ミスを特定してくれるのか試してみた](https://dev.classmethod.jp/articles/awsreinvent-devops-agent-cdk-miss-config/) |
| MCP サーバー接続 | Model Context Protocol を通じて外部の可観測性ツールおよびカスタム監視システムを接続して、調査機能を拡張する | [AWS DevOps AgentがどこまでCDKの設定ミスを特定してくれるのか試してみた](https://dev.classmethod.jp/articles/awsreinvent-devops-agent-cdk-miss-config/) |
| マルチアカウントAWSアクセス | インシデント対応中に組織全体のリソースを調査するためにセカンダリ AWS アカウントを設定する | [AWS DevOps Agent (Preview)のマルチアカウントアクセスをやってみた](https://dev.classmethod.jp/articles/aws-devops-agent-multi-account-access/) |
| テレメトリーソース統合 | Datadog、New Relic、Splunk などの監視プラットフォームを接続して、包括的な可観測性データへのアクセスを実現する | [AWS DevOps Agent（Preview）の Datadog MCP サーバ連携をやってみた](https://dev.classmethod.jp/articles/aws-devops-agent-datadog-mcp-connect/) |
| チケティングおよびチャット統合 | ServiceNow、PagerDuty、Slack を接続してインシデント対応ワークフローを自動化し、チーム コラボレーションを実現する | [AWS DevOps Agent (Preview)のSlack連携をやってみた](https://dev.classmethod.jp/articles/aws-devops-agent-slack-integration/) |
| Webhook 設定 | 外部システムが HTTP リクエストを通じて DevOps Agent の調査を自動的にトリガーできるようにする | [AWS DevOps Agent (Preview)のPagerDuty連携とWebhook設定をやってみようとした](https://dev.classmethod.jp/articles/aws-devops-agent-preview-pagerduty-webhook-integration/) |

[Configuring capabilities for AWS DevOps Agent - AWS DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-capabilities.html)

今回は、EKSアクセス設定の有無でDevOps AgentのEKS調査能力がどう変わるのかを検証してみました。

## さきにまとめ

- DevOps AgentにEKSアクセスを許可することで、Pod状態やKubernetesイベントを直接取得できる
- 設定はEKS Access EntriesでDevOps Agentが利用する `DevOpsAgentRole` に `AIOpsAssistantPolicy` を付与するだけ
- アクセス設定前と後でCloudWatch LogsやContainer Insights経由の間接的な調査からEKS APIを使用した直接的な調査に変わり、Root Causeの特定が迅速かつ明確になる

## 前提条件

- AWS DevOps Agentがセットアップ済みであること
- EKSクラスタを作成・管理できる権限があること
- kubectl、Terraformがローカル環境にインストール済みであること

## やってみる

以下の手順で検証を進めます。

### サンプルEKSアプリのデプロイ

今回はAWSサンプルで提供されている retail-store-sample-app を使って、EKSクラスタを作成します。

以下のコマンドを実行して、EKSクラスタを作成します。

```bash
# 1. リポジトリをクローン
git clone https://github.com/aws-containers/retail-store-sample-app.git
cd retail-store-sample-app/terraform/eks/minimal

# 2. EKSクラスタを作成
terraform init
terraform apply

# 3. kubectlを設定
terraform output -raw configure_kubectl  # 出力されたコマンドを実行

# 4. クラスタ動作確認
kubectl get nodes

# 5. アプリケーションをデプロイ
kubectl apply -f https://github.com/aws-containers/retail-store-sample-app/releases/latest/download/kubernetes.yaml
kubectl wait --for=condition=available deployments --all
```

構成は以下のようになります。

- VPC + EKS cluster（マルチAZ）
- RDS、DynamoDBなどのマネージドサービスは使用しない
- クラスタ内依存関係（MariaDB、Redis）のみで動作

デフォルトではNLBがinternal（内部向け）として作成されるため、ローカルマシンからアクセスするには以下のコマンドでポートフォワーディングを設定します。

```bash
kubectl port-forward service/ui 8080:80
```

デプロイできると以下のような画面が表示されます。

![CleanShot 2025-12-05 at 19.37.08@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/0nSYjWZj1aRG.png)

### EKS障害を起こす

アプリがデプロイできたので、意図的に障害を起こしてみます。

デプロイされたリソース状況はこちらです。

![CleanShot 2025-12-05 at 20.02.45@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/OgJCoiYxC4Gk.png)  
![CleanShot 2025-12-05 at 19.29.40@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/KKAlECofHHhP.png)

意図的にデータベース障害（停止）を発生させて、アプリケーションの依存関係エラーを再現します。

```bash
# データベースPodの状態を確認
kubectl get statefulsets
kubectl get pods catalog-mysql-0 orders-postgresql-0 orders-rabbitmq-0

# レプリカ数を0にしてデータベースを停止
kubectl scale statefulset catalog-mysql --replicas=0
```

実行結果

```bash
❯ # データベースPodの状態を確認
 ❯ kubectl get statefulsets                                                                                                                                ✘ INT ○ retail-store 22:59:06
NAME                READY   AGE
catalog-mysql       1/1     4h30m
orders-postgresql   1/1     4h30m
orders-rabbitmq     1/1     4h30m
 ❯ kubectl get pods catalog-mysql-0 orders-postgresql-0 orders-rabbitmq-0                                                                                        ○ retail-store 22:59:11

NAME                  READY   STATUS    RESTARTS   AGE
catalog-mysql-0       1/1     Running   0          151m
orders-postgresql-0   1/1     Running   0          151m
orders-rabbitmq-0     1/1     Running   0          151m

 ❯ # レプリカ数を0にしてデータベースを停止
kubectl scale statefulset catalog-mysql --replicas=0

statefulset.apps/catalog-mysql scaled
 ❯ kubectl get statefulsets                                                                                                                                      ○ retail-store 23:00:28
NAME                READY   AGE
catalog-mysql       0/0     4h33m
orders-postgresql   1/1     4h33m
orders-rabbitmq     1/1     4h33m
```

catalog-mysqlを停止すると、500エラーが発生します。

![CleanShot 2025-12-05 at 23.02.51@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/An2lWiDD1pns.png)

この状態で、AWS DevOps Agentがどのように依存関係の問題を診断し、復旧手順を提案するか確認します。

### EKSアクセス設定を行う前の状態でAWS DevOps Agentを使って調査を行う

AWSマネジメントコンソールのDevOps Agentから調査を開始します。

以下の情報を入力して調査を開始します。

| Field | Input |
| --- | --- |
| **Investigation details** | The catalog service in EKS cluster "retail-store" is returning 500 errors. There appears to be a connection failure to the catalog-mysql database. |
| **Investigation starting point** | User report: Accessing the catalog page via ui results in 500 errors. |

![CleanShot 2025-12-05 at 23.10.51@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/Hoq6mXJbmCxy.png)

調査が開始されるとEKS上のパラメーターやCloudWatch LogsやContainer Insightsを頼りに調査をしています。（ログは機械翻訳をかけています）

![CleanShot 2025-12-06 at 13.12.33@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-06/LzuVWRdANgq3.png)  
![CleanShot 2025-12-06 at 10.08.21@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-06/qUcomoKMyc0f.png)  
![CleanShot 2025-12-06 at 10.10.43@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-06/iCk3I6pefBJH.png)  
![CleanShot 2025-12-06 at 10.09.24@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-06/UThFDTfpbsSq.png)

わかりずらいと思いますが、この後の調査との比較のために全体ログを添付しておきます。

EKSアクセス設定前の全体ログ

（これでも一部見切れています。）  
![AWS-DevOps-エージェント-12-06-2025_01_02_AM_part1.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-06/6kMUpAiRjMVH.png)

AWS上のログ頼りの調査ですが、最終的にはcatalog-mysql StatefulSetが0レプリカにスケールされ、データベースPodが終了したことが原因と特定できました。

![CleanShot 2025-12-06 at 10.12.23@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-06/mDZCAeyyqXoY.png)

根本原因にたどり着いていますが、Pod状態やKubernetesイベントを間接的にログから推測しているようで試行錯誤が多かった印象です。

ここからEKSアクセスを許可して再度調査を行ってみます。

### EKSアクセス設定を行って再度AWS DevOps Agentを使って調査を行う

以下の手順でEKSアクセスエントリを設定します。

1. EKS Access Entriesを有効化: EKSコンソールのAccessタブから認証モードをEKS APIを使用するモードを設定
2. アクセスエントリを作成: IAM role ARN（ `arn:aws:iam::<アカウントID>:role/service-role/DevOpsAgentRole-AgentSpace-xxxxxxxx` ）をプリンシパルとして入力
3. ポリシーを追加: `AWS Managed AIOpsAssistantPolicy` を追加
4. 作成を完了: "Create"をクリックしてアクセスエントリを作成
5. 接続確認: DevOps AgentがEKSクラスタに接続できる状態になる

![CleanShot 2025-12-05 at 23.32.38@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/8Cr0xN5UhFe5.png)

「アクセス」 タブからEKS Access Entriesを有効化します。

![CleanShot 2025-12-06 at 00.14.55@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/3MeZ9bjZvus6.png)

EKS APIを使用するモードを設定します。

![CleanShot 2025-12-06 at 00.17.03@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/nInsMopOgZTB.png)

次にIAM アクセスエントリにDevOpsAgentRole-AgentSpaceを追加します。

![CleanShot 2025-12-06 at 00.24.43@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/UI0hBuaqyx0r.png)

IAM プリンシパル ARN にセットアップで表示されていたARNを入力します。

![CleanShot 2025-12-06 at 00.27.36@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/Q7Eku5k5pK0M.png)

アクセスポリシーに `AWS Managed AIOpsAssistantPolicy` を追加します。

![CleanShot 2025-12-06 at 00.28.48@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/WfihdrHK0vqf.png)

最終設定はこちらで作成します。

![CleanShot 2025-12-06 at 00.29.57@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/zgLTHQ85gb7j.png)

![CleanShot 2025-12-06 at 00.58.20@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/vmX7ARTXxe2w.png)

この状態で再度AWS DevOps Agentを使って調査を行ってみます。

![CleanShot 2025-12-06 at 00.33.38@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/IuZh0K3v5qSJ.png)

先ほどの調査と違い、調査フロー上では調査量が減り効率的に進んでいる感じがあります。

![CleanShot 2025-12-06 at 01.06.12@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/1uuw9FBrrI4k.png)  
![CleanShot 2025-12-06 at 01.07.30@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/R2FsHFzFXOo8.png)

EKSアクセス設定後の全体ログ

![テストエージェントスペース-AWS-DevOps-エージェント-12-06-2025_01_03_AM-1-1-1.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-06/aFCZZiEWI6PA.png)

ただ、調査フロー上ではEKS APIを使っているのか使っていないのかよくわかりませんでした。

なので、CloudWatch Logs上でのEKSコントロールプレーンのログを確認してみます。

EKSコントロールプレーンのログを確認すると `DevopsAgentRole` からのアクセスが確認できます。

裏側でEKS APIを使っていることがわかりますね。

![CleanShot 2025-12-06 at 13.34.26@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-06/t2BUu5q0xGri.png)

Root Causeについても最初の内容より分量が減り、より明確な回答になっています。

![CleanShot 2025-12-06 at 01.08.15@2x.png](https://devio2024-2-media.developers.io/upload/65vuxU9caegku7OBH9KIp4/2025-12-05/h1foIoT1KShB.png)

私自身、K8sについてはあまり詳しくないので、このレベルで情報をまとめてくれると障害調査で非常に助かると感じました。

## 最後に

AWS DevOps Agent (Preview)のEKSアクセス設定を試してみました。

EKSアクセスを許可することで、DevOps AgentはCloudWatch Logs経由の間接的な調査からEKS API経由の直接的な調査に変わり、Root Causeの特定が迅速かつ明確になることが確認できました。

設定も非常にシンプルで、EKS Access Entriesで適切な権限を付与するだけで利用開始できます。

ぜひEKSを利用している方はお試しください。

このブログがどなたかの参考になれば幸いです。

以上、たかやま([@nyan\_kotaroo](https://twitter.com/nyan_kotaroo))でした。

この記事をシェアする