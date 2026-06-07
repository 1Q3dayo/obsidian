---
title: "Terraformプロジェクトのオンボーディングコストをmise + aquaで削減した話"
source: "https://zenn.dev/leaner_dev/articles/e8297dcffcd38c"
author:
published: 2026-06-03
created: 2026-06-07
description: "miseとaquaでTerraform開発環境と認証設定を標準化する方法。"
tags:
  - "clippings"
  - "ai_summary"
  - "terraform"
  - "mise"
  - "aqua"
  - "aws"
  - "datadog"
---

## 概要

Terraformプロジェクトで必要なCLI、PATH、AWSプロファイル、Datadogキーの扱いをmiseとaquaで標準化し、オンボーディング時の手順差分を減らす方法を紹介。`mise install` を起点にaqua管理ツールの準備、AWS設定ファイルの固定、Terraform ephemeralによる秘匿情報参照までをまとめている。

## 主要ポイント

### miseとaquaの役割
- miseでaqua自体のバージョンを管理し、`mise install` で導入できるようにする
- miseのpostinstall hookで `aqua install -l` を実行し、必要CLIのリンクを自動準備
- miseのenv設定でaquaのPATHを通し、個人のシェル設定に依存しない形にする

### 認証情報の標準化
- `AWS_CONFIG_FILE` をプロジェクト配下に向け、AWS profile名をチームで統一
- DatadogなどのAPIキーはTerraform ephemeralブロックでSSM Parameterから参照
- tfstateやローカルPCに機密値を残さず、plan実行に必要な情報を揃える

### 効果
- 導入前はaqua導入、PATH設定、profile記載、APIキー設定が個人作業だった
- 導入後はmiseのtrust/installを実行すれば、Terraform planに必要な環境がほぼ整う
