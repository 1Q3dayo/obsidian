---
title: "爆速CLI入門 ~最初に知りたかったTips~"
source: "https://zenn.dev/mozumasu/articles/mozumasu-cli-beginner"
author:
  - "[[Zenn]]"
published: 2025-12-02
created: 2025-12-04
description:
tags:
  - "clippings"
  - "raw"
---
137

57[tech](https://zenn.dev/tech-or-idea)

この記事は [TechBullのアドカレ](https://adventar.org/calendars/11900) 2日目の記事です。

## はじめに

怠惰はプログラマの美徳である。  
CLIはそんな怠惰人間を支えてくれる最強の相棒である。

キーボードだけで操作し、自動化を積み重ねていく。  
そんな世界へ踏み込もうとすると、最初の一歩で壁にぶつかる。  
本を開けば呪文のようなコマンドオプションが並び、由来もわからない。  
man や help があると言われても英語がつらい。  
何から手をつければいいのかもわからない。

そこで、この記事では「最初に知りたかった」 CLI の Tips を紹介していく。

### 自分の使っているシェルを確認しよう

現在使用しているシェルは以下の環境変数から確認できる。

- `$SHELL` → ログインシェルの設定（標準で設定しているシェル）
- `$0` → 現在動いてるシェル または 実行中スクリプト名

```shell
# 現在のシェルを確認
echo $0
# ログインシェルを確認
echo $SHELL
```

この記事では zsh を例に解説していく。  
シェルを合わせたい場合は以下のコマンドで zsh に変更できる。

```shell
# 今のセッションだけzshにする
zsh
# デフォルトでzshを使うようにする
chsh -s /bin/zsh
```

コラム: 過去にハマったトラブル

CLIツールのアップデート時に、普段使用しているコマンドが使えなくなったことがある。  
こういった場合に、 `echo $0` と `echo $SHELL` を確認してみると自分のシェルの状態を確認できる。

```shell
# トラブル時の状態

# 標準で使用するシェルはzsh
$ echo $SHELL
/bin/zsh

# なのに実際に起動しているシェルはbash
$ echo $0
bash
```

この結果から、本来zshで起動するはずが、実際にはbashが起動してしまっていることが分かる。  
そのため、zshの設定ファイルが読み込まれずコマンドが使えなくなっていたのだ。

zshの設定ファイルから、アップデートしたCLIツールの古い設定の読み込み箇所を削除し、該当のツールを再インストールすることで元に戻すことができた。

こういったトラブルシューティングにも役立つので、ぜひ覚えておいてほしい。

## キーバインド → bindkeyを打て!

ぜひ最初に把握しておいてほしい物がある。それはキーバインドだ。  
どのツールを使う上でも必ずキーバインドを抑えておくのが上達のコツである。  
事前に取りのぞける「めんどう」は取りのぞいておこう。  
もちろん全てを覚える必要はない。よく使うものから覚えていけばよい。

ところで、君は zsh のキーバインドをいくつ知っているだろうか?  
せっかくなので数えてみよう。

足並みをそろえるために、まずは設定ファイルを読み込まずにまっさらなzshを起動しよう。

```shell
# 設定ファイルを読み込まずにzshを起動
# zsh -fでも同じことができる
zsh --no-rcs
```

キーバインドは `bindkey` コマンドで確認できる。  
そう、デフォルトでキーバインドのチートシートが用意されているのだ。  
記憶力が乏しい私のような人間にもCLIは親切である。

```shell
# キーバインド一覧の表示
bindkey
```

実行すると以下のような内容が表示されるはずだ。  
左側にキーバインド、右側にその動作が表示されている。  
`^` は Control キーを表している。

```shell
bindkey

# 出力例
# "^A"-"^C" self-insert
# "^D" list-choices
# "^E"-"^F" self-insert
# "^G" list-expand
# "^H" vi-backward-delete-char
# <省略>
```

さて、ここで `wc` (word count) コマンドを使ってキーバインドの数を数えてみよう。  
`-l` オプションは `--lines` の略で、改行を数えるオプションである。

```shell
# キーバインドの数を数える
bindkey | wc -l

# 出力結果
      31
```

「31個も覚えられない!」と思ったかもしれない。  
安心してほしい。これは重複したキーバインドも含まれている。  
重複を除くならこうする。

```shell
# 重複を除外してキーバインドの数を数える
bindkey | awk '{print $2}' | sort | uniq | wc -l

# 出力結果
      17
```

重複を除くと17個まで減った。  
案外覚えられそうな数ではないだろうか?

### 長いコマンドとの向き合い方

上のコマンドを見て、「こんなの覚えられないよ~」と思った人もいるかもしれない。  
長いコマンドがでてきたら `|` (パイプ) ごとに実行してみると理解しやすい。

まず、 `bindkey` コマンドだけを実行してみる。

```shell
bindkey

# 出力結果
# "^A"-"^C" self-insert
# "^D" list-choices
# ...
```

そして、次に `awk '{print $2}'` をつなげてみる。  
出力を比べてみると、1列目のキーバインドの表記が消え、2列目のみ表示されている。  
ここで、 `awk '{print $2}'` が「2列目を取り出す」という意味であることがわかる。

```shell
bindkey | awk '{print $2}'

# 出力結果
# self-insert
# list-choices
# ...
```

次に `sort` をつなげてみる。  
出力結果を見ると、重複したものがまとめられていることがわかる。

```shell
bindkey | awk '{print $2}' | sort

# 出力結果
# accept-line
# accept-line
# bracketed-paste
# clear-screen
# down-line-or-history
# down-line-or-history
# ...
```

`uniq` をつなげてみると、重複が取り除かれていることがわかる。

```shell
bindkey | awk '{print $2}' | sort | uniq

# 出力結果
# accept-line
# bracketed-paste
# clear-screen
# down-line-or-history
# ...
```

最後に `wc -l` をつなげてみると、先ほどの出力結果の行数が数えられていることがわかる。

```shell
bindkey | awk '{print $2}' | sort | uniq | wc -l
```

このように、長いコマンドはパイプごとに分解してみると案外理解できるものだ。  
コマンドに慣れるには分解して試してみるのが一番である。

コラム: alias と functions コマンド

`bindkey` と同じように、エイリアス一覧や関数一覧を表示するコマンドもある。  
引数を渡すと、その名前のエイリアスや関数の内容を表示してくれる。

```shell
# エイリアス一覧の表示
alias
# 関数一覧の表示
functions
```

### キーバインドのモード

実はシェルのキーバインドにはvimモードとemacsモードがある。  
現在のキーバインドモードを確認するには以下のコマンドを実行しよう。

```shell
# キーバインドモードの確認
bindkey -lL main

# 出力例

# vimモードの場合
# bindkey -A viins main

# emacsモードの場合
# bindkey -A emacs main
```

たいていの環境では emacsモードがデフォルトになっているため、emacsモードに変更することをオススメする。

```shell
# emacsモードに変更
bindkey -e
```

これは余談だが、 emacs モードの方がキーバインドの数が多い。

```shell
bindkey | awk '{print $2}' | sort | uniq | wc -l

#     69
```

### 設定の永続化

この設定を今回のセッションだけではなく、永続化したい場合は zshの設定ファイル (`~/.zshrc` など) に追記しよう。

~/.zshrc

```shell
bindkey -e
```

また、設定ファイルを更新したら以下のコマンドで再読み込みしよう。

```shell
# 設定を読み直すために、ログインシェルとして起動しなおす
exec $SHELL -l
```

### おすすめキーバインド

キーバインド一覧の中から、特によく使うものをピックアップして紹介しよう。

#### 初級

まずはここから。

```shell
# Mac標準でも使える
"^F" forward-char                 # 1文字右へ移動
"^B" backward-char                # 1文字左へ移動
"^P" up-line-or-history           # ひとつ前の履歴を呼び出す (↑)
"^N" down-line-or-history         # ひとつ次の履歴 (↓)

"^A" beginning-of-line            # 行頭へ移動
"^E" end-of-line                  # 行末へ移動

"^D" delete-char-or-list          # カーソル位置の文字を削除 何も無い行で押すとシェル終了
"^K" kill-line                    # カーソル以降を削除
"^Y" yank                         # ^K や ^W などで消したものを貼り付け
"^T" transpose-chars              # 隣り合う2文字を入れ替える (typo直しに便利)

# シェルで使える
"^H" backward-delete-char         # バックスペース
"^W" backward-kill-word           # 1単語削除
"^U" kill-whole-line              # 行全削除
"^L" clear-screen                 # 画面クリア (clear コマンドと同じ)
```

#### 中級

意外と知られていないのに便利なやつ。

```shell
"^Q" push-line                    # 今入力している行を一時退避. 別のコマンドを打って戻りたい時に便利
"^_" undo                         # 編集の取り消し

# Metaキー (^[) 系
"^[f" forward-word                # 単語単位で右へ移動
"^[b" backward-word               # 単語単位で左へ移動
"^[q" push-line                   # 行退避. ^Q がターミナル側で使われている環境向け
"^[." insert-last-word            # 直前のコマンドの「最後の引数」を挿入 連打でさらに遡れる
"^[H" run-help                    # 現在入力中のコマンドのヘルプを開く (zsh固有)
"^[?" which-command               # カーソル位置の単語がどのコマンドかを表示(zsh固有). PATH上の実体も確認できる
```

コラム: run-help をより便利にする設定

初期状態だと、run-help は `man` コマンドのエイリアスになっているだけで、zsh固有のヘルプ機能が使えない。

```shell
# run-help の実態を確認
type run-help
# run-help is an alias for man
```

> run-help=manの設定は zsh の ソースコード内でされている
> 
> zsh/Src/hashtable.c
> 
> ```
> /* add the default aliases */
> aliastab->addnode(aliastab, ztrdup("run-help"), createaliasnode(ztrdup("man"), 0));
> aliastab->addnode(aliastab, ztrdup("which-command"), createaliasnode(ztrdup("whence"), 0));
> ```
> 
> ref: [https://github.com/zsh-users/zsh/blob/master/Src/hashtable.c#L1214-L1216](https://github.com/zsh-users/zsh/blob/master/Src/hashtable.c#L1214-L1216)

zsh固有のヘルプ機能を使うには、以下の設定を追加しよう。

~/.zshrc

```
unalias run-help 2>/dev/null
autoload -Uz run-help
```

設定すると、 run-help の実態が関数になっていることが確認できる。

run-helpの関数の中身は `functions run-help` で確認できる。

この設定により、 `functions` コマンドのような、man では見つからない zsh 固有のコマンドのヘルプも開けるようになる。

```shell
# man で開こうとしてもマニュアルが見つからない
man functions
# No manual entry for functions
```

コマンドを入力して `ESC→H` (run-help) を実行すると、マニュアルが見つかる。

```shell
# コマンドを入力して
functions # ESC→H でマニュアルが開く
```

![run-help functions](https://res.cloudinary.com/zenn/image/fetch/s--rAXNhCne--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/c3dc096f6260c3cf68d21628.png%3Fsha%3D2e59dd04d62b252cc4997f2032101d186a8affcd)

`/^ *functions` で検索して該当箇所にジャンプできる

![run-help functions jump](https://res.cloudinary.com/zenn/image/fetch/s--eAAlKBbz--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/29600674132c6dcd79806326.png%3Fsha%3D96aed117d66c41e7feb508fd7e32bb2cc0806d67)

コラム: bindkey に出ないのに使えるキーがある理由

`Control + z` を押すと、今のコマンドが一時停止 (suspend) する。  
しかし、 `bindkey` を見ても、そのキー設定は出てこない。  
これはなぜか?

じつは、シェルに文字を送るまでには “二つの層” がある。

```
[ キーボード ]
      ↓
[ 端末(tty) ← OS がキー入力を先に処理する場所 ]
      ↓
[ シェル(zsh / bash) ← bindkey が見ているのはここだけ ]
      ↓
[ コマンド実行 ]
```

`bindkey` が教えてくれるのは、シェルが持っているキーバインドだけ。  
一方で `Control + z` のような「プロセスを止めるキー」は、OS の端末(tty) が先に処理している。

そのため、 `Control + z` は使えるのに、 `bindkey` の一覧には出てこないのだ。

端末(tty)で使えるキーは `stty -a` で確認できる。

```shell
# 端末 (tty) の設定を表示
stty -a

# 出力結果
# <省略>
# cchars: discard = ^O; dsusp = ^Y; eof = ^D; eol = <undef>;
#         eol2 = <undef>; erase = ^?; intr = ^C; kill = ^U; lnext = ^V;
#         min = 1; quit = ^\; reprint = ^R; start = ^Q; status = ^T;
#         stop = ^S; susp = ^Z; time = 0; werase = ^W;
```

ちなみに、suspend (一時停止) したプロセスは `fg` コマンドで再開できる。

```shell
# 直前の一時停止したプロセスを再開
fg

# suspend したプロセスの確認
jobs

# 再開したいジョブを指定して再開
fg %2
```

私は `Control + z` でsuspendをトグルできるようにしている。  
プロセス実行中に `Control + z` を押すと一時停止、再度 `Control + z` を押すと再開する。

```shell
#! /usr/bin/env zsh

fancy-ctrl-z () {
  if [[ $#BUFFER -eq 0 ]]; then
    BUFFER=" fg"
    zle accept-line
  else
    zle push-input
  fi
zle clear-screen
}
zle -N fancy-ctrl-z
bindkey '^Z' fancy-ctrl-z
```

> 参照:

#### 上級者

デフォルトで設定されていないキーバインドたち。  
全部知ってる人はシェルマスター。

```shell
'^X^R' redo                     # 実はデフォルトで設定されていない
'^[e'  edit-command-line        # 現在行を $EDITOR で編集
'^p'   history-beginning-search-backward-end  # 入力内容で前方一致検索
'^n'   history-beginning-search-forward-end   # 入力内容で前方一致検索
```

それぞれのキーバインドについて紹介してく。

##### redo

undo は知ってるのに redo を使っていない人はけっこう多い。  
以下のように設定しておくと、Control-\_ (undo) をしすぎた時に、Control-x Control-r でやり直しができる。

~/.zshrc

```shell
# Control-x Control-r で redo
bindkey '^X^R' redo
```

##### edit-command-line

コマンドを編集しているとふと vim のキーバインドが恋しくなる時がある。  
そんな時は `edit-command-line` がオススメだ。

以下の設定を追加しておくと、 `Esc→e` で現在の行を `$EDITOR` で開けるようになる。

~/.zshrc

```shell
# edit-command-line を読み込む
autoload -Uz edit-command-line
zle -N edit-command-line

# Esc→e (Alt-e) で現在行を $EDITOR で編集
bindkey '^[e' edit-command-line
```

##### history-beginning-search-backward-end / history-beginning-search-forward-end

Control-p / Control-n を単なる履歴の上下ではなく、 **今入力している文字列で前方一致する履歴だけをたどる** ことができる。  
例えば、docker と入力してから Control-p を押すと、docker で始まる過去のコマンドだけをたどれる。  
前方が一致している単語だけをたどるので、目的のコマンドにたどり着きやすい。

設定は以下の通り。

~/.zshrc

```shell
# 前方一致履歴検索のベースになるウィジェットを読み込む
autoload -Uz history-search-end

# 前方一致しながら行末にカーソルを置くウィジェットを定義
zle -N history-beginning-search-backward-end history-search-end
zle -N history-beginning-search-forward-end  history-search-end

# Control-p / Control-n を前方一致履歴検索に割り当て
bindkey '^p' history-beginning-search-backward-end
bindkey '^n' history-beginning-search-forward-end
```

## 使えるコマンドを増やしたい → tlrcで要約チェックだ!

使えるコマンドを増やしたい、でも何をどこまで抑えておくべきかわからない。  
そんな時に便利なのが tldrコマンド である。  
実用的な使用例に焦点を当てた、より簡潔なヘルプを確認することができる。

インストールは Homebrew で簡単にできる。

```shell
# tlrcをインストール
brew install tlrc
```

例えば、 `wc` コマンドの使い方を知りたいときは以下のように実行する。

```shell
# tldrでwcの使い方を確認
tldr wc
```

実行すると以下のようなコマンドの使い方の要約が確認できる。

![tldr wc の出力](https://res.cloudinary.com/zenn/image/fetch/s--g8NokZFt--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/b6d4f5c3550faed4aab2ae31.png%3Fsha%3D910b5d92100ce17fd16afa11fab8160209b820b3)  
*tldrコマンドでwcコマンドの使い方を確認*

## オプションが覚えられない → helpとmanは最高の情報源

オプションといえば、 `ls -la` でいう `-la` の部分である。  
そう、あのパっとみて何かわからないやつのことである。  
オプションは何の略か確認すると頭に入りやすい。  
そんな時に使えるのが `--help` と `man` である。

例えば、 `tldr` のコマンドオプションを確認したいときは以下のように実行する。

```shell
tldr --help

# Options:
#   -u, --update                    Update the cache
#   -l, --list                      List all pages in the current platform
#   -a, --list-all                  List all pages
```

出力を見ると、 `-u` は `--update` の略であることがわかる。  
また、manコマンドでより詳しい情報を確認することもできる。

```shell
man tldr
```

![man tldr の出力](https://res.cloudinary.com/zenn/image/fetch/s--qRU2J9Zx--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/cc88991dfccc4f4f692c99ea.png%3Fsha%3D5b063161b22c03352d99fc21b824f8539736192c)  
*man tldrの出力*

このように `--help` と `man` はコマンドの使い方を知る上で最高の情報源である。

しかし、英語が苦手な人にとっては読むのがつらい。  
そんな人にオススメの対処方法を紹介していく。

## 英語がつらい

英語がつらい人にぜひ試してほしいのが PLaMo翻訳 である。  
ブラウザの拡張機能とCLIツールの両方が提供されている。

PLaMo翻訳の紹介スライドもあるのでぜひ見てほしい。

### PLaMo翻訳のブラウザ拡張機能

拡張機能版はサブスク形式で提供されているが、無料で試せるFreeプランも用意されている。  
ページのレイアウトを崩さずに翻訳できる上に、ショートカットキーひとつで実行できる手軽さが魅力である。  
一度使うと作業の流れがグッと快適になり、手放せなくなるツールのひとつになるはず。

![PLaMo翻訳のデモ](https://storage.googleapis.com/zenn-user-upload/deployed-images/93a96ddd79c716dc752c68f8.gif?sha=fae029db233031b35371d9c611258b2cca46cee9)  
*動作している様子*

単語単位で知りたい場合はMouse Dictionaryという拡張機能もオススメだ。  
ホバーした単語の意味をポップアップで表示してくれる。

![Mouse Dictionaryのデモ](https://res.cloudinary.com/zenn/image/fetch/s--3zIZrTv9--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/a21c6809dcf9473d3ccea62c.png%3Fsha%3D4fdf5cd27e34045b4e62ba61bfa8adb7966505ee)  
*ポップアップウィンドウのカスタマイズはCSSできるため、自分好みにできるのも嬉しいポイント。*

### PLaMo翻訳のCLIツール: plamo-translate-cli

plamo-translate-cli は、 [plamo-2-translate](https://huggingface.co/pfnet/plamo-2-translate) という翻訳用の言語モデルをローカル環境で使うためのCLIツールである。

インストールは uv コマンドで簡単にできる。

```shell
# plamo-translate-cliをインストール
uv tool install plamo-translate-cli

# uvが無い場合は以下のコマンドでインストール
brew install uv
```

> 参照: [uv — Homebrew Formulae](https://formulae.brew.sh/formula/uv)

`| plamo-translate --to <言語>` のようにパイプで繋いで使うことができる。

```shell
# plamo-translateのプロセスを起動
# これによりモデルの読み込み時間をスキップできる
plamo-translate server

# tldr wcの出力を日本語に翻訳
tldr wc | plamo-translate --to Japanese
```

![plamo-translate-cliのデモ](https://res.cloudinary.com/zenn/image/fetch/s--WOcU42o6--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/84cdbe5ba6fce9d215a43f45.png%3Fsha%3D34d9f081cce25676d9c49c95af3734abbe7dabb3)  
*実際に翻訳してみた様子*

### Ghostでプロセス管理

plamo-translate-cli のプロセス用にタブを一つ占有するのはもったいない。  
そんな時に便利なのが Ghost である。

Ghost は シンプルなバックグラウンドプロセス管理ツールで、TUIでプロセスの状態を確認できる。

![ghost TUI](https://res.cloudinary.com/zenn/image/fetch/s--VG_T7Fpx--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://github.com/skanehira/ghost/raw/main/images/ghost.png?_a=BACAGSGT)

ghostインストール

公式ドキュメントより引用

```shell
git clone https://github.com/skanehira/ghost.git
cd ghost
cargo build --release
```

`ghost run <管理したいコマンド>` でバックグラウンド実行できる。  
なので、plamo-translate-cli のサーバーのプロセスを ghost で管理するには以下のコマンドを実行すればよい。

```shell
# ghost run で plamo-translateのサーバーをバックグラウンド実行
ghost run plamo-translate server
```

プロセスは `ghost` コマンドで確認できる。

```shell
# TUIでプロセス管理
ghost
```

### manの日本語化

ここまでで help や tldr を使ってコマンドの使い方を調べる方法を紹介した。  
せっかくなら **man コマンドも日本語で読みたい** と感じる人もいるはず。

じつは man の日本語マニュアルを翻訳・公開している JM Project というプロジェクトがある。  
ここで配布されている日本語 man ページを入れておくと、標準コマンドの説明を自然な日本語で読めるようになる。

マニュアルのダウンロード手順は以下の通り。  
ダウンロードリンクはこちらにあったものを使用している。

```shell
# 作業用のディレクトリへ移動 (自分はDownloadsディレクトリにした)
cd ~/Downloads

# manの日本語マニュアルページをダウンロード
curl -L -O https://github.com/linux-jm/manual/releases/download/v20251115/man-pages-ja-20251115.tar.gz

# ダウンロードしたファイルを展開
tar xfz man-pages-ja-20251115.tar.gz

# 展開されているかチェック
ls | grep man
# man-pages-ja-20251115
# man-pages-ja-20251115.tar.gz

# 展開したディレクトリに移動
cd man-pages-ja-20251115
```

インストールの際に、インストール先、 ユーザー、グループを指定する必要がある。  
必要な情報をあらかじめ確認しておこう。

インストールの設定を行うには、展開したディレクトリに移動して `make config` を実行する。

設定が完了したら、 `make install` でインストールを実行する。

```shell
make install
```

以下のメッセージが出力されたらインストール完了である。

```shell
# インストール中の出力
-n install GNU_gzip: zmore.1 ..
done.
-n install GNU_gzip: znew.1 ..
done.
```

試しにインストールしたマニュアルで `ls` コマンドを確認してみよう。  
`-M` で使用するマニュアルのパスを指定できる

うまくインストールができていれば日本語のマニュアルが表示される。

![日本語のマニュアル](https://res.cloudinary.com/zenn/image/fetch/s--Mop_2c9u--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/c945ceac14a233374dee3e05.png%3Fsha%3D565dc905dd008948b3832f036d501ee46e7738bf)

毎回パスを設定するのは面倒なので、zshの設定ファイル (~/.zshrcなど) にマニュアルのパスを追加しておくと `man ls` で日本語のマニュアルを参照することができる。

#### manをカラー表示にする

せっかくならカラーでマニュアルが見れたら便利だとは思わないだろうか?  
`MANPAGER` 環境変数で lessコマンド を指定し、 `LESS_TERMCAP` 系の環境変数を設定することで色を付けることができる。

~/.zshrc

```shell
export MANPAGER=less                 # man 専用ページャーとして less を使う
export LESS=-R                       # 色付き表示を保持

export LESS_TERMCAP_mb=$'\e[1;31m'   # 強調 赤
export LESS_TERMCAP_md=$'\e[1;34m'   # 太字 青
export LESS_TERMCAP_me=$'\e[0m'      # reset

export LESS_TERMCAP_so=$'\e[7m'      # 反転
export LESS_TERMCAP_se=$'\e[0m'

export LESS_TERMCAP_us=$'\e[4;32m'   # 下線 緑
export LESS_TERMCAP_ue=$'\e[0m'
```

この設定を追加して再度 `man ls` を実行するとカラーで表示されるようになる。

![man lessでカラー表示](https://res.cloudinary.com/zenn/image/fetch/s--UEGO2RKT--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/1e28bf120885471f57876ad2.png%3Fsha%3D43b0bd0971d87654ff1ef56cbca781d85af0b37e)  
*lessでmanをカラー表示*

man で Neovim を使う場合

もちろん、 man の表示に Neovim を使うこともできる。

~/.zshrc

```shell
export MANPAGER='nvim +Man!'
```

この状態で `man ls` を実行すると、 Neovim でマニュアルが開くようになる。

![man Neovimでカラー表示](https://res.cloudinary.com/zenn/image/fetch/s--pmB0U4Jd--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/bb04445eaaabf37ad8439917.png%3Fsha%3De96bb2c9254c4d64a04669f80a45228359d8167f)  
*Neovimでmanを表示*

この設定は Neovim のヘルプに記載があるので、設定を忘れてしまった場合は `:h :Man@en` で確認しよう。

![:h :Man@en](https://res.cloudinary.com/zenn/image/fetch/s--I6AJOlte--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/cf5aa0be97f02f3942815637.png%3Fsha%3Df3cd61d401b9386cb112465e35c871e2b1e28eae)

Neovimからマニュアルを開きたい場合は、`:Man コマンド名` で開ける。  
シェルスクリプトを書いている時は `K` でマニュアルを開くこともできる。

![カーソル位置のコマンドのマニュアルを開く](https://res.cloudinary.com/zenn/image/fetch/s--5sCJdrbY--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_1200/https://storage.googleapis.com/zenn-user-upload/deployed-images/3f7154aa2da4b5507f52641d.png%3Fsha%3D03035f6a52447a49791390904b6c4e88925a4d46)  
*Neovimでカーソル位置のコマンドのマニュアルを開く*

Neovimが無い場合のインストール方法

Neovimが無い場合は以下のコマンドでインストールできる。

```shell
brew install neovim
```

お試しでリッチな設定がされたNeovimを使いたい場合は、LazyVimがオススメだ。  
すぐに使い始められるNeovimを体験できる。

LazyVim のインストール手順は以下の通り。

> 参照: [🛠️ Installation | LazyVim](https://www.lazyvim.org/installation)

Neovim で開くと、 [プラグインで翻訳](https://zenn.dev/mozumasu/articles/mozumasu-translate-in-vim) もできるので日本語版のマニュアルが無いコマンドでも安心だ。

## おわりに

最初に知りたかった CLI の Tips を紹介してきた。  
参考になれば幸いである。

[GitHubで編集を提案](https://github.com/mozumasu/zenn/blob/main/articles/mozumasu-cli-beginner.md)

137

57