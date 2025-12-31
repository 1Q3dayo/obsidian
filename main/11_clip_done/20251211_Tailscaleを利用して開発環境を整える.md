---
title: "Tailscaleを利用して開発環境を整える"
source: "https://zenn.dev/chamafoobar/articles/8ccdb552ef0acf"
author: ""
published: "2025-12-06"
created: "2025-12-11"
description: ""
tags:
  - ""
  - "raw"
---

29

10[tech](https://zenn.dev/tech-or-idea)

この記事は [仮想通貨botter Advent Calendar 2025](https://qiita.com/advent-calendar/2025/botter) の6日目の記事です。

こんにちは、ちゃま([@chamafoobar](https://x.com/chamafoobar))と申します。

今回は「Tailscale」というサービスを利用してVPNを構築し、仮想通貨botter用の開発環境を整備する方法をご紹介します。

## Tailscaleとは

Tailscale は非常に簡単にVPNを構築可能なサービスです。  
E2E 暗号化には WireGuard ベースのプロトコルを使用しており、クライアントなど主要コンポーネントの [コード](https://github.com/tailscale/tailscale) は GitHub で公開されています。  
[SOC2レポート](https://tailscale.com/legal) も取得しており、データの取り扱いにも気を使っているようです。

## botterがどう使うのか

私は Tailscale を以下のように利用しています。

1. 自宅にある開発用の Linux server に外出先から安全にSSHアクセスする  
	前提として、開発環境のserverは可用性は不要だがスペックは欲しいという場合が多いかと思います。
	個人レベルだとクラウドを利用するよりも自宅にLinux serverを置く方がスペックやコストをコントロールしやすいと考え私自身、自宅に開発用serverを置いています。  
	VPNを構築することで、VS CodeのRemote - SSH などで自宅でも外出先でも簡単かつ安全に同じ環境で開発が行えます。
	Tailscale がなくても可能ですが、踏み台サーバとSSHトンネルの設定が必要になります。 [^1]
2. ダッシュボードツールなどを安全に自分だけがアクセスできるようにする  
	要はSSH以外でも接続できるよって話なだけですが、ホストしているダッシュボードなどを自分だけがアクセスできるようにします。botterは性質上、自分さえアクセスできれば良い(自分以外に見せたくない)ダッシュボードなどがあることも多いと思います(例. 損益グラフを表示するダッシュボードなど)。
	こういったダッシュボードを外出先などでも確認したい場合、VPNを利用しない場合であればインターネットに公開した上で、自分だけがアクセスできるようにアクセス制限をすることになるかと思います。
	その場合、以下のような設定を行うことになるかもしれません。
	- Domainの取得
	- httpsアクセスできるよう証明書の取得
	- (id/password認証を避け)SSO等でログインできるようOIDCなどの設定
	いずれもやらずともインターネットから表示自体はできますがセキュリティの観点などから設定する場合が多いかと思います。VPN内を一度構築してしまえばこれらがなくても一定程度安全と言えるでしょう。 [^2]  
	もちろん、パブリッククラウドのマネージドなサービスを利用することでこれらの煩雑な設定作業を減らすことは可能ですが今度はコストが気になるところです。

## 実際にやってみる

文章で書いても便利さがあまり伝わらないので実際にやってみたいと思います。  
Tailscaleは [無料プラン](https://tailscale.com/pricing) があり、無料でできる範囲で十分に実用的です。

### SSHで開発環境にアクセスできるようにする

アカウントを作成するとVPNに参加させる最初のデバイスを追加するように言われます。

ここでは普段持ち運んでいるmacbook proから自宅にある開発用のLinux serverに接続するシナリオを考えます。

![](https://storage.googleapis.com/zenn-user-upload/dcb9797fc809-20251201.png)  
*最初のデバイスを追加する*

追加したい端末のOSを選択すると追加方法が表示されます。  
まずは自宅のLinux serverを追加してみます。表示されたコマンドをコピペで実行し、暫く待つと以下のような表示なります。  
![](https://storage.googleapis.com/zenn-user-upload/328b248faad8-20251201.png)  
*コピペして待つだけ*

指示に従いコマンドを実行します。  
![](https://storage.googleapis.com/zenn-user-upload/2c169b73ea31-20251201.png)  
*表示されたURLにアクセスして認証をする*

表示されたURLをクリックすると認証が求められるので続行します。  
続行すると、デバイスをVPNに接続してよいか確認されるのでConnectしましょう。  
![](https://storage.googleapis.com/zenn-user-upload/0733418f9ca7-20251201.png)  
*Connectを押してVPNに参加*

これで一台目のデバイスをVPNに参加させることができました。  
二台目のデバイスとしてmacbook proを追加します。  
![](https://storage.googleapis.com/zenn-user-upload/380d8de84ef4-20251201.png)  
*二台目のデバイスの追加画面*

macはクライアントappがあるので表示されているURLからインストールします。  
![](https://storage.googleapis.com/zenn-user-upload/20be0135c842-20251201.png)  
*app storeでインストール*

それ以外にもAdmin Consoleから必要な数だけVPNに追加することが可能です。無料プランは100台まで追加可能。画像は一部マスキングしていますが三台のデバイス(Machines)がConnectedになっています。  
![](https://storage.googleapis.com/zenn-user-upload/4e3a13be747b-20251201.png)  
*tailscale admin console*

ひとまず必要な設定ができたら実際にVPN経由でアクセスしてみます。  
ここではmacbook pro -> Linux server(chama)へのSSHアクセスをvscodeを利用して行います。  
![](https://storage.googleapis.com/zenn-user-upload/72cf6fb2770b-20251201.png)  
*macbook proからchamaへアクセスします(さっきまでマスクしてた意味無くなってますが御愛嬌ｗ)*

Tailscaleでは [magicDNS](https://tailscale.com/kb/1081/magicdns) という仕組みによってVPN内の名前解決が可能となっており、デフォルトではmachine nameが利用されます。

つまり、SSHであれば、 `ssh chama` と打つだけでアクセスできるようになります。  
vscodeなら以下のようにSSH接続の際に `chama` と入力するだけです。  
![](https://storage.googleapis.com/zenn-user-upload/7c5ea83ba81a-20251201.png)  
*machine名でアクセス可能(設定で別名に変更も可能です)*

あとはここで自由に開発するだけです。  
自宅のデバイスだろうが外出先のノートPCだろうがTailscaleの設定がしてあれば同様にアクセス可能です。  
![](https://storage.googleapis.com/zenn-user-upload/01e9c4c962dd-20251201.png)

### 自分専用のダッシュボードサイトにアクセスできるようにする

Tailscaleの設定方法としてはここまでの説明で終わりなのですが、便利な使い方としてTailscaleはVPNを構築するサービスなので接続方法はSSHに限る必要がありません。

例えば、損益グラフをgrafanaで表示していて、外出先でもこれを確認したいとします。  
このように損益グラフを可視化することはbotterの中では比較的一般的なように思います。  
また、こういったダッシュボードはあまり他の人には見られたくないはずでしょう。

Tailscaleを利用してVPN内のVPSや自宅のサーバなどでダッシュボードをホストすることで簡単かつ安全に外出先からもアクセスできるようになります。

試してみます。  
以下のコマンドでgrafanaを起動してみます。(dockerを入れていない場合は入れてください。)  
![](https://storage.googleapis.com/zenn-user-upload/78dca8f1259d-20251205.png)

grafanaを起動したmachine名をtailscale admin consoleで確認します。  
前述の通りmagicDNSという仕組みによってこのmachine名でアクセスが可能になります。

![](https://storage.googleapis.com/zenn-user-upload/72cf6fb2770b-20251201.png)  
*machine名を再掲*

SSHと同様今回はchamaというmachineでgrafanaを起動して、macbook proからアクセスする構図です。

ブラウザのアドレスバーにmachine名とport番号を入れます。grafanaは3000番を利用しているので `chama:3000` になります。

![](https://storage.googleapis.com/zenn-user-upload/bf300bb7105b-20251205.png)  
*machine名でアクセスできました(/loginは自動でリダイレクトされます)*

本題とそれるので細かく触れませんが、もし3000という数字を入力するのも手間であれば [caddy](https://caddyserver.com/docs/quick-starts/reverse-proxy) などで80番にreverse proxyすればよいでしょう。

## 注意

Tailscale側に障害が発生すると新しい接続の確率などができなくなり、VPN内の端末にアクセスができなくなる場合があります。  
障害が発生した場合でもアクセスしたいなどの要件があれば前述した踏み台サーバを用意する方法でワークアラウンドを用意しておくと良いかもしれません。  
また、Tailscale側の障害情報については以下から確認ができます。

右上の `subscribe to updates` からslackに障害情報を通知することも可能なので自分は設定しています。

## 終わりに

今回はTailscaleの利用方法について紹介しました。  
AIでコードの作成が極めて簡単になった現代で、少しでも快適な開発環境を整備することが重要ではと考え今回の記事を作成しました。  
この記事がなにかのお役に立てば幸いです。  
Xやっているのでよろしければフォローお願いします。

脚注

29

10

[^1]: このやり方は以前まちゅけんさんがスクラップで紹介されていました。 [https://zenn.dev/mtkn1/scraps/1f6158237239d5](https://zenn.dev/mtkn1/scraps/1f6158237239d5)

[^2]: VPN内であってもこれらの設定は行った方が望ましいことが多いですが、個人開発のbotにおいて手間とのトレードオフから自分はそこまでせずとも必要十分かなと考えています。