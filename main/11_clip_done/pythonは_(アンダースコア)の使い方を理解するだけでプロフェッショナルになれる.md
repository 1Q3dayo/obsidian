---
title: "pythonは_(アンダースコア)の使い方を理解するだけでプロフェッショナルになれる"
source: "https://qiita.com/_Kohei_/items/069aa1e7b872f5ca96bf"
author:
  - "[[_Kohei_]]"
published: 2023-10-30
created: 2025-11-17
description: "1. 第3次AIブームの到来 米Google DeepMindが開発した人工知能（AI）の囲碁プログラム「AlphaGo」が世界トップレベルの実力を持つ韓国のプロ棋士、李世ドル（イ・セドル）九段に4勝1敗と大きく勝ち越したことが着火剤となり、2015年より第3次AIブーム..."
tags:
  - "clippings"
  - "raw"
---
![](https://relay-dsp.ad-m.asia/dmp/sync/bizmatrix?pid=c3ed207b574cf11376&d=x18o8hduaj&uid=217143)

この記事は最終更新日から1年以上が経過しています。

## 1\. 第3次AIブームの到来

米Google DeepMindが開発した人工知能（AI）の囲碁プログラム「AlphaGo」が世界トップレベルの実力を持つ韓国のプロ棋士、李世ドル（イ・セドル）九段に4勝1敗と大きく勝ち越したことが着火剤となり、2015年より第3次AIブームへと突入した。(ちなみにAIが誕生したのは1950～1960年代で第1次AIブームの到来)

---

### 1.1 余談になるがAlphaGo(4億円の知能)はなぜすごいのか？

AlphaGoがそれ以前のチェスや将棋のAIと異なるのは、 **畳み込みニューラルネットワーク（CNN）** を応用している点だ。このCNNはさらに強化学習を行い、自分自身と対局を数千万回も繰り返した。  
間違っていたらすみません、、、、

---

### 1.2 ChatGPTによる生成AIのブーム

ChatGPTに代表されるLLMは以前から開発競争が繰り広げられていた。  
GPT1は2018年に登場し、イーロン・マスクとサム・アルトマンが2015年に設立したOpenAIによって発表されました。  
[参考: GPT-4までの進化の軌跡と違いをまとめてみた](https://toukei-lab.com/gpt#:~:text=%E3%81%9D%E3%81%97%E3%81%A6%E3%81%9D%E3%82%8C%E3%81%8B%E3%82%891%E5%B9%B4%E5%BE%8C,%E3%81%AB%E3%82%88%E3%81%A3%E3%81%A6%E7%99%BA%E8%A1%A8%E3%81%95%E3%82%8C%E3%81%BE%E3%81%97%E3%81%9F%E3%80%82)

---

## 2\. Pythonってすごくない？？

機械学習やデータ解析に必要なライブラリが充実しているだけでなく、Webアプリケーションを開発するフレームワークDjangoの完成度の高さ(*特にセキュリティ面のサポートがすごい*)  
YouTubeも当初Djangoで作られていたような気がする、、、

できないことはないにも関わらず、簡単に書けてしまう。

---

### 2.1 個人的におすすめするのはFastAPI

個人的にはFastAPIを使用した開発がおすすめだ。  
昨今のトレンドはマイクロサービスアーキテクチャで、Djangoを選択するとどうしてもオーバースペックになってしまう。  
学習コストも低く、タイプヒントにも対応しているためチーム開発がやりやすい。

FastAPIを **AWS Lambda** 上に構築し、認証は　 **Cognito** 、ファイル管理は **S3** 、 DBは **Dynamo DB**, **Aurora Serverless** や **Open Search Service** などの構成にすると、サーバレスでフルマネージドなアーキテクチャになるのでスケールしやすくコスパも良くおすすめだ。

下記のようなシステムを個人で作成した。  
もちろんFastAPIをフル活用！！！

[![269824592-305d6e45-d3f5-41d4-88f2-a494221b0b3f.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1130166/92e10942-0fcc-e318-ed4b-9363bba0c664.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F1130166%2F92e10942-0fcc-e318-ed4b-9363bba0c664.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=8f37fc69a85c9a776509b989b87f126c)

**やっぱりPythonってすごい。**

---

## 3\. Pythonは書きやすいが読みにくい？

柔軟なコードが書けるがゆえ、初心者が書いてしまうと **２度見、いや4度見** してしまうコードがたくさんある。  
Pythonは「誰が書いても同じようなコードが完成する」をモットーに作られている、その真理から程遠い俗にいう「 **うんこーど** 」が生まれるのも事実である。

*Pythonのコードが人より上手く書けるように伝授しようではないか*

---

### 3.1 参考にしたサイト

コードや解説はこの方の記事がわかりやすく全く同じように真似しました。  
[参考: Pythonのアンダースコア( \_ )を使いこなそう！](https://medium.com/lsc-psd/pythonic%E8%89%B2%E3%80%85-python%E3%81%AE%E3%82%A2%E3%83%B3%E3%83%80%E3%83%BC%E3%82%B9%E3%82%B3%E3%82%A2-%E3%82%92%E4%BD%BF%E3%81%84%E3%81%93%E3%81%AA%E3%81%9D%E3%81%86-3c132842eeef)

---

## 4\. Pythonを書いているのにアンダースコアの区別がつかないって？

下記のような疑問を抱く初学者は多くいるだろう。  
「 `def __init__(self):` の `__init__` のアンダースコアは何故二つなのか？」

「 `def _function(x):` と `def function(x):` と `def function_(x):` に違いはあるのか？」

 「 `y, _ = _function(x)` のアンダースコアは何か？」

このようにわかりそうでわからないアンダースコアの使い方を、紐解いていこう。

### 4.1. そもそもアンダースコアはいつ使われるのか？

- 戻り値を無視する。
- 関数の名付けで使い方を区別する。
- 数字や文字を読みやすくする。(スネークケース)
- インタプリタで最後に表示された値を代表する。

**以上4種類を意識しアンダースコアを使いこなす事により、読みやすいpythonicなコードを書くことができる。**

##### 1\. Return値を無視

```python
x, _, z = (1, 2, 3)
# x=1, z=3

# * 2つの戻り値を返す関数
def func_return_2():
    return 'X', 'Y'
x, _ = funct_return_2()
# x='X'

# * enumerateはイテレータ(リスト等)の要素とIndexを返す関数
numbers = ["りんご", "ぶどう", "バナナ"]
for idx, _ in enumerate(numbers):
    print(idx)

"""結果
0
1
2
"""
```

これが *一番多いアンダースコアの使い方* だ。  
Pythonはライブラリが沢山あって、関数をインポートして使う事が多い。  
そういう時、もし関数からのreturn値が複数あって使わない部分があった場合、  
アンダースコアを使ってreturn値を使ってないよと、明示的に宣言できる。  
新規で開発に入った人からすると、アンダースコアの変数があると、使わないんだなと理解でき保守運用が上がる。  
**ただ、アンダースコアにも値が埋め込まれており、処理速度が向上するわけではない**

##### 2\. 関数の名付けで使い方を区別

関数の名付けで使うアンダースコアは、アンダースコアの付ける位置と数で関数の使い方を4種類に区別します。  
それぞれ *PEP8のコーディング規約* で定義されている。

### 4.1.1. \_function(x): #関数前に一つ

```python
def _single_leading_underscore(x):
    return something
# weak "internal use" indicator. E.g. from M import * does not 
# import objects whose names start with an underscore
```

関数前に一つアンダースコアを付ける事により、関数を”内部用”に定義できる。  
他のプログラミング言語のPrivate属性と似たような物ですが、  
Pythonには事実上のPrivate属性が存在しない。  
PEP8の説明ではweak internal useと説明されていて、

```python
from M import *
```

の時では,一つのアンダースコアで始まる関数はインポートされませんが、class内の関数だと **classx.\_func()** で関数を呼ぶ事が出来ます。

### 4.1.2. function\_(x): #関数後に一つ

```py
def single_trailing_underscore_: 
    return something
# used by convention to avoid conflicts with Python keyword, e.g. 
# Tkinter.Toplevel(master, class_='ClassName')
```

関数後に一つアンダースコアを付けるのはPython内の重要関数と名付けを被らせない為だ。  
例えばclass内でどうしてもlistと言う関数や引数を設定したい時、  
list\_ と名付けてPythonのlistと被ることを避ける。

### 4.1.3. \_\_function(x): #関数前に二つ

```python
def __double_leading_underscore: 
    return something
# when naming a class attribute, invokes name mangling 
# (inside class FooBar, __boo becomes _FooBar__boo; see below).
```

class内の関数前に二つアンダースコアを付けることで、 *名前の マングリング機構* を呼び出す。

ここのマングリングとは、インタプリタやコンパイラーが普通の方法で変数を扱わなくなる事です。

例えばclass FooBarの関数\_\_booについて説明すると、Foobar.\_\_barでは関数を呼べ出せなく、\_Foobar\_\_booという使い方になる。擬似的にPrivate属性を作れます。

### 4.1.4. function(x): #関数前後に二つずつ

```python
def __double_leading_and_trailing_underscore__: 
    return something
# "magic" objects or attributes that live in user-controlled 
# namespaces. E.g. __init__, __import__ or __file__. Never invent 
# such names; only use them as documented.
```

class内の関数の前後に二つずつアンダースコアを付けることで、 **magic method** になります。  
\_\_init\_\_や\_ *call\_* 、\_ *str\_* 、\_\_iter\_\_等既存のmagic methodがあってクラスを華やかに書けるが、普段の開発では自分で新しくマジックメソッドを定義しないことをお勧めする。

## 5\. 数字を読みやすく

```sh
>>> 1000000
Out: 1000000
>>> 1_000_000
Out: 1000000
```

**Python 3.6以降では、数字を読みやすくする様にアンダースコアを数字内に加える事が出来る。**  
一般で使われてる3桁ごとにカンマを実現可能。

## 結論

**アンダースコアは使いこなすと凄く見える！**  
実は他にも使い方がありますが、あまりにも使わないので今回は割愛しました。  
ちなみに \_ はアンダーバーやアンダーラインとか呼ばれていますが、英語ではアンダースコア(underscore)が正しい読み方です。  
\_\_の様にアンダースコアが二回連続で使われてると **dunders (double underscore)** と言うかっこいい名前がある。

---

[5](https://qiita.com/_Kohei_/items/#comments)

コメント一覧へ移動

X（Twitter）でシェアする

Facebookでシェアする

はてなブックマークに追加する

## Qiita Advent Calendar 開催！

[785](https://qiita.com/_Kohei_/items/069aa1e7b872f5ca96bf/likers)

いいねしたユーザー一覧へ移動

914