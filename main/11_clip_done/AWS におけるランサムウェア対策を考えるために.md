---
title: "AWS におけるランサムウェア対策を考えるために"
source: "https://blog.serverworks.co.jp/protecting-against-ransomware-on-aws"
author:
  - "[[swx-satake]]"
  - "[[エンジニアブログの記事一覧はコチラ]]"
published: 2025-11-10
created: 2025-11-17
description: "セキュリティサービス部 佐竹です。本日のブログは、ランサムウェア対策 on AWS をまとめることを目標としています。と言いましても、全てを詳細に記述すると膨大な量になるため、「ある程度 AWS のセキュリティに詳しい中級・上級エンジニア」が、これを読むことで「ランサムウェア対策のスタート地点での、議論の抜け漏れを無くす」ということを目指します。いわゆる、\"チートシート\"のようなものを目指します。"
tags:
  - "clippings"
  - raw

---
この記事は約13分で読めます。

セキュリティサービス部 佐竹です。  
本日のブログは、現時点で可能な **ランサムウェア対策 on AWS** をまとめることを目標としています。と言いましても、全てを詳細に記述すると膨大な量になるため、「ある程度 AWS のセキュリティに詳しい中級・上級エンジニア」が、これを読むことで **「ランサムウェア対策のスタート地点での、議論の抜け漏れを無くす」** ということを目指します [\*1](https://blog.serverworks.co.jp/#f-1ab526a6 "いわゆる、\"チートシート\"のようなものを目指します") 。

## はじめに

### AWS におけるセキュリティ対策の土台

さて、まず「ランサムウェア対策を始める前」に、 **AWS のセキュリティにおいてはそもそも何が重要なのか？** という大前提についての認識合わせが必須です。

**「セキュリティ」という言葉が意味する範囲は膨大** で、各人の立場によって見える景色も違います。見える景色≒バイアスが違うことで、同じ説明や内容が全く違う景色に見えてしまいます。ですので、私が見ている景色を皆様にもある程度共有することで、この最初のズレをある程度無くしたいと考えています。

### 弊社主催のセキュリティウェビナーに関して

その前提共有において、まずは以下セミナーについてお話します。

[www.serverworks.co.jp](https://www.serverworks.co.jp/event/security_webinar_ondemand.html)

私が登壇しました、2025年10月1日に開催したウェビナー **『セキュアなAWS環境を実現するために“必須セキュリティサービスとマルチアカウント戦略”』** では、AWS セキュリティの基本的な考え方についてお話ししました。上記の通り、現在オンデマンドでも配信中ですため、是非ご覧ください。

そして、このウェビナーの「前半」で説明している内容は、以下の通り資料（ブログ）形式でも展開しています。

[www.serverworks.co.jp](https://www.serverworks.co.jp/blog/security/aws_security_multi_account_strategy.html)

先のウェビナーは、本資料（ブログ）からさらに一歩進んだコストからの視点でも詳しく解説しておりますが、 **基本事項はこの資料をご理解頂くだけで十分となっています** 。

さて、と言いましてもこれらの資料を全部まずは読んでくださいというわけにもいきません [\*2](https://blog.serverworks.co.jp/#f-217460f1 "できればでよいですので、是非ウェビナーを見て頂いた方が理解が深まります") 。

ということで、ここからまず「セキュリティ対策の基本」をざっくりと説明するところから開始します。

### 上記セキュリティウェビナーの振り返り

はじめに、ウェビナーで解説した、AWS におけるセキュリティ対策の重要な観点をおさらいします。これらの考え方は、ランサムウェア対策だけではなく、そもそものセキュリティ対策として重要です。

#### 多層防御（スイスチーズモデル）

![](https://cdn-ak.f.st-hatena.com/images/fotolife/s/swx-satake/20251107/20251107171644.png)

セキュリティに「これだけで安全」という万能薬（銀の弾丸）はありません。複数の防御策を意図的に重ね合わせ（スイスチーズの穴が一直線に貫通しないように）、リスクを大幅に低減させるアプローチが不可欠です。

#### 主要セキュリティサービスの活用

![](https://cdn-ak.f.st-hatena.com/images/fotolife/s/swx-satake/20251107/20251107200239.png)

AWS は、この多層防御を実現するために多種多様なセキュリティサービスを提供しています。特に **Amazon GuardDuty** 、 **AWS Security Hub CSPM** 、 **AWS CloudTrail** 、 **AWS Config** といったサービスは、脅威の「検知」と「可視化」の核となり、セキュリティ運用の第一歩となります。

#### マルチアカウント戦略

![](https://cdn-ak.f.st-hatena.com/images/fotolife/s/swx-satake/20251107/20251107200411.png)

マルチアカウント戦略は AWS Well-Architected Framework のセキュリティの柱における最初のベストプラクティスであり、最も強力な「境界」の一つです。AWS アカウント自体を分離することで、万が一あるアカウントが侵害された場合でも、その影響を隔離し、被害の拡大を最小限に食い止めるための重要な戦略です。マルチアカウント戦略を効果的に実現し、管理・統制していくためには、 **AWS Organizations** や **AWS Control Tower** といった AWS サービスの活用が不可欠となっています。

簡単にまとめると、 **複数の AWS セキュリティ対策サービスを組み合わせて多層防御を実現すること** と、 **特に重要なセキュリティサービスから優先的に導入すること** 、という話です。

ではここから、ランサムウェア対策の話に入っていきます。

## 参考にした AWS 公式の有用資料とブログ

まずは AWS の公式サイトにおける「 [Protecting against ransomware](https://aws.amazon.com/jp/security/protecting-against-ransomware/) 」からリンクされている、以下の2つの資料を参考にします。

[aws.amazon.com](https://aws.amazon.com/jp/security/protecting-against-ransomware/)

- ホワイトペーパー
	- **AWS Blueprint for Ransomware Defense**: [https://d1.awsstatic.com/whitepapers/compliance/AWS-Blueprint-for-Ransomware-Defense.pdf](https://d1.awsstatic.com/whitepapers/compliance/AWS-Blueprint-for-Ransomware-Defense.pdf)
- eBook
	- **Protecting your AWS environment from ransomware**: [https://d1.awsstatic.com/psc-digital/2022/gc-200/security-ransomware-ebook/Security-Ransomware-eBook.pdf](https://d1.awsstatic.com/psc-digital/2022/gc-200/security-ransomware-ebook/Security-Ransomware-eBook.pdf)

どちらも英語で記述されている PDF になっていますが、本ブログは基本的に本資料をデータソースとして記述しています。

加えて特筆して重要なブログが、S3 におけるランサムウェア対策のブログ記事「 [Amazon S3 を標的としたランサムウェアの構造分析](https://aws.amazon.com/jp/blogs/news/anatomy-of-a-ransomware-event-targeting-data-in-amazon-s3/) ([The anatomy of ransomware event targeting data residing in Amazon S3](https://aws.amazon.com/jp/blogs/security/anatomy-of-a-ransomware-event-targeting-data-in-amazon-s3/))」です。

[aws.amazon.com](https://aws.amazon.com/jp/blogs/news/anatomy-of-a-ransomware-event-targeting-data-in-amazon-s3)

Amazon S3 は「オブジェクトストレージ」であるため、EC2 における EBS とは異なり、S3 自体の持つ機能とその特性を生かしたランサムウェア対策を行うことが重要です。

というわけで、これらの情報を元に、「AWS におけるランサムウェア対策」を考え、まとめていきます。

## 脅威としてのランサムウェア

ランサムウェア対策の前にまず、そもそもの「ランサムウェア」について少しご理解を頂くために、簡単な説明を記述します。

ランサムウェアとは、単なるマルウェアの一種ではなく、金銭を強要するための「ビジネスモデル」だと考えます。英語では「Ransomware」と記述します。「Ransom」が「身代金」という意味で、ソフトウェアを表す ware が最後にくっついた単語です [\*3](https://blog.serverworks.co.jp/#f-8b010469 "ランサムウェアは、決して「Run somewhere」ではありません") 。

攻撃者は様々な手口（例：盗まれた認証情報、未パッチの脆弱性）で環境に侵入し、データを暗号化または削除してアクセス不能にします [\*4](https://blog.serverworks.co.jp/#f-33338667 "最近では VPN 機器の脆弱性を突かれることが多い印象です") 。そして、その「安全な返却」と引き換えに身代金を要求します。

近年では、単に暗号化するだけでなく、事前にデータを盗み出し「身代金を支払わなければ、この機密データを公開する」と脅す「 **二重脅迫（ダブルエクストーション）** 」も一般的になっています。

さらに最近では、企業側のバックアップ対策が進んだことで「暗号化」による脅迫効果が薄れてきた背景もあり、攻撃者はデータの **暗号化プロセス自体を省略** し、 **データの窃取と「公開する」という脅迫** のみに特化した「 **ノーウェアランサム** 」と呼ばれる攻撃手法も増加しています。

そして注意すべきは、この脅威は従来のサーバーやデータベースだけのものではなく、Amazon S3 に保存されているようなクラウド上のデータも標的となっている点です。

## NIST CSF に沿ったランサムウェア対策 on AWS (本題)

ランサムウェアという複雑な脅威に対しては、体系的なアプローチが必要です。

[www.nist.gov](https://www.nist.gov/cyberframework)

AWS が推奨するベストプラクティスに基づき、ここでは「 [NIST Cybersecurity Framework (CSF)](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf) 」の5つの機能（特定、防御、検知、対応、復旧） に沿って、AWS で何をすべきかを整理します。

### 1\. 特定 (Identify) - 自環境を知る

まずは自環境の理解が必要です。そのために、AWS 環境内にどのような資産（リソース、ソフトウェア）が存在し、どこに重要データ・機密データがあるのかを把握・分類します。

- **関連する AWS サービス**:
	- **AWS Config**: AWS リソースのインベントリ（一覧）と構成変更履歴を自動で記録します。ガバナンスとセキュリティ評価の基盤となります。
	- **Amazon Macie**: S3 バケット内をスキャンし、PII（個人情報）などの機密データを自動で発見・分類してくれます。
	- **AWS Systems Manager Inventory**: EC2 インスタンスやオンプレミスサーバー上で稼働するOSやソフトウェアのインベントリを収集します。
	- **タグ付け**: 「機密（Confidential）」「重要（Critical）」といったタグをリソースに付与し、データ分類を明確にします。この分類が、後の防御や復旧の戦略にも有効活用できます。

リソースの棚卸には、組織を横断して利用が可能である AWS Resource Explorer マルチアカウント検索も有効な手立てです。

[blog.serverworks.co.jp](https://blog.serverworks.co.jp/multi-account-search-in-aws-resource-explorer)

### 2\. 防御 (Protect) - 侵入と拡散を防ぐ

基本的には、皆さんが考える防御はここに当てはまります。

よって、ここがランサムウェア対策の核です。ここで多層的な防御を具体的に実践します。

#### アカウントとアクセス管理 (IAM)

AWS を狙ったランサムウェア攻撃、そしてまた Amazon S3 を狙った同攻撃においても、最も一般的な侵入経路は、 **意図せず漏洩した「静的な IAM アクセスキー」** です。

- **長期クレデンシャルの排除**: 最優先で取り組むべきは、この静的なアクセスキー（長期クレデンシャル）を可能な限り排除することです。Security Hub CSPM でも、 [長期間ローテーションされていないアクセスキーを検出可能](https://docs.aws.amazon.com/securityhub/latest/userguide/iam-controls.html#iam-3) です。
- **IAM Identity Center**: 開発者や運用者が AWS にアクセスする際は、これを利用した **フェデレーション（一時クレデンシャル）** によるアクセスを強制します。
- **IAM ロール / IAM Roles Anywhere**: EC2 や Lambda などの AWS 内のプログラムからは IAM ロールを、オンプレミスなど AWS 外部のサーバーからは IAM Roles Anywhere を使用し、一時クレデンシャルでのアクセスを実現します。
- **MFA (多要素認証)**: クレデンシャルが万が一盗まれても、MFA があれば不正アクセスを防げる可能性が格段に上がります。

長期クレデンシャルの排除には、先日ブログでも紹介しました **「IAM Access Analyzer Unused Access」が有用** です。ただし、利用コストがネックになる場合がありますため、以下のブログを合わせて是非ご覧ください。

[blog.serverworks.co.jp](https://blog.serverworks.co.jp/iam-unused-access-cost-estimate)

#### 脆弱性管理とシステムの堅牢化

攻撃者は、認証情報の窃取と並行して、OS やソフトウェアの「未パッチの脆弱性」を狙って侵入します。

- **Amazon Inspector**: EC2、コンテナ、Lambda 関数を継続的にスキャンし、脆弱性を自動で検出します。
- **AWS Systems Manager Patch Manager**: 検出された脆弱性に対し、OS やソフトウェアのパッチ適用を自動化します。
- **マネージドサービスの活用**: Amazon RDS や AWS Lambda のようなマネージドサービスを積極的に利用することも有効な対策です。これらのサービスでは、AWS が基盤 OS のパッチ管理を代行してくれます。
- **イミュータブル（不変）インフラストラクチャ**: 稼働中のインスタンスに直接パッチを当てるのではなく、 **EC2 Image Builder** などでパッチ適用済みの新しいイメージ（AMI）を作成し、インスタンスごと置き換える運用（ [イミュータブルインフラ](https://docs.aws.amazon.com/ja_jp/wellarchitected/latest/reliability-pillar/rel_tracking_change_management_immutable_infrastructure.html) ）を採用します。これにより、設定変更ミスや人的アクセスによるリスクを根本から低減します。

#### ネットワークと S3 固有の保護

ネットワークレベルでの脅威ブロックと、データストア固有の防御策を組み合わせます。

- **ネットワーク境界防御**:
	- **AWS Network Firewall / Security Groups**: VPC の境界や内部で、不正な通信をきめ細かく制御します [\*5](https://blog.serverworks.co.jp/#f-db0e3bee "少し細かい話をします。Sg はステートフルです。NACLs はステートレスです。Sg はコネクショントラッキングで、NACLs はパケットごとの評価をします。よって、既に確立されたコネクションを断したい場合は、Sg では不可能です。NACLs でないと、遮断できません") 。
	- **Route 53 Resolver DNS Firewall**: C2 サーバー（攻撃者の指令サーバー）など、既知の悪意のあるドメインへのアウトバウンド通信を DNS レベルで遮断します。
	- **AWS WAF / AWS Shield**: Web アプリケーションを一般的な攻撃や DDoS 攻撃から保護します。
- **S3 データ固有の防御**:
	- **S3 MFA Delete**: S3 のバージョニング機能も、オブジェクト削除や改変対策として有用ですが、これと組み合わせてバケット削除に MFA（多要素認証）を必須とすることで、攻撃によるデータ損失を防ぎます。
	- **サーバーサイド暗号化 (SSE-KMS)**: 顧客管理キー（CMK）でデータを暗号化します。これにより、S3 オブジェクトへのアクセス権限（IAM ポリシー）とは別に、「暗号キーの使用権限（キーポリシー）」という第二のアクセス制御層を追加できます。

なお、今回はランサムウェア対策を主軸にしているため、AWS WAF には詳しく触れておりません。AWS WAF について学びたい方は以下のブログも参考にしてください [\*6](https://blog.serverworks.co.jp/#f-59f3ab3f "ペネトレーションテストに関する注意については「AWS WAF 適用環境におけるペネトレーションテストの目的と対応方法を整理する」も参考になると存じます [https://blog.serverworks.co.jp/aws-waf-penetration-testing-guide] ") 。

[blog.serverworks.co.jp](https://blog.serverworks.co.jp/what-is-aws-waf-learn-the-basics)

### 3\. 検知 (Detect) - 異常を早期に察知する

防御策をすり抜けてきた脅威を、被害が拡大する前に「早期検知」することが重要です。

- **Amazon GuardDuty**: AWS 環境における脅威検知の主軸です。AWS CloudTrail ログ、VPC フローログ、DNS ログなどを自動で分析し、悪意のある偵察活動、異常な API 呼び出し、マルウェアの兆候などを検出します。
	- **GuardDuty S3 Protection**: S3 上のデータアクセス異常（例: 普段アクセスしないユーザーからの大量の List/Get オペレーション）を検知し、ランサムウェアの兆候を捉えます。
	- **GuardDuty Malware Protection**: EC2 やコンテナで不審な動作を検知すると、EBS ボリュームのエージェントレススキャンを自動実行し、マルウェアを検出します。
- **AWS Security Hub**: GuardDuty や Inspector、Config など、様々なサービスからの検出結果（アラート）を一元的に集約し、優先順位付け（トリアージ）を行うダッシュボードです。セキュリティ体制の可視化に不可欠です。なお、先の PDF 群は、AWS Security Hub が AWS Security Hub CSPM の名称に変更される前に記載されたものですが、ここでは AWS Security Hub を AWS Security Hub CSPM の意味で記載しています [\*7](https://blog.serverworks.co.jp/#f-7b9d55a4 "名称変更については以下のブログに詳しく記載しました。[https://blog.serverworks.co.jp/reinforce2025-tdr309] ") 。

なお、昨今ランサムウェア攻撃に加え、EDoS (Economic Denial of Service) 攻撃も増えています [\*8](https://blog.serverworks.co.jp/#f-8847dc24 "わかりやすいように EDoS と記載しています。これは、侵入者に高額なインスタンスタイプである SageMaker や EC2 インスタンスを構築され、暗号通貨の採掘に利用されてしまったようなケースを包括してここでは記載しています。何故高額となるかというと、GPU を搭載したインスタンスが好まれるためです。このあたりは「AWS 環境における暗号通貨採掘悪用に備える」に詳しく記載しました。[https://blog.serverworks.co.jp/prepare-for-cryptocurrency-mining-abuse-on-aws] ") 。よってこれらに加えて業務継続性の観点からは **「コスト異常検出（Cost Anomaly Detection）」** の重要性が高まっています。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/s/swx-satake/20251107/20251107200442.png)

AWS Cost Anomaly Detection (コスト異常検出) は、意図しない突発的な AWS 利用料の増加（Cost Shock）を機械学習で検出し、早期対応を可能にする機能です。通知設定においては、以下も合わせてご覧ください。

[blog.serverworks.co.jp](https://blog.serverworks.co.jp/aws-cost-anomaly-detection-notification-guide)

### 4\. 対応 (Respond) - 影響を封じ込める

脅威を検知したら、即座に行動（封じ込め）を起こす必要があります。

- **アクセスの即時遮断**: 攻撃の疑いがある場合、最優先はアクセスの遮断です。侵害された **IAM アクセスキーを無効化** し、発行済みの一時クレデンシャルを「 **アクティブセッションの取り消し** 」で即座に失効させます。
- **対応計画**: 脅威を検知し遮断した後、技術的な対応を迅速に行うためにも、事前に「誰が何をどの順番で行うか」を定義した **インシデント対応計画を準備** し、定期的に演習しておくことが重要です。
- **調査**: **AWS CloudTrail** のログを分析し、攻撃者が検知されるまでに「何を」行ったのか、影響範囲はどこまでかを特定します。注意事項として、S3 等のデータイベントはデフォルトの設定では出力されません。特に S3 のデータイベントはフォレンジック調査において重要になる場合がありますので、事前にデータイベントの記録を忘れず設定します。
- **自動化**: **Amazon EventBridge** を使い、GuardDuty や Security Hub の「検知」をトリガーとして、 **AWS Lambda** を実行し「自動対応」の仕組みを構築することが推奨されます。なお2025年6月17日に、「 [AWS Network Firewall のアクティブ脅威防御マネージドルールグループを使用して自動的にブロック](https://aws.amazon.com/jp/about-aws/whats-new/2025/06/aws-network-firewall-active-threat-defense/) 」する機能もリリースされていますので、これを利用するのも手です。

[aws.amazon.com](https://aws.amazon.com/jp/blogs/news/improve-your-security-posture-using-amazon-threat-intelligence-on-aws-network-firewall/)

また、これらのインシデント対応プロセス全体を支援するマネージドサービスとして「AWS Security Incident Response」も2024年12月に発表されています。

[aws.amazon.com](https://aws.amazon.com/jp/security-incident-response/)

このサービスは、ランサムウェア攻撃を含むアカウント乗っ取り、データ侵害などのセキュリティインシデントに対し、迅速な準備・対応・復旧のガイダンスの提供を支援します。

Amazon GuardDuty や AWS Security Hub CSPM とのサードパーティー統合からアラートをレビューしてトリアージを支援し、重大インシデント時には AWS カスタマーインシデント対応チーム (CIRT) へのアクセスを提供。検出から復旧までのインシデントライフサイクル全体をガイドし、対応体制の強化を支援するものです。

ランサムウェア対策における「 **最後の砦** 」です。もし攻撃者にデータの暗号化や削除を許してしまっても、ここが機能すればビジネスは継続できます。

しかし、攻撃者もそれを理解しているため、 **近年のランサムウェアはバックアップデータ自体を最初の標的にします** 。バックアップを盗み、暗号化し、削除しようとします。

したがって、「バックアップを取る」ことと「 **バックアップを守る** 」ことは、同等以上に重要です。

- **バックアップの取得**:
	- **AWS Backup**: EC2, RDS, S3 など、AWS サービス全体のバックアップをポリシーベースで一元管理・自動化します。守るためのバックアップでは本番アカウントとは別の、隔離されたアカウントに（クロスアカウントで）保存することが推奨されます。
	- **S3 Versioning**: S3 バケットで有効にすることで、オブジェクトが上書き・削除されても古いバージョンが保持されます。削除操作は「削除マーカー」が追加されるだけなので、旧バージョンからの復元が可能です。
- **バックアップの保護 (WORM)**: 一度書き込んだら、一定期間は **ルートユーザーであっても絶対に削除・変更できなくする** 「WORM (Write-Once-Read-Many)」モデルの適用が、ランサムウェア対策の切り札となります。
	- **AWS Backup Vault Lock**: AWS Backup で取得したバックアップデータ（リカバリポイント）に対し、WORM 保護を強制します。これにより、管理者権限を奪った攻撃者によるバックアップデータの削除や保持期間の短縮を防ぎます。
	- **Amazon S3 Object Lock**: S3 バケット内のオブジェクト自体に WORM 保護を適用します。
- **インフラとシステムの復旧**:
	- **AWS CloudFormation**: インフラをコード (IaC) で定義しておけば、万が一インフラ構成自体が破壊されても、迅速にクリーンな環境を再デプロイ（復旧）できます。
	- **AWS Elastic Disaster Recovery (DRS)**: システム全体を迅速かつ低コストで別リージョンや別アカウントに復旧させるためのDR（ディザスタリカバリ）サービスです。

以下のブログでも触れましたが AWS Organizations における新しい OU として「Business Continuity OU」も AWS から新しく提案されています。

[blog.serverworks.co.jp](https://blog.serverworks.co.jp/business-continuity-ou)

Business Continuity OU はその名の通り「ビジネス継続性」を前提にした OU であり、それ専用の AWS アカウントを配置する枠組みです。これは「バックアップアカウント」とはまた異なる概念となっています。是非この観点も上記ブログにてご理解頂ければ幸いです。

#### Logically air-gapped vault

また、2024年8月の新機能、AWS Backup の Logically air-gapped vault も合わせてご紹介します。

[aws.amazon.com](https://aws.amazon.com/jp/blogs/news/building-cyber-resiliency-with-aws-backup-logically-air-gapped-vault/)

`Logically air-gapped vault` は、 **「WORM による削除防止」に加えて、「AWS owned key による暗号化の分離」と「別アカウントでの安全な復元」** をパッケージ化したことで、ランサムウェア攻撃に対する回復力を高めるための、新しいバックアップの仕組みとなっています。

AWS Backup Vault Lock (WORM) が防ぐものは、バックアップデータ自体の「削除」と「変更」。Logically air-gapped vault が防ぐのは、データの「削除」と「変更」に加えて、 **データの「窃取」と暗号化キーの「破壊 [\*9](https://blog.serverworks.co.jp/#f-afd960bf "CMK は即削除できないため、削除のスケジューリングにはなりますが") 」による復旧妨害** です。

## まとめ

本ブログでは、ランサムウェア対策という具体的なテーマで、AWS のソリューションを NIST CSF のフレームワークに沿って解説しました。

AWS のセキュリティの基本原則である「多層防御」と「マルチアカウント戦略」は、ランサムウェア対策においても強固な基盤となります。

特に重要なポイントは以下の通りです。

1. **防御 (Protect)**: 侵入経路を絶つことが最優先です。 **IAM Identity Center を活用** し、静的なアクセスキー（長期クレデンシャル）を予め排除しましょう。都合、IAM アクセスキーを作成せざるを得ない場合や、既に作成してしまった IAM アクセスキーの棚卸には、IAM Access Analyzer Unused Access が有用です [\*10](https://blog.serverworks.co.jp/#f-c739bfc7 "先に IAM Access Analyzer Unused Access に関するブログを紹介しましたが、コストには注意して利用してください") 。
2. **検知 (Detect)**: **Amazon GuardDuty** は基本必須です。これらが CloudTrail や VPC フローログといった基盤ログを自動分析し、脅威の兆候を早期に捉えてくれます。なお、ランサムウェア対策とは少し離れてしまうのですが、個人的には **コスト異常検出 (Cost Anomaly Detection) も基本必須としたい** と考えています。この2つの `Detect` サービスは AWS アカウントを利用しはじめたら直ちに設定したい2つのサービスです。
3. **復旧 (Recover)**: 「バックアップを取る」だけでは不十分です。「 **バックアップを WORM で保護する** 」こと、すなわち **AWS Backup Vault Lock** や **S3 Object Lock** の活用が、データを確実に守るための「 **最後の砦** 」となります。 **「Business Continuity OU」の概念を活用し、クロスアカウントのバックアップ戦略も有効** です。

そして最後に。セミナーでも最後に伝えた通り、セキュアな環境は「一度設定したら終わり」ではありません。脅威が日々進化するのと同様に、我々の防御体制も **「継続的な運用」を通じて改善し、進化させ続けることが鍵** となります。

では、またお会いしましょう。

---

[\*1](https://blog.serverworks.co.jp/#fn-1ab526a6):いわゆる、"チートシート"のようなものを目指します

[\*2](https://blog.serverworks.co.jp/#fn-217460f1):できればでよいですので、是非ウェビナーを見て頂いた方が理解が深まります

[\*3](https://blog.serverworks.co.jp/#fn-8b010469):ランサムウェアは、決して「Run somewhere」ではありません

[\*4](https://blog.serverworks.co.jp/#fn-33338667):最近では VPN 機器の脆弱性を突かれることが多い印象です

[\*5](https://blog.serverworks.co.jp/#fn-db0e3bee):少し細かい話をします。Sg はステートフルです。NACLs はステートレスです。Sg はコネクショントラッキングで、NACLs はパケットごとの評価をします。よって、既に確立されたコネクションを断したい場合は、Sg では不可能です。NACLs でないと、遮断できません

[\*6](https://blog.serverworks.co.jp/#fn-59f3ab3f):ペネトレーションテストに関する注意については「AWS WAF 適用環境におけるペネトレーションテストの目的と対応方法を整理する」も参考になると存じます [https://blog.serverworks.co.jp/aws-waf-penetration-testing-guide](https://blog.serverworks.co.jp/aws-waf-penetration-testing-guide)

[\*7](https://blog.serverworks.co.jp/#fn-7b9d55a4):名称変更については以下のブログに詳しく記載しました。 [https://blog.serverworks.co.jp/reinforce2025-tdr309](https://blog.serverworks.co.jp/reinforce2025-tdr309)

[\*8](https://blog.serverworks.co.jp/#fn-8847dc24):わかりやすいように EDoS と記載しています。これは、侵入者に高額なインスタンスタイプである SageMaker や EC2 インスタンスを構築され、暗号通貨の採掘に利用されてしまったようなケースを包括してここでは記載しています。何故高額となるかというと、GPU を搭載したインスタンスが好まれるためです。このあたりは「AWS 環境における暗号通貨採掘悪用に備える」に詳しく記載しました。 [https://blog.serverworks.co.jp/prepare-for-cryptocurrency-mining-abuse-on-aws](https://blog.serverworks.co.jp/prepare-for-cryptocurrency-mining-abuse-on-aws)

[\*9](https://blog.serverworks.co.jp/#fn-afd960bf):CMK は即削除できないため、削除のスケジューリングにはなりますが

[\*10](https://blog.serverworks.co.jp/#fn-c739bfc7):先に IAM Access Analyzer Unused Access に関するブログを紹介しましたが、コストには注意して利用してください

[« RDS for PostgreSQLで検索機能をリッチに…](https://blog.serverworks.co.jp/setting-of-pg-trgm-and-pg-bigm) [Docker on EC2のログ監視、CloudWatchで始… »](https://blog.serverworks.co.jp/monitoring-docker-on-ec2-minimum)