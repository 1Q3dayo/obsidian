---
title: "Amazon OpenSearch Serverless でのキャパシティ制限の管理 - Amazon OpenSearch Service"
source: "https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/serverless-scaling.html"
author:
published:
created: 2026-01-12
description: "OpenSearch ServerlessのOCUベースの自動スケーリングとキャパシティ制限設定の公式ガイド"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "opensearch"
  - "serverless"
  - "scaling"
---

## 要約

Amazon OpenSearch Serverlessのキャパシティ管理に関するAWS公式ドキュメント。コンピューティング性能はOpenSearch Compute Units（OCU）で測定され、ワークロードに応じて自動スケーリングする。

主要ポイント：
- 初回コレクション作成時、冗長性有効で4 OCU（インデックス2+検索2）、無効で2 OCUがインスタンス化される
- 同一KMSキーのコレクションはOCUを共有可能（ベクトルコレクションは例外）
- アカウントレベルでインデックス作成・検索それぞれの最大OCU数を設定可能
- デフォルト最大は各10 OCU、上限は各1,700 OCU
- 各OCUは120 GiBのホットストレージを含む
- CloudWatchのSearchOCU/IndexingOCUメトリクスでモニタリング推奨
