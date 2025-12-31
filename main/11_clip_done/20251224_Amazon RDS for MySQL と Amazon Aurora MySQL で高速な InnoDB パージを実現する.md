---
title: "Amazon RDS for MySQL と Amazon Aurora MySQL で高速な InnoDB パージを実現する"
source: "https://aws.amazon.com/jp/blogs/news/achieve-a-high-speed-innodb-purge-on-amazon-rds-for-mysql-and-amazon-aurora-mysql/"
author: ""
published: "2025-12-23"
created: "2025-12-24"
description: "本記事は、”Achieve a high-speed InnoDB purge on Amazon […]"
tags:
  - ""
  - "raw"
---

## Amazon Web Services ブログ

本記事は、” [Achieve a high-speed InnoDB purge on Amazon RDS for MySQL and Amazon Aurora MySQL](https://aws.amazon.com/blogs/database/achieve-a-high-speed-innodb-purge-on-amazon-rds-for-mysql-and-amazon-aurora-mysql/) ” を翻訳したものです。

[パージ](https://dev.mysql.com/doc/refman/8.0/en/innodb-purge-configuration.html) は、MySQL データベースにおけるハウスキーピング操作です。InnoDB ストレージエンジンは、 [マルチバージョン同時実行制御 (MVCC)](https://dev.mysql.com/doc/refman/8.0/en/innodb-multi-versioning.html) やロールバック操作のために不要となった、 [undo ログ](https://dev.mysql.com/doc/refman/8.0/en/innodb-undo-logs.html) や削除マークの付いたテーブルレコードのクリーンアップを、この操作に依存しています。私たちのアプリケーションは、元より最高の書き込みスループットを提供することを目的としたデータベース設計を追求していますが、同様にパージがバックグラウンドでタイムリーに実行できることを確認することも重要です。大量のデータ変更とパージの進行のバランスが崩れると、データベースのパフォーマンスが低下する可能性があります。

この投稿では、 [Amazon Relational Database Service (Amazon RDS) for MySQL](https://aws.amazon.com/rds/mysql/) DB インスタンス、及び [Amazon Aurora MySQL 互換エディション](https://aws.amazon.com/rds/aurora/) DB クラスターにおける、高速なパージのための一連の設計およびチューニング戦略の概要を説明します。まず、MySQL データベースの内部構造について私たちの理解を活用して、パージの仕組みを簡単に紹介します。次に、パージの課題となる一般的な要因と、使用できる最適化手法について説明します。この記事は [MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html) に基づいており、ほとんどの推奨事項は一般的な MySQL データベースに適用可能です。また、Amazon マネージドデータベースサービスに特有の考慮事項も示します。

## パージの仕組みを理解する

他の多くの主流のリレーショナルデータベース管理システム (RDBMS) と同様に、MySQL は MVCC を実装して、データにアクセスするための読み取りと書き込みの同時操作を可能にしています。MVCC の核となる考え方は、トランザクションによってテーブルレコードが更新されたときに、データベースエンジンにテーブル内の新しいバージョンのデータを作成させることです。古いデータのバージョンは物理的には削除されず、削除済みとマークされます。クエリは望ましい分離レベルで、適切なデータバージョンを選択してデータベースの独自のビューを構築できます。そうすることの大きな利点は、読み取りと書き込み間でのブロッキングが発生する状況を回避することです。読み取りは常に古いデータバージョンにアクセスできますが、書き込みは新しいバージョンで実行されます。テーブルレコードの複数のバージョンを保持できるので、データベースエンジンがトランザクション内またはクラッシュリカバリ中にロールバック操作を実行することも容易になります。

スケーラブルなソリューションとして、MVCC には固有の制約があります。削除マークが付いたテーブルレコードはガベージコレクションにより処理される必要があるということです。さまざまなデータベースエンジンに、独自のバージョントラッキングとガベージコレクションメカニズムが備わっています。一般的な課題は、大量のトランザクションにより古いデータバージョンが速く生成され過ぎ、ガベージコレクションが追いつけない場合です。その結果、テーブル構造に古いデータバージョンが大量のバックログとして蓄積されることがあります。表面的には、これはスペース使用量の予想外の増加を直接引き起こします。その裏で、古いバージョンをチェックして読み取り操作を実行するには、追加の I/O 操作を行う必要があります。この I/O 消費量の増加は、システムリソースを奪い合い、データベース全体のパフォーマンスを低下させる可能性があります。

MySQL データベースでは、InnoDB は MVCC とロールバック操作をサポートするための主要なデータ構造として undo ログを使用します。テーブルレコードが変更されると、古いデータバージョンは undo ログに保存されます。同じテーブルレコードに関連するすべての undo ログはリンクされ、バージョンチェーンを形成します。その裏返しとして、パージはガベージコレクションのことです。undo ログだけでなく、それらが参照する削除マークの付いたテーブルレコードもクリーンアップします。本質的に、パージは InnoDB トランザクションシステムの不可欠な部分と見なされます。

次のグラフは、InnoDB パージの高レベルの設計アイデアと 3 段階のワークフローを示しています。

![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/10/23/DBBLOG-4263-img1.png)

1. トランザクションが開始されると、 [ロールバックセグメント](https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos_rollback_segment) が割り当てられます。ロールバックセグメントは、 [undo テーブルスペース](https://dev.mysql.com/doc/refman/8.0/en/innodb-undo-tablespaces.html) 内の多数の undo ログページで構成されます。テーブルレコードが保存されるデータページのように、undo ログページを読み書きするには InnoDB バッファプールにロードする必要があります。
2. トランザクションによってテーブルデータが変更されると、undo ログレコードが作成されます。undo ログレコードには、テーブル ID、クラスタ化インデックス、変更前の古いデータバージョンなど、テーブルレコードに行われた変更をロールバックするために必要な関連情報が含まれています。INSERT、DELETE、UPDATEステートメント用に、異なる種類の undo ログレコードがあります。後でパージする必要があるかどうかに応じて、それらは別々の undo ログにグループ化されます。
3. コミット中、トランザクションはトランザクションシリアル番号 (trx\_no) を取得し、それを undo ログに書き込みます。パージする必要のある undo ログが存在する場合、それらは trx\_no 順に並べられた [ロールバックセグメント履歴リスト](https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos_history_list) に追加されます。InnoDB トランザクションシステムは trx\_no を使用して、コミットされたすべてのトランザクションの順序を追跡します。その意味では、履歴リストはデータベース全体でグローバルなリストです。
4. パージはマルチスレッド操作です。パージスレッドの数は、 `[innodb_purge_threads](https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html#sysvar_innodb_purge_threads)` を使用して設定されます。通常、1 つのパージコーディネーターといくつかのワーカースレッドが存在します。これらのスレッドは、3 つのステップを含むパージ操作を継続的に繰り返します。
1. 1. パージコーディネータースレッドは、パージできる undo ログがあるかどうかをチェックします。そのような undo ログが見つかったらひとまとめに取り出し、undo レコードを解析して、テーブル ID でソートします。次に、処理を行うため各グループをワーカースレッドに割り当てます。
	2. パージワーカースレッドは、undo ログレコードをテーブル ID ごとに並行して処理します。undo ログレコード中の情報を使用して、クラスタ化インデックス、セカンダリインデックス、BLOB 列など、削除マークの付いたレコードを識別して削除します。クリーンアップ後にデータページ内のデータが少なすぎる場合は、ストレージを最適化するために別のページにマージされます。
	3. いくつかの undo ログのまとまった単位が処理された後、パージコーディネータスレッドはそれらをロールバックセグメント履歴リストから削除して、ロールバックセグメントを解放します。MySQLには、undo テーブルスペースを自動的に切り捨てる `[innodb_undo_log_truncate](https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html#sysvar_innodb_undo_log_truncate)` というオプションが用意されています。これは、undo テーブルスペースが `[innodb_max_undo_log_size](https://dev.mysql.com/doc/refman/8.4/en/innodb-parameters.html#sysvar_innodb_max_undo_log_size)` で指定されたサイズ制限を超え、内部に含まれるすべてのロールバックセグメントが解放されたときに、物理ストレージスペースを縮小するためのものです。このステップが完了すると、パージコーディネータースレッドは別のパージサイクルを開始します。

undo テーブルスペースの自動切り捨てオプションは、Aurora MySQL 互換 [バージョン 3.06.0](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/AuroraMySQL.Updates.3060.html) 以降で使用できます。

## 読み取りと書き込みのワークロードのバランスを取る

トランザクションがレコードを変更するために INSERT、DELETE、UPDATEなどのデータ操作言語 (DML) ステートメントを使用するとき、InnoDB は異なる種類の undo ログレコードを作成します。ただし、すべての種類の undo ログレコードをパージする必要はありません。INSERT ステートメントにより生成された undo ログには古いデータバージョンが含まれていないため、トランザクションがコミットされた直後に削除され、ロールバックセグメント履歴リストには追加されません。

DELETE 及び UPDATE ステートメントによって生成された undo ログレコードには、テーブルレコードが削除または更新される前の古いデータバージョンが保存されているため、パージ操作の対象となります。他の並行した SELECT クエリやオープントランザクションは、MVCC の目的で [一貫した読み取り](https://dev.mysql.com/doc/refman/8.0/en/innodb-consistent-read.html) を構築するために、それらにアクセスする必要があるかもしれません。InnoDB は、アクティブなクエリとトランザクションのために undo ログの可視性を追跡するメカニズムとして、 [読み取りビュー](https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos_read_view) を使用しています。また、パージコーディネータースレッドが undo ログを安全に削除できるかどうかを判断するためにも使用されます。

undo ログの作成と使用の両方を行うデータベースワークロードは、パージスレッドの動作に直接影響します。undo ログは、ロールバックセグメント履歴リストから trx\_no の昇順で削除されます。undo ログをパージできない場合、trx\_no が大きい他の undo ログは、別のテーブルに属していてもパージされなくなります。つまり、パージはデータベース全体でグローバルな操作であり、1 つの長時間実行されたクエリまたはトランザクションにより、それより後に開始された全てのトランザクションの undo レコードのクリーンアップがブロックされます。パージが常に懸念事項となる MySQL データベースでは、データベースワークロードのタイミング、同時実行性、およびトランザクション特性を確認することをお勧めします。

1つの戦略は、DELETE よりも DROP PARTITION または DROP TABLE ステートメントを選択することです。これらのステートメントは undo ログを生成しないからです。次の図に示すように、DROP PARTITION を使用してデータのサブセットを削除できるようにテーブルをパーティション化すれば、パージを回避できます。テーブルから大量のデータを削除したい場合は、新しいテーブルを作成し、データをコピーして、古いテーブルを削除するという方法をいつも検討する価値があります。

![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/10/23/DBBLOG-4263-img2.png)

もう 1 つの戦略は、大量の DELETE または UPDATE ステートメントが実行されている間、読み取りビューが undo ログを保持しパージをブロックする可能性がある、長時間実行される SELECT クエリを避けることです。 `[max_execution_time](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_execution_time)` を使用して最大制限時間を設定することで、実行時間が長すぎる SELECT クエリを自動的に停止できます。トランザクションの分離レベルを、 `[REPEATABLE READ](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html#isolevel_repeatable-read)` から `[READ COMMITTED](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html#isolevel_read-committed)` に切り替えることもできます。これにより、SQL ステートメントによって作成される読み取りビューの範囲が狭まり、undo ログのパージがブロックされる可能性が低くなります。

Aurora MySQL は、1 つ以上の DB インスタンスで構成されるクラスター化されたデータベースであり、すべての DB インスタンスが同じ共有されたクラスターストレージボリュームを使用します。InnoDB のパージの実装は、そのクラスタリングトポロジーの影響を受けます。Aurora MySQL DB クラスターを使用する場合、Amazon RDS for MySQL DB インスタンスと比較すると、次のような違いがあります。

- パージがデータベース全体のグローバルな操作であるという概念は、Aurora MySQL のデータベースアーキテクチャ全体で一貫しています。パージはプライマリ (ライター) DB インスタンスで実行されます。ただし、Auroraレプリカ DB インスタンス上の SELECT クエリが読み取りビューを作成するため、パージがブロックされる可能性があります。 [Aurora Global Database](https://aws.amazon.com/rds/aurora/global-database/) においても、セカンダリ DB クラスター上の SELECT クエリがプライマリ DB クラスターのパージをブロックする可能性があります。
- Aurora レプリカ DB インスタンスでは、 `[READ COMMITTED](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Reference.IsolationLevels.html)` 分離レベルは、長時間実行される SELECT クエリがパージスレッドに与える影響を軽減するように最適化されており、Aurora MySQL 固有の動作をします。クエリの結果は、プライマリDBインスタンスで MySQL のネイティブの `READ COMMITTED` レベルを使用する場合とは少し異なる場合がありますが、それでも ANSI SQL 標準に準拠しています。この機能を有効にするには、DBクラスターパラメータグループ、またはセッションレベルで `[aurora_read_replica_read_committed](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Reference.ParameterGroups.html)` を ON に設定します。

## テーブルとインデックスの構造を最適化する

undo ログに加えて、InnoDB テーブルで削除済みとマークされたテーブルレコードもパージ操作の対象になります。一般的な意味では、テーブルレコードとは、クラスター化インデックス、セカンダリインデックス、 [InnoDB の行フォーマット](https://dev.mysql.com/doc/refman/8.0/en/innodb-row-format.html) に従って外部に保存された可変長列など、テーブルの行データを格納または示すさまざまなデータ構造を参照します。undo ログレコードにはテーブル ID とクラスタ化インデックスしか含まれていないため、パージスレッドは削除マークの付いた他の関連するテーブルレコードを識別し、存在する場合は削除する必要があります。これは、パージ操作で最も負荷の高い部分になる可能性があります。

セカンダリインデックスがパージ操作に与える影響の例を考えましょう。次のグラフは、2 つの Aurora MySQL DB クラスターの [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) メトリック `[RollbackSegmentHistoryListLength](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.AuroraMonitoring.Metrics.html)` を比較しています。どちらのクラスターにも r7g.2xlarge プライマリ (ライター) DB インスタンスがあり、 [Sysbench](https://github.com/akopytov/sysbench) の `oltp_write_only.lua prepare` ワークロードを使用して 80 GB のデータを含む 1 つのテーブルをロードします。1 つのクラスター (クラスターA) では、 `oltp_update_non_index.lua` ワークロードを実行して、セカンダリインデックスでカバーされていない列を更新します。他のクラスター (クラスターB) では、 `oltp_update_index.lua` ワークロードを実行して、その上にセカンダリインデックスが構築されている列を更新します。どちらの Sysbench ワークロードも、 `--rate` を使用して同じレートでトランザクションを生成します。

![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/10/23/DBBLOG-4263-img3.png)

次のことを観察できます。

- `[DMLThroughput](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.AuroraMonitoring.Metrics.html)` は両方のクラスターで同じパターンを示し、同じ数の UPDATE ステートメントを実行していることを示しています。
- `oltp_update_index.lua` ワークロードを実行するクラスターでは、 `RollbackSegmentHistoryListLength` がピーク時に 300 万を超えます。しかし、他のクラスターではゼロに近いままです。これは、セカンダリインデックスを含むundo ログを処理すると、パージスレッドが大幅に遅くなる可能性があることを示しています。セカンダリインデックスの使用は必ずしも問題ではありません。両方のクラスターのテーブル構造は同じで、どちらのテーブルにもセカンダリインデックスがあります。セカンダリインデックスは、データベースのワークロードによって変更された場合にのみ、パージスレッドに課題をもたらします。
- 11:52 の縦線は、クラスター B のセカンダリインデックスをいつ削除したかを示しています。セカンダリインデックスを削除すると、パージによりセカンダリインデックスのレコードを検索してクリーンアップする必要がなくなるため、パージ操作がすぐにスピードアップします。セカンダリインデックスを削除してから数分で `RollbackSegmentHistoryListLength` がゼロに下がることがわかります。SYS スキーマの `[schema_unused_indexes](https://dev.mysql.com/doc/refman/8.0/en/sys-schema-unused-indexes.html)` ビューを使用して、使用されていないセカンダリインデックスを特定し、必要かどうかを評価できます。

MySQL 8.0 以降、パージワーカースレッドは、削除マークの付いたテーブルレコードをクリーンアップするために、異なるテーブルで並行して動作するように設計されています。並列処理の効率は、いくつかの要因によって決まります。次のグラフは、パージワーカースレッドの数と、パージされるのを待機している undo ログを保持するテーブルの数との相関関係の例を示しています。

データは、前の 2つの Aurora MySQL DB クラスターでの別のテストから収集されました。1 つのクラスター (クラスターB) は 80 GB のデータを持つ 1 つのテーブルを引き続き使用し、もう 1 つのクラスター (クラスターA) は合計 80 GB のデータを、それぞれ 8 GB のデータを持つ 10 個のテーブルに分散させています。どちらのクラスターも Sysbench `oltp_update_index.lua` ワークロードを実行し、 `--rate` を使用して同じレートでトランザクションを生成します。両方のクラスターの DB インスタンスは r7g.2xlarge なので、 `innodb_purge_threads` はデフォルトで 3 に設定されています。つまり、2 つのパージワーカースレッド (及びパージコーディネーター) を同時に実行できます。

![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/10/23/DBBLOG-4263-img4.png)

次のことを観察できます。

- `DMLThroughput` は両方のクラスターで同じパターンを示し、同じ数の UPDATE ステートメントを実行していることを示しています。
- `RollbackSegmentHistoryListLength` は、1 つのテーブルがロードされたクラスター A では 300 万ですが、10個のテーブルを持つクラスター B ではピーク時に約 50 万に達します。パージ速度が速いのは、2 つのワーカースレッドが並行して動作することと、作業する各ワーカースレッドにとってテーブルサイズが小さいことの 2 つの要因によるものです。一度に 1 つのテーブルを消去できるワーカースレッドは1つだけです。並列処理を最大限に活用するには、パージワーカースレッドよりも多いか同数のテーブルに対し、データ変更を均等に分散するのが理想的です。
- `innodb_purge_threads` は、パージ操作のスピードに影響する要因です。他の要因が作用している場合、パージスレッドをスピードアップするのに役立つかもしれません。

## 適切なインスタンスクラスを選択する

設計上、パージは非干渉的です。パージスレッドはバックグラウンドで実行され、ユーザートランザクションとは非同期に動作します。妥当な遅延時間でジョブを終わらせるために、システムリソースの消費を最小限に抑えることが期待されています。MySQL では、 `innodb_purge_threads` の最大値を 32 と定義しています。つまり、MySQL データベースには最大 32 のパージスレッドを設定できます。このような設定は、負荷の高い本番データベースに何千ものユーザー接続を同時に許可する `[max_connections](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_max_connections)` と比較して、パージスレッドに競争上の優位性をもたらすことを意図したものではありません。

パージスレッドが undo ログや削除マークの付いたテーブルレコードを処理する際、undo ログページと InnoDB バッファプールのデータページからデータを読み取る必要があります。それらのデータページがバッファプールに存在しない場合は、I/O コールを発行してストレージから取得します。RDS DB インスタンスの CPU、メモリ、IO 帯域幅などのシステムリソースが、パージ操作の速度に大きな影響を与える可能性があります。

高速なパージ操作には、パージスレッドだけでなく、データベース全体のワークロードについてもキャパシティプランニングが必要です。リソースが不足している、またはユーザートランザクションによるシステムリソースの使用率が高い DB インスタンスでは、リソースの競合によりパージスレッドが遅くなり、パージの遅延が予期せず現れることがあります。次のグラフは、この状況の例を示すために、r7g.2xlarge のプライマリ (ライター) DB インスタンスを持つ Aurora MySQL DB クラスターで実施したテストの結果です。

テストは、2 つの異なる Sysbench データセットを順番にロードすることから始まります。まず、クラスターにはそれぞれ 8 GB のデータを含む 10 個の Sysbench テーブルがロードされ、次に、34 GB のデータの別のテーブルがロードされます。データをロードした後、テストは 34 GB のテーブルに対して `oltp_read_only.lua` ワークロードを実行します。 `[innodb_buffer_pool_size](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_buffer_pool_size)` はデフォルトで 42 GB に設定されているため、この 34 GB のテーブルデータは InnoDB バッファプールに完全にキャッシュされます。同時に、他の 10 個のテーブルのほとんどのデータはバッファプールから削除されます。読み取り専用ワークロードが完了する前に、テストは他の 10 個のテーブルで `oltp_update_index.lua` ワークロードを開始します。

![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/10/23/DBBLOG-4263-img5.png)

![](https://d2908q01vomqb2.cloudfront.net/887309d048beef83ad3eabf2a79a64a389ab1c9f/2024/10/23/DBBLOG-4263-img6.png)

次のことを観察できます。

- `[SelectThroughput](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.AuroraMonitoring.Metrics.html)` と `DMLThroughput` は、2つの異なるタイプのワークロードが、自身のデータセットをロードするために InnoDB バッファプールをめぐって競合していることを示しています。
- `oltp_update_index.lua` ワークロードの終了時、 `RollbackSegmentHistoryListLength` が 500 万を超えました。これは前のテストと比較すると想定外です。そのテストでは、10 個のテーブルで同じ `oltp_update_index.lua` ワークロードをより高いレート ( 1 万 5 千対 1 万) で実行したところ、 `RollbackSegmentHistoryListLength` は約 50 万でした。
- `oltp_update_index.lua` ワークロードが開始されると、バッファプールの競合が原因で、 `[BufferCacheHitRatio](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.AuroraMonitoring.Metrics.html)` が急激に低下します。ワークロードが完了した後も低いままです。これは、パージスレッドが undo ログやテーブルレコードをバッファプールに取り込むときに、I/O パスでボトルネックになっていることを示しています。
- InnoDB バッファプールへの適切なメモリ割り当ては、パージ操作の速度に大きな影響を与える可能性があります。必要な undo ログやテーブルデータがバッファプールにない場合、パージスレッドのパフォーマンスは IO レイテンシーと相関します。

MySQL データベースでは、 `innodb_purge_threads` パラメーターを変更することで、パージスレッドの数を設定できます。RDS for MySQL を使用する場合、MySQL コミュニティエディションと同じくデフォルト値は 1 で、DB パラメータグループで変更できます。Aurora MySQL を使用する場合、デフォルトは、DB インスタンスのサイズが大きくなるにつれて増加し、 [DB クラスターパラメータグループ](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_WorkingWithDBClusterParamGroups.html) で変更できます。次の表は、r7g インスタンス~タイプのデフォルト式に基づいた、パージ関連の設定の有効値を示しています。

| **RDS インスタンスタイプ** | **vCPU** | **メモリ (GiB)** | **innodb\_buffer\_pool\_size (GiB)** | **innodb\_purge\_threads** | **innodb\_purge\_batch\_size** |
| --- | --- | --- | --- | --- | --- |
| db.r7g.large | 2 | 16 | 7.76 | 1 | 600 |
| db.r7g.xlarge | 4 | 32 | 19.36 | 1 | 600 |
| db.r7g.2xlarge | 8 | 64 | 42.59 | 3 | 1800 |
| db.r7g.4xlarge | 16 | 128 | 89.11 | 3 | 1800 |
| db.r7g.8xlarge | 32 | 256 | 182.06 | 6 | 3600 |
| db.r7g.12xlarge | 48 | 384 | 275.11 | 12 | 7200 |
| db.r7g.16xlarge | 64 | 512 | 368.13 | 12 | 20000 |

Aurora Serverless V2 インスタンスタイプでは、この設定はインスタンスのスケールアップまたはスケールダウン時に自動的に設定され、パラメータグループでは変更できません。

## 監視とアラーム

InnoDB のパージを監視するためのよく知られたメトリックは、パージラグとも呼ばれるロールバックセグメント履歴リストの長さです。これは、パージされるのを待機している undo ログの数を示します。MySQL データベースでは、 `SHOW ENGINE INNODB STATUS` を実行して、 `History list length` を直接確認できます。Aurora MySQL は、すべての 3.0 リリースで `RollbackSegmentHistoryListLength` を CloudWatch メトリックとして提供しています。Amazon RDS for MySQL では、 [Performance Insights](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html) にて `trx_rseg_history_len` というメトリックを提供しており、それを [CloudWatch に公開](https://docs.aws.amazon.com/prescriptive-guidance/latest/amazon-rds-monitoring-alerting/publishing-performance-insights-to-cloudwatch.html) できます。

パージラグがはるかに遅れ、データベースのパフォーマンス上の問題を引き起こす可能性がある状況を検出するために、このメトリックに [CloudWatch アラーム](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html) を設定することをお勧めします。アラームのしきい値は、データベースがこれまでに到達した過去の正常値と、アラームがトリガーされたときに取るアクション項目に基づいて設定できます。

データベースワークロードによって、パージスレッドが十分に速く処理仕切れないほどの undo ログが生成され、パージラグが増加していることに気付いた場合は、データベースインスタンスのサイズを増やして、パージスレッドに割り当てるシステムリソースを確保してください。または、 [データベースシャーディング](https://aws.amazon.com/blogs/database/sharding-with-amazon-relational-database-service/) アーキテクチャを使用して、複数のデータベースシャードにワークロードを分散することもできます。MySQLには、ロールバックセグメント履歴リストの長さの閾値を設定するための `[innodb_max_purge_lag](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_max_purge_lag)` も用意されています。違反すると、INSERT、DELETE、UPDATE ステートメントに対し内部のスロットリングが開始され、最大 `[innodb_max_purge_lag_delay](https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_max_purge_lag_delay)` までの遅延が発生します。これらのオプションをテストして、どれが自分のユースケースに最適かを確認できます。

## まとめ

InnoDB のパージ効率を向上させるには、ワークロードの最適化、データベースのキャパシティプランニング、および設定を組み合わせる必要があります。この記事では、RDS for MySQL DB インスタンス、Aurora MySQL DB クラスター、またはその他の種類の MySQL データベースでそれを実行するために役立つガイドラインを提供します。

### 著者について

Lei Zeng は AWS のデータベースエンジニアです。

本記事の翻訳はクラウドサポートエンジニアの野沢が担当しました。