---
title: "「私の環境では動く」を撲滅したDev Container導入記"
source: "https://zenn.dev/nabewata/articles/95361314ebaa30"
author:
  - "[[Zenn]]"
published: 2025-12-07
created: 2025-12-11
description: "Dev Containerで環境差異を撲滅。Dockerコンテナで開発環境を統一し、オンボーディングを高速化。"
tags:
  - "clippings"
  - "ai_summary"
  - "devcontainer"
  - "docker"
  - "development"
  - "vscode"
---

## 概要

Dev Containerを導入して環境構築のストレスを解消。VS Codeの機能で開発環境をDockerコンテナに統一し、「clone即開発」を実現。環境差異バグの撲滅と新メンバーのオンボーディング高速化を実現。

## 主要ポイント

### Dev Containerとは
- VS Code/Cursorの機能で開発環境をDockerコンテナ化
- `.devcontainer/devcontainer.json`で設定
- Node.js、CLIツール、DB、拡張機能までコードで定義

### 実装方法
- 最小構成: ベースイメージ指定とpostCreateCommandのみ
- Docker Compose連携: DBやRedisなどの依存サービスも管理
- features機能: AWS CLI、GitHub CLIなどを簡単追加

### 効果
- 新メンバーオンボーディングが劇的に高速化
- 環境差異によるバグが消失
- PC移行が容易に

