---
title: "Findyの爆速インフラ構築を支えるTerraform活用術 〜汎用モジュール編〜"
source: "https://tech.findy.co.jp/entry/2026/01/26/070000"
author:
  - "[[kouzyun]]"
  - "[[たかぼー (id:Taka_bow)]]"
  - "[[starfish719]]"
  - "[[thedan]]"
  - "[[nesskazu]]"
  - "[[Shun (id:ShunDeveloper)]]"
  - "[[とみー (id:Cooking_ENG)]]"
  - "[[ryu-furuta]]"
  - "[[dev2bo]]"
  - "[[adachin (id:adachin0817)]]"
published: 2026-01-26
created: 2026-01-27
description: "Findy SREチームがTerraform汎用モジュールで6サービスのインフラを高速構築した事例"
tags:
  - "clippings"
  - "ai_summary"
  - "terraform"
  - "aws"
  - "infrastructure"
  - "sre"
---

## 要約

FindyのSREチーム（4名）が2025年に6サービスのインフラ環境を短期間で構築した事例。頻繁に利用するAWSリソース（ECS、ALB、RDS、VPCなど）を再利用可能なTerraform汎用モジュールとして整備し、HCP Terraformのプライベートレジストリに登録して共有。

Network、Container、Databaseなどカテゴリ別にパッケージを分け、パラメータ指定だけで標準化された環境が立ち上がる仕組みを実現。Production+Staging環境を最短3日で構築可能に。新メンバーもすぐ戦力化できる。

課題として「planは成功するがApplyが失敗する」問題が発生し、Terraform Testで対処。今後はPlatform Engineering推進で開発チームの自律的インフラ構築を目指す。
