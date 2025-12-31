---
title: "Amazon RDS for MySQL と Amazon Aurora MySQL で高速な InnoDB パージを実現する"
source: "https://aws.amazon.com/jp/blogs/news/achieve-a-high-speed-innodb-purge-on-amazon-rds-for-mysql-and-amazon-aurora-mysql/"
author:
published: 2025-12-23
created: 2025-12-24
description: "RDS/Aurora MySQLでInnoDBパージを高速化。MVCCのundoログ処理を最適化し、パフォーマンス低下を防止。"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "rds"
  - "mysql"
  - "database"
---

## 概要

RDS/Aurora MySQLでInnoDBパージを高速化する設計・チューニング戦略。MVCCのundoログ処理を最適化し、パフォーマンス低下を防止。ワークロード最適化、キャパシティプランニング、設定調整を組み合わせて実現。

## 主要ポイント

### パージの仕組み
- MVCCのundoログと削除マーク付きレコードをクリーンアップ
- パージスレッドがマルチスレッドで処理
- ロールバックセグメント履歴リストから順次処理

### 最適化手法
- DELETEよりDROP PARTITION/DROP TABLEを選択
- 長時間実行クエリを避ける
- セカンダリインデックスの最適化
- テーブル分散による並列処理効率化

### 監視とアラーム
- RollbackSegmentHistoryListLengthを監視
- CloudWatchアラーム設定
- インスタンスサイズの適切な選択

