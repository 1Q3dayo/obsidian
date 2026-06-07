---
title: "Terraformプロジェクトのオンボーディングコストをmise + aquaで削減した話"
source: "https://zenn.dev/leaner_dev/articles/e8297dcffcd38c"
author:
published: 2026-06-03
created: 2026-06-07
description:
tags:
  - "clippings"
  - "raw"
---
12

2[AWS](https://zenn.dev/topics/aws)

[

Terraform

](https://zenn.dev/topics/terraform)[

Datadog

](https://zenn.dev/topics/datadog)[

aqua

](https://zenn.dev/topics/aqua)[

mise

](https://zenn.dev/topics/mise)[

tech

](https://zenn.dev/tech-or-idea)

## はじめに

リーナーテクノロジーズ技術基盤部の [@mizukmb](https://x.com/mizukmb) です。

弊社ではAWSをはじめ、DatadogなどのSaaSの構成管理にTerraformを採用しています。また、Terraformやtflint等のローカル開発・CI/CD環境で必要なCLIのバージョン管理にaquaを採用しています。

<iframe src="https://embed.zenn.studio/card#zenn-embedded__cffa8a6fa1982" frameborder="0" height="122"></iframe>

aquaの導入により、初期の環境構築が簡単になるだけでなく、CI/CD環境とローカル環境のCLIのバージョンを揃える事ができるため非常に便利なツールと感じています。

しかし、 `terraform plan` を実行するためには、awsやdatadog等のproviderに渡す認証情報が必要になってきます。例えば以下のようなものです

- AWSのプロファイル情報 (マルチアカウント運用の場合)
- Datadog App Key等の認証情報

これらは開発メンバー各自のローカルPC内に設定する必要があり、人によって微妙に設定が異なる場合があります。 `terraform plan` が動かない等のトラブルが発生する事もあるため、各自の環境の差異はなるべく無くしたいと思っています。

今回はこちらの実現のため、簡単に `terraform plan` を実行できるための環境作りを目指しました。

## miseを使ってaquaの実行環境を整える

<iframe src="https://embed.zenn.studio/card#zenn-embedded__31df34141e27a" frameborder="0" height="122"></iframe>

miseは開発環境用にプログラミング言語やCLI等のバージョン管理ができるツールです。 aqua自身のバージョン管理をmiseに任せる事で、 `mise install` でaqua自身をインストールする事が可能になります。

mise.tomlに以下のように記述します。

```
[tools]
aqua = "2.59.1"
```

この状態で `mise install` を実行すると指定されたバージョンのaquaをインストールする事ができます。しかしながら、これだけではaquaが管理するツールを利用する事はできません。まず、 `aqua install` を実行しなければなりませんし、aqua専用のPATHを通す必要もあります。

miseはツールのバージョン管理だけでなく、プロジェクト内の環境変数の追加やHooksによる特定コマンドの実行などを定義する事ができます。

<iframe src="https://embed.zenn.studio/card#zenn-embedded__49ece16f92401" frameborder="0" height="122"></iframe>

<iframe src="https://embed.zenn.studio/card#zenn-embedded__3a88da857667e" frameborder="0" height="122"></iframe>

そこで、これらを使って上記問題を解決します。

### Hooks

まず、 `aqua install` の未実行問題ですが、Hooks機能を使います。hookの条件はいくつか書けるのですが、今回は `mise install` の実行後に `aqua install` を実行してほしいので、 `postinstall` を使います。

<iframe src="https://embed.zenn.studio/card#zenn-embedded__c7101f68e83a7" frameborder="0" height="122"></iframe>

mise.tomlに以下のように書くと、 `mise install` の後に自動的に `aqua install -l` が走るようになります。

```
[hooks]
# mise install で aqua がインストールされた直後に aqua.yaml のツールも揃える。
postinstall = "aqua install -l"
```

この時の `-l` オプションですが、これはツールのシンボリックリンクを追加するのみにとどめるためのオプションになっています。aquaは遅延インストールを採用しているため、 `aqua install -l` コマンドの実行は早く終わらせて、各種CLIを初めて呼び出したタイミングでダウンロード・インストールが実行しておくといった動きになります。必要になるまではダウンロードしないという動きになるため、初期の環境構築の時短になります。

<iframe src="https://embed.zenn.studio/card#zenn-embedded__e602d23734d24" frameborder="0" height="122"></iframe>

### Environments

aqua用のPATHを通す作業は、本来であれば各自のシェル設定ファイル ( `.bashrc` など) で設定を追記するように [aqua公式ドキュメントでも案内されています](https://aquaproj.github.io/docs/install/#2-set-the-environment-variable-path) が、各自のローカル環境でPATHを通した・通してない問題が発生してしまいます。そこで、Environments機能を活用します。

```
[env]
# aqua install したツールに PATH を通す。aqua のデフォルト配置を前提とする（macOS/Linux）。
_.path = ["~/.local/share/aquaproj-aqua/bin"]
```

これにより、ローカル環境の `~/.bashrc` などを編集する事なくPATHを通す作業が完了し、aqua管理のツールを利用する事ができるようになります。

ちなみに `aqua root-dir` コマンドを使ってPATHを出力する方法もありますが、aqua未インストールのタイミングで評価されてしまうためこの方法は採用できませんでした。そのため、一旦aquaのPATHは決め打ちで記載しています。

## 環境変数 AWS\_CONFIG\_FILE で AWS profileを統一管理する

AWSのプロファイル情報を統一するために、環境変数 `AWS_CONFIG_FILE` を活用します。こちらはaws profile設定ファイルの読み込み場所を指定する事ができる環境変数です。プロファイル情報を読み込む設定ファイルのデフォルトパスは `~/.aws/config` ですが、この環境変数を使う事でTerraformプロジェクト内で管理している設定ファイルを指定する事ができ、profile名を統一する事ができます。

<iframe src="https://embed.zenn.studio/card#zenn-embedded__1f63887ce2ab2" frameborder="0" height="122"></iframe>

この環境変数はmise.tomlで設定します。

```
[env]
# AWS CLI の profile 定義をこのリポジトリ配下に閉じ込める。
# .aws/config を編集してもユーザーの ~/.aws/config には影響しない。
AWS_CONFIG_FILE = "{{config_root}}/.aws/config"
```

`/path/to/project-root/.aws/config` ファイルを用意して、AWSプロファイル情報を記載しておけば、Terraformプロジェクト内ではこちらを優先して読み込むため、AWSのプロファイル情報を統一する事が可能になります。

## 秘匿情報をTerraform ephemeralブロックで管理する

awsプロバイダーは上記の設定ファイル+ローカル環境での `aws sso login` で認証情報を取得できますが、DatadogのようにAPI Keyが必要なプロバイダーもあります。

このような場合はTerraform ephemeralブロックを活用する事でローカルにAPI Keyを管理する事なく `terraform plan` ができるようになります。

<iframe src="https://embed.zenn.studio/card#zenn-embedded__c92cd4609be53" frameborder="0" height="122"></iframe>

弊社の場合、AWS SSM ParameterにAPI Keyを置き、ephemeralブロックを経由してdatadog providerにAPI Keyを渡すといった実装をしています。ephemeralブロックはtfstateにその値を記録せずに扱う事ができるためセキュアな運用が可能になります。

```
provider "aws" {
  region  = "ap-northeast-1"
  profile = "example"
}

ephemeral "aws_ssm_parameter" "datadog_api_key" {
  arn = "arn:aws:ssm:ap-northeast-1:123456789012:parameter/terraform_project/datadog/api_key"
}

ephemeral "aws_ssm_parameter" "datadog_app_key" {
  arn = "arn:aws:ssm:ap-northeast-1:123456789012:parameter/terraform_project/datadog/app_key"
}

provider "datadog" {
  api_key = ephemeral.aws_ssm_parameter.datadog_api_key.value
  app_key = ephemeral.aws_ssm_parameter.datadog_app_key.value
}
```

## 改善策の導入前後における環境構築作業の変化

miseの導入と、miseのHooks, Environemnts機能、Terraform ephemeralブロックの導入によって必要な手順がシンプルになりました。

### 導入前

1. aquaが必要なので各自でインストールする
2. aqua用のPATHを通すために `~/.bashrc` などの設定ファイルを編集する
3. `aqua install` を実行する
4. (aws providerの場合) Plan用のprofileを `~/.aws/config` に記載する
5. (datadog providerの場合) api key, app keyをローカルPCに持ってきて環境変数に追加する
6. `terraform init` や `terraform plan` が動作する状態になる

### 導入後

1. miseが必要なので各自でインストールする
2. `mise trust && mise install` を実行する
	- miseのpostinstall hookが起動して `aqua install -l` が自動的に走る
3. `terraform init` や `terraform plan` が動作する状態になる
	- これまで必要だったaws profileやdatadog provider用のapi keyやapp keyは既に設定が完了済

## まとめ

`mise install` 一発でTerraformの開発環境が整う方法について共有しました。

オンボーディングコストを削減できただけでなく、API Key等の機密情報をローカルに保存する必要が無くなるといったセキュリティ面でのメリットもありました。皆様のご参考になれば幸いです。

## おまけ：最終成果物

### aqua.yaml

```
registries:
  - type: standard
    ref: v4.511.0
packages:
  - name: hashicorp/terraform@v1.15.3
  - name: terraform-linters/tflint@v0.58.0
```

### mise.toml

```
[tools]
aqua = "2.59.1"

[env]
# AWS CLI の profile 定義をこのリポジトリ配下に閉じ込める。
# .aws/config を編集してもユーザーの ~/.aws/config には影響しない。
AWS_CONFIG_FILE = "{{config_root}}/.aws/config"
# aqua install したツールに PATH を通す。aqua のデフォルト配置を前提とする（macOS/Linux）。
_.path = ["~/.local/share/aquaproj-aqua/bin"]

[hooks]
# mise install で aqua がインストールされた直後に aqua.yaml のツールも揃える。
postinstall = "aqua install -l"
```

### datadog/terraform.tf

```
provider "aws" {
  region  = "ap-northeast-1"
  profile = "example"
}

ephemeral "aws_ssm_parameter" "datadog_api_key" {
  arn = "arn:aws:ssm:ap-northeast-1:123456789012:parameter/terraform_project/datadog/api_key"
}

ephemeral "aws_ssm_parameter" "datadog_app_key" {
  arn = "arn:aws:ssm:ap-northeast-1:123456789012:parameter/terraform_project/datadog/app_key"
}

provider "datadog" {
  api_key = ephemeral.aws_ssm_parameter.datadog_api_key.value
  app_key = ephemeral.aws_ssm_parameter.datadog_app_key.value
}
```

12

2