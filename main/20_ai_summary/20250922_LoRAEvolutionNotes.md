---
title: "LoRAの進化：基礎から最新のLoRA-Proまで"
source: "https://zenn.dev/mkj/articles/11168509d10eb4"
author:
  - "[[Zenn]]"
published: 2025-09-22
created: 2025-11-17
description: "LoRA派生比較とLoRA-Pro解説"
tags:
  - "ai_summary"
  - "finetuning"
  - "lora"
  - "optimization"
  - "research"
---
## Key Points
- LoRA派生手法をスケーリング調整、構造変更、勾配最適化/初期化の系統に分類し、AdaLoRA/rsLoRA/DoRA/LoRA+/PiSSA/LoRA-GA/LoRA-Proを比較。
- LoRA-ProはLoRA更新がフルファインチューニングの低ランク勾配に等価という洞察から、勾配のフロベニウスノルム差を最小化する最適化問題として定式化。
- Sylvester方程式で任意行列Xを求め、A/B行列をフルFTの勾配方向に沿わせる手順と、Llama-2で初期ステップ後にフルランク化する実験を紹介。
- GLUE等でLoRA-Proが他手法やフルFTを上回る例と、DeepSpeed実装のみ/PEFT未統合という実用上の課題が挙げられている。
## 実務メモ
- 勾配計算コスト増と専用Optimizer依存を理解した上で、導入可能な環境かどうかを先に確認する必要があると示唆している。
