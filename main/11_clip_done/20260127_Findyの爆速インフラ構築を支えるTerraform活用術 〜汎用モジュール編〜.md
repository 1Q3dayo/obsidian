---
title: "Findyの爆速インフラ構築を支えるTerraform活用術 〜汎用モジュール編〜"
source: "https://tech.findy.co.jp/entry/2026/01/26/070000"
author:
  - "[[kouzyun]]"
  - "[[たかぼー (id:Taka_bow)]]"
  - "[[starfish719]]"
  - "[[thedan]]"
  - "[[nesskazu]]"
  - "[[Shun (id:ShunDeveloper)]]"
  - "[[とみー (id:Cooking_ENG)]]"
  - "[[ryu-furuta]]"
  - "[[dev2bo]]"
  - "[[adachin (id:adachin0817)]]"
published: 2026-01-26
created: 2026-01-27
description: "はじめに こんにちは、ファインディのPlatform開発チームでSREを担当している原（こうじゅん）です。 2025年は、ファインディにとって新規サービスリリースが相次ぐ年でした。 Platform開発チーム(以降、SREチーム)では、この1年間で6つのサービスのインフラ環境を構築してきました。 スピード感を持った環境構築を実現するために、私たちがどのような工夫を行ったのか、今回はTerraformの汎用モジュールを活用した取り組みについてお話しします。 はじめに 2025年、6つのサービスをリリース スピード感のある環境構築で直面した課題 Terraformでの汎用モジュールの導入 Netw…"
tags:
  - "clippings"
  - "raw"
---
## はじめに

こんにちは、ファインディのPlatform開発チームでSREを担当している原（ [こうじゅん](https://x.com/kouzyunJa) ）です。

2025年は、ファインディにとって新規サービスリリースが相次ぐ年でした。

Platform開発チーム(以降、SREチーム)では、この1年間で6つのサービスのインフラ環境を構築してきました。

スピード感を持った環境構築を実現するために、私たちがどのような工夫を行ったのか、今回はTerraformの汎用モジュールを活用した取り組みについてお話しします。

- [はじめに](https://tech.findy.co.jp/entry/2026/01/26/#%E3%81%AF%E3%81%98%E3%82%81%E3%81%AB)
- [2025年、6つのサービスをリリース](https://tech.findy.co.jp/entry/2026/01/26/#2025%E5%B9%B46%E3%81%A4%E3%81%AE%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E3%82%92%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9)
- [スピード感のある環境構築で直面した課題](https://tech.findy.co.jp/entry/2026/01/26/#%E3%82%B9%E3%83%94%E3%83%BC%E3%83%89%E6%84%9F%E3%81%AE%E3%81%82%E3%82%8B%E7%92%B0%E5%A2%83%E6%A7%8B%E7%AF%89%E3%81%A7%E7%9B%B4%E9%9D%A2%E3%81%97%E3%81%9F%E8%AA%B2%E9%A1%8C)
- [Terraformでの汎用モジュールの導入](https://tech.findy.co.jp/entry/2026/01/26/#Terraform%E3%81%A7%E3%81%AE%E6%B1%8E%E7%94%A8%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E3%81%AE%E5%B0%8E%E5%85%A5)
	- [Network、Container、Databaseなど、様々なパッケージを整備](https://tech.findy.co.jp/entry/2026/01/26/#NetworkContainerDatabase%E3%81%AA%E3%81%A9%E6%A7%98%E3%80%85%E3%81%AA%E3%83%91%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B8%E3%82%92%E6%95%B4%E5%82%99)
	- [モジュールごとにパラメーターを指定すれば環境が立ち上がる仕組み](https://tech.findy.co.jp/entry/2026/01/26/#%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E3%81%94%E3%81%A8%E3%81%AB%E3%83%91%E3%83%A9%E3%83%A1%E3%83%BC%E3%82%BF%E3%83%BC%E3%82%92%E6%8C%87%E5%AE%9A%E3%81%99%E3%82%8C%E3%81%B0%E7%92%B0%E5%A2%83%E3%81%8C%E7%AB%8B%E3%81%A1%E4%B8%8A%E3%81%8C%E3%82%8B%E4%BB%95%E7%B5%84%E3%81%BF)
- [汎用モジュールで解決した課題](https://tech.findy.co.jp/entry/2026/01/26/#%E6%B1%8E%E7%94%A8%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB%E3%81%A7%E8%A7%A3%E6%B1%BA%E3%81%97%E3%81%9F%E8%AA%B2%E9%A1%8C)
- [Terraformのplanは成功するけどApplyはコケる問題](https://tech.findy.co.jp/entry/2026/01/26/#Terraform%E3%81%AEplan%E3%81%AF%E6%88%90%E5%8A%9F%E3%81%99%E3%82%8B%E3%81%91%E3%81%A9Apply%E3%81%AF%E3%82%B3%E3%82%B1%E3%82%8B%E5%95%8F%E9%A1%8C)
- [まとめ](https://tech.findy.co.jp/entry/2026/01/26/#%E3%81%BE%E3%81%A8%E3%82%81)

## 2025年、6つのサービスをリリース

2025年、SREチームでは次のサービスのインフラ環境を構築しました。

- Findy Conference
- Findy AI+
- Findy Team+ AIチャットボット
- Findy ID
- Findy Insights
- アーキテクチャ壁打ちAI by Findy Tools

これらのサービスは、それぞれStaging環境やProduction環境といった複数の環境が必要であり、SREチームとしては短期間で多数の環境構築を実施する必要がありました。

## スピード感のある環境構築で直面した課題

新規サービスのリリースラッシュの中で、私たちは次のような課題に直面しました。

サービス開発はスピード感を持って行われており、インフラ環境の構築にも「2週間でStaging環境とProduction環境を用意してほしい」といった依頼も珍しくありません。サービスリリースのタイミングが重なると、複数の環境構築依頼が同時に舞い込むこともあります。

SREチームは環境構築だけに専念できるわけではなく、既存サービスの運用改善、障害対応、セキュリティ対応なども並行して進める必要があります。

2025年当時、SREチームのメンバーは4名でした。この人数で、これだけのサービスリリースに対応するのは容易ではありませんでした。

## Terraformでの汎用モジュールの導入

これらの課題を解決するために、ファインディのプロダクトで頻繁に利用するAWSリソース（ECS、ALB、RDS、VPCなど）を、再利用可能なTerraformモジュールとして整備しました。

これらを「汎用モジュール」と呼んでいます。

汎用モジュールの目的は、次の2点です。

1. スピード: 環境構築にかかる時間を大幅に短縮する
2. 品質: 標準化されたモジュールを使うことで、設定ミスを減らし、品質を担保する

![generic_terraform_module](https://cdn-ak.f.st-hatena.com/images/fotolife/f/findyinc/20260122/20260122205123.png)

generic\_terraform\_module

汎用モジュールは、HCP Terraform（旧Terraform Cloud）のプライベートレジストリに登録しています。これにより、チーム内で簡単にモジュールを共有・再利用できるようになりました。

### Network、Container、Databaseなど、様々なパッケージを整備

汎用モジュールは、リソースの機能ごとにパッケージを分けて整備しています。

例えば次のようなカテゴリーに分けています。

- Network: VPC、サブネット、ルートテーブル、NATゲートウェイなど
- Container: ECS、Fargate、ALB、タスク定義など
- Database: RDS、Aurora、パラメータグループなど
- その他、必要に応じてモジュールを追加

### モジュールごとにパラメーターを指定すれば環境が立ち上がる仕組み

汎用モジュールを使えば、必要なパラメーター（プロジェクト名、環境名、リソースサイズなど）を指定するだけで、標準化された環境が立ち上がります。

例えば、次のようなイメージです。

```hcl
module "database" {
  source  = "app.terraform.io/Findy/findy-XXXX-platform/aws//modules/database"
  version = "X.XX"

  environment = "staging"

  engine_type             = "postgresql"
  db_parameter_group_name = "sre-staging"
  instance_class          = "db.t4g.medium"
  number_of_instances     = 2
  preferred_backup_window = "20:05-20:35"
  service_name            = "sre-sandbox"
}
```

このように、モジュールを組み合わせることで、複雑なインフラ環境を短時間で構築できます。

## 汎用モジュールで解決した課題

汎用モジュールの導入により、品質が担保されてスピード感のある構築が可能になりました。

汎用モジュールを使うことで、モジュール内の構成ならProduction環境とStaging環境を含めても最短3日で完了できるようになりました。

またパラメーターを指定するだけで環境が立ち上がるので、新しいメンバーでもすぐに戦力になれる仕組みを作ることができました。

## Terraformのplanは成功するけどApplyはコケる問題

汎用モジュールの導入で大きな成果が得られた一方、汎用モジュールから呼び出した構成でTerraformのplanは成功するけどApplyはコケるという問題も発生しました。

この問題は、構築スピードの低下につながるため、Terraform Testを導入して対処しました。

詳細については、次の記事で詳しく紹介していますので、ぜひご覧ください。

[tech.findy.co.jp](https://tech.findy.co.jp/entry/2025/08/29/070000)

## まとめ

2025年、SREチームは多数のインフラ環境を構築しました。その裏側で、Terraformの汎用モジュールを活用することで、スピード感と品質を両立した環境構築を実現しました。

汎用モジュールの導入により、SREチームの環境構築はスピードアップしましたが、まだまだ改善の余地があります。

現在は、SREチームが主体となってインフラ環境を構築していますが、今後は開発チームが主体となって容易にインフラ構築できるPlatformを作りたいと考えています。

これにより、開発チームがより自律的にサービスをリリースできるようになり、SREチームはより注力すべきタスクに集中できるようになります。いわゆるPlatform Engineeringの取り組みを進めていきます。

---

ファインディでは一緒に会社を盛り上げてくれるメンバーを募集中です。 興味を持っていただいた方はこちらのページからご応募お願いします。

[herp.careers](https://herp.careers/v1/findy/requisition-groups/14c4a661-5e48-40c5-99d0-ea657b8b4c04)

[「開発生産性」に関する実態調査レポート… »](https://tech.findy.co.jp/entry/2026/01/23/070000)

![](https://cdn.blog.st-hatena.com/images/admin/quote/quote-x-icon.svg?version=eaea272eb8e81c181a130f9f518cd0 "引用して投稿する")