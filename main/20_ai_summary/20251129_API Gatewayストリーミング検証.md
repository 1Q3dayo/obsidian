---
title: "API Gatewayのストリーミング機能を試してみました"
source: "https://qiita.com/yakumo_09/items/db2d2df88863136483e7"
author:
  - "[[yakumo_09]]"
published: 2025-11-29
created: 2025-12-04
description: "API Gatewayのレスポンスストリーミング機能をBedrockとLambdaで実装。逐次応答でUX改善。"
tags:
  - "clippings"
  - "ai_summary"
  - "aws"
  - "api-gateway"
  - "streaming"
  - "lambda"
  - "bedrock"
---

## 概要

Amazon API Gatewayがストリーム応答をサポートする新機能を紹介。従来のバッファ方式から逐次送信方式への変更により、Bedrockなどの生成系APIの体感速度が大幅に改善される。

## 主な変更点

- **バッファ方式からストリーミング方式へ**: バックエンドが生成したデータを逐次クライアントへ送信可能に
- **UX改善**: チャットボットや文章生成系APIで最初の一文字目をすぐに表示可能
- **制限緩和**: 10MBのレスポンスサイズ制限や29秒のタイムアウトの影響を軽減

## 実装構成

- **API Gateway**: REST APIでストリーミングモードを有効化
- **Lambda**: Node.jsでストリーミング関数を実装（`awslambda.streamifyResponse`を使用）
- **Bedrock**: Claude 4.5 Haikuを使用し、`ConverseStreamCommand`でストリーミング応答を取得

## 実装のポイント

1. Lambda関数で`awslambda.streamifyResponse`を使用してストリーミング対応
2. API Gatewayの統合リクエストでレスポンス転送モードを「ストリーム」に設定
3. Bedrockのチャンクを逐次処理して`httpStream.write()`で送信

## 動作確認

`curl --no-buffer {URL}`でストリーミング動作を確認。処理が逐次送信される様子を確認できる。

