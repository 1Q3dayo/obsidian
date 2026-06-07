---
title: "クラウドエンジニアが効率よくClaude Codeを活用する方法"
source: "https://zenn.dev/incudata/articles/fb9d4b0389257f"
author:
published: 2026-04-13
created: 2026-06-07
description: "クラウドエンジニア向けClaude Code活用とコンテキスト管理の実践集。"
tags:
  - "clippings"
  - "ai_summary"
  - "claude-code"
  - "cloud-engineering"
  - "iac"
  - "terraform"
  - "context-management"
---

## 概要

クラウドエンジニアがClaude Codeを使う際の、CLAUDE.md設計、コンテキスト管理、IaC生成、アーキテクチャレビュー、運用ドキュメント生成の実践パターンを整理。特に、設計判断を先に固めてから実装させること、PlanとImplementを分けること、モデルを用途別に使い分けることを重視している。

## 主要ポイント

### CLAUDE.mdとコンテキスト
- CLAUDE.mdは全ルール集ではなく、500行以内のインデックスとして設計する
- 詳細手順はSkillなどオンデマンドで読ませる形に分離する
- 長いセッションではcontext rotを避けるため、compactやclearをタスク区切りで使う

### クラウド業務での使い方
- Terraform生成はいきなりコードを書かせず、要件と設計判断を先に出させる
- セキュリティ、コスト、可用性、Terraformベストプラクティスなど観点を明示してレビューさせる
- IaCからリソース一覧や運用ドキュメントを逆引き生成し、手動更新を減らす

### 避けるべき使い方
- CLAUDE.mdへの詰め込み、曖昧な依頼、大きすぎるタスク、Opus常用は効率を落とす
- 日常の修正やレビューはSonnet中心、複雑な設計はOpusなど用途で切り替える
