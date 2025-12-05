---
title: "Kubernetes History Inspector(KHI)を使って入門する本格的なKubernetesの障害原因調査(RCA)"
source: "https://zenn.dev/google_cloud_jp/articles/703890e264751f"
author:
  - "[[Zenn]]"
published: 2025-12-02
created: 2025-12-04
description: "KHIはKubernetesの障害原因調査用ログビューア。タイムライン可視化で迅速なRCAを実現。"
tags:
  - "clippings"
  - "ai_summary"
  - "kubernetes"
  - "troubleshooting"
  - "gke"
  - "rca"
---

## 概要

Kubernetes History Inspector (KHI)は、Kubernetes上の障害原因調査（RCA）を迅速に行うためのログビューア。Google Cloudの技術サポートチームで開発され、数千のサポートケースで活用されている。

## KubernetesのRCAの難しさ

- 動的なスケーリングや自動回復により、問題発生時に既に解消していることが多い
- 多数のコンポーネントが自立分散的に稼働し、ログが散在
- ログのタイミングを見て複数のログを突合する必要がある

## KHIの特徴

- **ログビューア**: クラスタ上にエージェントをインストールする必要がない
- **タイムライン表示**: クラスタ上の各リソースの状態をログから復元しタイムラインとして表示
- **リソーストポロジ**: 特定のタイミングのリソース配置をダイアグラムとして表示
- **Cloud Logging連携**: Cloud Logging上のログを活用

## 使い方

1. Dockerで起動: `docker run -p 127.0.0.1:8080:8080 gcr.io/kubernetes-history-inspector/release:latest`
2. `New inspection`からクラスタタイプとログタイプを選択
3. 時間範囲を指定してログを収集
4. タイムライン画面で問題のありそうなリソースを特定
5. リソースをクリックして関連ログをドリルダウン

## 実例: Service接続問題の調査

- EndpointSlicesでReady状態を確認
- Podのタイムラインで終了処理を確認
- コンテナIDも自動認識してPod名・コンテナ名に置き換え
- `.status.containerStatuses`でコンテナの状態を確認

