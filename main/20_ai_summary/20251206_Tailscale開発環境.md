---
title: "Tailscaleを利用して開発環境を整える"
source: "https://zenn.dev/chamafoobar/articles/8ccdb552ef0acf"
author:
published: 2025-12-06
created: 2025-12-11
description: "TailscaleでVPN構築。自宅サーバーへの安全なSSHアクセスとプライベートダッシュボードへのアクセスを実現。"
tags:
  - "clippings"
  - "ai_summary"
  - "tailscale"
  - "vpn"
  - "development"
  - "networking"
---

## 概要

Tailscaleを利用してVPNを構築し、開発環境を整備。自宅のLinuxサーバーへの安全なSSHアクセスとプライベートダッシュボードへのアクセスを実現。無料プランで100台まで接続可能。

## 主要ポイント

### Tailscaleとは
- WireGuardベースのVPNサービス
- 簡単にVPN構築可能
- SOC2レポート取得済み

### 利用シーン
- 自宅サーバーへのSSHアクセス（VS Code Remote - SSH）
- プライベートダッシュボードへの安全なアクセス
- magicDNSによる名前解決

### 設定方法
- デバイスの追加はコマンド実行と認証のみ
- Admin Consoleから管理
- 無料プランで100台まで

