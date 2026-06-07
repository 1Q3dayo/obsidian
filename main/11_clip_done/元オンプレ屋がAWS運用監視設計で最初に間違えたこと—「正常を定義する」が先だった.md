---
title: "元オンプレ屋がAWS運用監視設計で最初に間違えたこと—「正常を定義する」が先だった"
source: "https://zenn.dev/aa_taka/articles/e835abca466897"
author:
published: 2026-06-05
created: 2026-06-07
description:
tags:
  - "clippings"
  - "raw"
---
7

5

> 本記事の執筆にはAIを活用しています。

## はじめに

前回の記事（ [元オンプレ屋が疑似AWS環境のログをGemiclawに確認してもらうまで](https://zenn.dev/aa_taka/articles/c5e67c212e4a40) ）で、GemiclawにLocalStackのログを確認してもらったとき、出てきたのはこれだけでした。

```
START RequestId: ccefc143-7e11-4371-8472-5e8eac510bbd Version: $LATEST
END RequestId: ccefc143-7e11-4371-8472-5e8eac510bbd
REPORT RequestId: ccefc143-7e11-4371-8472-5e8eac510bbd  Duration: 0.97ms  Memory Size: 128MB
```

このログから読み取れる情報は「Lambdaが0.97ミリ秒で終了した」だけです。認証が成功したのか失敗したのか、DynamoDBへのアクセスが通ったのかどうか、何もわかりません。

あのとき自分が見ていたのは、監視ではありませんでした。

この記事で伝えたいことは1つです。

> AWS運用監視設計において最初の、かつ最も重要な判断は、アラームを設定することではなく、 **正常を定義することだった** 。そしてその定義は、 **インフラ設計と同時に行わなければ機能しない** 。

この主張は、オンプレ8年・監視ツール実装経験ゼロの自分が、LocalStackから本番AWSへの移行を経て、実際に詰まりながら発見したものです。

この記事では以下を記録しています。

- なぜLocalStackの段階でそれが見えなかったか
- 本番AWSに移行して初めて見えたものは何か
- 「正常」をどう定義し、Alarmとして機能させたか
- 設計ミスをどう発見し、どう修正したか

---

## 1\. システム構成と前提

### 1-1. 今回のシステム

前回の記事で構築した写真管理システムを使っています。構成は前回から変わっていませんが、今回は監視設計のスタック（SNS・CloudWatch Alarm・X-Ray・DLQ・Dashboard）を追加しました。

```
AWS Environment (本番 ap-northeast-1)
│
├── API Gateway (AuthAPI / ステージ: dev)
│   ├── /login (POST) ──→ auth-handler（認証・署名付きURL発行）
│   ├── /admin/list (GET) ──→ admin-list-handler（写真一覧取得）
│   └── /admin/update (POST) ──→ admin-update-handler（ステータス更新）
│
├── S3: photo-storage-<アカウントID>
│   └── s3:ObjectCreated:* ──→ photo-handler（自動起動・DB登録）
│
├── Lambda Functions（Go / provided.al2023）
│   ├── auth-handler（timeout: 10秒）
│   ├── photo-handler（timeout: 30秒・DLQ設定済み）
│   ├── admin-list-handler（timeout: 10秒）
│   └── admin-update-handler（timeout: 10秒）
│
├── SQS: photo-handler-dlq（Dead Letter Queue）
├── SNS: gemiclaw-alarm-topic（アラーム通知先）
├── CloudWatch Alarm（9件）
├── CloudWatch Dashboard: gemiclaw-ops
├── CloudWatch Logs（全関数・retention: 14日）
└── DynamoDB
    ├── AuthUser（管理者: aataka / 社員: tanaka）
    └── PhotoMetadata（写真メタデータ）
```

インフラはすべてTerraformで管理しています。GitHubリポジトリ（ [Aataka/gemiclaw-cloud](https://github.com/Aataka/gemiclaw-cloud) ）は公開しています。

### 1-2. 前回との差分

前回の記事では、このシステムをLocalStack上で構築し、Gemiclawがログを確認できる状態にするところまでを記録しました。今回は以下を追加しています。

- 全4Lambda関数への構造化ログ（ `log.Printf` ）の追加
- 本番AWSへの移行（LocalStack固有設定の除去・Go側エンドポイント設定の除去）
- main.tfへの本番向けセキュリティ設定追加（S3パブリックアクセスブロック・サーバサイド暗号化・バージョニング・DynamoDBのpoint-in-time recovery）
- `terraform.tfvars.production` を`.gitignore` に追加し、本番環境のメールアドレス等をGitにコミットしない設計にしました
- 監視スタックの実装（SNS・CloudWatch Alarm×9・メトリクスフィルター×3・X-Ray・Dashboard）
- 運用テスト10シナリオの実施とベースライン計測

前回の「今後の展望」に書いた「SQSやSNSで非同期処理の堅牢性を高めたい」「LocalStackと本番AWSで検証したい」は、この記事で実現しています。

---

## 2\. オンプレ8年の「監視」とは何だったか

なぜGemiclawにログを確認させようとしたのか。前回の記事に書いたとおり、LocalStack上のシステムが「動いている」ことをDiscordから確認できたら便利だと思ったからです。そしてそのとき、自分の中には「ログを見れば何かわかるはずだ」という感覚がありました。オンプレでは確かにそうだったので。

8年のオンプレ経験での障害対応フローは、大体こうでした。

1. **pingが通るか** ——まず疎通確認。サーバが死んでいればここで終わり
2. **プロセスが生きているか** —— `ps aux | grep` で確認。死んでいれば起こす
3. **ログで死因を特定** —— `/var/log/messages` や各種アプリログをgrepして原因を探す
4. **syslogで時系列追跡** ——単体のエラーではなく「いつから」「どの順番で」を追う

ログの読み方は「grepで探す」ではなく「時系列で流れを追う」という感覚でした。サーバが何かを処理するとき、OSやミドルウェアは勝手にsyslogに吐いてくれます。自分はそのログを時系列で読んで、何が起きたかを組み立てる作業をしていました。

「このエラーは無視していい」「これはクリティカルだ」という判断は、現場で先輩から受け継いだ暗黙知として存在していました。Zabbixなどの監視ツールを使っている現場もありましたが、自分の担当案件では「何かあったら確認しに行く」という受動的な運用が多かったです。

ここに、AWSで詰まる原因のすべてがありました。

オンプレではOSとミドルウェアが「何かが動いている」という前提を担保してくれていました。プロセスが死んでいればpingが落ちます。何かが失敗すればsyslogに残ります。自分がやっていたのは「用意されたログを読む」ことでした。

AWSのLambdaは違います。

---

## 3\. LocalStackで「見えていたもの」と「見えていなかったもの」

### 3-1. ログは書かないと残らない

前回の記事でGemiclawが取得したログをもう一度見てください。

```
START RequestId: ccefc143-7e11-4371-8472-5e8eac510bbd Version: $LATEST
END RequestId: ccefc143-7e11-4371-8472-5e8eac510bbd
REPORT RequestId: ccefc143-7e11-4371-8472-5e8eac510bbd  Duration: 0.97ms  Memory Size: 128MB
```

これはauth-handlerのログです。このログが出た時点で、Lambdaは正常に終了しています。しかし：

- 認証が成功したのか失敗したのか、わかりません
- DynamoDBへのアクセスが通ったのか、わかりません
- 誰がログインしようとしたのか、わかりません

なぜこうなるのか。LambdaはGoで書かれており、 `log.Printf` を明示的に書かない限り、START/END/REPORTしか残りません。オンプレではOSが勝手にsyslogに吐いてくれていましたが、Lambdaはアプリケーションコードが何も言わなければ何も記録しません。

修正前のauth-handler（ `src/lambda/auth/main.go` ）の中を見ると、 `log` パッケージすらimportされていませんでした。

修正後に追加したログは以下です：

```
// リクエストパースエラー
log.Printf("[ERROR] Failed to parse request body: %v", err)

// 空IDでのアクセス
log.Printf("[WARN] Login attempt with empty ID")

// 認証フロー
log.Printf("[INFO] Login attempt: userID=%s", req.ID)
log.Printf("[ERROR] AWS config load failed: %v", err)
log.Printf("[ERROR] DynamoDB GetItem failed: userID=%s error=%v", req.ID, err)
log.Printf("[WARN] Login failed - user not found: userID=%s", req.ID)
log.Printf("[WARN] Login failed - invalid password: userID=%s", req.ID)
log.Printf("[INFO] Login succeeded: userID=%s role=%s", req.ID, role)

// 署名付きURL発行
log.Printf("[ERROR] PresignPutObject failed: userID=%s bucket=%s key=%s error=%v", req.ID, bucketName, objectKey, err)
log.Printf("[INFO] PresignedURL issued: userID=%s key=%s", req.ID, objectKey)
```

修正後のログはこうなりました：

```
START RequestId: xxx Version: $LATEST
2026/05/22 12:34:01 [INFO] Login attempt: userID=aataka
2026/05/22 12:34:01 [INFO] Login succeeded: userID=aataka role=Admin
2026/05/22 12:34:01 [INFO] PresignedURL issued: userID=aataka key=uploads/aataka/1748000000.jpg
END RequestId: xxx
REPORT RequestId: xxx  Duration: 29.4ms  Memory Size: 128MB
```

START→ENDの間に「何が起きたか」が見えるようになりました。これが出発点です。

photo-handler・admin-list-handler・admin-update-handlerの3関数も同様に修正しました。全4関数のログ追加が完了して初めて、「監視する準備ができた」という状態になりました。

### 3-2. 成功と失敗がログ上で区別できない

修正前、photo-handlerに対して意図的に失敗するリクエストを送ったことがあります。存在しないバケット名（ `wrong-bucket` ）を指定してS3にアップロードを試みました。

レスポンスは `StatusCode: 200` 、body `null` 。

そしてログは：

```
START RequestId: yyy Version: $LATEST
END RequestId: yyy
REPORT RequestId: yyy  Duration: 16.2ms  Memory Size: 128MB
```

正常実行と **完全に同一でした** 。

photo-handlerのGoコードを確認すると、エラー時は `return err` だけで、何も記録していませんでした。成功したのか失敗したのかを区別するには、 `log.Printf` でエラーを明示的に記録する必要があります。

修正後のphoto-handler全体：

```
func handler(ctx context.Context, s3Event events.S3Event) error {
    cfg, err := config.LoadDefaultConfig(ctx,
        config.WithRegion("ap-northeast-1"),
    )
    if err != nil {
        log.Printf("[ERROR] AWS config load failed: %v", err)
        return err
    }

    dbClient := dynamodb.NewFromConfig(cfg)

    for _, record := range s3Event.Records {
        rawKey := record.S3.Object.Key
        key, err := url.QueryUnescape(rawKey)
        if err != nil {
            key = rawKey
        }

        parts := strings.Split(key, "/")
        if len(parts) < 3 {
            log.Printf("[WARN] Skipping invalid key format: %s", key)  // ← 追加
            continue
        }

        userID := parts[1]
        log.Printf("[INFO] Processing: bucket=%s key=%s userID=%s",  // ← 追加
            record.S3.Bucket.Name, key, userID)

        _, err = dbClient.PutItem(ctx, &dynamodb.PutItemInput{
            TableName: aws.String(os.Getenv("METADATA_TABLE")),
            Item: map[string]types.AttributeValue{
                "PhotoID": &types.AttributeValueMemberS{Value: key},
                "UserID":  &types.AttributeValueMemberS{Value: userID},
            },
        })
        if err != nil {
            log.Printf("[ERROR] DynamoDB PutItem failed: key=%s error=%v", key, err)  // ← 追加
            return err
        }

        log.Printf("[INFO] DynamoDB PutItem succeeded: key=%s userID=%s", key, userID)  // ← 追加
    }

    return nil
}
```

これで失敗時のログが出るようになりました。ただし、これだけでは足りません。次のセクションで説明します。

### 3-3. 非同期処理の失敗検知はオンプレに概念がない

photo-handlerは、S3にファイルがアップロードされたとき、イベント通知によって自動的に起動します。誰かが呼び出すのではなく、S3イベントが引き金になります。

オンプレで「プロセスが死んでいればpingで気づける」という前提が通用しないのは、このためです。photo-handlerが失敗しても、呼び出し元（S3イベント）は「失敗した」とユーザーに返しません。ユーザーはS3へのアップロード自体は成功しているため、何も気づきません。DynamoDBへの登録が失敗したまま、静かに処理が消えてしまいます。

この問題に対処するのがDead Letter Queue（DLQ）です。Lambdaの非同期呼び出しは、リトライ（デフォルト2回）が全て失敗した場合、イベントをDLQに転送します。DLQに滞留したメッセージをアラームで検知することで、「誰も気づかない失敗」を捕捉できます。

LocalStackのmain.tfを確認すると、SQSリソースも `dead_letter_config` も存在しませんでした。DLQはLocalStack段階では「動いているように見えたが、本番では通用しない」設計の代表例です。

### 3-4. LocalStackでの確認状況まとめ

| 確認項目 | LocalStackでの状態 | 本番で必要な追加作業 |
| --- | --- | --- |
| CloudWatch Logsのロググループ | ✅ 見えた（Lambda実行後に自動生成） | — |
| START/END/REPORTログ | ✅ 見えた | — |
| DynamoDB登録の成否 | ❌ 修正前は見えなかった | `log.Printf` の追加 |
| 認証の成否（200/401） | ❌ 見えなかった | `log.Printf` の追加 |
| CloudWatch Metrics | ❌ 未設定 | Alarmの追加 |
| X-Ray | ❌ 未設定 | tracing設定＋IAM権限 |
| DLQ | ❌ 未設定 | SQS＋dead\_letter\_config |
| CloudWatch Alarm | ❌ 未設定 | main.tfへの追加 |

---

## 4\. 「正常を定義する」という判断 - Alarm設計の前に何が必要だったか

### 4-1. エラーの判断基準は自分で明文化しなければならない

オンプレでは「このエラーは無視していい」「これはクリティカルだ」という判断が、先輩の経験知として現場に存在していました。自分はそれを受け取って使っていました。

AWSでは、その判断を自分でCloudWatch AlarmとSNSとして定義しなければ、何も動きません。誰も教えてくれないし、勝手にアラームは鳴りません。

Alarmを設定しようとして最初に気づいたのは、「何をもって異常とするか」が決まらないと設定できないということでした。閾値を決めるには「正常な状態がどのようなものか」を先に知っていなければなりません。これが「正常を定義する」という判断の実体です。

### 4-2. auth-handlerの設計判断

auth-handlerへのリクエストは2種類あります。

1. **システム障害** ：DynamoDBへのアクセスが失敗する、AWS設定の初期化が失敗する
2. **ユーザー操作の失敗** ：パスワードを間違える、存在しないユーザーIDを入力する

この2種類を同じAlarmで扱うとどうなるか。一般ユーザーが日常的にパスワードを入力し間違えるたびにアラームが鳴ります。ノイズになってしまいます。

そのためAlarmを2種類に分けました。

**障害系（1回で発火）：**

```
- DynamoDB GetItemエラー
- AWS config load失敗
```

1回でも発生したらシステム障害の可能性があるため、即座に通知します。

**失敗頻度（まとめて発火）：**

```
- Login failed：1分間に10回以上（ベースライン計測後に更新）
```

通常の誤入力と不正アクセスを区別するために頻度で判断します。閾値は後述のベースライン計測で根拠を持って決めました。

この判断の根拠は「誰が、何のために操作するか」です。auth-handlerは一般ユーザーも使います。一般ユーザーはパスワードを間違えます。これを知らなければ、同じ閾値を全部のAlarmに適用してしまいます。

### 4-3. photo-handlerの設計判断

photo-handlerには、CloudWatch AlarmとDLQの両方が必要です。それぞれが検知できる失敗の種類が異なるからです。

**CloudWatch Alarm（Lambda Errors）：**  
Lambdaそのものが例外で終了したケースを検知します。

**メトリクスフィルター経由のAlarm：**  
Lambdaが正常終了したにもかかわらず、DynamoDB書き込みが失敗したケースを検知します。これが重要です。

前述のwrong-bucketのケースを思い出してください。Lambdaは `StatusCode: 200` で終了していますが、DynamoDBには何も書かれていません。Lambda Errorsメトリクスは上昇しません。このケースを検知するには、ERRORログを直接カウントするメトリクスフィルターが必要になります。

```
resource "aws_cloudwatch_log_metric_filter" "photo_error_filter" {
  name           = "photo-handler-error-filter"
  log_group_name = aws_cloudwatch_log_group.photo_logs.name
  pattern        = "[ERROR]"

  metric_transformation {
    name          = "PhotoHandlerErrorCount"
    namespace     = "GemiclawApp"
    value         = "1"
    default_value = "0"
  }
}
```

**DLQ：**  
S3イベント経由の非同期呼び出しが全リトライ（2回）を経ても失敗した場合、イベントをDLQに転送します。DLQ滞留数が1件以上になったらAlarmを発火させます。

LocalStackでの動作確認で記録しておきたいことがあります。DLQへのメッセージ転送は、 **リトライが完了した後（約2分後）に発生します** 。エラーログを見た直後にDLQ滞留数を確認しても0件になっています。この時間差を知っていないと、「DLQが動いていない」と誤判断してしまいます。実際に一度そう誤判断しました。

**DLQのTerraform設定：**

```
resource "aws_lambda_function" "photo_lambda" {
  # ...
  dead_letter_config {
    target_arn = aws_sqs_queue.photo_dlq.arn
  }
}
```

### 4-4. admin-update・admin-list-handlerの設計判断

admin-update-handlerとadmin-list-handlerは、管理者のみが操作します。操作内容も限定されています（ステータス変更・一覧取得のみ）。

この2つについては、全てのAlarmを「1回で発火」に設定しました。

理由は単純です。管理者操作でノイズになる「通常の失敗」が構造的に起きにくいためです。auth-handlerと違って不特定多数のユーザーが操作しません。DynamoDB Updateが失敗したなら、それはシステム障害か設計ミスです。

### 4-5. 「誰が、何のために操作するか」がAlarm設計を決める

auth-handlerとadmin-update-handlerでAlarm設計が異なります。その差を生んだのは「誰が、何のために操作するか」という情報です。

この情報はインフラ設計の段階ですでに存在しています。API Gatewayのエンドポイント設計、DynamoDBのテーブル設計、Lambdaの役割分担——これらを決める時点で「誰が使うか」は決まっています。

だからインフラ設計と監視設計は同時に行わなければなりません。後から監視を追加しようとすると、「誰が使うか」を思い出すところから始めることになります。実際、前回の記事では `main.tf` にAlarmは一切ありませんでした。今回、設計し直すにあたって最初にやったのは「このLambdaは誰が使うのか」を再確認することでした。

---

## 5\. 本番移行で初めて見えたもの - LocalStackとの差分

### 5-1. S3バケット名がグローバル名前空間で衝突した

`terraform apply` の最初のエラーはこれでした。

```
Error: creating S3 Bucket (my-photo-storage): BucketAlreadyExists:
The requested bucket name is not available.
```

S3のバケット名はAWSの全アカウントをまたいでグローバルに共有されます。LocalStackではアカウントが存在しないため、どんな名前でも通ります。本番では `my-photo-storage` という一般的な名前はすでに誰かが使っていました。

対応：アカウントIDを含む名前に変更しました。

```
bucket = "photo-storage-${data.aws_caller_identity.current.account_id}"
```

### 5-2. LocalStack固有設定の除去漏れが複数箇所に散在していた

`main.tf` からLocalStack固有設定を削除したつもりでした。しかしterraform applyが通って動作確認をしたとき、ログインは成功したものの、発行された署名付きURLがこうなっていました。

```
http://photo-storage-<アカウントID>.localhost:4566/uploads/aataka/1748000000.jpg?X-Amz-Algorithm=...
```

LocalStackを指したままです。

原因はGoコードの中にありました。auth-handlerの `src/lambda/auth/main.go` に、S3クライアントの初期化でLocalStack用のエンドポイントが残っていました。

```
// 削除前（問題のコード）
s3Client := s3.NewFromConfig(cfg, func(o *s3.Options) {
    o.BaseEndpoint = aws.String("http://localhost:4566")
})

// 修正後
s3Client := s3.NewFromConfig(cfg)
```

Terraform側の設定だけ見ていて、Goコードの中を確認していませんでした。 `grep -r "localhost\|4566" src/` で全検索するべきでした。これを本番移行前のチェックリストに加えることにしました。

フロントエンド（ `index.html` ）のBASE\_URLもLocalStackを指したままだったため、同様に修正しました。

### 5-3. nil panicが本番で初めて発生した（最重要）

これが今回の移行で最も重要な発見です。

本番でadmin-list-handlerを叩いたとき、Lambdaがpanicしました。エラーログ：

```
runtime error: interface conversion: types.AttributeValue is nil,
not *types.AttributeValueMemberS
```

原因はGoコードのこの行です：

```
PhotoID: item["PhotoID"].(*types.AttributeValueMemberS).Value,
UserID:  item["UserID"].(*types.AttributeValueMemberS).Value,
```

DynamoDBのレスポンスに含まれるAttributeValueがnilだった場合、この型アサーションがpanicします。

なぜLocalStackで発生しなかったのか。LocalStackでのテスト時、PhotoMetadataテーブルは空（0 records）でした。 `result.Items` のループが一度も回らないため、型アサーションが実行されませんでした。本番では、事前に投入したテストデータが存在したため、初めてループが回ってpanicしました。

「LocalStackで0 recordsだったnil panicが本番で初めて発生した」——これはLocalStackと本番の差分として記録しておく価値があります。LocalStackでの検証が「空のテーブルに対して処理する」ケースになりがちであることを示しています。

修正： `getStringValue` ヘルパー関数を追加し、nilチェックを2段階で行うよう修正しました。

```
func getStringValue(item map[string]types.AttributeValue, key string) string {
    if v, ok := item[key]; ok {
        if s, ok := v.(*types.AttributeValueMemberS); ok {
            return s.Value
        }
    }
    return ""
}
```

キーがmap内に存在するか（1段階目）、型アサーションが成功するか（2段階目）の2重チェックになっています。前記事のコードは型アサーションを1ステップで直接行っていたため、キー自体がmapに存在しない場合にpanicしました。

`getStringValue` への変更をレコード取得ループ全体に適用しました：

```
for _, item := range result.Items {
    photoID := getStringValue(item, "PhotoID")
    if photoID == "" {
        log.Printf("[WARN] Skipping record with missing PhotoID")
        continue
    }
    records = append(records, PhotoRecord{
        PhotoID: photoID,
        UserID:  getStringValue(item, "UserID"),
        Status:  getStringValue(item, "Status"),
    })
}
```

`Status` フィールドは前記事でも `ok` チェック付きで取得していましたが、 `PhotoID` と `UserID` は型アサーションを直接行っていました。本番で実データが入ったとき、これら2フィールドのループで初めてpanicが発生しました。

### 5-4. 本番移行トラブルの記録

| # | トラブル | 原因 | 対応 |
| --- | --- | --- | --- |
| 1 | S3バケット名衝突 | グローバル名前空間。LocalStackでは起きない | アカウントIDを含む名前に変更 |
| 2 | IAMポリシー連鎖失敗 | S3失敗→ポリシー→Lambda作成が連鎖失敗 | 2回目のapplyで解決 |
| 3 | 署名付きURLがlocalhost:4566 | GoコードのS3エンドポイント設定が残存 | `s3.NewFromConfig(cfg)` のみに修正 |
| 4 | フロントエンドがlocalhost:4566に接続 | index.htmlのBASE\_URLがLocalStackのまま | 本番API GatewayのURLに変更 |
| 5 | nil panicが本番で初めて発生 | LocalStackでは0 recordsだったため未発生 | `getStringValue` ヘルパー追加 |

---

## 6\. Alarmが機能しなかった話 - 設計ミスの発見と修正

### 6-1. auth-login-failed-rateが発火しなかった

Alarmを設定してから、実際に発火するか確認しました。auth-handlerに対して、不正なパスワードで12回ログイン試行しました。

Alarmは発火しませんでした。

15回試しました。発火しませんでした。

原因を調べると、AlarmがLambda Errorsメトリクスを参照していました。

```
# 問題のAlarm設定
metric_name = "Errors"
namespace   = "AWS/Lambda"
```

ログイン失敗は、Lambdaとして正常終了します。 `[WARN] Login failed - invalid password` というログを出して200を返します。Errorsメトリクスは上昇しません。

これはAlarm設計のミスでした。「ログイン失敗を検知したい」のに「Lambdaのエラーを検知する」Alarmを設定していました。

修正：auth-handler用のメトリクスフィルターを追加し、 `[WARN] Login failed` ログをカウントするカスタムメトリクス（ `AuthLoginFailedCount` ）を作りました。AlarmのNamespaceを `GemiclawApp` に変更しました。

```
resource "aws_cloudwatch_log_metric_filter" "auth_login_failed_filter" {
  name           = "auth-login-failed-filter"
  log_group_name = aws_cloudwatch_log_group.auth_logs.name
  pattern        = "Login failed"

  metric_transformation {
    name          = "AuthLoginFailedCount"
    namespace     = "GemiclawApp"
    value         = "1"
    default_value = "0"
  }
}
```

修正後、15回ログイン試行したところ、 `auth-login-failed-rate` AlarmがALARMに遷移しました。SNSメール通知も届きました。

この失敗から気づいたこと： **「何を検知したいか」と「どのメトリクスを参照するか」は別の問いです。** 最初に「何を検知したいか」を決め、そのメトリクスが標準で存在するか確認し、なければメトリクスフィルターで作る、という順番で設計しなければなりませんでした。

### 6-2. X-Rayがトレースを送信していなかった

Alarmの確認を終えてX-Rayの確認をしようとしたとき、AWSコンソールのトレースマップに「サービスがありません」と表示されました。

CLIで確認：

```
aws xray get-trace-summaries \
  --start-time $(date -d '1 hour ago' +%s) \
  --end-time $(date +%s)
```

空配列が返ってきました。Lambda設定を確認すると `Mode: Active` になっています。なのにトレースデータが存在しません。

原因：IAMロール `lambda_common_role` にX-Ray権限がありませんでした。

```
# main.tfのIAMポリシーに追加
"xray:PutTraceSegments",
"xray:PutTelemetryRecords"
```

`tracing_config { mode = "Active" }` を設定するだけでは不十分で、LambdaのIAMロールにX-Rayへの書き込み権限が必要です。

修正後、トレースマップにAPI Gateway→auth-handlerの流れが表示されるようになりました。

補足：今回の構成では、DynamoDBが別ノードとして表示されませんでした。GoのAWS SDKで `aws-xray-sdk-go` を使っていないため、DynamoDBへのリクエストにX-Rayサブセグメントが付与されません。Lambda→DynamoDBのレイテンシを可視化するには `aws-xray-sdk-go` の導入が必要です。今回は実装していないため、記録として残しておきます。

### 6-3. AWS config load失敗Alarmを発火確認できなかった

auth-handler用に `auth-config-load-error` Alarmを設定しました。発火確認をしようとしたとき、「config loadが失敗する状況」を再現できないことに気づきました。

Goコードを確認すると、全4関数で `config.WithRegion("ap-northeast-1")` がハードコードされています。 `config.LoadDefaultConfig` はリージョンが環境変数から取れなくても、ハードコードした値でfallbackするため、通常の検証環境では失敗しません。

このAlarmが発火するのはAWSインフラ自体の障害レベルの場合のみです。

Alarmの定義自体はmain.tfに実装しています：

```
resource "aws_cloudwatch_log_metric_filter" "auth_config_load_error_filter" {
  name           = "auth-config-load-error-filter"
  log_group_name = aws_cloudwatch_log_group.auth_logs.name
  pattern        = "AWS config load failed"
  metric_transformation {
    name          = "AuthConfigLoadErrorCount"
    namespace     = "GemiclawApp"
    value         = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "auth_config_load_error" {
  alarm_name          = "auth-config-load-error"
  alarm_description   = "auth-handler: AWS config load失敗（システム障害）"
  namespace           = "GemiclawApp"
  metric_name         = "AuthConfigLoadErrorCount"
  statistic           = "Sum"
  period              = 60
  evaluation_periods  = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
}
```

判断：修正しないことにしました。ただし記録として残します。 **Alarmの設計は監視設計とコード設計が切り離せないことを示しています。** 今後、コードのリファクタリングでリージョンをハードコードから環境変数に変更する際は、このAlarmの発火確認を同時に行う必要があります。

### 6-4. auth-config-load-errorの実装漏れ

全Alarmの最終確認をしたとき、設計では9件のはずがmain.tfに8件しかありませんでした。 `auth-config-load-error` AlarmとそのメトリクスフィルターがTerraformに未実装でした。

気づいた経緯は単純です。最終確認でAlarmの件数を数えたところ8件だったため、設計書と照合して発覚しました。数を数えるという作業をしなければ気づきませんでした。実際のmain.tfでは、このAlarmはファイル末尾に後から追記する形になっています——最初から設計に組み込めていれば、こうはなっていなかったと思います。最終確認で数を数えることをチェックリストに追加しました。

---

## 7\. 「正常を定義する」の実測 - ベースラインと更新プロセス

### 7-1. 実測値

運用テストとして、各関数を複数回実行してDurationを計測しました。

**Cold Start（関数が一定時間未実行の状態から起動）：**

| 関数 | Duration | Init Duration |
| --- | --- | --- |
| auth-handler | 1695〜1987ms | 119〜123ms |
| photo-handler | 1566ms | 114ms |
| admin-list-handler | 1549〜1594ms | 90〜114ms |
| admin-update-handler | 1653ms | 110ms |

**Warm Start（直近に実行済みの状態から起動）：**

| 関数 | Duration |
| --- | --- |
| auth-handler | 29〜57ms |
| photo-handler | 24〜41ms |
| admin-list-handler | 31〜114ms |
| admin-update-handler | 27〜125ms |

Goのバイナリは軽量で、Cold Startでも2秒以内に収まりました。Warm StartはDynamoDB通信込みで最大114msでした。

なお、REPORTログに `XRAY TraceId` と `Sampled: true` が記録されていることを確認しました。X-Rayが本番で自動的にサンプリングしていることをここで初めて知りました。LocalStackでは確認できなかった情報です。

### 7-2. しきい値の更新プロセス

最初に設定したしきい値は仮の値でした。

```
photo-duration-high：20000ms（仮）
auth-login-failed-rate：1分・5中3回（仮）
```

ベースライン計測後、根拠のある値に更新しました。

**photo-duration-high：20000ms → 500ms**

Warm Startの実測値が最大41msでした。Cold Startでも最大1987msです。20000msというしきい値は「何も考えていない値」でした。実測値から「1000ms以上かかったら異常」と判断して500msに設定しました（Warm Startの10倍以上）。

**auth-login-failed-rate：1分・5中3回 → 1分間に10回以上**

ログイン失敗の頻度を計測しました。通常の誤入力（1秒間隔で手入力）では1分間に5〜10回程度になります。10回/分を超えたら不正アクセスの可能性があると判断しました。

**「仮で設定→計測→更新」がなぜ正しい手順か：**

しきい値を最初から正確に決めることはできません。根拠となる実測値がないからです。「仮の値でAlarmを動かし、正常な状態を観察し、その観察から根拠を得て更新する」——これが正しい手順だと感じています。

Practical Monitoring（Mike Julian著）にも「アラートのしきい値は時間をかけて調整するものだ」と明記されています。最初から完璧なしきい値を決めようとするのは、正常を定義する前にAlarmを設定しようとすることと同じ誤りです。

---

## 8\. X-RayとDashboard - 「見つける」から「組み立てる」へ

### 8-1. X-Rayが変えること

オンプレでの障害特定はこうでした。

`/var/log/messages` を開きます。時刻を絞り込みます。 `grep` でキーワードを探します。関連するログを見つけたら別のログファイルを開きます。複数のサーバーをまたぐ場合は、それぞれのログを別々に開いて、タイムスタンプで突き合わせます。「見つける」作業です。

X-Rayはこうです。

API GatewayがリクエストをLambdaに渡し、LambdaがDynamoDBにアクセスした一連の処理が、1本のトレースとして組み立てられた状態で見えます。どこでどれだけ時間がかかったか、エラーがどの段階で発生したかが、視覚的に構造化されています。「組み立てる」作業が、すでに終わっています。

これが「見つける」から「組み立てる」へのシフトです。

### 8-2. 障害対応フロー

X-RayはAlarmが発火した後に使うツールです。

```
① 正常を定義する（Alarm設計）
　↓
② Alarmが発火する（SNSメール通知）
　↓
③ ログで「何が起きたか」を確認する（CloudWatch Logs）
　↓
④ X-Rayで「どこで起きたか」を特定する（トレースマップ）
```

①がなければ②は起きません。②がなければ気づけません。③がなければ原因がわかりません。④がなければ複数サービスをまたぐ問題の特定に時間がかかります。

X-Rayは「正常定義の道具」ではなく「障害特定の道具」です。最初から混同していましたが、この順番を理解してから設計が整理されました。

### 8-3. Dashboard

CloudWatch Dashboard（gemiclaw-ops）を作成しました。以下のウィジェットを配置しています。

- Lambda Errors（4関数）
- Lambda Duration（4関数）
- DLQ滞留数（photo-handler-dlq）
- photo-handler ERRORログ数（メトリクスフィルター経由）
- Alarmウィジェット（9件の状態を一覧表示）

Alarm発火状態でDashboardを開いたとき、 `photo-dlq-messages` Alarmウィジェットが赤くなっていることを確認しました。Lambda Errorsグラフにphoto-handlerのエラースパイクが、Lambda Durationグラフに2秒超のCold Startスパイクが表示されていました。

「障害時に最初に開く画面」として機能しています。

---

## 9\. まとめ - インフラ設計と監視設計は同時に行わなければならない

この記事で伝えたかったことをもう一度書きます。

> AWS運用監視設計において最初の、かつ最も重要な判断は、アラームを設定することではなく、 **正常を定義することだった** 。そしてその定義は、 **インフラ設計と同時に行わなければ機能しない** 。

前回の記事でLocalStack上のシステムを構築したとき、main.tfにAlarmは一切ありませんでした。監視設計は「後でやること」でした。

今回の作業を振り返ると、もしLocalStack段階で正常を定義していたら、以下が変わっていたはずです。

- **DLQ設定がmain.tfに最初から含まれていた** ——photo-handlerが非同期であることはインフラ設計の時点でわかっていました
- **ログ設計が実装と同時に決まっていた** ——「何を `log.Printf` で出力するか」はAlarm設計があって初めて具体化できます
- **auth-handlerのAlarm設計がメトリクスフィルター前提になっていた** ——Lambdaのロール（一般ユーザーが使う）をインフラ設計の時点で知っていました

監視は後から追加するものではなく、インフラと同時に設計するものです。この発見は、オンプレ8年で監視ツールを使ってこなかったからこそ気づけた視点だと思っています。「監視設計を知らなかった」が強みになった唯一の瞬間かもしれません。

### 既知の課題

以下は今回の実装の限界として正直に記録しておきます。

- **Cognito未導入** ：現在の認証はDynamoDBに平文パスワードを保存しています。本番品質には程遠い状態です
- **Secrets Manager未使用** ：DBの接続情報管理が未整備です
- **X-RayでDynamoDBサブセグメントが見えない** ： `aws-xray-sdk-go` の導入が必要です
- **auth-config-load-error Alarmの発火確認未実施** ：Goコードのリージョンハードコードにより再現できませんでした
- **tfstateのローカル管理** ：本番品質にするにはS3バックエンドへの移行が必要です。今回はスコープ外としました

---

## 付録

### A. オンプレ→AWS監視対応表（完成版）

| オンプレの確認行動 | 判断の所在 | AWSの対応物 | 備考 |
| --- | --- | --- | --- |
| pingが通るか | OSが自動で応答 | CloudWatch Alarm（Lambda Errors） | Lambdaは「起動できたか」で判断します |
| プロセスが生きているか | OSが管理 | Lambda Invocations / Errors | 実行回数が0ならイベントが来ていません |
| ログで死因を特定 | 先輩の経験知 | CloudWatch Logs（要 `log.Printf` ） | 書かなければ何も残りません |
| syslogで時系列追跡 | ツールが自動収集 | CloudWatch Logs Insights | クエリを事前に設計しておく必要があります |
| エラーが既知か未知か | 現場の暗黙知 | CloudWatch Alarmのしきい値定義 | 自分で明文化しなければ動きません |
| クリティカルか無視か | 先輩・案件ごと | SNS通知先・Alarmアクション | 同上 |
| 過去の障害パターン | 先輩の頭の中 | CloudWatch Logsの蓄積 | 保持期間を設定しないと無期限課金になります |
| 非同期処理の失敗検知 | **オンプレに概念なし** | DLQ滞留数のAlarm | S3イベント駆動の処理には必須です |

### B. Alarm設計の最終確定値（9件）

| Alarm名 | メトリクス | Namespace | 閾値 | 根拠 |
| --- | --- | --- | --- | --- |
| auth-config-load-error | AuthConfigLoadErrorCount | GemiclawApp | 1 | システム障害 |
| auth-dynamodb-error | Errors | AWS/Lambda | 1 | システム障害 |
| auth-login-failed-rate | AuthLoginFailedCount | GemiclawApp | 10/分 | ベースライン計測 |
| photo-dlq-messages | ApproximateNumberOfMessagesVisible | AWS/SQS | 1 | 失敗イベント検知 |
| photo-duration-high | Duration | AWS/Lambda | 500ms | ベースライン計測 |
| photo-error-log-alarm | PhotoHandlerErrorCount | GemiclawApp | 1 | Lambda正常終了でも失敗検知 |
| photo-lambda-errors | Errors | AWS/Lambda | 1 | 非同期で誰も気づかない |
| admin-update-errors | Errors | AWS/Lambda | 1 | 管理者操作の失敗 |
| admin-list-errors | Errors | AWS/Lambda | 1 | 管理画面の障害 |

### C. 記事で言及した発見の一覧

| # | 発見 | フェーズ |
| --- | --- | --- |
| 1 | ログは書かないと残らない | Phase 1 |
| 2 | 成功と失敗がログ上で区別できない（修正前） | Phase 1 |
| 3 | 非同期処理の失敗検知はオンプレに概念がない | Phase 1 |
| 4 | エラーの判断基準は自分で明文化しなければならない | Phase 1 |
| 5 | DLQへの転送はリトライ完了後（約2分後）に発生する | Phase 1 |
| 6 | 「誰が、何のために操作するか」を知らないとAlarmの閾値は決められない | Phase 2準備 |
| 7 | terraform applyは手動変更を上書きする | Phase 2 |
| 8 | ログ保管期間の設定もインフラ設計と同時に行わなければならない | Phase 3 |
| 9 | LocalStack固有設定の除去漏れは複数箇所に散在する | Phase 2 |
| 10 | S3バケット名はグローバル名前空間で共有される | Phase 2 |
| 11 | LocalStackで0 recordsだったnil panicが本番で初めて発生した | Phase 2 |
| 12 | Alarmのしきい値は実測値なしには決められない | Phase 4 |
| 13 | Alarm設計ミス：ログイン失敗をLambda Errorsで検知しようとしていた | Phase 4 |
| 14 | X-Rayに `tracing_config` だけでなくIAM権限が必要 | Phase 4 |
| 15 | 監視設計とコード設計は切り離せない | Phase 4 |
| 16 | Alarmの実装漏れは最終確認で数を数えないと気づかない | Phase 4 |

### D. 参考資料

- [Practical Monitoring（Mike Julian著・O'Reilly）](https://www.oreilly.com/library/view/practical-monitoring/9781491957349/)
- [Site Reliability Engineering（Google SRE Book）](https://sre.google/sre-book/table-of-contents/)
- [AWS Well-Architected Framework - Operational Excellence Pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
- [前回記事：元オンプレ屋が疑似AWS環境のログをGemiclawに確認してもらうまで](https://zenn.dev/aa_taka/articles/c5e67c212e4a40)
- [GitHubリポジトリ：Aataka/gemiclaw-cloud](https://github.com/Aataka/gemiclaw-cloud)

7

5