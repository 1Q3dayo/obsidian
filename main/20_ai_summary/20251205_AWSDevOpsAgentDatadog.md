---
title: "AWS DevOps Agent（Preview）の Datadog MCP サーバ連携をやってみた #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/aws-devops-agent-datadog-mcp-connect/"
author:
published: 2025-12-05
created: 2025-12-09
description: "AWS DevOps AgentにDatadog MCPサーバを連携。メトリクス・ログ・トレースを統合し、インシデント調査機能を拡張。"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "devops"
  - "datadog"
  - "monitoring"
---

## 概要

AWS DevOps AgentにDatadog MCPサーバを連携。ALBのヘルスチェック失敗を例に、Datadogメトリクス・ログ・トレースを統合してインシデント調査機能を拡張。MCPサーバ経由でDatadog APIリクエストを実行。

## 主要ポイント

### 連携設定
- Agent SpaceのCapabilitiesタブからTelemetry追加
- Datadog MCP Server DetailsでServer Name指定
- Datadogサイトで認証・認可

### 調査機能
- Datadogメトリクス・ログ・トレースを統合
- AWSリソース調査とシームレスに連携
- MCPサーバ経由でAPIリクエスト実行

### 効果
- 包括的な可観測性データへのアクセス
- インシデント調査の効率化

