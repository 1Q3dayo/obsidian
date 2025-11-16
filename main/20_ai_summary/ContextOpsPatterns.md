---
title: "Context Engineering"
source: "https://zenn.dev/kun432/scraps/d462287d9dbfa9"
author:
  - "[[Zenn]]"
published: 5ヶ月前にクローズ
created: 2025-11-17
description: "圧縮・永続化・分離で文脈管理"
tags:
  - "ai_summary"
  - "agents"
  - "context"
  - "optimization"
  - "scaling"
---
## Key Points
- LLMはCPU、コンテキストはRAMという比喩で、指示/知識/ツール出力を限られたウィンドウに詰める技術を整理している。
- 圧縮カテゴリではオートコンパクトや階層的要約、Devin型のイベント保持など、長尺コンテキストを段階的に縮める手法を比較。
- 永続化カテゴリではファイル/埋め込み/知識グラフ/Reflexionメモリの使い分けと、類似度・最新性・重要度スコアリングの指標をまとめる。
- 分離カテゴリではPydanticスキーマでmessagesとsectionsを切り分ける、Swarmのサブエージェント、CodeAgentのサンドボックスなどを紹介。
- レッスンとして、トークン計測→状態スキーマ設計→ツール出力の圧縮→小さなメモリから開始→並列タスクならマルチエージェント検討、という段階的指針を提示。
## 補足メモ
- 会議調整のCheap DemoとMagical Productの比較が掲載され、コンテキストの量と質で体験がどう変わるかが直感的に理解できる。
