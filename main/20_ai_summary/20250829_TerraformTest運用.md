---
title: "Findyの爆速インフラ構築を支えるTerraform活用術 〜Terraform Test導入編〜"
source: "https://zenn.dev/findyinc/articles/terraform-test"
author:
  - "[[Findy]]"
published: 2025-08-29
created: 2025-11-17
description: "Terraform Testで汎用モジュールを検証する仕組み"
tags:
  - "clippings"
  - ai_summary
  - terraform
  - testing
  - ci
  - sre
---
## 要約
FindyのSREチームが、汎用TerraformモジュールのPlan/Apply落差や構築失敗を解消するためにTerraform Testを導入した記録。Unitテスト（plan）とIntegrationテスト（apply）を分け、mock providerや依存モジュール連携、GitHub Actionsでの自動実行方法まで具体例を示す。

## 重点ポイント
- `.tftest.hcl`にrunブロックを記述し、assertでリソースの属性を検証。`command=plan`で論理チェック、`command=apply`で実リソース検証を切り替える。
- mock providerで外部データソースをスタブ化し、依存モジュールが必要なIntegrationテストはネットワーク→コンテナの順にrunして出力値を受け渡す構成にしている。
- CIではPR作成時にUnitテストを実行し、mainマージ後にSandbox環境でIntegrationテストを走らせてからHCP Terraformへリリース。Auroraなど時間が掛かるテストは後段に回してレビュー速度を維持。

## メモ
- 「汎用モジュール＋Terraform Test＋CI」の組み合わせで、Plan成功後のApply失敗という典型的なIaC痛点を自動検出できる体制を作っている。
