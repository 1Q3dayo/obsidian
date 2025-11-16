---
title: "[アップデート] Service Quotas にクォータが最大使用率に近づいた時に通知を送信できる「自動管理設定」機能が追加されました | DevelopersIO"
source: "https://dev.classmethod.jp/articles/automatic-quota-management-service-quotas/"
author:
  - "[[いわさ]]"
published: 2025-10-11
created: 2025-11-17
description:
tags:
  - "clippings"
  - raw
---
いわさです。

AWS には様々なサービスクォータが存在しています。  
AWS Well-Architected でも、ワークロードではこれらの制限を理解したうえで、適切な上限緩和や監視などサービスクォータの管理を行うことが推奨されています。  
これまではそれを実現するために EventBridge や CloudWatch や Trusted Advisor でモニタリングしたり、あるいは Quota Monitor for AWS などのソリューション実装を導入するなど様々な工夫が必要でした。

先日のアップデートで AWS Service Quotas の機能として、このサービスクォータを自動管理する機能が追加されました。

色々なテクニックを駆使しなくても、Service Quotas コンソールから簡単に設定することができるようになります。  
本日時点では通知のみが行えるようで、将来的には通知+クォータ引き上げも行えるようになりそうです。

本日は自動管理設定を有効化し、どのような設定がされるのか、サービス上限に達した際にどういう挙動が起きるのかを確認してみましたので紹介します。  
ただ、どういう通知がされるかまで確認したかったのですが、本日私が確認した限りではイベント通知がされていないようでした。どうして...

## 設定方法

自動管理設定機能ですが、Servcie Quotas のメニューに新しく追加されています。

![2E3F8495-DA4A-4A5C-92BB-9E98D5EC1E0D.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/wEPUImc7bT21.png)

このメニューからそのまま自動管理設定を行うことが出来ます。  
自動管理モードという概念があるようで、本日時点では「通知のみ」が選択可能です。クォータが最大に達しそうな時に通知されます。  
近日公開となっているのが「通知と自動調整」で、こちらはクォータが使用率に達すると自動的にクォータ引き上げリクエストが行われつつ通知までしてくれるみたいです。これはすごいですね。自動引き上げ実装するのまぁまぁ面倒だったと思うので。

![1411923C-BD1B-488C-9E24-53E1E5186C27.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/A4TJMAZVdCMW.png)

今回は「通知のみ」で作成してみましょう。  
この機能、仕組みとしては AWS User Notifications が使われており通知されるみたいです。  
この自動管理設定画面からそのまま User Notifications の通知設定を作成できるみたいです。

![FC248DA9-E443-41C0-89F5-8BF5CC8B1D1C.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/6lh6fPDjeUEX.png)

なので、通知先に選択できるのは User Notifications でサポートされている「Eメール」「AWS コンソールモバイルアプリケーション」「チャットチャネル（Teams / Slack）」から選択が出来ます。

![D898A8C8-328F-490F-8EB1-B3E315028731.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/uH7dz25uWRWX.png)

ステップ３がおもしろいなぁと思ったのですが、通知の例外を指定することが出来ます。  
これがサービスごと、クォータごとに例外設定することが出来て、とても設定しやすそうだなと思いました。

![06E34317-C7A9-4C09-873B-B962F6034C1F.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/6ywpSbcviYfR.png)

作成後、Service Quotas のダッシュボードに遷移しますが、ダッシュボード上でも自動管理設定への導線が追加されていました。

![6489A8D5-0B76-4BD5-81C6-502EF5CDB9B4.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/Xd9JhuCEbqBk.png)

User Notiifications の通知設定としてはこんな感じで作成されます。EventBridge で Health イベント全般を引っ掛けて、User Notifications のアドバンスドフィルターで自動管理設定で指定した内容でフィルタリングされる感じですね。

![7E85D928-ACC4-4D1D-9793-228CCA76DF28.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/ssLLk906UqsO.png)

## 通知を確認したかったのだが...

この自動管理機能の仕様は以下のドキュメントに記載がされていまして、クォータ使用率が 80% に達したとき、95% に達したときに通知を受け取ることが出来ます。

アドバンスドフィルターの以下のあたりで設定されていますね。

![image.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/FnQihHkc7Puh.png)

今回実際に動作確認を行ってみました。  
結論だけ先にお伝えすると通知がうまくされませんでした。いくつかのクォータやリージョン、AWS アカウントで試してみましたけどダメでしたね。ちょっと時間がかかるのかな。

例として私のアカウントだとリージョンあたりの VPC 数が 20 まで許可されているのですが、この上限に近づけて VPC を作成しつづけてみました。

![A3A709F0-E81B-415C-9245-9FE1E62A660A.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/HgXjDGcNZpXn.png)

20 個 VPC を作成してみました。

![16CDC090-0424-48EB-AF6C-955A394C7646.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/xMnscU5BqG3P.png)

そのタイミングで Health Event の通知を受信して「おっ」と思ったのですが内容は CodeCatalyst の話でした。違う...

![0834F241-C7A6-4C01-ACAC-0754EEBD6652.png](https://devio2024-2-media.developers.io/upload/6zWUnlDies1gnRi1IhiTa6/2025-10-10/bbHBJ7LIrtoI.png)

その後も Elastic IP の上限で試してみたり、バージニア北部で試してみたり、全く別の AWS アカウントで試してみたりしたのですが変わらずでしたね。  
ちょっと時間を置いてまた試してみたいと思います。

### 2025.10.12 追記

1日経過したタイミングで通知を受信しました！  
これくらいタイムラグがあるものなのか？アップデート直後でうまく通知できてなかったのか不明ですが一応受信が出来ました。

![A6F5FB74-34DD-4F21-9D1F-E0E88DF4D161](https://devio2024-media.developers.io/image/upload/v1760225535/2025/10/12/kd4k2ezcstpibn4nkiif.png)

## さいごに

本日は Service Quotas にクォータが最大使用率に近づいた時に通知を送信できる「自動管理設定」機能が追加されたので使ってみました。

設定は非常に簡単で、例外設定までできて良いですね。  
また、将来的には通知だけでなく自動での上限緩和申請まで出来るみたいでとても良さそうです。

一方で本日時点だと私はまだうまく通知の受信ができなかったので、もう少し評価が必要です。何か前提条件あるのかな。  
通知を受信できた方がもしいらっしゃったらぜひ教えてください。

この記事をシェアする