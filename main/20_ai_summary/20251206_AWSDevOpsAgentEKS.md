---
title: "AWS DevOps Agent (Preview)のEKSアクセス設定をやってみた #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/aws-devops-agent-preview-eks-access/"
author:
published: 2025-12-06
created: 2025-12-09
description: "AWS DevOps AgentにEKSアクセスを許可。Pod状態やKubernetesイベントを直接取得し、Root Cause特定を迅速化。"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "devops"
  - "eks"
  - "kubernetes"
---

## 概要

AWS DevOps AgentにEKSアクセス設定を追加。EKS Access EntriesでDevOpsAgentRoleにAIOpsAssistantPolicyを付与するだけで、EKS API経由で直接調査可能に。CloudWatch Logs経由の間接調査から直接調査へ変更し、Root Cause特定が迅速かつ明確に。

## 主要ポイント

### EKSアクセス設定
- EKS Access EntriesでIAMロールを追加
- AIOpsAssistantPolicyを付与
- 設定は非常にシンプル

### 効果
- Pod状態やKubernetesイベントを直接取得
- CloudWatch Logs経由の間接調査から直接調査へ
- Root Cause特定が迅速かつ明確に

### 検証内容
- サンプルEKSアプリのデプロイ
- 意図的な障害発生（DB停止）
- EKSアクセス設定前後の比較

