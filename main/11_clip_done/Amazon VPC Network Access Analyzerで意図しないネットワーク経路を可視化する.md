---
title: "Amazon VPC Network Access Analyzerで意図しないネットワーク経路を可視化する"
source: "https://tech.nri-net.com/entry/network_access_analyzer"
author:
  - "[[nnc-t-fujimoto]]"
  - "[[tech.nri-net.com]]"
  - "[[https://tech.nri-net.com/archive/author/nnc-t-fujimoto]]"
  - "[[nnc-t-fujimotoの記事一覧]]"
  - "[[m6-yamada]]"
  - "[[y-obayashi]]"
  - "[[y2-shibahara]]"
  - "[[t3-kato]]"
  - "[[やまもと (id:m4-yamamoto)]]"
  - "[[小山 (id:c-koyama)]]"
published: 2025-10-29
created: 2025-11-17
description: "本記事は ネットワークウィーク 13日目の記事です。 💻 12日目 ▶▶ 本記事 ▶▶ 14日目 🌐 はじめに サービス概要 料金 他Analyzerとの違い VPC Reachability Analyzer AWS IAM Access Analyzer 使い方 1. Network Access Analyzerの有効化 2. Network Access Scopeを設定 3. 分析開始 4. 分析結果の確認 Network Access Analyzerを実際に使ってみる 検証の前提 Network Access Scopeの設定 結果 終わりに 参考 はじめに VPCを運用・構築す…"
tags:
  - "clippings"
  - raw

---
本記事は [ネットワークウィーク](https://tech.nri-net.com/entry/network_week) 13日目の記事です。  
💻 [12日目](https://tech.nri-net.com/entry/introduction_to_google_cloud_vpc) ▶▶ 本記事 ▶▶ [14日目](https://tech.nri-net.com/entry/use_glue_securely) 🌐

## はじめに

VPCを運用・構築する過程では、設定ミスにより意図しないネットワーク経路が生じることがあります。こうしたリスクは継続的に監視し、見直し・修正していく運用が必要になります。そこで本記事では、 **意図しないネットワーク経路** を特定できるAmazon VPC Network Access Analyzerの機能についてまとめてみました。

## サービス概要

Amazon VPC Network Access Analyzerとは、AWSネットワーク内のリソース間の経路を静的解析し、ポリシー（要件）に反する意図しない到達経路を検出する機能です。大規模・複雑なAWSネットワークでも手動チェックに頼らず分析を行うことができます。名前にVPCが付いているように、VPCから提供されている分析ツールになり、VPCのコンソールから、「ネットワークマネージャー」に移動し、「セキュリティとガバナンス」からアクセスすることが可能です。

## 料金

Network Access Analyzerの料金は、評価実行時に分析対象となった ENI（Elastic Network Interface）1 個あたり 0.002 USDです。分析は継続的な監視ではなくオンデマンドで実行します。実行後の結果はコンソールから何度でも確認でき、結果の閲覧自体に追加料金は発生しません。検出内容を見ながら設定を調整し、再分析するサイクルで運用することができます。

[料金 - Amazon VPC | AWS](https://aws.amazon.com/jp/vpc/pricing/)

## 他Analyzerとの違い

AWSには、Network Access Analyzerの他にAnalyzerと名付けられている機能がVPC Reachability AnalyzerとAWS IAM Access Analyzerの2つあります。特に、VPC Reachability Analyzerに関しては、同じVPCから提供されている分析ツールであるため、役割・Network Access Analyzerとの機能の違いについては利用前に理解しておく必要があります。

## VPC Reachability Analyzer

VPC Reachability Analyzerは、VPC内の2つのエンドポイント間、あるいは複数VPC間の到達性（つながる/つながらない）を解析し、接続トラブルの原因を突き止めるためのネットワーク分析ツールです。 Network Access Analyzerが設計ポリシーを参照して **意図しないネットワーク経路の網羅的な洗い出し** を目的にすることに対して、Reachability Analyzer は、特定の送信元と宛先の **到達可否を検証** し、通らない場合はどこでブロックされているかを明らかにすることを目的とします。  
また、Network Access Analyzerが **複数VPCや多数リソースなど設定するスコープ** が検出対象であるのに対して、Reachability Analyzerは **指定した2点に関わる経路** が検出対象になるという違いもあります。  
そのため、Reachability Analyzerは接続トラブルの切り分けや、特定の通信の事前検証に適します。一方で、Network Access Analyzerは、広範囲における意図しないネットワーク経路の検出や「アウトバウンド通信において、NAT経由のみ許容し、IGW直通は禁止する」といった設計基準の監査に適しています。

Reachability Analyzerの料金については、検証対象とする接続（分析）あたり、0.10 USDになります。

[料金 - Amazon VPC | AWS](https://aws.amazon.com/jp/vpc/pricing/)

## AWS IAM Access Analyzer

AWS IAM Access Analyzerは、リソースベースポリシーを解析し、外部／内部への意図しない公開や未使用アクセスを検出します。また、ポリシーの検証・生成も可能です。 Network Access Analyzerが **ネットワーク到達性** （AWSネットワーク内のリソース間の経路）が対象であるのに対して、IAM Access Analyzerでは権限の可否や過剰・誤った権限付与（外部公開や過剰な権限付与）といった **アイデンティティ／リソースポリシー** を対象に静的解析を行います。 例えば、外部アカウントからのAssumeRoleの許可、S3 バケットのパブリックアクセスなど意図しないアクセス許可を検知します。

IAM Access Analyzerの料金については、 [IAM Access Analyzer の料金](https://aws.amazon.com/jp/iam/access-analyzer/pricing/) をご確認ください。

また、以前私がIAM Access Analyzerに関するブログを2つ執筆しているので、よかったら見てみてください。

[tech.nri-net.com](https://tech.nri-net.com/entry/automatically_create_archive_rules_for_aws_iam_access_analyzer)

## 使い方

## 1\. Network Access Analyzerの有効化

初回のみ、コンソールから「使用を開始する」を選択します。 Network Access Analyzerはリージョン単位の機能であるため、使用するリージョンごとに「使用を開始する」を行う必要があります。 開始するとNetwork Access Scopesが表示されます。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/n/nnc-t-fujimoto/20251026/20251026153942.png)

Network Access Analyzerマネジメントコンソール「使用を開始する」

## 2\. Network Access Scopeを設定

Network Access Scopeとは、AWS 環境内でどのような通信経路を分析対象にするかを定義し、インバウンド／アウトバウンドの到達要件（許容・非許容の条件）を仕様として記述するものです。このスコープに基づいてNetwork Access Analyzerが経路を洗い出し、要件に合わない経路を分析結果として可視化します。 デフォルトで以下4つのスコープがAWSによって作成されます。

| Network Access Scope | 内容 |
| --- | --- |
| AWS-VPC-Ingress | インターネットゲートウェイ、ピアリング接続、VPCサービスエンドポイント、VPN、トランジットゲートウェイからVPCへの入力パスを特定 |
| AWS-VPC-Egress | すべてのVPCからインターネットゲートウェイ、ピアリング接続、VPCエンドポイント、VPN、トランジットゲートウェイへの出力パスを特定 |
| AWS-IGW-Egress | すべてのネットワークインターフェイスからインターネットゲートウェイへの出力パスを特定 |
| All-IGW-Ingress | インターネットゲートウェイからすべてのネットワークインターフェイスへの入力パスを特定 |

Network Access Scopeは、カスタムで定義することも可能です。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/n/nnc-t-fujimoto/20251026/20251026214218.png)

Network Access Analyzerマネジメントコンソール「Network Access Scopeを作成」

## 3\. 分析開始

デフォルトまたは作成したNetwork Access Scopeを選択し、右上の「分析」を選択します。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/n/nnc-t-fujimoto/20251026/20251026214725.png)

Network Access Analyzerマネジメントコンソール「分析」

## 4\. 分析結果の確認

分析の結果が、「最新の分析」の部分に表示されます。 また、「過去の分析」から過去に行った分析結果を閲覧することができます。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/n/nnc-t-fujimoto/20251027/20251027102848.png)

「AWS-IGW-Egress（Amazonが作成）」分析結果の例

## Network Access Analyzerを実際に使ってみる

## 検証の前提

今回は、プライベートサブネットに存在するEC2インスタンスがNATゲートウェイを経由せずに、インターネットゲートウェイに到達するような経路になっていないか、Network Access Analyzerを用いて検証していきます。 検証のために、以下リソースを事前に作成しておきます。

- リソース一覧
	- VPC：プライベートサブネット1つ、パブリックサブネット1つ
	- NATゲートウェイ
	- インターネットゲートウェイ
	- EC2：プライベートサブネットに存在
- プライベートサブネットのルートテーブル

| 送信先 | ターゲット |
| --- | --- |
| 10.0.0.0/16 | local |
| 0.0.0.0/0 | インターネットゲートウェイ |

リソースの具体的な構築方法に関しては、割愛します。 検出を行うために、EC2が存在するプライベートサブネットのルートテーブルの送信先を `0.0.0.0/0`, ターゲットを `インターネットゲートウェイ` に設定しておきます。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/n/nnc-t-fujimoto/20251027/20251027112756.png)

アーキテクチャ図

## Network Access Scopeの設定

「Network Access Scope の作成」を選択し、カスタムでスコープを設定します。 一致条件（ `MatchPaths` ）では、検出したい経路の条件を定義します。 今回の場合は、ネットワークインターフェイスからインターネットゲートウェイへの出力パスを対象とするため、送信元（ `Source` ）にネットワークインターフェース、送信先（ `Destination` ）にインターネットゲートウェイを設定します。

除外条件（ `ExcludePaths` ）では、見つかった経路のうち、検出を行わない(除外する)条件を定義します。 今回の場合は、NATゲートウェイを経由している場合は、正常な設定とし検出は行わないようにするため、経由（ `ThroughResources` ）にNATゲートウェイを設定します。 以下、今回の設定で定義されるNetwork Access Scopeになります。

- Network Access Scopeの定義
```
{  "NetworkInsightsAccessScopeId": "nis-*****************",  "MatchPaths": [    {      "Source": {        "ResourceStatement": {          "ResourceTypes": [            "AWS::EC2::NetworkInterface"          ]        }      },      "Destination": {        "ResourceStatement": {          "ResourceTypes": [            "AWS::EC2::InternetGateway"          ]        }      }    }  ],  "ExcludePaths": [    {      "ThroughResources": [        {          "ResourceStatement": {            "ResourceTypes": [              "AWS::EC2::NatGateway"            ]          }        }      ]    }  ]}
```

## 結果

分析を開始してから、数分後に分析が完了します。 分析結果を確認すると、EC2インスタンスからインターネットゲートウェイの経路が検出されていることが分かります。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/n/nnc-t-fujimoto/20251027/20251027095954.png)

Network Access Analyzer 分析結果

右側に表示される分析結果のパスからルートの詳細を確認することができます。 プライベートサブネットにあるENIから、セキュリティグループ、NACLを経由してルーティングテーブルにより、インターネットゲートウェイに直接ルーティングされていることを確認することができます。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/n/nnc-t-fujimoto/20251027/20251027100438.png)

Network Access Analyzer 分析結果パス

## 終わりに

今回はNetwork Access Analyzerの活用方法についてまとめてみました。 Network Access Analyzerは、スコープ作成に少し慣れが必要な一方で、経路の可視化、運用への組み込みやすさ、そして費用対効果の面で非常に扱いやすいサービスだと感じました。意図しない経路の早期発見に強く、組織のネットワーク設計の自動検証に適していると思います。  
Network Access Analyzerを定期的なネットワークの健全性チェックとして活用しつつ、Reachability Analyzerと併用することでネットワーク経路に関する分析の効率化を行うこともできます。  
また、Security Hubとの連携も可能であるため、検出結果を組織横断で一元集約し、ポリシー違反の継続監視や自動通知まで含めた組織的な導入も検討するとよいでしょう。

[aws.amazon.com](https://aws.amazon.com/jp/blogs/networking-and-content-delivery/continuous-verification-of-network-compliance-using-amazon-vpc-network-access-analyzer-and-aws-security-hub/?utm_source=chatgpt.com)

## 参考

- [新機能 – Amazon VPC Network Access Analyzer | Amazon Web Services ブログ](https://aws.amazon.com/jp/blogs/news/new-amazon-vpc-network-access-analyzer/)
- [What is Network Access Analyzer? - Amazon Virtual Private Cloud](https://docs.aws.amazon.com/vpc/latest/network-access-analyzer/what-is-network-access-analyzer.html?utm_source=chatgpt.com)

[« Glueをセキュアに使おう！〜VPC内で完結す…](https://tech.nri-net.com/entry/use_glue_securely) [ゼロから始める AWS 生活 ～ Amazon Rek… »](https://tech.nri-net.com/entry/starting_aws_life_from_scratch)