---
title: "「私の環境では動く」を撲滅したDev Container導入記"
source: "https://zenn.dev/nabewata/articles/95361314ebaa30"
author:
  - "[[Zenn]]"
published: 2025-12-07
created: 2025-12-11
description:
tags:
  - "clippings"
  - "raw"
---
3

6[tech](https://zenn.dev/tech-or-idea)

![](https://storage.googleapis.com/zenn-user-upload/556e94754314-20251207.png)

チーム開発で何度も同じ問題にぶつかっていました。

「手元では動くんですけど、本番で動かないんですよね」  
「新しく入った人の環境構築に半日かかった」  
「Node.jsのバージョンが違っててエラーが出た」

READMEに環境構築手順を書いても、OSが違えば微妙に手順が変わる。バージョンを揃えたつもりでも、グローバルに入っているツールが違ったりする。

これ、根本的に解決する方法はないのかな、、、と思っていたときに出会ったのがDev Containerでした。

## Dev Containerとは

VS Code（やCursor）の機能で、開発環境をまるごとDockerコンテナに入れてしまう仕組みです。

仕組みはシンプル。プロジェクトのルートに`.devcontainer` というフォルダを作って、そこに設定ファイルを置く。VS Codeでプロジェクトを開くと「コンテナで開き直しますか？」と聞かれる。Yesを押すと、定義された環境がDockerで立ち上がって、その中で開発できるようになる。

Node.jsのバージョン、必要なCLIツール、データベース、VS Codeの拡張機能まで、全部コードで定義できます。

## 導入してみる

最小構成はびっくりするほど簡単です。

```
your-project/
├── .devcontainer/
│   └── devcontainer.json
└── ...
```

devcontainer.jsonの中身はこれだけ。

```json
{
  "name": "My Project",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",
  "postCreateCommand": "npm install"
}
```

Microsoftが公式で配布しているベースイメージを指定して、コンテナ作成後に `npm install` を走らせる。これだけで、Node.js 20がインストールされた開発環境が手に入ります。

## 実際のプロジェクト構成

実務では、DBやRedisも必要になりますよね。Docker Composeと組み合わせることで、依存サービスもまとめて管理できます。

docker-compose.ymlを用意します。

```yaml
services:
  app:
    image: mcr.microsoft.com/devcontainers/typescript-node:20
    volumes:
      - ../:/workspace:cached
    command: sleep infinity
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: myapp
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres-data:
```

devcontainer.jsonでこのComposeファイルを参照します。

```json
{
  "name": "Full Stack Dev",
  "dockerComposeFile": "docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "prisma.prisma"
      ],
      "settings": {
        "editor.formatOnSave": true
      }
    }
  },

  "postCreateCommand": "npm install",
  "forwardPorts": [3000, 5432, 6379]
}
```

これで、VS Codeでプロジェクトを開いて「Reopen in Container」を押すだけで、Node.js、PostgreSQL、Redisが全部揃った環境が立ち上がります。

## 何が変わったか

導入して数ヶ月経って、明らかに変わったことがいくつかあります。

まず、新メンバーのオンボーディングが劇的に速くなりました。以前は「READMEを読んで環境構築してください」から始まって、詰まるたびにSlackで質問が飛んでくる、という流れでした。今は「Docker Desktopを入れて、リポジトリをcloneして、VS Codeで開いてください。あとは勝手に環境ができます」で終わり。

環境差異によるバグがなくなりました。「手元では動くんですけど」という報告が消えた。全員が同じDockerイメージを使っているので、動くか動かないかは全員同じ。これは精神的にもかなり楽です。

PCを変えても怖くなくなりました。以前は「このPCには何を入れてたっけ」と毎回思い出しながら環境構築していた。今はDocker DesktopとVS Codeさえあれば、あとはcloneするだけで完全な開発環境が復元されます。

## featuresという便利機能

Dev Containerにはfeaturesという仕組みがあって、追加のツールを簡単にインストールできます。

```json
{
  "features": {
    "ghcr.io/devcontainers/features/aws-cli:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-in-docker:2": {}
  }
}
```

AWS CLI、GitHub CLI、Docker-in-Docker。よく使うツールはたいていfeaturesとして公開されているので、JSONに1行追加するだけで導入できます。

Dockerfileを自分で書く必要がないのがありがたい。「このツールをインストールするコマンドなんだっけ」と調べる手間が省けます。

## 気になる点と対策

パフォーマンスの問題はたまに話題になります。特にMacでDockerを使うとファイルI/Oが遅い。

対策としては、マウントオプションに `cached` をつける、 `node_modules` をnamed volumeに逃がす、などがあります。最近のDocker Desktopはかなり改善されているので、以前ほど気にならなくなった印象です。

オフライン環境でも使えるかという質問もよく受けます。一度イメージをpullしておけば、オフラインでもコンテナは起動できます。出張先でWi-Fiがなくても開発可能です。

## まとめ

Dev Containerを導入して、環境構築に関するストレスがほぼゼロになりました。

「clone即開発」が実現できる。環境差異バグが消える。PC移行が怖くない。新メンバーのオンボーディングが一瞬で終わる。

設定ファイルを書く手間は最初だけ。その後はずっと恩恵を受け続けられます。まだ試していないなら、小さなプロジェクトから始めてみることをおすすめします。

3

6

### Discussion

![](https://static.zenn.studio/images/drawing/discussion.png)

ログインするとコメントできます