---
title: "EKS Capabilities で AWS Controllers for Kubernetes(ACK) を利用してみた #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/eks-capabilities-aws-controller-for-kubernetes/"
author:
published: 2025-12-05
created: 2025-12-09
description: "EKS CapabilitiesのACK機能でKubernetes API経由でAWSリソースを構築。GitOpsによるインフラ管理とドリフト修正を実現。"
tags:
  - "clippings"
  - "ai_summary"
  - "eks"
  - "kubernetes"
  - "aws"
  - "ack"
---

## 概要

EKS CapabilitiesのACK（AWS Controllers for Kubernetes）機能を紹介。Kubernetes API経由でAWSリソースを構築し、アプリケーションリソースとクラウドリソースを統一管理。Reconciliation loopによるドリフト修正とGitOps導入を実現。

## 主要ポイント

### ACKとは
- Kubernetes API経由でAWSリソースを構築
- 50以上のAWSサービスに対応
- Reconciliation loopでドリフトを自動修正（10時間ごと）

### セットアップ
- EKS Capabilityロールの作成
- IAMロールに権限付与
- Capabilityの作成と有効化

### 実装例
- S3バケットの作成例を紹介
- ライフサイクルルール、暗号化、パブリックアクセスブロックの設定

