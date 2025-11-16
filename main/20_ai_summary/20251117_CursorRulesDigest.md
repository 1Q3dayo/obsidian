---
title: "kinopeee/cursorrules"
source: "https://github.com/kinopeee/cursorrules"
author:
  - "[[kinopeee]]"
published:
created: 2025-11-17
description: "Cursor向けv5カスタム指示の狙い"
tags:
  - "ai_summary"
  - "cursor"
  - "workflow"
  - "automation"
---
## Key Points
- Cursor Agent用カスタムインストラクションv5はタスク着手前にチェックリストを作り、軽量/標準/重要に応じて報告粒度を変えて分析力不足を補う。
- Auto-Run前提で重複生成や意図しないデザイン変更、無限ループを防ぐガードを盛り込み、モデル刷新に合わせた改善を続けている。
- '/'始まりの入力をスラッシュコマンドとみなし、AIがコマンドファイルを編集しない/明示引数だけを渡すといった安全策を定義。
- `.cursor/rules`にv5(日本語/英語)とtest-strategyを配置する手順、alwaysApply設定の調整、等価分割や境界値分析などのテスト方針ルールを説明。
- User RulesやMemoriesとの矛盾回避、フィードバック窓口(X/Misskey/マシュマロ)やMITライセンス情報も明記されている。
## 運用メモ
- CHANGELOGとTRANSLATION_GUIDEを参照し、導入前に現行ルールとの差分レビューとモデル評価を行うことが推奨される。
