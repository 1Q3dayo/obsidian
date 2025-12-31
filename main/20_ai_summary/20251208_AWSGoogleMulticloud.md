---
title: "【レポート】 AWS re:Invent に Google が登壇！AWS Interconnect - Multicloud による手間のかからないマルチクラウド #NET205 #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/aws-re-invent-google-aws-interconnect-multicloud-net205-awsreinvent/"
author:
published: 2025-12-08
created: 2025-12-09
description: "AWS Interconnect - MulticloudでAWSとGoogle Cloudを直結。VPC同士を接続するだけでマルチクラウド接続を実現。"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "google-cloud"
  - "multicloud"
  - "networking"
---

## 概要

AWS re:InventでGoogleが登壇。AWS Interconnect - Multicloudを紹介。AWSとGoogle CloudをVPC同士を接続するだけでマルチクラウド接続を実現。複雑な設定不要で、作成と承認のみで完了。

## 主要ポイント

### AWS Interconnect - Multicloud
- Direct Connect GatewayとCloud Routerを接続
- 2箇所以上の物理施設で冗長化
- ユーザールーターやBGP設定不要

### 従来の課題
- スケーラビリティ
- 管理コスト
- 障害点の増加
- トラブルシューティングの難しさ

### リファレンスアーキテクチャ
- 単一リージョン - 単一Interconnect
- マルチリージョン - 単一Interconnect（Cloud WAN連携）
- マルチリージョン - マルチInterconnect

