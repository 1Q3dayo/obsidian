---
title: "pythonは_(アンダースコア)の使い方を理解するだけでプロフェッショナルになれる"
source: "https://qiita.com/_Kohei_/items/069aa1e7b872f5ca96bf"
author:
  - "[[_Kohei_]]"
published: 2023-10-30
created: 2025-11-17
description: "アンダースコア活用で可読性を守る"
tags:
  - "ai_summary"
  - "python"
  - "style"
  - "naming"
  - "conventions"
---
## Key Points
- AIブームやPythonエコシステムの広がり、FastAPI+AWS構成などの実例を紹介しつつ、柔軟さゆえの読みづらさに言及。
- '_'の使い方を戻り値破棄/内部API命名/スネークケース/REPLの前回値の4パターンで整理。
- `_single_leading`, `single_trailing_`, `__double_leading`, `__double_trailing__`をPEP8準拠で分類し、公開制御や名前マングリング、特殊メソッドの意味を解説。
- `x, _ = func()` や数値リテラルの桁区切りなど具体例を示し、Pythonicな書き方を促している。
- 終盤でアンダースコア理解の重要性を訴え、参考リンクとQiitaカレンダー案内で締める。
## 補足メモ
- Medium記事へのリンクやサンプルコードがそのまま講習資料に転用しやすい構成。
