---
title: "コードレビューではgtrが便利！"
source: "https://qiita.com/Nozomuts/items/0f16c7de2a85a7aad6c8"
author:
  - "[[Nozomuts]]"
published: 2025-12-01
created: 2025-12-04
description: "はじめに GitHubのアップデートは頻繁に行われていて、GitHub上でのコードレビューもしやすくなってきてますね！ ただ、やっぱり手元のエディタで動かしながら確認したいことってありますよね でも、そのために現在の作業を stash したり、ブランチを切り替えて npm..."
tags:
  - "clippings"
  - "raw"
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=)

## Qiitaにログインして、便利な機能を使ってみませんか？

あなたにマッチした記事をお届けします

便利な情報をあとから読み返せます

[ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2FNozomuts%2Fitems%2F0f16c7de2a85a7aad6c8&realm=qiita) [新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2FNozomuts%2Fitems%2F0f16c7de2a85a7aad6c8&realm=qiita)

## はじめに

GitHubのアップデートは頻繁に行われていて、GitHub上でのコードレビューもしやすくなってきてますね！  
ただ、やっぱり手元のエディタで動かしながら確認したいことってありますよね

でも、そのために現在の作業を `stash` したり、ブランチを切り替えて `npm install` し直したりするのは正直面倒です…

そんな課題を解決するのが [gtr (Git Worktree Runner)](https://github.com/coderabbitai/git-worktree-runner) です！  
（なぜ `gtr` と略すのかはわかってないです😇）

## なぜ gtr なのか？

Git標準の `git worktree` を使えばフォルダ単位でブランチを展開できます。  
しかし、コマンドが長くて覚えにくいのが難点でした。  
`gtr` はそれをシンプルにラップし、さらに便利機能を追加したツールです。

### コマンドがシンプル

`git gtr new <branch>` だけで作成完了

### 多様なエディタに対応

VS Code, Cursor, Zed などを指定して即座に開ける

### AIエージェントとの連携

Claude Code や Codex などを、そのブランチで独立して起動可能

### 環境構築の自動化

`npm install` の自動実行や `.env` ファイルのコピーも設定可能

## 導入方法

Git 2.5以上がインストールされている前提です🙏

リポジトリをクローンし、PATHを通すだけで完了します！

```bash
# リポジトリをクローン
git clone https://github.com/coderabbitai/git-worktree-runner.git
cd git-worktree-runner

# 実行ファイルへのシンボリックリンクを作成（またはPATHに追加）
sudo ln -s "$(pwd)/bin/git-gtr" /usr/local/bin/git-gtr
```

Tabキーによる入力補助の設定方法は以下です！（Zsh の例を記載）

```bash
# 1. 補完用ディレクトリを作成し、ファイルをコピー
mkdir -p ~/.zsh/completions
cp /path/to/git-worktree-runner/completions/_git-gtr ~/.zsh/completions/

# 2. .zshrc に設定を追加
cat >> ~/.zshrc <<'EOF'
fpath=(~/.zsh/completions $fpath)
autoload -Uz compinit && compinit
source ~/.zsh/completions/_git-gtr
EOF

# 3. キャッシュをクリアして設定を反映
rm -f ~/.zcompdump*
source ~/.zshrc
```

## 基本的な使い方

使い方は非常にシンプルです。

```bash
# 1. レビュー用ブランチのワークツリーを作成
git gtr new feature/new-ui

# 2. 設定したエディタで開く
git gtr editor feature/new-ui

# 3. CLIベースのコーディングエージェントなどで開く（任意）
git gtr ai feature/new-ui

# --- レビュー終了後 ---

# 4. サクッと削除
git gtr rm feature/new-ui
```

これだけで、メインの作業環境を一切汚さずにレビュー環境を構築・破棄できます！  
もちろん通常の開発でも便利に使えます。

## 便利な連携設定

`gtr` はリポジトリごとに柔軟な設定が可能です。

### 1\. エディタとAIツールの設定

お好みのツールをデフォルトに設定できます。  
特にAIツールをブランチごとに独立して走らせられるのは、並行作業時に強力です。

```bash
# エディタ (code, cursor, zed など)
git gtr config set gtr.editor.default code

# AIツール (claude, aider, copilot など)
git gtr config set gtr.ai.default claude
```

### 2\. 面倒なセットアップを自動化 (Hooks)

ワークツリー作成後に `npm install` などを自動で走らせることができます。「開いたらすぐ動く」状態が作れるので必須級の設定です。

```bash
git gtr config add gtr.hook.postCreate "npm install"
```

### 3\. ファイルの自動コピー

`.env.example` などを新しいワークツリーに自動コピーする設定も可能です。

```bash
git gtr config add gtr.copy.include "**/.env.example"
```

## さらに楽にするTips

頻繁に使うなら、以下の関数を `.zshrc` や `.bashrc` に入れておくと楽でした！

```bash
gtr() {
  git gtr new "$1" && git gtr editor "$1"
}
```

これで `gtr feature/branch-name` と打つだけで、用意できます！

## おわりに

読んでいただきありがとうございます！  
作業の中断もコンフリクトも気にせず、快適なレビューができて便利ですね！  
ぜひ試してみてください！

## 参考

[0](https://qiita.com/Nozomuts/items/#comments)

コメント一覧へ移動

X（Twitter）でシェアする

Facebookでシェアする

はてなブックマークに追加する

新規登録して、もっと便利にQiitaを使ってみよう

1. あなたにマッチした記事をお届けします
2. 便利な情報をあとで効率的に読み返せます
3. ダークテーマを利用できます
[ログインすると使える機能について](https://help.qiita.com/ja/articles/qiita-login-user)

[新規登録](https://qiita.com/signup?callback_action=login_or_signup&redirect_to=%2FNozomuts%2Fitems%2F0f16c7de2a85a7aad6c8&realm=qiita) [ログイン](https://qiita.com/login?callback_action=login_or_signup&redirect_to=%2FNozomuts%2Fitems%2F0f16c7de2a85a7aad6c8&realm=qiita)

[76](https://qiita.com/Nozomuts/items/0f16c7de2a85a7aad6c8/likers)

いいねしたユーザー一覧へ移動

64