---
title: "API Gatewayのストリーミング機能を試してみました"
source: "https://qiita.com/yakumo_09/items/db2d2df88863136483e7"
author:
  - "[[yakumo_09]]"
published: 2025-11-29
created: 2025-12-04
description: "はじめに Amazon API Gatewayがストリーム応答をサポートするアップデートがありました。 いきなりですが、下はストリーミングと非ストリーミングの比較です。 めっちゃ見やすくなってますよね。 今回は動作検証をしながら、どのようなアップデー..."
tags:
  - "clippings"
  - "raw"
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=)

## Qiitaにログインして、便利な機能を使ってみませんか？

あなたにマッチした記事をお届けします

便利な情報をあとから読み返せます

[ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fyakumo_09%2Fitems%2Fdb2d2df88863136483e7&realm=qiita) [新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fyakumo_09%2Fitems%2Fdb2d2df88863136483e7&realm=qiita)

## はじめに

Amazon API Gatewayがストリーム応答をサポートするアップデートがありました。

いきなりですが、下はストリーミングと非ストリーミングの比較です。  
めっちゃ見やすくなってますよね。

[![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F3aba8a02-2200-4340-bade-ca38b181c2a6.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3c0a6a1e3c13da9ae50f831268efd75d)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F3aba8a02-2200-4340-bade-ca38b181c2a6.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3c0a6a1e3c13da9ae50f831268efd75d) [![](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F9b4e1afd-1fa1-4de5-b0b6-9062dbc746d7.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3235042ec94cbb9cbf699e0cae2acdb4)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F9b4e1afd-1fa1-4de5-b0b6-9062dbc746d7.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3235042ec94cbb9cbf699e0cae2acdb4)

今回は動作検証をしながら、どのようなアップデートなのか紹介できればと思います。

## 何が変わった？

API Gateway はこれまで、バックエンドがレスポンスをすべて生成し終わってからまとめて返す “バッファ方式” が基本でした。  
そのため、処理が重い API や、生成系の処理（例：Bedrock で文章を生成する API）では 最初のレスポンスが返ってくるまで待ち時間が長くなる という課題がありました。また、レスポンス全体をまとめて返す都合上、10MB のレスポンスサイズ制限 や 29 秒のタイムアウト の影響もあり、大きな出力や長時間処理には工夫が必要でした。

今回追加された「レスポンス・ストリーミング（Response Streaming）」は、バックエンドが生成したデータをそのまま 逐次クライアントへ送れるようになった新機能です。

Bedrock のような「トークン単位で徐々に出力が進む」モデルとは相性が良く、ユーザーは“最初の一文字目”をすぐに見ることができるようになります。これにより、チャットボットや文章生成系 API の体感速度（UX）は大きく改善されます。

## 作ってみる

本記事では、この新しいストリーミング機能を Amazon Bedrockをバックエンドに使った構成 で検証します。

- API Gateway
- Lambda
- Bedrock  
	という構成を用意し、
- 従来のバッファ方式とどう変わるのか
- Bedrock の出力がどのようにストリーミングされるのか
- UI 側ではどのタイミングでデータが到達するのか

を確認しながらまとめていきます。

### 構成図

AWSの公式ブログから構成図を拝借し、以下のような構成で今回検証します。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3951176/5b3d462b-a5bd-44c2-a551-9233573dcbb3.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F5b3d462b-a5bd-44c2-a551-9233573dcbb3.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=ec5bb709146fb45b30347ed9c457af32)

### Lambda関数

Lambdaのストリーミング関数ですが、現在Node.jsにしか対応していないようでした😭  
なので、今回はNode.jsで実施していきます。

コードは以下になります！また、Lambdaのタイムアウト時間も30秒くらいにしています。

index.mjs

```javascript
import {
  BedrockRuntimeClient,
  ConverseStreamCommand,
} from "@aws-sdk/client-bedrock-runtime";

// Lambda Response Streaming
export const handler = awslambda.streamifyResponse(
  async (event, responseStream, _ctx) => {
    // ---------------------------
    // 1. API Gateway 用のメタデータ
    // ---------------------------
    const httpStream = awslambda.HttpResponseStream.from(responseStream, {
      statusCode: 200,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "x-api-gw-streaming": "true",
      },
    });

    try {
      // ---------------------------
      // 2. 入力取得（POST body）
      // ---------------------------
      let userPrompt = "あなたのAWSの推しサービスを教えて";

      if (event?.body) {
        try {
          const body = JSON.parse(event.body);
          userPrompt = body.message ?? body.prompt ?? userPrompt;
        } catch (_) {
          /* malformed JSON → デフォルトで進む */
        }
      }

      // ---------------------------
      // 3. Bedrock クライアント
      // ---------------------------
      const client = new BedrockRuntimeClient({
        region: process.env.BEDROCK_REGION ?? "us-west-2",
      });

      // Claude 4.5 Haiku（Inference Profile）
      const modelId =
        "global.anthropic.claude-haiku-4-5-20251001-v1:0";

      // ---------------------------
      // 4. ConverseStream 呼び出し
      // ---------------------------
      const command = new ConverseStreamCommand({
        modelId,
        messages: [
          {
            role: "user",
            content: [
              { type: "text", text: userPrompt },
            ],
          },
        ],
      });

      const response = await client.send(command);

      // ---------------------------
      // 5. Bedrock のチャンクを逐次処理 → API Gateway へ流す
      // ---------------------------
      for await (const item of response.stream) {
        if (!item?.contentBlockDelta) continue;

        const delta = item.contentBlockDelta.delta;
        const text = delta?.text;

        if (text) {
          httpStream.write(text);
        }
      }

      // ---------------------------
      // 6. 完了
      // ---------------------------
      httpStream.end();
    } catch (e) {
      // ---------------------------
      // 7. エラー時もストリームを閉じる
      // ---------------------------
      console.error("Lambda Error:", e);

      httpStream.write("\n[ERROR]\n");
      httpStream.write(String(e));
      httpStream.end();
    }
  }
);
```

Lambda関数の実行ロールにBedrockのポリシーをつけるのも忘れずに！

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3951176/50a915e4-04a6-4bcc-9849-acc3d024d4d7.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F50a915e4-04a6-4bcc-9849-acc3d024d4d7.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=35785f1acca1b9d8adf27b95e1a75b1b)

### API Gateway

LambdaのトリガーとなるAPI Gatewayは設定欄から追加することができます。

[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3951176/1d2465f8-e086-4c03-8b02-0fc9acac7efd.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F1d2465f8-e086-4c03-8b02-0fc9acac7efd.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=73af5c631f2ebe1fda1aa7df737960c6)

ここは「REST API」を選択します。  
[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3951176/7d8f12e0-d082-4c29-9ae2-438ec0e4b231.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F7d8f12e0-d082-4c29-9ae2-438ec0e4b231.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=6a18c59d6f904a60c1728ffe09e302be)

API Gateawyの統合リクエストを設定します。  
[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3951176/c405a9c8-c07c-4eab-91ee-adf57579cb15.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2Fc405a9c8-c07c-4eab-91ee-adf57579cb15.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=b383b17820835fb5fbead1f03e6ad884)

レスポンス転送モードで「ストリーム」を選択します。  
[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3951176/ed521b19-e171-468f-9fa0-6b85d65b3638.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2Fed521b19-e171-468f-9fa0-6b85d65b3638.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=c0cf972c785c16d4a9c30446ca81a389)

あとは、APIをデプロイするだけです。

## 動作確認

ステージのツリーを開いて、URLをコピーします。  
[![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3951176/ec8c982b-5d85-458e-9f50-de8deb4186ef.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2Fec8c982b-5d85-458e-9f50-de8deb4186ef.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=7fb07bb72ce189764ac42fd6319f9266)

以下のコマンドターミナルから実行できます。

```text
curl --no-buffer {URL}
```

実行時は以下のようなイメージです！  
やはり処理がストリーミングされてくるといいですね。

[![2025-11-2913.33.19-ezgif.com-video-to-gif-converter.gif](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F6cd163fd-6bf6-4c0b-aaac-f1b52dae034f.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=5e62211c1e359d6387c1c4bcad220be0)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3951176%2F6cd163fd-6bf6-4c0b-aaac-f1b52dae034f.gif?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=5e62211c1e359d6387c1c4bcad220be0)

## さいごに

今回はAPI Gateawayのストリーミング処理を試してみました。  
今回はシンプルにモデル呼び出しでしたが、AgentCoreやStrandsと組み合わせるとより面白そうではありますね。  
機会があれば試してみたいと思います。

[0](https://qiita.com/yakumo_09/items/#comments)

コメント一覧へ移動

X（Twitter）でシェアする

Facebookでシェアする

はてなブックマークに追加する

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2Fyakumo_09%2Fitems%2Fdb2d2df88863136483e7&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2Fyakumo_09%2Fitems%2Fdb2d2df88863136483e7&realm=qiita)

[21](https://qiita.com/yakumo_09/items/db2d2df88863136483e7/likers)

いいねしたユーザー一覧へ移動

8