---
title: "AWS DevOps Agent（Preview）の Datadog MCP サーバ連携をやってみた #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/aws-devops-agent-datadog-mcp-connect/"
author: ""
published: "2025-12-05"
created: "2025-12-09"
description: ""
tags:
  - ""
  - "raw"
---

こんにちは。AWS re:Invent2025 に参加しているオペレーション部のshiinaです。

## はじめに

AWS DevOps Agent ではオブザーバビリティツールの Datadog と連携が可能です。  
早速 Datadog MCP サーバと接続し、メトリクス・ログ・トレースの連携を行い、調査機能を拡張してみました。

## やってみた

今回のインシデント調査は ALB のヘルスチェックに失敗し、ターゲットが異常となるケースで行います。  
下記 Datadog のメトリクスモニターがアラート状態となったシーンで実施してみます。

- aws.applicationelb.httpcode\_target\_5xx
- aws.applicationelb.un\_healthy\_host\_count monitor

![dd-monitor1](https://devio2024-media.developers.io/image/upload/v1764869258/2025/12/04/spuk5ovoobpxlezv2jxi.png)

![dd-monitor2](https://devio2024-media.developers.io/image/upload/v1764869262/2025/12/04/o4dhrormjggfe3cnsykz.png)

### 前提

- AgentSpace 作成済み

### Datadog テレメトリー連携設定

1. Agent Space の Capabilities タブを選択します。
2. Telemetry より Add を選択します。  
	![add1](https://devio2024-media.developers.io/image/upload/v1764869213/2025/12/04/fotjazokohbzjaofagyn.png)
3. Telemetry 一覧より Datadog の Register を選択します。  
	![add2](https://devio2024-media.developers.io/image/upload/v1764869216/2025/12/04/lhwlyvbgbkdt9yxsuxry.png)
4. Datadog MCP Server Details では任意の Server Name を指定し、追加します。  
	![add3](https://devio2024-media.developers.io/image/upload/v1764869222/2025/12/04/jvxncjktigqvobah81j5.png)
5. Datadog のサイトにリダイレクトし、アクセス認可を行います。  
	![add4](https://devio2024-media.developers.io/image/upload/v1764869227/2025/12/04/c1fndvvxvg1nrkgpaflx.png)
6. 連携先の Datadog organization を選択します。  
	![add5](https://devio2024-media.developers.io/image/upload/v1764869234/2025/12/04/ljhlrgottloayifan7xg.png)
7. 権限を確認の上、認可します。  
	![add6](https://devio2024-media.developers.io/image/upload/v1764869239/2025/12/04/jpjagxc915vj3s7zuwom.png)
8. 「Datadog registered successfully」のメッセージが表示されたら、SAVE を選択します。  
	![add7](https://devio2024-media.developers.io/image/upload/v1764869247/2025/12/04/okk43hcicbhapcaynvsf.png)
9. Configure Webhook Connection のセットアップが表示されます。  
	今回は Datadog MCP サーバ のみ利用するため、そのまま Close を選択し、セットアップは完了させます。

![add8](https://devio2024-media.developers.io/image/upload/v1764869252/2025/12/04/umdw6rbbhh4qoygap1jo.png)

### インシデント調査

意図的に ALB のヘルスチェックに失敗し、ターゲットが異常にさせ、DevOps Agent でインシデント調査を行います。  
Start Investigation にて以下を指定して実施してみます。

- Investigation details

```bash
Please investigate the cause of the Datadog monitor alert that occurred around 4:30 JST on December 3.
```

![start invension](https://devio2024-media.developers.io/image/upload/v1764869203/2025/12/04/ekfr6o4j4vgcnaxka3px.png)

### MCP 連携を確認してみる

MCP サーバを経由して Datadog API リクエストを行っていることが確認できます。  
Datadog メトリクスやログを元に AWS リソースの調査がシームレスに行われています。

![mcpuse](https://devio2024-media.developers.io/image/upload/v1764869268/2025/12/04/dnwtwptqrlhf1qdhdgxy.png)

![mcpuse2](https://devio2024-media.developers.io/image/upload/v1764869208/2025/12/04/o1nve9ca3fic53oec78k.jpg)

![mpcuse3](https://devio2024-media.developers.io/image/upload/v1764869274/2025/12/04/t0oy6zwfytsta21m3goo.png)

## まとめ

今回、AWS DevOps Agent（Preview）と Datadog MCP Server を連携し、インシデント（ALB のヘルスチェック異常）のシナリオで動作検証を行ってみました、  
従来は Datadog 側と AWS 側を行き来していた調査フローを、AI エージェントにより一つのインターフェースに集約できるので、インシデント対応フローをより簡素化できそうです。  
Preview 段階ではありますが、Datadog をすでに利用している環境では比較的手軽に試せるので、インシデント対応の自動化や効率化に関心のある方は、一度触ってみる価値があると感じました。  
本記事が参考になれば幸いです。

#AWSreInvent

この記事をシェアする