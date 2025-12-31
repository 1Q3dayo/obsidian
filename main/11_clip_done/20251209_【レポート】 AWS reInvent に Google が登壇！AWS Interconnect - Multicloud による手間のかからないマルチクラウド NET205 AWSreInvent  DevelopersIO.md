---
title: "【レポート】 AWS re:Invent に Google が登壇！AWS Interconnect - Multicloud による手間のかからないマルチクラウド #NET205 #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/aws-re-invent-google-aws-interconnect-multicloud-net205-awsreinvent/"
author: ""
published: "2025-12-08"
created: "2025-12-09"
description: "AWS と Google Cloud を直結する AWS Interconnect の紹介。AWS re:Invent なのに Google の方が登壇しています。"
tags:
  - ""
  - "raw"
---

ウィスキー、シガー、パイプをこよなく愛する大栗です。

現在ラスベガスで AWS re:Invent に参加しています。AWS と Google Cloud をsすぐに接続してできる AWS Interconnect のセッションに参加したのでレポートをお届けします。

## Hassle-free multicloud connectivity with AWS Interconnect - Multicloud

![image1](https://devio2024-media.developers.io/image/upload/v1764813372/2025/12/03/xi4avphvkwcdhm13yhgl.jpg)

## 登壇者

AWS re:Invent ですが、Google の Judy Issa さんが登壇されています。

- Judy Issa
	- Product Manager
	- Google
- Alexandra Huides
	- Principal Networking Specialist SA
	- Amazon WEB Services
- Santiago Riesco
	- Sr. Product Manager – Tech
	- AWS

![image2](https://devio2024-media.developers.io/image/upload/v1765178416/2025/12/08/twqtidpxef4xczcrujjj.jpg)

### オープニング

### 01\. AWS ネットワークの基礎

AWS Interconnect のベースラインの内容です。

- Amazon VPC
	- グローバルの Google Cloud とは異なりリージョンリソース
	- サブネットとアベイラビリティゾーンを内包
- VPC ネットワーク
	- リージョン内のルーティングハブになる AWS Transit Gateway
- グローバルネットワーク
	- グローバルなハイブリットネットワークを構築する AWS Cloud WAN
- ハイブリッドネットワーク
	- AWS Site-to-Site VPN
- ハイブリッドの接続性
	- AWS Direct Connect
	- AWS Direct Connect Gateway

![image16](https://devio2024-media.developers.io/image/upload/v1765177728/2025/12/08/agkh8fuk0ky9yxsc9dhl.jpg)

### 02\. マルチクラウド接続の背景

今までマルチクラウド接続をするには、主に4種類の方法がありました。

- インターネット経由の Site-to-Site VPN
- Direct Connect を使用したコロケーション施設経由のルーティング
- ホスト接続 DX を経由したサードパーティのファブリック
- トランスポートオプションとして DX/VPN を使用したオーバーレイ構築

これらには課題があります。

- スケーラビリティ
- 管理コスト
- 障害点の増加
- トラブルシューティングの難しさ
- グローバルのカバレッジ

![image24](https://devio2024-media.developers.io/image/upload/v1765177786/2025/12/08/b72xokgvsym3lak97hvx.jpg)

### 03\. ビジョンとワーキング・バックワーズ

お客様と話し合いワーキング・バックワーズ（逆算）して課題解決に取り組み、『こんなに難しいはずがない』というビジョンで解決しました。複雑なアーキテクチャを避けて、VPC をもう一つの VPC につなぐだけで完了するべきです。

Google Cloud とのパートナーシップでこれを始められます。

![image30](https://devio2024-media.developers.io/image/upload/v1765177929/2025/12/08/pecbjw0no5kmrzs2lafe.jpg)

### 04\. AWS Interconnect - multicloud の紹介

AWS Interconnect を紹介します。

AWS 側のアタッチメントオブジェクトは Direct Connect Gateway であり、Virtual PrivateGateway、Transit Gate、Cloud WAN とシームレスに接続できます。Google Cloud 側のアタッチメントポイントは Cloud Router です。少なくとも 2 箇所の物理施設と複数のルーターにまたがる複数の冗長接続が構築されます。お客様ルーターや BGP、ピア IP アドレスを意識しません。

![image41](https://devio2024-media.developers.io/image/upload/v1765177968/2025/12/08/f5czmk2ygqiwae4a7qsh.jpg)

ユーザーが行う主要な操作は作成と承認だけです。

1. Interconnect の作成。パートナーである Google Cloud を選択して AWS と Google Cloud のリージョンを決めます。帯域や Direct Connect Gateway、Google Cloud プロジェクトを指定します。
2. アクティベーションキーを元に対向のクラウドで承認します。

![image47](https://devio2024-media.developers.io/image/upload/v1765177992/2025/12/08/tnutlmx9ugv2ugxamxbg.jpg)

実際には、以下の流れで実現されます。

1. お客様が Interconnect を作成
2. AWS が新しい Interconnect の作成をリクエスト
3. お客様がアクティベーションキーを使用して Interconnect を承認
4. AWSと CSP はリクエストのキャパシティで Interconnect をプロビジョニング

4個のルーターに分散され耐障害性を向上させ、ワークロードが急増しても論理接続を切り替えてスケールアップ/スケールダウンが可能で、冗長性が失われても API でやり取りを行いメンテナンスを行います。オープンな仕様として GitHub に公開されている API です。

![PXL_20251203_185355618.MP](https://devio2024-media.developers.io/image/upload/v1765178105/2025/12/08/tiochmh5mghmtecb8dir.jpg)

### 05\. Google Cross-Cloud Interconnect

Google の Cloud Interconnect について説明します。Google の Cloud Interconnect はお客様の Google Cloud へのプライベートな入口であり安全な接続を提供します。お客様が他のクラウドも利用したいと考えているため 2023 年に Cross-Cloud Interconnect を導入しました。

レジリエンスオプションにはいくつかあります。

- エッジ アベイラビリティ ドメインは Interconnect の運命の分離を保証
- 重複しないメンテナンスウィンドウ
- 物理的なインフラの複雑さと管理コストを覗いた TCO 削減

![PXL_20251203_190415906.MP](https://devio2024-media.developers.io/image/upload/v1765178152/2025/12/08/ro1v9gmw6hwp4r72nweu.jpg)

しかし、専用のリンクは最小 10 Gbps で、物理的な対応のためのリードタイムが必要となります。またクラウド間で冗長化の設定が同期されないこともあり、クラウド間でメンテナンスウィンドウを管理する必要があります。

もしこのようなことができたらどうでしょう

- 物理インフラを事前に構築して、デフォルトで暗号化
- すぐに使えて E2E の信頼性を提供
- 垂直、水平の接続スケーリング
- ネットワークを抽象化して、不要な手順の排除

![PXL_20251203_191057129.MP](https://devio2024-media.developers.io/image/upload/v1765178212/2025/12/08/jsqaxpfexagixfptxkeb.jpg)

Google 側は以下のような動作をします。

- VPC が両クラウドでシームレスに接続
- ネイティブな Google Cloud のサブネットを AWS へアドバタイズ可能
- 範囲の追加は Private Google Access で到達可能
- テナント VPC はスポークとして NCC ハブへ接続できる
- ルートのアドバタイズはハブ経由で他のスポークから可能

![PXL_20251203_191122757.MP](https://devio2024-media.developers.io/image/upload/v1765178256/2025/12/08/u7j3bhimgm972onbp5sh.jpg)

### 06\. リファレンスアーキテクチャー

リファレンスアーキテクチャを見ていきます。

#### 単一リージョン - 単一 Interconnect

ユーザー視点では AWS Direct Connect と Google Cloud Router が論理的に直接繋がっているように見えます。Interconnect を通して透過的にアクセスできます。

![PXL_20251203_191613343.MP](https://devio2024-media.developers.io/image/upload/v1765176185/2025/12/08/b14momsscraxa65nrshg.jpg)

![PXL_20251203_191706071.MP](https://devio2024-media.developers.io/image/upload/v1765176218/2025/12/08/p6lekvehypnpqpsgmstn.jpg)

#### マルチリージョン - 単一 Interconnect

AWS のリージョン間は Cloud WAN で接続を行います。

![PXL_20251203_192150345.MP](https://devio2024-media.developers.io/image/upload/v1765176357/2025/12/08/qisfh6xeffpbs4yghjof.jpg)

![PXL_20251203_192312812.MP](https://devio2024-media.developers.io/image/upload/v1765176439/2025/12/08/chyziejiusls2mycutnw.jpg)

#### マルチリージョン - マルチ Interconnect

2 個の Direct Connect Gateway を使用して Cloud WAN のグローバルルーティングを細かく制御できます。

![PXL_20251203_192529260](https://devio2024-media.developers.io/image/upload/v1765176507/2025/12/08/cuh015sf8rfwbkqzf6ao.jpg)

![PXL_20251203_192715053](https://devio2024-media.developers.io/image/upload/v1765176572/2025/12/08/o79xpa0eyap6szdp7psq.jpg)

Azure とも協力して 2026年に同じ製品を Azure で提供する予定です。グローバル展開のために今後も投資を続けていき今後の展開について別途情報提供をしていきます。

![PXL_20251203_193029111.MP](https://devio2024-media.developers.io/image/upload/v1765178303/2025/12/08/eo7ta6b6mal0d3f0hayq.jpg)

## さいごに

AWS re:Invent に Google から登壇があるというのは驚きのセッションでした。現在クラウドがコモディティ化して、AI 対応へのシフトが進んでいるため、単一のクラウドだけでなく他社クラウドやモデルプロバイダーとの連携を進んでいくと思われます。クラウド間をシームレスに直結できるので、使いたい機能ごとにクラウド選んでベスト・オブ・ブリードのような使い方も容易になります。AWS のサービスと Google Cloud のサービスを連携させるハードルが下がり、今後当たり前の選択肢になっていくかもしれません。

この記事をシェアする