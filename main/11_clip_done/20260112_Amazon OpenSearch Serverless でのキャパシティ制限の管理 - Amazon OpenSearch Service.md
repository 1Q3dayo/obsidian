---
title: "Amazon OpenSearch Serverless でのキャパシティ制限の管理 - Amazon OpenSearch Service"
source: "https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/serverless-scaling.html"
author:
published:
created: 2026-01-12
description: "OpenSearch Serverless の容量制限を設定して、ワークロードのパフォーマンスを維持しつつ、リソースの割り当てを制御してコストを最適化します。"
tags:
  - "clippings"
  - "raw"
---
Amazon OpenSearch Serverless でのキャパシティ制限の管理 - Amazon OpenSearch Service

[キャパシティの設定](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/#serverless-scaling-configure) [最大キャパシティの制限](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/#serverless-scaling-limits) [キャパシティ使用量のモニタリング](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/#serverless-scaling-monitoring)

Amazon OpenSearch Serverless では、キャパシティを自分で管理する必要はありません。OpenSearch Serverless は、現在のワークロードに基づいて、アカウントのコンピューティング性能を自動的にスケーリングします。Serverless のコンピューティング性能は、 *OpenSearch Compute Units* (OCU) で測定されます。各 OCU は、6 GiB のメモリと対応する仮想 CPU (vCPU)、および Amazon S3 へのデータ転送を組み合わせたものです。OpenSearch Serverless の分離アーキテクチャの詳細については、「 [仕組み](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/serverless-overview.html#serverless-process) 」を参照してください。

最初のコレクションを作成すると、OpenSearch Serverless は冗長性の設定に基づいて OCU をインスタンス化します。デフォルトでは、冗長アクティブレプリカが有効になっています。つまり、別のアベイラビリティーゾーンのスタンバイノードで高可用性を確保するために、合計 4 つの OCU がインスタンス化されます (インデックス作成用に 2 つ、検索用に 2 つ)。開発やテストの目的では、コレクションの **\[冗長性を有効化\]** 設定を無効にできます。これによりスタンバイレプリカが排除され、2 つの OCU のみがインスタンス化されます (インデックス作成用に 1 つ、検索用に 1 つ)。これらの OCU は、インデックス作成や検索が行われていない場合でも常に存在します。後続のコレクションはすべてこれらの OCU を共有できます (ただし、固有の AWS KMS キーを持つコレクションを除く。これらのコレクションは、OCU セットを独自でインスタンス化します)。必要に応じて、OpenSearch Serverless はインデックス作成および検索での使用量の増加に合わせて自動的にスケールアウトし、OCU を追加します。コレクションエンドポイントのトラフィックが減少すると、キャパシティはデータサイズに必要な最小限の OCU 数まで縮小されます。検索および時系列コレクションの場合、アイドル状態のときに必要な OCU の数は、データサイズとインデックス数に比例します。ベクトルの場合、ベクトルグラフを保存するメモリ (RAM) と、インデックスを保存するディスクスペースの両方に依存します。アイドル状態でない場合、OCU の要件にはこれらの両方が考慮されます。

ベクトルコレクションは、インデックスデータを OCU ローカルストレージに保持します。OCU の RAM 上限は OCU のディスク上限よりも速く到達するため、ベクトルコレクションは RAM スペースによって制限されます。冗長性を有効にすると、OCU 容量はインデックス作成用に 1 OCU \[0.5 OCU x 2\]、検索用に 1 OCU \[0.5 OCU x 2\] にスケールダウンされます。冗長性を無効にすると、ドメインはインデックス作成用に 0.5 OCU、検索用に 0.5 OCU にスケールダウンできます。スケーリングでは、コレクションまたはインデックスに必要なシャードの数も考慮されます。各 OCU は、指定された数のシャードをサポートできます。インデックスの数はシャード数に比例する必要があります。必要な基本 OCU の合計数は、必要なデータ、メモリ、シャードの最大量です。詳細については、 *AWS Big Data Blog* の「 [Amazon OpenSearch Serverless によるあらゆる規模における費用対効果の高い検索機能](https://aws.amazon.com/blogs/big-data/amazon-opensearch-serverless-cost-effective-search-capabilities-at-any-scale/) 」を参照してください。

*検索* および *ベクトル検索* コレクションでは、迅速なクエリ応答時間を確保するために、すべてのデータがホットインデックスに保存されます。 *時系列* コレクションでは、ホットストレージとウォームストレージを組み合わせて使用し、より頻繁にアクセスされるデータのクエリ応答時間を最適化するために、最新のデータがホットストレージに保存されます。詳細については、「 [コレクションタイプを選択する](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/serverless-overview.html#serverless-usecase) 」を参照してください。

###### 注記

ベクトル検索コレクションが *検索* コレクションまたは *時系列* コレクションと同じ KMS キーを使用している場合でも、ベクトル検索コレクションは OCU を *検索* コレクションおよび *時系列* コレクションと共有することはできません。最初のベクトルコレクション用に新しい OCU セットが作成されます。ベクトルコレクションの OCU は、同じ KMS キーコレクション間で共有されます。

コレクションのキャパシティを管理してコストを制御するため、現在のアカウントおよびリージョン用にインデックス作成と検索の全体的な最大キャパシティを指定できます。OpenSearch Serverless は、これらの仕様に基づいて、コレクションリソースを自動的にスケールアウトします。

インデックス作成と検索のキャパシティは個別にスケーリングされるため、それぞれにアカウントレベルの制限を指定します。

- **インデックス作成の最大キャパシティ** — OpenSearch Serverless は、この数の OCU までインデックス作成のキャパシティを増やすことができます。
- **検索の最大キャパシティ** — OpenSearch Serverless は、この数の OCU まで検索のキャパシティを増やすことができます。

###### 注記

現時点では、キャパシティの設定はアカウントレベルでのみ適用されます。コレクションごとにキャパシティの制限を設定することはできません。

目標は、最大キャパシティがワークロードの急増を処理するために十分な量であるのを確実にすることです。OpenSearch Serverless は、ユーザーの設定に基づいてコレクションの OCU 数を自動的にスケールアウトして、インデックス作成と検索のワークロードを処理します。

###### トピック

- [キャパシティの設定](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/#serverless-scaling-configure)
- [最大キャパシティの制限](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/#serverless-scaling-limits)
- [キャパシティ使用量のモニタリング](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/#serverless-scaling-monitoring)

## キャパシティの設定

OpenSearch Serverless コンソールでキャパシティの設定を行うには、左側のナビゲーションペインで **\[Serverless\]** を展開し、 **\[Dashboard\]** (ダッシュボード) を選択します。 **\[Capacity management\]** (キャパシティ管理) で、インデックス作成と検索の最大キャパシティを指定します。

![Capacity management dashboard showing indexing and search capacity graphs with 10 OCU limits.](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/images/ServerlessCapacity.png)

AWS CLI を使用してキャパシティを設定するには、 [UpdateAccountSettings](https://docs.aws.amazon.com/opensearch-service/latest/ServerlessAPIReference/API_UpdateAccountSettings.html) リクエストを送信します。

```
aws opensearchserverless update-account-settings \
    --capacity-limits '{ "maxIndexingCapacityInOCU": 8,"maxSearchCapacityInOCU": 9 }'
```

## 最大キャパシティの制限

コレクションに含めることができるインデックスの最大合計は 1000 です。3 種類のコレクションすべてにおいて、デフォルトの最大キャパシティは、インデックス作成用に 10 OCU、検索用に 10 OCU です。アカウントで利用可能な最小キャパシティは、インデックス作成用に 1 OCU \[0.5 OCU x 2\]、検索用に 1 OCU \[0.5 OCU x 2\] です。すべてのコレクションで、許可される最大キャパシティは、インデックス作成用に 1,700 OCU、検索用に 1,700 OCU です。OCU の数は、1 から、最大許容キャパシティ (2 の倍数) までの任意の数に設定できます。

各 OCU には、120 GiB のインデックスデータを保存するのに十分なホットエフェメラルストレージが含まれています。OpenSearch Serverless は、 *検索* および *ベクトル検索* コレクションのインデックスあたり最大 1 TiB のデータと、 *時系列* コレクションのインデックスあたり最大 100 TiB のホットデータをサポートします。時系列コレクションの場合は、さらに多くのデータを取り込むことができ、S3 にウォームデータとして保存できます。

すべてのクォータのリストについては、「 [OpenSearch Serverless のクォータ](https://docs.aws.amazon.com/general/latest/gr/opensearch-service.html#opensearch-limits-serverless) 」を参照してください。

## キャパシティ使用量のモニタリング

`SearchOCU` および `IndexingOCU` におけるアカウントレベルの CloudWatch メトリクスをモニタリングして、コレクションでどのようにスケーリングされているかを把握できます。アカウントがキャパシティに関するメトリクスのしきい値に近づいた際に通知を行うアラームを設定することをお勧めします。そうすることで、状況に応じてキャパシティの設定を調整できます。

最大キャパシティの設定が適切か、または調整が必要どうかを判断するために、これらのメトリクスを使用することもできます。これらのメトリクスを分析することで、コレクションの効率を最適化することに集中できます。OpenSearch Serverless が CloudWatch に送信するメトリクスの詳細については、「 [Amazon OpenSearch Serverless のモニタリング](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/serverless-monitoring.html) 」を参照してください。