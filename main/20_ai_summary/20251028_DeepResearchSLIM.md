---
title: "「Deep Research」の精度を要約で底上げする"
source: "https://zenn.dev/knowledgesense/articles/92d21e1c57c828"
author:
  - "[[Zenn]]"
published: 2025-10-28
created: 2025-11-17
description: "SLIM手法でDeepResearchの文脈爆発を抑える"
tags:
  - "clippings"
  - ai_summary
  - research
  - llm
  - summarization
  - workflow
---
## 要約
ナレッジセンス須藤氏による、LLMのDeepResearchループで起きるコンテキスト肥大と精度低下を、要約モジュール「SLIM」で抑える手法の紹介。検索ツール・閲覧ツール・要約モジュールの3構成を用い、決められた観点（これまでの発見／現在の仮説／次の予定）で要約し続けることで、情報を失わず調査を深める。

## 重点ポイント
- DeepResearchは反復検索で膨大なテキストを扱えるが、情報過多で精度が落ちる。SLIMは50回に1回要約を挟み、「必要十分な情報だけを残す」ことに専念。
- 要約観点を適切に設計することが最重要。観点が質問とマッチしないと肝心の情報が消える危険がある。
- BrowseCompやHLEとの比較では、SLIMがループ回数150でも精度を維持し、コストも抑えられた。

## メモ
- 幅広い題材での観点設計が課題として残っており、応用する際は質問カテゴリごとのテンプレを作る必要がある。
