---
title: "2026年3月31日付けで発表されたAWSサービス終了・新規利用停止まとめ | DevelopersIO"
source: "https://dev.classmethod.jp/articles/aws-service-lifecycle-summary-20260331/"
author:
  - "[[Takuya Shibata]]"
published: 2026-04-10
created: 2026-04-02
description:
tags:
  - "clippings"
---
しばたです。

先日のAWS What's newで複数AWSサービスの終了および新規利用停止がアナウンスされました。

本記事ではこの内容をまとめていきます。

## 対象サービス一覧

対象となるサービスがそれなりにあったので新規利用停止と終了それぞれ分けて一覧にします。

### 新規利用停止

| サービス | 内容 | 新規利用停止日 | 特記事項 |
| --- | --- | --- | --- |
| Amazon Application Recovery Controller (ARC) Readiness check | 新規利用停止 | 2026年4月30日 | 他の機能には影響なし |
| Amazon ComprehendのうちTopic modeling, Event detection, prompt safety classificationの機能 | 新規利用停止 | 2026年4月30日 | 他の機能には影響なし |
| Amazon RekognitionのうちStreaming Video Analysisの機能 | 新規利用停止 | 2026年4月30日 | 他の機能には影響なし |
| Amazon SNS Message Data Protection | 新規利用停止 | 2026年4月30日 | 他の機能には影響なし |
| AWS App Runner | 新規利用停止 | 2026年4月30日 |  |
| AWS Audit Manager | 新規利用停止 | 2026年4月30日 |  |
| AWS CloudTrail Lake | 新規利用停止 | 2026年5月31日 |  |
| AWS Glue for Ray | 新規利用停止 | 2026年4月30日 |  |
| AWS IoT FleetWise | 新規利用停止 | 2026年4月30日 |  |

### サービス終了

| サービス | 内容 | 終了日 | 特記事項 |
| --- | --- | --- | --- |
| RDS Custom for Oracle | サービス終了 | 2027年3月31日 |  |
| Amazon WorkMail | サービス終了 | 2027年3月31日 | 2026年4月30日より新規利用停止 |
| Amazon WorkSpaces Thin Client | サービス終了 | 2027年3月31日 | 2026年4月20日より新規利用停止 |
| AWS Service Management Connector | サービス終了 | 2027年3月31日 |  |
| Amazon Chime SDKのうちProxy Sessionsの機能 | 提供終了 | 2026年3月31日 | アナウンス時点で終了済み |

## \[新規利用停止\] Amazon Application Recovery Controller Readiness check

Amazon Application Recovery Controller (ARC)のうちRediness check(準備状況チェック)の機能が2026年4月30日をもって新規利用不可となります。  
Rediness check以外の機能に影響はなくARC自体も従来通り利用可能です。

AWSとしては代替として新機能となるRegion switch(リージョン切り替え)の利用を推奨しています。

- [Amazon Application Recovery Controller (ARC) readiness check availability change](https://docs.aws.amazon.com/r53recovery/latest/dg/arc-readiness-availability-change.html)

本日時点でRediness checkのマネジメントコンソールにアクセスすると新規利用を停止する旨の警告が表示されていました。

![aws-service-lifecycle-summary-20260331-01](https://devio2024-media.developers.io/image/upload/f_auto/q_auto/v1775030705/2026/04/01/gqzuse3hfgfdaqwgwkxm.png)

## \[新規利用停止\] Amazon Comprehend Topic modeling, Event detection, prompt safety classification

Amazon Comprehendのうち

- [Topic modeling](https://docs.aws.amazon.com/comprehend/latest/dg/topic-modeling.html)
- [Event detection](https://docs.aws.amazon.com/comprehend/latest/dg/how-events.html)
- [prompt safety classification](https://docs.aws.amazon.com/comprehend/latest/dg/trust-safety.html#prompt-classification)

の機能が2026年4月30日をもって新規利用不可となります。  
既存顧客に影響は無く、Amazon Comprehendのその他の機能にも影響ありません。

AWSからは代替としてAmazon Bedrockの利用が推奨されており、ドキュメントにいくつか移行例が記載されています。

- [Amazon Comprehend feature availability changen](https://docs.aws.amazon.com/comprehend/latest/dg/comprehend-availability-change.html)

## \[新規利用停止\] Amazon Rekognition Streaming Video Analysis

Amazon RekognitionのうちStreaming Video Analysisの機能が2026年4月30日をもって新規利用不可となります。  
既存顧客に影響は無く、Amazon Rekognitionのその他の機能にも影響ありません。

代替となるサービスは無い様で、AWSとしては以下のブログにあるソリューションの構築を移行例として紹介しています。

- [Create a Serverless Solution for Video Frame Analysis and Alerting](https://aws.amazon.com/jp/blogs/machine-learning/create-a-serverless-solution-for-video-frame-analysis-and-alerting/)

## \[新規利用停止\] Amazon SNS Message Data Protection

Amazon SNSのうちMessage Data Protection(データ保護ポリシー)の機能が2026年4月30日をもって新規利用不可となります。  
既存顧客に影響は無く、今後新機能の追加はしないもののセキュリティアップデートは継続するとのことです。

代替となるサービスや機能は無くAWSとしては以下のサンプルにあるソリューションを代替例として紹介しています。

- [Amazon Simple Notification Service (Amazon SNS) Sensitive Data Protection with Amazon Bedrock Guardrails](https://github.com/aws-samples/sample-sns-sensitive-data-protection-bedrock)

## \[新規利用停止\] AWS App Runner

AWS App Runnerが2026年4月30日をもって新規利用不可となります。  
既存顧客に影響は無く既存の利用者であれば2026年4月30日以降もサービスの新規作成ができるとのことです。  
今後新機能の追加はしないもののセキュリティアップデートは継続して提供されます。

AWSとしてはAmazon ECS Express Modeの利用を代替として推奨しています。  
基本的な移行方法もドキュメントにあるので参考にすると良いでしょう。

- [AWS App Runner availability change](https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html)

ちなみに、今年の2月に一瞬だけ公開されたAWSブログについては今も非公開のままでした。

- 現在も404エラー: [https://aws.amazon.com/blogs/containers/migrating-from-aws-app-runner-to-amazon-ecs-express-mode/](https://aws.amazon.com/blogs/containers/migrating-from-aws-app-runner-to-amazon-ecs-express-mode/)

本日時点でマネジメントコンソールにアクセスすると新規利用停止の警告が表示される様になっており、ちょっとくどい位Amazon ECS Express Modeの利用を推奨しております。

![aws-service-lifecycle-summary-20260331-02](https://devio2024-media.developers.io/image/upload/f_auto/q_auto/v1775030714/2026/04/01/rwsv8umf8c3angbhc8w4.png)

## \[新規利用停止\] AWS Audit Manager

AWS Audit Managerが2026年4月30日をもってメンテナンスモードに移行し新規利用不可となります。  
AWSとしては各種セキュリティフレームワークに対応するAWS Config適合パックの利用を代替として推奨しています。

- [AWS Audit Manager availability change](https://docs.aws.amazon.com/audit-manager/latest/userguide/audit-manager-availability-change.html)

ドキュメントにAudit Manager FrameworkとAWS Config適合パックの対比表があるので参考にしてください。

- [Mapping AWS Audit Manager Frameworks to AWS Config Conformance Packs](https://docs.aws.amazon.com/audit-manager/latest/userguide/audit-manager-availability-change.html#audit-manager-availability-change-framework-mapping)

## \[新規利用停止\] AWS CloudTrail Lake

AWS CloudTrailのうちCloudTrail Lakeの機能が2026年5月31日をもって新規利用不可となります。  
既存顧客に影響はないものの、AWS Organizations環境でのイベントデータストアの扱いには注意が必要そうです。

- 組織レベルのイベントデータストア → 既存アカウントのデータストアはそのまま利用可能で、組織に新アカウントが増えた場合もそのまま利用可能
- アカウント単位のイベントデータストア → 既存アカウントのデータストアはそのまま利用可能だが、新規アカウントではデータストアは利用不可

AWSとしては代替にCloudWatchの利用を推奨していますが、機能がきれいに一致するわけではなくアーキテクチャの比較表が提供されているので確認しておくと良いでしょう。

- [CloudTrail Lake availability change](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-service-availability-change.html)

## \[新規利用停止\] AWS Glue for Ray

AWS GlueでRayを使ったジョブを記述できるAWS Glue for Rayですが、2026年4月30日をもって新規利用不可となります。  
既存顧客はRayジョブをそのまま利用可能です。

AWSとしては代替としてAmazon EKS上にRayの環境を構築するアーキテクチャを推奨しており、移行手順がドキュメントに記載されています。

- [AWS Glue for Ray end of support](https://docs.aws.amazon.com/glue/latest/dg/awsglue-ray-jobs-availability-change.html)

## \[新規利用停止\] AWS IoT FleetWise

車両データの収集と可視化を行うAWS IoT FleetWiseですが、2026年4月30日をもって新規利用不可となります。  
既存顧客はサービスをそのまま利用可能です。

AWSとしては代替として [Guidance for Connected Mobility on AWS](https://aws.amazon.com/jp/solutions/guidance/connected-mobility-on-aws/) ソリューションの利用を推奨してます。

ちなみにAWS IoT FleetWiseはバージニア北部とフランクフルトの2リージョンのみ利用可能なサービスでした。

## \[終了\] Amazon RDS Custom for Oracle

Amazon RDS CustomのうちAmazon RDS Custom for Oracleが2027年3月31日をもってサービス終了します。  
サービス終了後はコンソールおよび各種リソースにアクセス不可となります。

Amazon RDS for Oracleでは満たせない要件がある顧客がRDS Custom for Oracleを使うため、移行先としてはEC2 Oracleが基本となり、ドキュメントにデータベースおよびいくつかの機能の移行方法が記載されています。

- [RDS Custom for Oracle end of support](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/RDS-Custom-for-Oracle-end-of-support.html)

本記事では細かい手順まで触れませんが、RDS Customはインスタンス内部にログインできるのでパラメーターファイルやデータファイルを直接コピーして移行可能である点は特徴的だと思います。

## \[終了\] Amazon WorkMail

Amazon WorkMailが2027年3月31日をもってサービス終了します。  
2026年4月30日をもって新規顧客の受付が停止され、サービス終了後は全機能が利用不可となります。

AWSとしては移行先として外部サービスの利用を挙げており、ドキュメントには

- [Kopano Cloud](https://kopano.cloud/workmail-migration/)
- [Zoho Mail](https://www.zoho.com/workplace/lp/aws-workmail-alternative.html)
- [Zoom Mail](https://www.zoom.com/en/lp/amazon-workmail/)

が例示されています。  
もちろんこれ以外のサービスを使っても構いません。

- [Amazon WorkMail end of support](https://docs.aws.amazon.com/workmail/latest/adminguide/workmail-end-of-support.html)

## \[終了\] Amazon WorkSpaces Thin Client

Amazon WorkSpaces Personal、Amazon WorkSpaces Applications (旧AppStream 2.0)、Amazon WorkSpaces Secure Browser用のシンクライアント端末とデバイスの管理サービスであるAmazon WorkSpaces Thin Clientが2027年3月31日をもって終了します。  
2026年4月20日(もしくは2026年3月31日 [^1])をもって新規顧客の受付が停止されます。

- [Amazon WorkSpaces Thin Client end of support](https://docs.aws.amazon.com/workspaces-thin-client/latest/ug/workspacesthinclient-end-of-support.html)

サービス終了後はAmazon WorkSpacesの各種サービスにアクセス不可になるとのことで、これ以上具体的な内容は記載されていないものの、おそらくはデバイスがロックされるのでしょう。  
併せてマネジメントコンソールへのアクセスも不可となります。  
利用者はサービス終了までに接続用の別デバイスを用意する必要があります。

利用不可になったデバイスの廃棄方法が以下のページにまとめられており、基本的にはAmazonのリサイクルセンターに引き渡す形になる様です。

- [Amazon WorkSpaces Thin Client Device Recycling Information](https://aws.amazon.com/workspaces-family/thin-client/terms/device-recycling-information/)

ちなみに私の検証用AWSアカウントでは既にマネジメントコンソールからAmazon WorkSpaces Thin Clientが非表示にされていました。

## \[終了\] AWS Service Management Connector

AWS Service Management Connector (旧称 AWS Service Catalog Connector)がが2027年3月31日をもってサービス終了します。

- ServiceNow Store: [AWS Service Management Connector](https://store.servicenow.com/store/app/6b19eb6e1be06a50a85b16db234bcb2d)
- Atlassian Marketplace: [AWS Service Management Connector for JSM](https://marketplace.atlassian.com/apps/1221283/aws-service-management-connector-for-jsm)

AWSとしてはSecurity Hub CSPM向けには各社のインテグレーションを、それ以外の用途にはパートナー製品を利用するか各種SDKを直接利用することで代替となるソリューションを構築することを勧めています。

- [AWS Service Management Connector end of support](https://docs.aws.amazon.com/smc/latest/ag/smc-end-of-support.html)

## \[終了\] Amazon Chime SDK Proxy Sessions

Amazon Chime SDKのうちProxy Sessionに関わる機能が2026年3月31日をもって終了したとのことです。  
こちらの機能に関する詳細や影響範囲に関するドキュメントを見つけることができず、これ以上の情報を得ることができませんでした。

## 余談: AWS Product Lifecycle ページも無くなっていた

今回のアナウンスに合わせてかAWS Product Lifecycleのページが無くなっており、「AWS Lifecycle Changes」という形でAWS General Reference配下のページにリダイレクトされる様になっていました。

- [https://aws.amazon.com/products/lifecycle/](https://aws.amazon.com/products/lifecycle/)
	- → [https://docs.aws.amazon.com/general/latest/gr/service-lifecycle.html](https://docs.aws.amazon.com/general/latest/gr/service-lifecycle.html) にリダイレクト

ただ、このAWS Lifecycle Changesでは以下の形で状態毎の子ページに分けられており網羅性も従来よりずっと良くなっていました。

- メンテナンスモード: [Services in Maintenance](https://docs.aws.amazon.com/general/latest/gr/maintenance_services.html)
- サービス終了予定: [Services in Sunset](https://docs.aws.amazon.com/general/latest/gr/sunset_services.html)
- サービス終了済み: [Services in Full Shutdown](https://docs.aws.amazon.com/general/latest/gr/full_shutdown_services.html)

まさに「私が欲しかったものがここにある」という感じなのでこれは良い改善だと思います。  
終了済みサービスのほとんどは私がブログにまとめていますが、

については今回初めて終了を知りました...  
これまでかなり頑張って調査してきたので漏れがあったことがちょっと悔しいです。

あとサービス終了予定サービスについて、たとえばAWS WAF Classic(2025年9月30日 → 2026年10月7日終了予定に延長)などいくつか終了時期が延長されているものがありました。

## 最後に

長くなりましたが以上となります。

最近はAWSサービスの終了も落ち着いたかと思ったのですが今回一気に来た印象です。  
利用しているサービスや製品がある場合は適宜対応してください。

脚注

[^1]: ドキュメント中で新規受付停止日が統一されていない...