---
title: "[アップデート] Amazon SES API VPCエンドポイントが使用できるようになりました | DevelopersIO"
source: "https://dev.classmethod.jp/articles/amazon-ses-vpc-api-endpoints/"
author: ""
published: "2025-12-08"
created: "2025-12-09"
description: "わざわざNAT Gatewayを作成する必要がなくなった"
tags:
  - ""
  - "raw"
---

## NAT Gatewayを経由せずにAmazon SESのAPIを使ってメール送信したい

こんにちは、のんピ([@non\_\_\_\_97](https://twitter.com/non____97))です。

皆さんはNAT Gatewayを経由せずにAmazon SESのAPIを使ってメール送信したいなと思ったことはありますか? 私はあります。

従来からAmazon SESのVPCエンドポイントはありました。しかし、このVPCエンドポイントはSMTPインターフェイスのみをサポートしています。

Amazon SESによるメール送信はSMTPとAPIの2種類の操作がありますが、認証情報の管理やスループットの観点からAPI利用での送信が推奨されています。

つまりは推奨されるAPIを使ったメール送信をする際には、NAT Gatewayを経由させたり、メールクライアント自身にElastic IPアドレスを付与したりする必要がありました。セキュリティポリシー上これを許容できない場合もあるでしょう。

今回、アップデートによりAmazon SES APIがVPCエンドポイントをサポートしました。

これにより、NAT Gatewayを用意することなく、メール送信することが可能です。

実際に試してみたので紹介します。

## いきなりまとめ

- SES API VPCエンドポイントを作成することで、NAT GatewayなしにSES API経由でメール送信ができるようになった
- SES IDの送信承認ポリシーを用いることで、特定のSES API VPCエンドポイント経由でしかメール送信させないことも可能

## やってみた

### 検証環境

検証環境は以下のとおりです。

![検証環境構成図.png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/LAFhupemKDfo.png)

Internet GatewayもNAT Gatewayも存在しないため、AWSのサービスエンドポイントへ通信をするためにはVPCエンドポイントが必要になってきます。

この図に含まれていないSES API VPCエンドポイントは後ほど作成します。

### SMTPインターフェイスのVPCエンドポイント経由でSESのAPIでメール送信できることの確認

まず、SMTPインターフェイスのVPCエンドポイント経由でSESのAPIでメール送信できることを確認をします。

以下AWS公式ドキュメントにSMTP インターフェイスを使用してコマンドラインからメール送信をするスクリプトが紹介されていました。

実際のスクリプトは以下のとおりです。

```bash
$ vi send-mail.sh
$ cat send-mail.sh 
#!/bin/bash

# Prompt user to provide following information
read -p "Configuration set: " CONFIGSET
read -p "Enter SMTP username: " SMTPUsername
read -p "Enter SMTP password: " SMTPPassword
read -p "Sender email address: " MAILFROM
read -p "Receiver email address: " RCPT
read -p "Email subject: " SUBJECT
read -p "Message to send: " DATA

echo

# Encode SMTP username and password using base64
EncodedSMTPUsername=$(echo -n "$SMTPUsername" | openssl enc -base64)
EncodedSMTPPassword=$(echo -n "$SMTPPassword" | openssl enc -base64)

# Construct the email
Email="EHLO www.non-97.net
AUTH LOGIN
$EncodedSMTPUsername
$EncodedSMTPPassword
MAIL FROM: $MAILFROM
RCPT TO: $RCPT
DATA
X-SES-CONFIGURATION-SET: $CONFIGSET
From: $MAILFROM
To: $RCPT
Subject: $SUBJECT

$DATA
.
QUIT"

echo "$Email" | openssl s_client -crlf -quiet -starttls smtp -connect email-smtp.us-east-1.amazonaws.com:587
```

また、スクリプト内に記載されていSMTPインターフェイスのエンドポイントの名前解決をします。

プライベートIPアドレスが返ってきましたね。これはSMTPインターフェイスのVPCエンドポイントに割り当てられているIPアドレスと一致します。

![3.SMTPインターフェイスのVPCエンドポイント.png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/wcZzmAlDf4rB.png)

では、メール送信します。

正常にメール送信が行われていそうですね。

送信先のメールボックスを確認すると、メールが届いていました。

![1.メールを受信したことを確認.png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/tcPc3WLS7Jz2.png)

また、SES IDのメールのフィードバック通知で `Delivery` を設定していたため、以下通知を受信しました。

```json
{
  "notificationType": "Delivery",
  "mail": {
    "timestamp": "2025-12-08T05:14:09.443Z",
    "source": "mail-client@www.non-97.net",
    "sourceArn": "arn:aws:ses:us-east-1:<AWSアカウントID>:identity/www.non-97.net",
    "sourceIp": "10.0.137.142",
    "callerIdentity": "ses-smtp-user.20251208-135820",
    "sendingAccountId": "<AWSアカウントID>",
    "messageId": "0100019afc61a6a3-642eaf57-7afe-449e-a1f2-79b7a0e7a531-000000",
    "destination": [
      "<送信先メールアドレス>"
    ],
    "headersTruncated": false,
    "headers": [
      {
        "name": "Received",
        "value": "from www.non-97.net (ip-10-0-137-142.ec2.internal [10.0.137.142]) by email-smtp.amazonaws.com with SMTP (SimpleEmailService-d-AKB5QEBJG) id n5pYSOJsgSqVzbGOd7ww for <送信先メールアドレス>; Mon, 08 Dec 2025 05:14:09 +0000 (UTC)"
      },
      {
        "name": "X-SES-CONFIGURATION-SET",
        "value": ""
      },
      {
        "name": "From",
        "value": "mail-client@www.non-97.net"
      },
      {
        "name": "To",
        "value": "<送信先メールアドレス>"
      },
      {
        "name": "Subject",
        "value": "test mail subject"
      }
    ],
    "commonHeaders": {
      "from": [
        "mail-client@www.non-97.net"
      ],
      "to": [
        "<送信先メールアドレス>"
      ],
      "subject": "test mail subject"
    }
  },
  "delivery": {
    "timestamp": "2025-12-08T05:14:10.368Z",
    "processingTimeMillis": 925,
    "recipients": [
      "<送信先メールアドレス>"
    ],
    "smtpResponse": "250 2.0.0 OK  1765170850 af79cd13be357-8b6252997aesi973912185a.207 - gsmtp",
    "remoteMtaIp": "142.251.111.26",
    "reportingMTA": "a48-105.smtp-out.amazonses.com"
  }
}
```

### SMTPインターフェイスのVPCエンドポイント経由でSESのAPIでメール送信できないことの確認

続いて、SMTPインターフェイスのVPCエンドポイント経由でSESのAPIでメール送信できないことの確認をします。

まず、EC2インスタンスにアタッチしているIAMロールには以下IAMポリシーを追加しておきます。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "ses:SendEmail",
            "Resource": [
                "arn:aws:ses:*:<AWSアカウントID>:configuration-set/*",
                "arn:aws:ses:*:<AWSアカウントID>:identity/*",
                "arn:aws:ses:*:<AWSアカウントID>:template/*"
            ]
        }
    ]
}
```

この状態でSES APIを使ったメール送信を試します。

```bash
$ aws ses send-email \
    --from mail-client@www.non-97.net \
    --to <送信先メールアドレス> \
    --subject "api test mail subject" \
    --text "API test mail"

Connect timeout on endpoint URL: "https://email.us-east-1.amazonaws.com/"
```

はい、エンドポイントに接続できないということでメール送信できませんでした。

名前解決をしてみます。

パブリックIPアドレスが返ってきましたね。やはりSMTPインターフェイスとSES APIのエンドポイントは別物ということが分かります。

### SES API VPCエンドポイント経由でSESのAPIでメール送信できることの確認

では、SES API VPCエンドポイント経由でSESのAPIでメール送信できることの確認をします。

SES APIのVPCエンドポイントを作成します。

![2.SES APIのVPCエンドポイントの作成.png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/e1AkpGtHArZZ.png)

しばらくすると作成が完了しました。

![4.SES APIのVPCエンドポイント.png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/C2nQSe5FCLUn.png)

SES APIのサービスエンドポイントを名前解決します。

今度はプライベートIPアドレスが返ってきましたね。

この状態でメール送信をします。

```bash
$ aws ses send-email \
    --from mail-client@www.non-97.net \
    --to <送信先メールアドレス> \
    --subject "api test mail subject" \
    --text "API test mail"
{
    "MessageId": "0100019afc78b53f-65858957-f3d3-4a50-865e-2c5d3adb9d22-000000"
}
```

はい、先ほどとコマンドは全く変えていないですが、メール送信できました。

送信先のメールボックスにも届いていました。

![5.メールを受信したことを確認.png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/RPX0u5kJXyjA.png)

また、Deliveryの通知も届いていました。

```json
{
  "notificationType": "Delivery",
  "mail": {
    "timestamp": "2025-12-08T05:39:20.511Z",
    "source": "mail-client@www.non-97.net",
    "sourceArn": "arn:aws:ses:us-east-1:<AWSアカウントID>:identity/www.non-97.net",
    "sourceIp": "10.0.137.142",
    "callerIdentity": "AmazonSSMRoleForInstancesQuickSetup",
    "sendingAccountId": "<AWSアカウントID>",
    "messageId": "0100019afc78b53f-65858957-f3d3-4a50-865e-2c5d3adb9d22-000000",
    "destination": [
      "<送信先メールアドレス>"
    ],
    "headersTruncated": false,
    "headers": [
      {
        "name": "From",
        "value": "mail-client@www.non-97.net"
      },
      {
        "name": "To",
        "value": "<送信先メールアドレス>"
      },
      {
        "name": "Subject",
        "value": "api test mail subject"
      },
      {
        "name": "MIME-Version",
        "value": "1.0"
      },
      {
        "name": "Content-Type",
        "value": "text/plain; charset=UTF-8"
      },
      {
        "name": "Content-Transfer-Encoding",
        "value": "7bit"
      }
    ],
    "commonHeaders": {
      "from": [
        "mail-client@www.non-97.net"
      ],
      "to": [
        "<送信先メールアドレス>"
      ],
      "subject": "api test mail subject"
    }
  },
  "delivery": {
    "timestamp": "2025-12-08T05:39:21.394Z",
    "processingTimeMillis": 883,
    "recipients": [
      "<送信先メールアドレス>"
    ],
    "smtpResponse": "250 2.0.0 OK  1765172361 d75a77b69052e-4f027cfce10si131947051cf.171 - gsmtp",
    "remoteMtaIp": "172.253.62.27",
    "reportingMTA": "a8-95.smtp-out.amazonses.com"
  }
}
```

### 送信承認ポリシーを使ってVPCエンドポイント経由でしか送信できないようにする

応用として、送信承認ポリシーを使ってVPCエンドポイント経由でしか送信できないようにしましょう。

送信承認ポリシー設定前に、手元のMac端末からSES APIを使ってメール送信できることを確認します。なお、この操作をしているユーザーの権限はAdministratorAccessです。

```bash
$ aws ses send-email \
    --from mail-client@www.non-97.net \
    --to <送信先メールアドレス> \
    --subject "api test mail subject from mac" \
    --text "API test mail from mac"
{
    "MessageId": "0100019afc7c489d-7c804289-2535-4c7a-aa05-3b6b15fbb282-000000"
}
```

正常にメール送信できました。

メールの受信も確認しています。

![6.api test mail subject from mac.png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/eejixT6lG7RQ.png)

では、送信承認ポリシーを使ってVPCエンドポイント経由でしか送信できないようにしましょう。

AWS公式ドキュメントには以下記載があったため `aws:SourceVpce` も使用できるでしょう。

> IAM ユーザーガイドの「使用可能なキー」に記載されている AWSすべてのキーを使用できます。

具体的なポリシーは以下のとおりです。

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Resource": "arn:aws:ses:us-east-1:<AWSアカウントID>:identity/www.non-97.net",
      "Action": [
        "ses:SendEmail",
        "ses:SendRawEmail",
        "ses:SendTemplatedEmail",
        "ses:SendBulkTemplatedEmail"
      ],
      "Principal": "*",
      "Condition": {
        "StringNotLike": {
          "aws:SourceVpce": "vpce-0495ff730c01bb661"
        }
      }
    }
  ]
}
```

送信承認ポリシーを設定すると以下のようになります。

![9.承認ポリシー .png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/ZRrZKIkAnX96.png)

この状態でメール送信します。

まずは手元のMac端末からです。

```bash
$ aws ses send-email \
    --from mail-client@www.non-97.net \
    --to <送信先メールアドレス> \
    --subject "api test mail subject from mac" \
    --text "API test mail from mac"
An error occurred (AccessDenied) when calling the SendEmail operation: User \`arn:aws:sts::<AWSアカウントID>:assumed-role/<IAMロール名>/<セッション名>' is not authorized to perform \`ses:SendEmail' on resource \`arn:aws:ses:us-east-1:<AWSアカウントID>:identity/www.non-97.net'
```

はい、メールが送信できなくなりました。エラーメッセージから `ses:SendEmail` がSES IDで許可されていないユーザーを使っているためによるものということが分かります。

では、EC2インスタンスからメール送信します。

```bash
$ aws ses send-email \
    --from mail-client@www.non-97.net \
    --to <送信先メールアドレス> \
    --subject "api test mail subject from ec2" \
    --text "API test mail from ec2"
{
    "MessageId": "0100019afc8cdd7a-28af6dff-b160-4a72-85fc-37a2dd032ff0-000000"
}
```

こちらは問題なく受け付けられました。

メールも正常に受信しています。

![10.api test mail subject from ec2.png](https://devio2024-2-media.developers.io/upload/0RqxpJ2Gm3nEdxVLGKLWmq/2025-12-08/Lz4v3m8shtci.png)

「メールを送信する際には特定一箇所経由からでなければ送信できない」という要件があったとしても対応できそうですね。

## わざわざNAT Gatewayを作成する必要がなくなった

Amazon SES API VPCエンドポイントが使用できるようになったアップデートを紹介しました。

わざわざNAT Gatewayを作成する必要がなくなったのが非常に大きいですね。

具体的には以下のような方に刺さると考えます。

- SES APIでメール送信するためだけにNAT Gatewayを用意していた
- 「インターネットとの口を用意してはならない」という制約事項としてあったため、SMTPインターフェイスを使わざるを得なかった

加えて、大容量のデータを添付したメールを大量に送信する場合はSES API VPCエンドポイントを使用した方がNAT Gatewayよりもデータ転送量的にもお安くなることもあるでしょう。

この記事が誰かの助けになれば幸いです。

以上、クラウド事業本部 コンサルティング部の のんピ([@non\_\_\_\_97](https://twitter.com/non____97))でした!

この記事をシェアする