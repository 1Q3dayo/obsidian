---
title: "Vibe Codingの限界を学ぶ！「From Zero to SaaS: When Vibe Coding Meets Production」参加レポート #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/from-0-to-saas-report-reinvent-2025/"
author:
  - "[[佐藤智樹]]"
published: 2025-12-03
created: 2025-12-04
description: "Vibe Codingで作られたSaaSの限界を学ぶワークショップ。Amazon Q Developerで脆弱性分析。"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "saas"
  - "vibe-coding"
  - "security"
---

## 概要

AWS re:Invent 2025のワークショップ「From Zero to SaaS: When Vibe Coding Meets Production」の参加レポート。Vibe Codingで作られたSaaSアプリケーションの脆弱性を段階的に分析する内容。

## ワークショップの目標

- **Understand**: AIは常に正しいとは限らない、SaaSの概念はVibe Codingで失われることがある
- **Learn**: LLMに対して新しいルールを設定して知識を拡張する方法、AIに教える必要があるSaaSの概念

## アーキテクチャ

CloudFront + API Gateway + Lambda + DynamoDBの構成で複数テナントをもつSaaSのコードが提供された。

## 脆弱性の例

### IAM Role/PolicyのCondition不足

DynamoDBアクセス権のConditionがテナント単位で設定されていないため、他のテナントの情報も読み込める脆弱性。

**修正**: `conditions`を追加してテナントごとの分離をIAMレベルで担保

```typescript
conditions: {
  'ForAllValues:StringLike': {
    'dynamodb:LeadingKeys': ['tenant#${aws:PrincipalTag/TenantId}#*'],
  },
}
```

## ワークフロー

1. 脆弱性について、Amazon Q Developerが指摘できるかを確認
2. SaaS特有の問題の指摘ができないため、ルールを追加し再調査
3. 指摘事項が妥当であることを確認し、手動かQ Developerで修正
4. チェックツールで指摘の修正ができているか確認

## 所感

ドメインに特化した領域をLLMがまだ苦手なのは分かっていたが、SaaSのテナント設計という広く知られている概念でもうまく回答できていないことに驚き。エンジニアリングがある程度分かっている方がいないと今後大きく問題が出そう。

