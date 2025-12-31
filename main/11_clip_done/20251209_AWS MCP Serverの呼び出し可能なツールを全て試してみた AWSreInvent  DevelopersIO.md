---
title: "AWS MCP Serverの呼び出し可能なツールを全て試してみた #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/aws-mcp-server-all-tools-awsreinvent/"
author: ""
published: "2025-12-05"
created: "2025-12-09"
description: ""
tags:
  - ""
  - "raw"
---

リテールアプリ共創部のるおんです。先日、 **AWS MCP Server** がプレビュー版としてリリースされました。これまでAWS Knowledge MCP ServerやAWS API MCP Serverとして提供されていた機能が統合され、さらに **Agent SOP Tools** という新機能も追加されています。

CursorからこのAWS MCP Serverに接続すると、ツール群の一覧が以下のように表示されます。

![スクリーンショット 2025-12-05 2.45.45](https://devio2024-media.developers.io/image/upload/v1764870350/2025/12/05/gnseeywqqcn1dfclf2mz.png)

今回は上の画像にある、現在（2025年12月5日時点）で利用可能な8ツールを全て試してみました！使用したモデルはClaude Opus 4.5です。

## AWS MCP Serverとは

[AWS MCP Server](https://docs.aws.amazon.com/aws-mcp/latest/userguide/what-is-mcp-server.html) は、AIアシスタントとエージェントに安全で認証されたAWSサービスへのアクセスを自然言語対話で提供する完全マネージド型の **リモートサーバー** です。

AWS MCP Serverを使用すると、以下のようなタスクを実行できます。

- **複数ステップのAWSワークフローの実行**
- **リアルタイムのAWS知識の取得**
- **認証済みAWS API呼び出しの実行**
- **AWSの問題のトラブルシューティング**
- **インフラストラクチャのプロビジョニングと設定**
- **コストの管理**

このAWS MCP Serverを使用することで、AWSの様々な操作を自然言語で実行できるようになります。  
詳細なセットアップ方法についてはこちらの記事が参考になるので、そちらをご確認ください。

## 提供される3つのツールカテゴリ

AWS MCP Serverは、大きく分けて3つのツールカテゴリを提供しています。

### 1\. Agent SOP Tools

Agent SOP（Standard Operating Procedure）Toolsは、AWSベストプラクティスに従った段階的なワークフローを提供する新機能です。

これは、AWSの典型的な構成作業を「設計＋手順」のセットでパッケージ化したものです。例えば「静的サイトをCloudFrontで配信したい」と言えば、S3バケットの作成・アクセス制御・証明書設定・キャッシュポリシーなどを、ベストプラクティスに沿った順序で自動的に組み立ててくれます。

### 2\. AWS Knowledge Tools

AWS Knowledge Toolsは、従来の [AWS Knowledge MCP Server](https://awslabs.github.io/mcp/servers/aws-knowledge-mcp-server) と同様の機能を提供します。AWSドキュメント、APIリファレンス、ベストプラクティス、サービスガイドなどの検索と取得が可能です。

### 3\. AWS API Tools

AWS API Toolsは、従来の [AWS API MCP Server](https://awslabs.github.io/mcp/servers/aws-api-mcp-server) の機能に相当します。15,000以上のAWS APIをサポートし、自然言語リクエストをAPI呼び出しに変換して実行します。

## 全ツール一覧

以下が2025年12月5日時点で利用可能な全8ツールです。

| カテゴリ | ツール名 | 説明 |
| --- | --- | --- |
| Agent SOP Tools | `aws___retrieve_agent_sop` | Agent SOPの検索または特定のSOPの詳細情報取得 |
| AWS Knowledge Tools | `aws___search_documentation` | すべてのAWSドキュメント、APIリファレンスなどを検索 |
| AWS Knowledge Tools | `aws___read_documentation` | AWSドキュメントページをマークダウン形式で取得 |
| AWS Knowledge Tools | `aws___recommend` | 関連トピックと頻繁に閲覧されるコンテンツに基づく推奨 |
| AWS Knowledge Tools | `aws___list_regions` | すべてのAWSリージョンの識別子と名前を取得 |
| AWS Knowledge Tools | `aws___get_regional_availability` | サービスと機能の地域別対応状況を確認 |
| AWS API Tools | `aws___call_aws` | 15,000以上のAWS APIをサポートし、認証情報を自動管理 |
| AWS API Tools | `aws___suggest_aws_commands` | AWS APIの説明と構文ヘルプを提供 |

それでは、実際にそれぞれのツールを試してみます。

## 1\. aws\_\_\_retrieve\_agent\_sop

まず、Agent SOP Toolsから試してみます。このツールは、利用可能なすべてのSOPを一覧表示したり、特定のSOP向けの完全なワークフローを取得できます。

Cursorで以下のようにプロンプトを入力してみました。

```
LambdaとAPI Gatewayの構成のAgent SOPを教えてください
```

すると、以下のように `aws___retrieve_agent_sop__` ツールが実行され、その結果からAIが構成のベストプラクティスをまとめてくれました。

![スクリーンショット 2025-12-05 3.45.35](https://devio2024-media.developers.io/image/upload/v1764873957/2025/12/05/ts1qpj5ro2fujs0j5tdc.png)

このように、AWSの主要なサービスに対する標準的な操作手順がSOPとして定義されています。  
必要なAPIコールのパラメーター、実行ステップ、注意点などが含まれており、AWSのベストプラクティスに従った操作が可能になっています。

次に、AWS Knowledge Toolsのドキュメント検索機能を試してみます。今回はre:Invent 2025で発表された [Lambda Durable Functions](https://docs.aws.amazon.com/lambda/latest/dg/durable-functions.html) についての最新のドキュメントを検索してみます。

```
Lambda関数のDurable Functionsについての最新のドキュメントを教えてください
```

このプロンプトを入力すると、 `aws___search_documentation` ツールが実行され、Lambda関数のDurable Functionsに関連するドキュメントが検索されました。とても興味深いことに、Lambda Durable Functionsは発表されて間もないのでAIの学習データには含まれていませんでしたが、AWS MCP Serverのドキュメント検索機能によってドキュメントが取得され、この機能についてのデータを補完してくれました。これこそMCPサーバーの真価ですね。

![スクリーンショット 2025-12-05 2.59.56](https://devio2024-media.developers.io/image/upload/v1764871257/2025/12/05/b0wisqczjm5ajt9xg0ba.png)

## 3\. aws\_\_\_read\_documentation

`aws___search_documentation` で見つけたドキュメントのURLを使って、実際にドキュメントの内容を取得してみます。特にプロンプトを打ち込まずとも、先ほどの続きで勝手に `aws___read_documentation` ツールを使用してドキュメントの内容を読み込んでくれました。そして、その結果をAIがまとめてくれました。

![スクリーンショット 2025-12-05 3.05.35](https://devio2024-media.developers.io/image/upload/v1764871577/2025/12/05/mesitjhiivtciyvwiurz.png)

![スクリーンショット 2025-12-05 3.05.51](https://devio2024-media.developers.io/image/upload/v1764871583/2025/12/05/zfk01uh50apdjlgib0z4.png)

関連トピックと頻繁に閲覧されるコンテンツに基づいた推奨を取得してみます。

```
Lambda関数に関連する推奨トピックを教えてください
```

すると、 `aws___recommend` ツールが実行され、Lambda関数に関連する推奨トピックが表示され、AIがよってわかりやすくまとめてくれました。

![スクリーンショット 2025-12-05 3.08.15](https://devio2024-media.developers.io/image/upload/v1764871720/2025/12/05/ibs0tfnrv7el1h1rakrv.png)

![スクリーンショット 2025-12-05 3.08.47](https://devio2024-media.developers.io/image/upload/v1764871734/2025/12/05/idqcymuu0wmo8r91b0oq.png)

## 5\. aws\_\_\_list\_regions

次に、AWSリージョンの一覧を取得してみます。

```
利用可能なAWSリージョンを教えてください
```

すると、 `aws___list_regions` ツールが実行され、すべてのAWSリージョンの識別子と名前がリスト形式で表示されました。

![スクリーンショット 2025-12-05 3.11.35](https://devio2024-media.developers.io/image/upload/v1764871918/2025/12/05/vsbj7pxaeor6wgdnmgli.png)

## 6\. aws\_\_\_get\_regional\_availability

このツールは、特定のサービスがどのリージョンで利用可能かを確認するためのツールです。

```
Amazon Bedrockは大阪リージョンでも利用可能か教えてください
```

すると、 `aws___get_regional_availability` ツールが実行され、Amazon Bedrockが大阪リージョンでも利用可能かが表示されました。

![スクリーンショット 2025-12-05 3.16.40](https://devio2024-media.developers.io/image/upload/v1764872221/2025/12/05/wu684rlhh2l4xna0n9cw.png)

## 7\. aws\_\_\_call\_aws

次に、 **AWS API Tools** を試してみます。まずは実際にAWS APIを呼び出してみましょう。

```
現在のアカウントのS3バケット一覧を取得してください
```

すると、 `aws___call_aws` ツールが実行され、S3のListBuckets APIが呼び出されました。結果として、現在のアカウントに存在するS3バケットの一覧が表示されました。

![スクリーンショット 2025-12-05 3.28.49](https://devio2024-media.developers.io/image/upload/v1764872936/2025/12/05/veytpsxbsqxyjiaemvm5.png)

## 8\. aws\_\_\_suggest\_aws\_commands

最後に、 **AWS API Tools** の説明と構文ヘルプを取得する機能を試してみます。

```
EC2インスタンスを起動するAPIコマンドの構文を教えてください
```

すると、 `aws___suggest_aws_commands` ツールが実行され、EC2インスタンスを起動するコマンド説明と基本構文についての解説、必須パラメータ、オプションパラメータ、使用例などが表示されました。

![スクリーンショット 2025-12-05 3.21.56](https://devio2024-media.developers.io/image/upload/v1764872547/2025/12/05/gxy8rqarm4hoopzeol9x.png)

![スクリーンショット 2025-12-05 3.23.47](https://devio2024-media.developers.io/image/upload/v1764872637/2025/12/05/pmtibab5f4inmbjxivoa.png)

## 全ツールを試してみた感想

全8ツールの検証が完了しました！実際に全てのツールを試してみて、以下のような点が特に便利だと感じました。

**1\. Agent SOP Toolsの価値**  
Agent SOP Toolsは、AWSのベストプラクティスに従った段階的なワークフローを提供してくれるため、AWSの操作に不慣れな方でも安全に作業を進められます。また、複雑な複数ステップの操作も、SOPに従うことで漏れなく実行できるのが便利です。

**2\. ドキュメント検索の効率化**  
AWS Knowledge系のツール群を使用することで、ブラウザを開かずにCursor内でAWSドキュメントの検索・閲覧・推奨取得が完結します。開発中にドキュメントを参照する際のコンテキストスイッチが減り、開発効率が向上します。AIの学習データに含まれていない内容でも、ドキュメントを参照することで、AIが学習していない内容を補完してくれます。

**3\. API呼び出しの簡便性**  
AWS API Toolsは、認証情報の管理を自動化してくれるため、複雑な設定なしにAWS APIを呼び出せます。また、 `aws___suggest_aws_commands` により、使用したいAPIの構文をその場で確認できるので、APIの使い方を素早く理解できるのが便利です。

**4\. 統合による利便性**  
従来は別々のMCP Serverとして提供されていた機能が一つに統合されたことで、セットアップが簡単になり、ツール間の連携もスムーズになりました。認証情報を設定し、リモート上にAWS MCP Serverが展開されたことで、多くのAWSの操作をエディタ上で実行できるようになったのはとても嬉しいです。

## おわりに

今回は、AWS MCP Serverの全8ツールを実際に試してみました。Agent SOP Toolsの追加により、AWSの操作がより安全かつ効率的に行えるようになり、従来のAWS Knowledge MCP ServerとAWS API MCP Serverの機能も統合されて使いやすくなっています。  
CursorなどのAI開発ツールからAWSを操作する機会が増えている中、このAWS MCP Serverは非常に強力なツールになると感じました。プレビュー版ということで、今後さらなる機能追加や改善が期待できそうです。

参考になれば幸いです。

## 参考

この記事をシェアする