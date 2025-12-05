---
title: "Linux向けウィルス対策ソフトClamAVの使い方"
source: "https://zenn.dev/gladevise/articles/clamav-usage"
author:
  - "[[Zenn]]"
published: 2022-10-31
created: 2025-12-04
description:
tags:
  - "clippings"
  - "raw"
---
40

4[tech](https://zenn.dev/tech-or-idea)

今回はLinux向けウィルスチェックソフトの定番、ClamAVを紹介します

いきなりタイトルを否定しますが、ClamAVは別にLinux向けというわけではありません。macOSでもWindowsでも動作します。それぞれのOSのインストール方法に関しては [公式ページ](https://docs.clamav.net/manual/Installing.html) をご確認ください。

ClamAVにLinuxのイメージが強いのは、単にWindowsにはWindows Defenderやその他商用のウィルス対策ソフトが溢れている一方で、シェアの少ないLinuxに対応しているウィルス対策ソフトそのものが少ないためと思われます。それどころか、ウィルスの絶対数自体もWindowsよりも圧倒的に少ないです。ウィルス開発もソフトウェア開発には変わりないので、わざわざシェアの少ないOS向けに開発するコストを支払いたくないというのがウィルス開発者の本音ではないかと想像します(まあ、知りませんけど)。しかし、最近ではPythonやJavaScriptなどで動作するクロスプラットホームなウィルスも増えてきています。Linuxと言えどウィルスと無縁ではいられなくなっているのが現状です。

ここでは `clamscan` と `clamdscan` というClamAVの基本的なスキャンコマンドの使い方や `clamd.conf` の設定方法を説明します。

## ClamAVのインストール

まずは以下のコマンドを実行してClamAVをインストールしてください。

```shell
sudo apt install -y clamav clamav-daemon libclamunrar9
```

インストールできたら、以下のコマンドでdaemonが起動しているか確認してください

```shell
sudo systemctl status clamav-daemon.service
```

起動できていれば以下のような結果が返ってきます。

```
● clamav-daemon.service - Clam AntiVirus userspace daemon
     Loaded: loaded (/lib/systemd/system/clamav-daemon.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/clamav-daemon.service.d
             └─extend.conf
     Active: active (running) since Fri 2022-10-28 07:00:00 JST; 7h ago
       Docs: man:clamd(8)
             man:clamd.conf(5)
             https://docs.clamav.net/
   Main PID: 1000 (clamd)
      Tasks: 2 (limit: 10000)
     Memory: 572.0M
     CGroup: /system.slice/clamav-daemon.service
             └─1068 /usr/sbin/clamd --foreground=true
```

## テストファイルのダウンロード

実行したコマンドが正常に動作しているか確認するためにウィルスを検出できる環境を作りたいと思いますが、まさか本物のウィルスをダウンロードするわけにはいきません。

Eicarではウィルスチェックのためのテストファイルを配布しています。 [こちら](https://www.eicar.org/download-anti-malware-testfile/) にアクセスして、 `eicar.com.txt` や `eicar_com.zip` などのファイルをダウンロードしてください。

以下のようにどこか適当なディレクトリを作ってまとめておくのがオススメです。

```shell
mkdir -p ~/workspace/clamav-test/tests/
mv ~/Downloads/eicar.* ~/workspace/clamav-test/tests
```

## ClamAVでのスキャン方法

スキャンを実行するコマンドには `clamscan` と `clamdscan` があります。名前が似ていることもあり、両者の違いに対する説明がStack Overflowなどに溢れています。簡単にまとめると以下のようになります。

| 比較項目 | clamscan | clamdscan |
| --- | --- | --- |
| 実行スレッド | シングルスレッド | マルチスレッド |
| ウィルスデータベースのロードタイミング | 実行時 | `clamd` コマンド実行時 |
| スキャンオプションの設定方法 | コマンドラインオプション | `clamd.conf` ファイル |

手元のファイルをちょっとスキャンしたいなら `clamscan` 、定期実行したり、大量のディレクトリをスキャンしたいなら `clamdscan` が便利です。

## clamscanの使い方

以下のコマンドでスキャンを実行できます。

```shell
sudo clamscan <options> <path to scan directory or file>
```

よく使うコマンドラインオプションは以下の通りです。

- `-r`: ディレクトリを再帰的に走査します
- `-i`: ウィルスに感染したファイルのみを出力します
- `-l <log file>`: 結果を<log file>に出力します
- `--max-filesize=<number>`: ここに指定したファイルサイズ以上のファイルをスキップします。デフォルトは25MBに設定されています。 `--max-filesize=100M` のように指定します
- `--max-scansize=<number>`: ここに指定したファイルサイズ以上の圧縮ファイルをスキップします。 `--max-scansize=300M` のように指定します
- `--bell`: ウィルス発見時にベルを鳴らします

ちょっとしたファイルのスキャンなら、下のように指定するのがオススメです。

```shell
sudo clamscan -r --bell -i --max-filesize=100M -l scan.log <path to directory>
```

## clamdscanの使い方

`clamdscan` は実行前に `clamd` が実行されている必要があります。実行前に `sudo systemctl status clamav-daemon.service` を実行してdaemonが実行されていることを確認してください。

`clamdscan` は以下のように使用します。

```shell
sudo clamscan <options> <path to scan directory or file>
```

よく使うコマンドラインオプションは以下の通りです。

- `-m`: マルチスレッドで実行します
- `--fdpass`: ファイルへのアクセス権をclam daemonへ委譲します。 `clamav` userがアクセスできないファイルに対してスキャンを行いたい場合に指定します
- `-l <log file>`: 結果を<log file>に出力します
- `--verbose`: より詳しいログを出力します
- `--stdout`: 標準出力にもログを出力します
- `--config-file=<config path>`: 指定したパスの設定ファイルを読み込みます

なお、 `--config-file` を指定して設定ファイルを読み込ませる場合は事前にその設定ファイルを読み込ませた `clamd` を実行しておく必要があります。

```shell
sudo clamd -c <config path> -F
```

実行すると500MB近くメモリを使用しつつ、シグネチャをロードします。 `-F` オプションはコマンドをフォアグラウンドで実行するためのオプションです。Ctrl+Cで気軽に落とせるようになるので、設定ファイルの編集をしている時は付けておくことをオススメします。

### clamd.confの書き方

clamdの設定ファイルについて、詳しくは [こちら](https://docs.clamav.net/manual/Usage/Configuration.html) を参照してください。ここでは設定ファイルを読み込ませる上で最低限必要な設定とよく使う設定について解説します。

まず以下のコマンドでサンプルのコンフィグを生成します。

```shell
clamconf -g clamd.conf > clamd.conf
```

適当なエディタで `clamd.conf` を開いたら、まず `Example` を以下のようにコメントアウトします。

```
# Comment out or remove the line below.
# Example
```

さらに、 `LocalSocket` と `LocalSocketMode` のオプションをアンコメントします。

```
# path to a local socket file the daemon will listen on.
# Default: disabled
LocalSocket /tmp/clamd.socket

# Sets the permissions on the unix socket to the specified mode.
# Default: disabled
LocalSocketMode 660
```

これで必要最低限の設定は完了です。以下のコマンドを実行してconfigを読み込ませられるかテストします。

```shell
sudo clamd -c ./clamd.conf -F
```

問題が無ければ別の端末で `clamdscan` を実行します

```shell
sudo clamdscan --config-file=./clamd.conf -m --fdpass -l ./log/test_basic.log ./tests/
```

以下のような結果が得られれば成功です

```
--------------------------------------
/home/username/workspace/clamav-test/tests/eicar.com.txt: Win.Test.EICAR_HDB-1 FOUND
/home/username/workspace/clamav-test/tests/eicar_com.zip: Win.Test.EICAR_HDB-1 FOUND
/home/username/workspace/clamav-test/tests/eicarcom2.zip: Win.Test.EICAR_HDB-1 FOUND

----------- SCAN SUMMARY -----------
Infected files: 3
Time: 0.011 sec (0 m 0 s)
Start Date: 2022:10:31 15:53:10
End Date:   2022:10:31 15:53:10
```

`clamd.conf` でよく使うオプションは以下の通りです。

- `LogFile <path to log file>`: ログファイルのパスです。なおこのログは `-l` オプションで指定するログファイルとは独立して存在します。
- `LogFileMaxSize <number>`: ログファイルの最大サイズを指定します。 `10M` や `100k` のようにしてサイズ指定します。0で制限を無くします。
- `LogTime <yes/no>`: `yes` にすると、ログに時間表記が付きます
- `LogClean <yes/no>`: `yes` にすると、ウィルスに感染していない正常なファイルのスキャン結果もログに表示します。デバッグ時に便利です。
- `LogVerbose <yes/no>`: `yes` にすると、より詳しいログを出力します。
- `ExtendedDetectionInfo <yes/no>`: `yes` にすると、ウィルスのサイズやハッシュなど、より詳しい情報をログに出力します。
- `MaxScanSize <number>`: `clamscan` で言う所の `--max-scansize` です。ここに指定したファイルサイズ以上の圧縮ファイルをスキップします。 `300M` のように指定します
- `MaxFileSize <number>`: `clamscan` で言う所の `--max-filesize` です。ここに指定したファイルサイズ以上のファイルをスキップします。 `100M` のように指定します
- `MaxRecursion <number>`: 圧縮ファイルの中の圧縮ファイルを最大何回まで展開するかの指定です。デフォルトは17です。
- `MaxFiles <number>`: 圧縮ファイルをスキャンする際のファイルの最大数です。デフォルトは10000です。
- `MaxDirectoryRecursion <number>`: 再帰的にディレクトリを操作する際の最大数です。デフォルトは15です。
- `MaxThreads <number>`: マルチスレッドオプションが指定された際の最大のスレッド数です。デフォルトは10です。

特に `MaxThreads` はRaspberry Piや薄さと軽さに振り切ったノートパソコンなど、 **CPUの冷却に難があるハードウェア** でスキャンを実行する際に指定することをオススメします。最大コア数の半分くらいのスレッド数を指定すると比較的安定します。

以上が基本的なClamAVの使い方です。評判が良ければウィルスが検出された際の挙動を設定する `VirusEvent` や定期実行の設定方法などを追記していきます。

最後にこの記事を書くに当たって参考にしたサイトを載せます。

40

4