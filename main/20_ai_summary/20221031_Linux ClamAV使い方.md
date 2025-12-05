---
title: "Linux向けウィルス対策ソフトClamAVの使い方"
source: "https://zenn.dev/gladevise/articles/clamav-usage"
author:
  - "[[Zenn]]"
published: 2022-10-31
created: 2025-12-04
description: "ClamAVの基本的な使い方。clamscanとclamdscanの違い、clamd.conf設定方法を解説。"
tags:
  - "clippings"
  - "ai_summary"
  - "linux"
  - "security"
  - "antivirus"
  - "clamav"
---

## 概要

Linux向けウィルス対策ソフトClamAVの基本的な使い方を解説。`clamscan`と`clamdscan`の違い、`clamd.conf`の設定方法を紹介。

## ClamAVの特徴

- Linux、macOS、Windowsで動作
- オープンソースのウィルス対策ソフト
- クロスプラットフォームなウィルスにも対応

## インストール

```bash
sudo apt install -y clamav clamav-daemon libclamunrar9
```

## スキャン方法

### clamscan vs clamdscan

| 比較項目 | clamscan | clamdscan |
| --- | --- | --- |
| 実行スレッド | シングルスレッド | マルチスレッド |
| ウィルスDBロード | 実行時 | clamd実行時 |
| 設定方法 | コマンドラインオプション | clamd.conf |

- **clamscan**: 手元のファイルをちょっとスキャンしたい場合
- **clamdscan**: 定期実行や大量ディレクトリのスキャンに便利

## clamd.confの設定

よく使うオプション:
- `LogFile`: ログファイルのパス
- `MaxThreads`: マルチスレッド時の最大スレッド数（CPU冷却に難があるハードウェアでは重要）
- `MaxScanSize`: 圧縮ファイルの最大サイズ
- `MaxFileSize`: ファイルの最大サイズ

