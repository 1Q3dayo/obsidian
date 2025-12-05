---
title: "Vibe Codingの限界を学ぶ！「From Zero to SaaS: When Vibe Coding Meets Production」参加レポート #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/from-0-to-saas-report-reinvent-2025/"
author:
  - "[[佐藤智樹]]"
published: 2025-12-03
created: 2025-12-04
description:
tags:
  - "clippings"
  - "raw"
---
## はじめに

今回は、「From Zero to SaaS: When Vibe Coding Meets Production」というワークショップの参加レポートです。構築済みのSaaSアプリケーションにAmazon Q Developerを使って、脆弱性を段階的に分析していくという内容でした。人間側が適切な指示を行えなければ、AIエージェントも適切にレビューができないという限界を感じられた内容で、Vibe Codingの限界を知るために非常に良い内容でした。

## 概要(日本語訳)

Vibeコーディングは楽しく高速ですが、本番環境のSaaSを構築する際に隠れたギャップを残す可能性があります。このハンズオン形式のビルダーセッションでは、Vibeコーディングで作成されたSaaSアプリケーションを本番稼働に向けて準備する任務を負ったAWS開発者の役割を担います。LLMが見落としがちなコードの穴を発見します。その後、堅牢なセキュリティとスケーラビリティを実現するためにコードベースを本番環境対応にするためのルールとより賢いプロンプトを学びます。テナントコンテキストとIAMポリシーに取り組みながら、強力な戦略と実用的なSaaSパターンを学びます。より深いSaaSの勘、向上したAIアシスタントスキル、そして本番環境のSaaSアプリにおいて「Vibe」がどこで不十分になるかの明確な見解を持ち帰ってください。

## 内容

このビルダーズセッションでは、最初に以下のような目標が設定されました。

- Understand
	- AI は常に正しいとは限らないことを知る — 基盤モデルはすべてを知っているわけではない！
	- SaaS の概念は、Vibe Codingで失われることがある
- Learn
	- LLMに対して新しいルールを設定して、知識を拡張する方法
	- AI に教える必要がある SaaS の概念

タイトルの通り、Vibe Codingで作られたアプリケーションの限界を知るためのワークショップでした。実際のアーキテクチャ自体は、以下のようなCloudFront+API Gateway+Lambda+DynamoDBの構成で複数テナントをもつSaaSのコードが提供されました。

![IMG_5003.jpeg](https://devio2024-2-media.developers.io/upload/6SxfQhAuEvOXuP6ne0ms3I/2025-12-03/u7qrzbNtFEQQ.jpeg)

上記のアーキテクチャとアプリケーションを実現するコードが提供されます。このコードの中には、SaaSのテナント分離特有の考え方が実装されていない部分が複数あり、それをAmazon Q Developerが指摘できるか確認していくワークを行いました。

ミッションとしては、5つのテーマが用意され、それぞれに合わせて5つの脆弱性が埋め込まれたコードが提供されます。

![IMG_5004.jpeg](https://devio2024-2-media.developers.io/upload/6SxfQhAuEvOXuP6ne0ms3I/2025-12-03/d0f6GYNUcGFW.jpeg)

たとえば、1つはLambda→DynamoDBのアクセス権に関するものです。以下のようなCDKのコードでIAM Role/PolicyのConditionがテナント単位で設定されていないため、他のテナントの情報も読み込める脆弱性です。

```ts
export class ApplicationTable extends Construct {
  public readonly table: TableV2;

  constructor(scope: Construct, id: string, props: ApplicationTableProps) {
    super(scope, id);

    this.table = new TableV2(this, 'Data', {
      // 割愛
    });
  }
  grantWrite(role: Role) {
    role.addToPolicy(
      new PolicyStatement({
        effect: Effect.ALLOW,
        actions: [
          'dynamodb:BatchGetItem',
          'dynamodb:BatchWriteItem',
          'dynamodb:ConditionCheckItem',
          'dynamodb:DeleteItem',
          'dynamodb:DescribeTable',
          'dynamodb:GetItem',
          'dynamodb:PutItem',
          'dynamodb:Query',
          'dynamodb:UpdateItem',
        ],
        resources: [
          this.table.tableArn,
        ]
      }),
    );
  }
```

ここにConditionを入れる必要があることを指摘させて、以下のように修正させるよう進めます。conditionsが設定されることで、テナントごとの分離がIAMレベルでも担保できます。

```ts
export class ApplicationTable extends Construct {
  public readonly table: TableV2;

  constructor(scope: Construct, id: string, props: ApplicationTableProps) {
    super(scope, id);

    this.table = new TableV2(this, 'Data', {
      // 割愛
    });
  }
  grantWrite(role: Role) {
    role.addToPolicy(
      new PolicyStatement({
        effect: Effect.ALLOW,
        actions: [
          'dynamodb:BatchGetItem',
          'dynamodb:BatchWriteItem',
          'dynamodb:ConditionCheckItem',
          'dynamodb:DeleteItem',
          'dynamodb:DescribeTable',
          'dynamodb:GetItem',
          'dynamodb:PutItem',
          'dynamodb:Query',
          'dynamodb:UpdateItem',
        ],
        resources: [
          this.table.tableArn,
        ],
        conditions: {
          'ForAllValues:StringLike': {
            'dynamodb:LeadingKeys': ['tenant#${aws:PrincipalTag/TenantId}#*'],
          },
        },
      }),
    );
  }
```

流れとしては以下のように進めていました。

1. 脆弱性について、Amazon Q Developerが指摘できるかを確認
2. SaaS特有の問題の指摘ができないため、ルールを追加し再調査
3. 指摘事項が妥当であることを確認し、手動かQ Developerで修正
4. チェックツールで指摘の修正ができているか確認

1の部分で、Vibe Codingだけに頼ることの限界を感じつつ、2の部分でソフトウェアエンジニアとしての知識が活かせることを確認するようなワークでした。自分自身もQ Developerが最初指摘漏れをしても、以下のようにルールを設定することで正しく指摘を挙げてくれることが確認できました。

.amazonq/rules/review-rule.md

```bash
# レビュー観点

アプリは以下のテナント分離実装がされています。
DynamoDBの項目を使ってテナントを分離しています。
SaaSの観点でテナント分離が適切に行われているか確認してください。
```

おまけとして、5つの調査項目ごとに点数が設定されており、テーブル内の参加者で最も得点の高い方には、コアラの人形がプレゼントされていました。自分は最終的に160点だったので、ぜひ同じようなワークショップに参加される方は、試してみてください。

![IMG_5006.jpeg](https://devio2024-2-media.developers.io/upload/6SxfQhAuEvOXuP6ne0ms3I/2025-12-03/e34Ef1ry2HTA.jpeg)

![IMG_5008.jpeg](https://devio2024-2-media.developers.io/upload/6SxfQhAuEvOXuP6ne0ms3I/2025-12-03/xdnmQw4tS91H.jpeg)

## 所感

ドメインに特化した領域をLLMがまだ苦手なのは分かっていましたが、SaaSのテナント設計という広く知られている概念でもうまく回答できていないことに少し驚きました。公知なものでも、エンジニアリングがある程度分かっている方がいないと今後大きく問題が出そうという実感を得れました。

またワークショップがよくできていて、LLMの限界→メモリによる知識の強化、という流れがよくできていたのでLLMの限界を理解してもらうワークショップとしてかなり有効だと感じました。もしワークショップ作られる方がいれば、参考にしてみてください！

この記事をシェアする