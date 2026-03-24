---
title: "Claude Codeに長期記憶を持たせたら、壁打ちの質が変わった"
source: "https://zenn.dev/noprogllama/articles/7c24b2c2410213"
author:
  - "[[Zenn]]"
published: 2026-03-22
created: 2026-03-23
description: "SQLite+ベクトル検索でClaude Codeの長期記憶エンジンsui-memoryを自作した話"
tags:
  - "clippings"
  - "ai_summary"
  - "claude"
  - "memory"
  - "rag"
  - "sqlite"
---

## 要約

CLAUDE.mdでは伝えられない「過去の会話の文脈」を保持するため、記憶エンジン「sui-memory」を自作した実践記録。1,942セッション分・7,059件のメモリを蓄積し、壁打ちの精度が向上した。

設計方針は3つ：SQLite1ファイル完結、LLM不使用（トークン消費ゼロ）、セッション終了時の自動保存。会話をQ&A形式にチャンク分割し、日本語特化モデルRuri v3でベクトル化してSQLiteに保存。

検索はFTS5によるキーワード検索とベクトル検索をRRF（Reciprocal Rank Fusion）で統合。時間減衰（半減期30日）も導入。前回の失敗（claude-mem：LLM要約でトークン消費大）を踏まえ、生のtranscriptをルールベースで分割する方式に切り替えた。
