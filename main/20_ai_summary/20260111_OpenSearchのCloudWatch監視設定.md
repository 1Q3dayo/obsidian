---
title: "Monitoring OpenSearch cluster metrics with Amazon CloudWatch - Amazon OpenSearch Service"
source: "https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-cloudwatchmetrics.html"
author:
published:
created: 2026-01-11
description: "OpenSearch ServiceのCloudWatchメトリクス一覧と監視方法の公式リファレンス"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "opensearch"
  - "monitoring"
  - "cloudwatch"
---

## 要約

Amazon OpenSearch ServiceがCloudWatchに送信するメトリクスの公式リファレンス。60秒間隔でメトリクスが送信され（汎用/マグネティックEBSは5分間隔）、2週間保持される。

主要メトリクスカテゴリ：クラスター、専用マスターノード、専用コーディネーターノード、EBSボリューム、インスタンス、ウォーム/コールドストレージ、OR1インスタンス、アラート、異常検出、非同期検索、Auto-Tune、Multi-AZ Standby、SQL、k-NN、クロスクラスター検索/レプリケーション、Learning to Rank、PPL。

コンソールのInstance Healthタブではボックスチャートでノードの健全性を一覧でき、青はノード間で一貫、赤は外れ値を示す。CLIでの確認コマンドも紹介。
