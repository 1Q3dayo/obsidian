---
title: "[アップデート] Amazon SES API VPCエンドポイントが使用できるようになりました | DevelopersIO"
source: "https://dev.classmethod.jp/articles/amazon-ses-vpc-api-endpoints/"
author:
published: 2025-12-08
created: 2025-12-09
description: "SES API VPCエンドポイントでNAT Gateway不要に。API経由でのメール送信がVPCエンドポイント経由で可能に。"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "ses"
  - "vpc"
  - "networking"
---

## 概要

Amazon SES API VPCエンドポイントが利用可能に。従来はSMTPインターフェイスのみサポートしていたが、API経由でのメール送信もVPCエンドポイント経由で可能に。NAT Gateway不要でセキュアなメール送信を実現。

## 主要ポイント

### 新機能
- SES API VPCエンドポイントのサポート
- NAT Gateway不要でメール送信可能
- セキュリティポリシーに適合

### 設定方法
- VPCエンドポイントの作成
- ルートテーブルの設定
- 送信承認ポリシーの設定

### 効果
- コスト削減（NAT Gateway不要）
- セキュリティ向上
- 特定のVPCエンドポイント経由のみ許可可能

