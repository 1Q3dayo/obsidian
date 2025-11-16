---
title: "Amazon ECS でリニアデプロイとカナリアデプロイが標準機能としてサポート開始 - AWS"
source: "https://aws.amazon.com/jp/about-aws/whats-new/2025/10/amazon-ecs-built-in-linear-canary-deployments/"
author:
  - "[[Amazon Web Services]]"
  - "[[Inc.]]"
published:
created: 2025-11-17
description: "AWS の新機能についてさらに詳しく知るには、 Amazon ECS でリニアデプロイとカナリアデプロイが標準機能としてサポート開始"
tags:
  - "clippings"
  - raw

---
## Amazon ECS でリニアデプロイとカナリアデプロイが標準機能としてサポート開始

投稿日: 2025年10月30日

[Amazon Elastic Container Service](https://aws.amazon.com/ecs/) (Amazon ECS) でリニアデプロイとカナリアデプロイがサポートされるようになりました。これにより、コンテナ化されたアプリケーションのデプロイ時に、より柔軟かつ細かな制御が可能になります。これらの新しいデプロイ戦略は、ECS に備わっているブルー/グリーンデプロイを補完するもので、お客様はアプリケーションのリスク許容度や検証要件に応じて、最適なトラフィックの切り替え方法を選べます。

リニアデプロイでは、現在のサービスリビジョンから新しいリビジョンへ、指定した期間内に一定の割合で段階的にトラフィックを切り替えられます。各ステップでどの程度トラフィックを切り替えるかを制御するために、ステップの割合 (例: 10%) を設定します。また、切り替えの間にモニタリングや検証を行うための待機時間 (ステップベイク時間) も設定します。これにより、本番トラフィックを徐々に増やしながら新しいアプリケーションバージョンを複数段階で検証できます。カナリアデプロイでは、まず本番トラフィックのごく一部を新しいリビジョンにルーティングし、残りの大部分は現行の安定したバージョンにとどめます。カナリアベイク時間を設定することで、新しいリビジョンのパフォーマンスをモニタリングし、その後に Amazon ECS によって残りのトラフィックが新しいリビジョンへ切り替えられます。どちらの戦略でも、すべての本番トラフィックを新しいリビジョンに切り替えた後に、旧リビジョンを終了するまでの待機時間 (デプロイベイク時間) を設定できます。これにより、問題が発生した場合でもダウンタイムなしで迅速にロールバックできます。デプロイライフサイクルフックを設定すれば、独自の検証ステップを組み込むことも可能です。また、Amazon CloudWatch アラームを使用すれば、障害を自動的に検出してロールバックをトリガーできます。

この機能は、Amazon ECS が提供されているすべての商用 [AWS リージョン](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) で利用できます。 リニアデプロイやカナリアデプロイは、Application Load Balancer (ALB) または ECS Service Connect を使用する新規または既存の Amazon ECS サービスに対して使用できます。この操作は、AWS マネジメントコンソール、SDK、CLI、CloudFormation、CDK、Terraform を使って実行できます。詳細については、 [Amazon ECS のリニアデプロイ](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-linear.html) および [カナリアデプロイ](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/canary-deployment.html) に関するドキュメントをご覧ください。