---
title: "Claude Code に draw.io の図を描かせるコツ"
source: "https://zenn.dev/genda_jp/articles/2025-12-12-drawio-tips-claude-code"
author:
published: 2025-12-12
created: 2025-12-19
description: "Claude Codeでdraw.io図を描く際のハマりポイントと解決策。フォント反映、矢印ラベル被り、テキスト改行などの対処法。"
tags:
  - "clippings"
  - "ai_summary"
  - "claude"
  - "draw.io"
  - "diagram"
  - "ai-coding"
---

## 概要

Claude Codeでdraw.io形式の図を描く際のハマりポイントと解決策。フォントが反映されない、矢印がラベルと被る、テキストが意図しない改行をするなどの問題への対処法を実践的に解説。

## 主要ポイント

### フォント設定
- defaultFontFamilyだけでは不十分
- 各要素にfontFamilyを明示
- PNG出力時のフォント反映

### 矢印とラベル
- ラベル位置の調整
- 矢印とラベルの重なり回避

### テキスト改行
- 意図しない改行の防止
- テキスト幅の制御

### メリット
- 自然言語での指示
- 一括変更が高速
- Gitでバージョン管理可能

