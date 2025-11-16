---
title: "2025年版 サーバーレス Web アプリケーションの作り方"
source: "https://speakerdeck.com/hayatow/2025nian-ban-sabaresu-web-apurikesiyonnozuo-rifang"
author:
  - "[[Hayato Watanabe]]"
published: 2025-09-20
created: 2025-11-17
description: "サーバーレスWeb構成の比較指針"
tags:
  - "ai_summary"
  - "serverless"
  - "architecture"
  - "aws"
  - "frontend"
---
## Key Points
- ServerlessDays Tokyo 2025の資料で、AWS上のWebアプリをSPA/SSR/SSG/ISRの4方式に分類し、CloudFront+S3+API Gateway+Lambdaなどの組み合わせを図解。
- SPAはフロントとAPIを別技術で構築できるが、OpenAPI等で契約を固定しないと互換性維持が難しいと注意している。
- SSR/常駐型(Fargate)とイベント駆動型(Lambda)の比較では、レンダリング責務やチームスキル統一、コスト最適化の観点を整理。
- B2B IoT可視化案件など実例を通じて、Vue.js SPA+Python APIを選択した理由と後にSSRへ載せ替えた際のメリデメを共有。
- AWS CDKで責務を分けつつAmplifyを採用しなかった判断や、ECS常駐→Lambda移行によるコスト効果など意思決定プロセスを記録。
## 実装ヒント
- レンダリング方式を選ぶ前に保守担当とAPI検証方法を明確にし、資料のチェックリストをミーティングテンプレに流用できる。
