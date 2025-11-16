---
title: "Findyの爆速インフラ構築を支えるTerraform活用術 〜Terraform Test導入編〜"
source: "https://tech.findy.co.jp/entry/2025/08/29/070000"
author:
  - "[[kouzyun]]"
  - "[[たかぼー (id:Taka_bow)]]"
  - "[[starfish719]]"
  - "[[ひらき (id:h-piiice16)]]"
  - "[[Shun (id:ShunDeveloper)]]"
  - "[[rokumura7]]"
  - "[[chida (id:t-chida0909)]]"
  - "[[たがしらけいすけ (id:tagasyksk)]]"
  - "[[shoota-dev]]"
  - "[[ham (id:hamchance0215)]]"
published: 2025-08-29
created: 2025-11-17
description: "はじめに こんにちは。CTO室 Platform開発チーム SREの原(@kouzyunJa)です。 ファインディでは日々サービスが爆速で開発されており、新しいプロダクトも次々と生まれています。それらのインフラ構築を、私たちのチームが支えています。 インフラ構築にもスピード感が求められるため、効率的かつ安全に進める仕組みが欠かせません。 今回は、そのスピード感あるインフラ構築を支えるTerraform Testの取り組みについてご紹介します。 はじめに Terraform Testの導入背景 Terraform Testの書き方紹介 UnitテストとIntegrationテスト ディレクトリ構…"
tags:
  - "clippings"
  - raw

---
## はじめに

こんにちは。CTO室 Platform開発チーム SREの原([@kouzyunJa](https://x.com/kouzyunJa))です。

ファインディでは日々サービスが爆速で開発されており、新しいプロダクトも次々と生まれています。それらのインフラ構築を、私たちのチームが支えています。

インフラ構築にもスピード感が求められるため、効率的かつ安全に進める仕組みが欠かせません。

今回は、そのスピード感あるインフラ構築を支えるTerraform Testの取り組みについてご紹介します。

## Terraform Testの導入背景

[developer.hashicorp.com](https://developer.hashicorp.com/terraform/language/tests)

Terraform TestはTerraform 公式のテストフレームワークで、Terraform v1.6.0から利用可能です。

モジュール更新による破壊的変更を事前に検証でき、テストは新規にリソースが構築され、その後自動的に削除されます。既存のインフラ環境やstateへの影響はありません。

弊社ではIaCとしてTerraformを導入しており、HCP Terraformにてstateの情報を管理しています。

スピード感のあるインフラ構築を実現するため、ファインディのプロダクトでよく利用するリソースをモジュール化しています。

これらのモジュールを、私たちは「汎用モジュール」と呼んでいます。

AWSの新規インフラ環境構築時にはこの汎用モジュールを活用する取り組みを推進しています。

しかし、汎用モジュールから環境を構築する際にTerraform Planは通るものの、Terraform Applyで失敗するケースがあり、その結果、構築スピードが低下するという課題がありました。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/k/kouzyun/20250826/20250826141618.png)

この課題を解決するため、Terraform Testを導入しました。

## Terraform Testの書き方紹介

Terraform Test は専用のテストファイルに記述します。`.tftest.hcl` または`.tftest.json` の拡張子のファイルにテストコードを記載していきます。

イメージが付きやすいように、S3バケットを構築するシンプルな例を使って説明します。

```tf
# main.tf

provider "aws" {
    region = "ap-northeast-1"
}

variable "bucket_prefix" {
  type = string
}

resource "aws_s3_bucket" "example" {
  bucket = "${var.bucket_prefix}-bucket"
}
```

このS3バケットの名前が想定通りで構築されているかのテストを書いてみますと次のようになります。

```tf
# main.tftest.hcl

variables {
  bucket_prefix = "test"
}

run "valid_string_concat" {
  command = plan

  assert {
    condition     = aws_s3_bucket.bucket.bucket == "test-bucket"
    error_message = "S3 bucket name did not match expected"
  }
}
```

runブロック内でテストを記述しており、assertで条件式を定義し、期待する値と一致するかを検証します。

このように作成するリソースの値が正常に設定されているかを確認できます。

### UnitテストとIntegrationテスト

ファインディではTerraform Testにおいて、独自にUnitテストとIntegrationテストの2種類のテストカテゴリを設けています。

- Unitテスト: Terraform Planに相当し、リソースを作らず論理的に検証する
- Integrationテスト: 実際にリソースをApplyして作成し検証、その後は自動的にリソースのDestroy行われる

この2つを組み合わせることで、インフラ環境のテストを行っています。

使い分けはrunブロック内のcommandの指定によって決まります。

- `command = plan` を指定すればUnitテストを実行する
- `command = apply` を指定すればIntegrationテストを実行する

よって、さきほどの例は `command = plan` を指定しているのでunitテストとしています。Integrationテストでも、assertでの値の確認は同様に行うことができます。

### ディレクトリ構成

テストのコードは、各モジュール配下のtestsディレクトリに配置しています。

UnitテストとIntegrationテストをディレクトリで分けており、対象のテストだけを個別に実行できます。

```
# Terraform モジュール と テスト構成例
modules/
  <module-name>/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── tests/
        ├── unit/
        │   └── main.tftest.hcl
        └── integration/
            └── main.tftest.hcl
```

テストを実施したい場合は、 `terraform test` コマンドを使用します。

また、 `-test-directory` オプションを指定することで、Unitテスト用のディレクトリや Integrationテスト用のディレクトリを切り替えて実行できます。

```bash
$ terraform test -test-directory=./tests/unit
```

実行結果は次のように表示されます。

runブロックごとにテスト名と結果が表示され、成功(pass)か失敗(fail)かを確認できます。

```
tests/unit/main.tftest.hcl... in progress
  run "test1"... pass
  run "test2"... pass
  run "test3"... pass
  run "test4"... pass
  run "test5"... pass
tests/unit/main.tftest.hcl... tearing down
tests/unit/main.tftest.hcl... pass

Success! 5 passed, 0 failed
```

### mock providorとUnitテスト

Unitテストではcommand = planを利用して実リソースを作らず論理的に検証します。

テストを行うモジュールの外部にあるリソース情報(例: 既存のIAM RoleのARNや、外モジュールのS3バケットのARN)を参照する場合、 mock providerを活用すると、外部リソースを実際に参照せずにテストを実行できます。

```tf
# main.tftest.hcl

mock_provider "aws" {
  mock_data "aws_iam_role" {
    defaults = {
      arn = "arn:aws:iam::111122223333:role/mock-role"
    }
  }
}

run "check_role_arn" {
  command = plan

  assert {
    condition     = data.aws_iam_role.example.arn == "arn:aws:iam::111122223333:role/mock-role"
    error_message = "IAM Role ARN does not match expected value"
  }
}
```

このようにmock providorを活用することで、モジュール外部のリソースを実際に参照せずともUnitテストを行うことができます。

### 複数モジュールを組み合わせたIntegrationテスト

ファインディでは汎用モジュールを「Network」「Container」など機能単位でモジュールを分けて作成しています。

このため、例えばContainerモジュールを単体でIntegrationテストしようとしても、Networkモジュールで作成しているVPCやSubnetが存在しないためApplyに失敗します。

そこで依存するNetworkモジュールを先にApply → その出力値をContainerモジュールに渡す、という流れを取り入れました。

これにより、依存関係を含めた最小構成を再現しながら Integrationテストを実行できます。

```tf
# main.tftest.hcl

run "network_module_apply" {
  command = apply

  # Call the Network module
  module {
    source = "./../../../network"
  }

  variables {
    vpc_cidr_block = "XX.XX.XX.XX/XX"

    subnet_public_1a_cidr_block = "XX.XX.XX.XX/XX"
    subnet_public_1c_cidr_block = "XX.XX.XX.XX/XX"
    subnet_public_1d_cidr_block = "XX.XX.XX.XX/XX"

    subnet_private_1a_cidr_block = "XX.XX.XX.XX/XX"
    subnet_private_1c_cidr_block = "XX.XX.XX.XX/XX"
    subnet_private_1d_cidr_block = "XX.XX.XX.XX/XX"
  }
}

run "container_module_apply" {
  command = apply

  # Call the container module
  module {
    source = "./../../../container"
  }

  variables {
    vpc_id = run.network_module_apply.vpc_id
    private_subnets = [
      run.network_module_apply.subnet_private_1a_id,
      run.network_module_apply.subnet_private_1c_id,
      run.network_module_apply.subnet_private_1d_id
    ]
    public_subnets = [
      run.network_module_apply.subnet_public_1a_id,
      run.network_module_apply.subnet_public_1c_id,
      run.network_module_apply.subnet_public_1d_id
    ]
  }
}
```

## CIワークフローでの活用

ここからはGitHub ActionsのCIに組み込んだTerraform Test活用方法について紹介します。

Terraform TestはCI ワークフローに組み込んで自動実行しています。

CIに組み込む際のポイントとしてUnitテストとIntegrationテストは使い分けています。

- Unitテスト: PR作成時に実行
- Integrationテスト: Mainブランチへマージ後、HCP Terraformへリリースする前に実行

使い分けている理由として、Integrationテストはリソースの構築から削除までを伴うため、完了まで時間がかかります。

例えばAuroraの場合、構築から削除完了まで長時間のテストを待つ必要があり、PRのレビュー速度に影響するため、マージ後に実行する設計としています。

Unitテストは論理的に検証するため、PR作成時に実行してスピーディーな確認ができます。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/k/kouzyun/20250821/20250821145525.png)

サンプルコードは次のようになります。

```
name: PR - Terraform Test (Unit)

on:
  pull_request:
    paths:
      - "**.tf"
      - "**.hcl"

jobs:
  unit-tests:
    runs-on: ubuntu-XX.XX

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: X.XX

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-region: ap-northeast-1
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          role-duration-seconds: 1200

      - name: Terraform init
        run: terraform init

      - name: Terraform validate
        run: terraform validate -no-color

      - name: Terraform test (unit)
        run: terraform test -test-directory=tests/unit
```

PRのUnitテストで問題ないと判断したら、mainブランチへマージを行いIntegrationテストを実行します。

AWSのSandbox環境で `apply → assert → destroy` を行い、リソースがApplyに失敗せず正しく作成できるかを検証します。

Integrationテストがパスされれば汎用モジュールのstateを管理しているHCP Terraformへリリースされます。

![](https://cdn-ak.f.st-hatena.com/images/fotolife/k/kouzyun/20250826/20250826141647.png)

サンプルコードはこちらになりますが、ほとんどUnitテストと変わりません。

```
name: Release - Terraform Test (Integration)

on:
  push:
    branches:
      - main

jobs:
  integration-tests:
    runs-on: ubuntu-XX.XX

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: X.XX

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-region: ap-northeast-1
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          role-duration-seconds: 1200

      - name: Terraform init
        run: terraform init

      - name: Terraform validate
        run: terraform validate -no-color

      - name: Terraform test (integration)
        run: terraform test -test-directory=tests/integration
```

このようにCIのワークフローにTerraform Testを組み込むことで、PR時にUnitテストで素早いフィードバックを得られ、マージ後にはIntegrationテストで実際の構築検証を行うという二段構えが実現できました。

結果として、より信頼性の高い汎用モジュールを安全に開発できるようになっています。

## まとめ

以上がTerraform TestとCIワークフローへの組み込みの紹介となります。

テストを汎用モジュールに組み込むことで、事前にApply失敗を検知できる仕組みを整え、信頼性を高めつつスピード感のあるインフラ構築を進められるようになりました。

一方で、Integration TestはSandbox環境に実際のリソースを構築するため実行時間が長くなるという課題もあります。今後はテストスピードの改善や効率化の仕組みを検討していく予定です。

皆さんのTerraform活用のヒントになれば幸いです。

ファインディでは一緒に会社を盛り上げてくれるSREメンバーを募集中です。興味を持っていただいた方はこちらのページからご応募お願いします。

[herp.careers](https://herp.careers/v1/findy/requisition-groups/14c4a661-5e48-40c5-99d0-ea657b8b4c04)

[« 小さな積み重ねと準備が生んだ生成AIフレ…](https://tech.findy.co.jp/entry/2025/09/02/070000) [Findy AI Meetup in Fukuoka #2 を開催し… »](https://tech.findy.co.jp/entry/2025/08/27/113000)