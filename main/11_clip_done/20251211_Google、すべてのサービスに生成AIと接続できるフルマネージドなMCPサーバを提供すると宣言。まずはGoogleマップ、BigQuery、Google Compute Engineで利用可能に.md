---
title: "Google、すべてのサービスに生成AIと接続できるフルマネージドなMCPサーバを提供すると宣言。まずはGoogleマップ、BigQuery、Google Compute Engineで利用可能に"
source: "https://www.publickey1.jp/blog/25/googleaimcpgooglebigquerygoogle_compute_engine.html"
author: ""
published: ""
created: "2025-12-11"
description: "Googleは、Geminiなどの生成AIと同社のクラウドサービスを接続できるMCPサーバを今後すべての同社のサービスで提供すると発表しました。   Google’s existing API infrastructure is now e..."
tags:
  - ""
  - "raw"
---

2025年12月11日

  

Googleは、Geminiなどの生成AIと同社のクラウドサービスを接続できるMCPサーバを今後すべての同社のサービスで提供すると [発表しました](https://cloud.google.com/blog/products/ai-machine-learning/announcing-official-mcp-support-for-google-services?hl=en) 。

> Google’s existing API infrastructure is now enhanced to support MCP, providing a unified layer across all Google and Google Cloud services.
> 
> Googleの既存のAPIインフラはMCPをサポートするように強化され、GoogleおよびGoogle Cloudのすべてのサービスに統合されたレイヤを提供します。

## AIから複数サービスを組み合わせた処理も可能に

その第一弾としてGoogleマップ、BigQuery、Google Compute Engine、Google Kubernetes Engineに対応したフルマネージドなリモートMCPサーバが利用可能になっています。

これにより、例えばGeminiにチャットで「最寄りの公園までの距離は？」と自然言語で問い合わせるとGoogleマップで調べたり、BigQueryの大規模データに自然言語で問い合わせたりすることが可能になります。

Googleはさらに、Agent Development Kit(ADK)を使うことでGemini 3 Proを基盤とした自然言語エージェントを構築し 、BigQueryと接続して収益ベースの売上データを予測しつつ、AIエージェントがGoogleマップを照合して補完的なビジネスを探し、配送ルートを検証するといった複数のGoogleサービスを組み合わせた高度な処理も実現できると説明しています。

## 生成AIとアプリケーションをつなぐMCP

MCPとは一般に、生成AIやAIエージェントが外部のツールを呼び出して情報を取得したり操作したりする際に使われるプロトコルです。生成AIやAIエージェントがMCPクライアントとなり、情報提供や操作の対象となる側がMCPサーバとなります。

今回Googleは、同社の各サービスに対応したフルマネージドなリモートMCPサーバを提供すると発表しています。

そのためユーザーは自分でMCPサーバを設置や運用することなく、Googleが提供するリモートMCPサーバに接続することで、容易にGeminiやChatGPTなどの生成AIをGoogleの各サービスに接続し、生成AIから利用できるようになります。

## 今後さらに多くのGoogleサービスに展開

今後さらに以下のGoogleサービスについても、リモートMCPサーバが展開される予定です。

#### あわせて読みたい

- [［速報］Google、AIが支援してくれる「Duet AI」サービス群を多数展開へ。Google WorkspaceやBigQuery、Looker、Meet、Chatなど。Google Cloud Next '23](https://www.publickey1.jp/blog/23/googleaiduet_aigoogle_workspacebigquerylookermeetchatgoogle_cloud_next_23.html)
- [［速報］Google Cloudの開発や問題解決をAIが支援してくれる「Duet AI in Google Cloud」がVSCodeなどで利用可能に。Google Cloud Next '23](https://www.publickey1.jp/blog/23/google_cloudaiduet_ai_in_google_cloudvscodegoogle_cloud_next_23.html)
- [オラクル、「Oracle AI Database 26ai」発表。AIベクトルサーチをデータベースのコア機能に統合、MCPサーバをサポートなど。Oracle AI World 2025](https://www.publickey1.jp/blog/25/oracle_database_26aiaimcporacle_ai_world_2025.html)
- [生成AIによるプログラミング支援のCodeium、VSCodeフォークの「Windsurf」エディタ発表。変数名を1カ所変更して残りの修正を生成AIが行うなど高度な開発支援を提供へ](https://www.publickey1.jp/blog/24/aicodeiumvscodewindsurf1ai.html)

[![fbシェア](https://www.publickey1.jp/2024/fbshare_btn.png)](http://www.facebook.com/share.php?u=https%3A%2F%2Fwww.publickey1.jp%2Fblog%2F25%2Fgoogleaimcpgooglebigquerygoogle_compute_engine.html)

[![Xポスト](https://www.publickey1.jp/2024/xpost_btn.png)](https://twitter.com/intent/tweet?original_referer=https%3A%2F%2Fwww.publickey1.jp%2F&text=Google%E3%80%81%E3%81%99%E3%81%B9%E3%81%A6%E3%81%AE%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E3%81%AB%E7%94%9F%E6%88%90AI%E3%81%A8%E6%8E%A5%E7%B6%9A%E3%81%A7%E3%81%8D%E3%82%8B%E3%83%95%E3%83%AB%E3%83%9E%E3%83%8D%E3%83%BC%E3%82%B8%E3%83%89%E3%81%AAMCP%E3%82%B5%E3%83%BC%E3%83%90%E3%82%92%E6%8F%90%E4%BE%9B%E3%81%99%E3%82%8B%E3%81%A8%E5%AE%A3%E8%A8%80%E3%80%82%E3%81%BE%E3%81%9A%E3%81%AFGoogle%E3%83%9E%E3%83%83%E3%83%97%E3%80%81BigQuery%E3%80%81Google%20Compute%20Engine%E3%81%A7%E5%88%A9%E7%94%A8%E5%8F%AF%E8%83%BD%E3%81%AB%20%EF%BC%8D%20Publickey&url=https%3A%2F%2Fwww.publickey1.jp%2Fblog%2F25%2Fgoogleaimcpgooglebigquerygoogle_compute_engine.html)

[![Feedly](https://www.publickey1.jp/2024/feedly_btn.png)](https://feedly.com/i/subscription/feed%2Fhttps%3A%2F%2Fwww.publickey1.jp%2Fatom.xml)

  

*≪前の記事*  
[Claude CodeにSlackでコーディングタスクを依頼可能に。Anthropicがリサーチプレビュー公開](https://www.publickey1.jp/blog/25/claude_codeslackanthropic.html)

  
  

#### タグクラウド

[クラウド](https://www.publickey1.jp/cloud/)  
[AWS](https://www.publickey1.jp/cloud/aws/) / [Azure](https://www.publickey1.jp/cloud/microsoft-azure/) / [Google Cloud](https://www.publickey1.jp/cloud/google-cloud/)  
[クラウドネイティブ](https://www.publickey1.jp/cloud/cloud-native/) / [サーバレス](https://www.publickey1.jp/cloud/serverless/)  
[クラウドのシェア](https://www.publickey1.jp/cloud/cloud-share/) / [クラウドの障害](https://www.publickey1.jp/cloud/cloud-failure/)  

[コンテナ型仮想化](https://www.publickey1.jp/container-vm/)

[プログラミング言語](https://www.publickey1.jp/programming-lang/)  
[JavaScript](https://www.publickey1.jp/programming-lang/javascript/) / [Java](https://www.publickey1.jp/programming-lang/java/) / [.NET](https://www.publickey1.jp/programming-lang/net/)  
[WebAssembly](https://www.publickey1.jp/programming-lang/webassembly/) / [Web標準](https://www.publickey1.jp/programming-lang/web-standards/)  
[開発ツール](https://www.publickey1.jp/devtools/) / [テスト・品質](https://www.publickey1.jp/devtools/software-test/)

[アジャイル開発](https://www.publickey1.jp/devops/agile/) / [スクラム](https://www.publickey1.jp/devops/scrum/) / [DevOps](https://www.publickey1.jp/devops/)

[データベース](https://www.publickey1.jp/database/) / [機械学習・AI](https://www.publickey1.jp/database/machine-learning-ai)  
[RDB](https://www.publickey1.jp/database/rdb/) / [NoSQL](https://www.publickey1.jp/database/nosql/)  

[ネットワーク](https://www.publickey1.jp/network/) / [セキュリティ](https://www.publickey1.jp/network/security)  
[HTTP](https://www.publickey1.jp/network/http/) / [QUIC](https://www.publickey1.jp/network/quic/)

[OS](https://www.publickey1.jp/os) / [Windows](https://www.publickey1.jp/os/windows) / [Linux](https://www.publickey1.jp/os/linux) / [仮想化](https://www.publickey1.jp/os/vm)  
[サーバ](https://www.publickey1.jp/hardware/server/) / [ストレージ](https://www.publickey1.jp/hardware/storage/) / [ハードウェア](https://www.publickey1.jp/hardware/)

[ITエンジニアの給与・年収](https://www.publickey1.jp/trends/payment/) / [働き方](https://www.publickey1.jp/trends/workstyle/)

[殿堂入り](https://www.publickey1.jp/after-words/recommend/) / [おもしろ](https://www.publickey1.jp/after-words/funny) / [編集後記](https://www.publickey1.jp/after-words/)

[全てのタグを見る](https://www.publickey1.jp/tags.html)

#### Blogger in Chief

![photo of jniino](https://www.publickey1.jp/images/profile.jpg)

Junichi Niino（jniino）  
IT系の雑誌編集者、オンラインメディア発行人を経て独立。2009年にPublickeyを開始しました。  
（ [詳しいプロフィール](https://www.publickey1.jp/about-us.html) ）

Publickeyの新着情報をチェックしませんか？  
Twitterで ： [@Publickey](https://twitter.com/publickey/)  
Facebookで ： [Publickeyのページ](https://www.facebook.com/publickey/)  
RSSリーダーで ： [Feed](https://www.publickey1.jp/atom.xml)  

#### 最新記事10本

- [Google、すべてのサービスに生成AIと接続できるフルマネージドなMCPサーバを提供すると宣言。まずはGoogleマップ、BigQuery、Google Compute Engineで利用可能に](https://www.publickey1.jp/blog/25/googleaimcpgooglebigquerygoogle_compute_engine.html)
- [Claude CodeにSlackでコーディングタスクを依頼可能に。Anthropicがリサーチプレビュー公開](https://www.publickey1.jp/blog/25/claude_codeslackanthropic.html)
- [さくらのクラウド、「AppRun」正式提供開始。自動的にスケールするコンテナ実行基盤。仮想マシンを専有する「専有型」が登場](https://www.publickey1.jp/blog/25/apprun_2.html)
- [OpenAI、Google、MS、Anthropic、AWSらがAIエージェントの普及と相互運用を促進する団体「Agentic AI Foundation」（AAIF）設立。Linux Foundation傘下で](https://www.publickey1.jp/blog/25/openaigooglemsanthropicawsaiagentic_ai_foundationaaiflinux_foundation.html)
- [「あなたが修正するのは自分だけのバグではない」、リーナス・トーバルズ氏が東京開催のOpen Source Summit Japan基調講演で語ったこと（後編）](https://www.publickey1.jp/blog/25/open_source_summit_japan.html)
- [「AIは過剰に宣伝されているが、ツールとしては大いに信じている」、リーナス・トーバルズ氏が東京開催のOpen Source Summit Japan基調講演で語ったこと（前編）](https://www.publickey1.jp/blog/25/aiopen_source_summit_japan.html)
- [Kafka開発元のConfluentをIBMが買収。AI向けデータプラットフォームを強化へ](https://www.publickey1.jp/blog/25/kafkaconfluentibmai.html)
- [Supabaseのバックエンドサービスを自社ブランドのBaaSとして提供できる「Supabase for Platforms」リリース。AIによる開発ツールを提供するベンダなどに向け](https://www.publickey1.jp/blog/25/supabasebaassupabase_for_platformsai.html)
- [Vercel、Webアプリで顧客ごとのマルチテナント構成が簡単に作れる「Vercel for Platforms」発表。VercelがSaaS基盤に進化へ](https://www.publickey1.jp/blog/25/vercelwebvercel_for_platformsvercelsaas.html)
- [AIエージェントをどのコードエディタでも使えるようにする「ACP（Agent Client Protocol）」、JetBrainsがベータ提供開始](https://www.publickey1.jp/blog/25/aiacpagent_client_protocoljetbrainszeddocker.html)