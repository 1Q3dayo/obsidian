---
title: "「ゆっくり実況」みたいな動画をAWSサービスを駆使して作ってみる"
source: "https://zenn.dev/aws_japan/articles/acc24ed211393e"
author:
  - "[[Zenn]]"
published: 2025-10-05
created: 2025-11-17
description:
tags:
  - "clippings"
  - raw
---
[アマゾン ウェブ サービス ジャパン (有志)](https://zenn.dev/p/aws_japan)

63

21[tech](https://zenn.dev/tech-or-idea)

## はじめに

ゆっくり実況やVOICEBOXの製品を利用した解説動画ってよく見かけますよね。  
ああいったタイプの、いわゆる「バーチャルキャラクターによる解説動画」ってのがあると思うんですが、この前見ていてふと思ったんですよね、「Amazon PollyとAmazon Bedrockを使えば私でも作れるんじゃないか…？」って。  
台本やキャラクターの絵はBedrockでいけるし、読み上げる音声はPollyでいけるんじゃないか？と。

よし、やってみよう！

## 先に結果

できあがった動画をご覧になりたい方は、こちらのYouTubeをどうぞ。

<iframe src="https://www.youtube-nocookie.com/embed/Ka-3MrIaX9I" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe>

※記事を読んでいただければわかりますが、わりと人力パートも多いのであまりご期待なさらず…。

## 開発の流れ

## 素のAmazon Pollyを試す

さて、ではまずは声からということで、最初にAmazon Pollyのニューラル音声を聞いてみよう。  
…うーん、そのままだと大人すぎる…ビジネスすぎる…

もう少しアニメキャラっぽい声がいいですね。科学的にアニメキャラクターの声って普通の声とどう違うんだろう？

アニメキャラクター音声の音響特性

研究論文や音響分析から、アニメキャラクター音声には以下の特徴があります：

### 1\. 基本周波数（ピッチ）の特徴

• **高いピッチ**: 通常の成人女性より高い基本周波数（300-500Hz程度）  
• **ピッチレンジの拡大**: 感情表現のため、ピッチの変動幅が大きい  
• **特定周波数帯域**: 3-6kHzの範囲で特徴的な音響エネルギー

### 2\. 発話速度とリズム

• **やや遅めの発話速度**: 明瞭性を重視  
• **音節の長さ**: 通常より長めの音節持続時間  
• **抑揚の強調**: 感情表現のための大きな音調変化

### 3\. 音質（Timbre）の特徴

• **フォルマント周波数の調整**: 声道の長さを短く見せる効果  
• **高周波成分の強調**: 明るく可愛らしい印象  
• **低周波エネルギーの制御**: 力強さと覚醒度の調整

ふむふむ、なんとなくわかった。  
Amazon Pollyは音声合成マークアップ言語 (SSML) を使用すると音声を細かく制御できるので、試しにそれでアニメ声を表現してみます。

```xml
<speak>
    <prosody pitch="high" rate="85%" volume="medium">
        <break time="0.2s"/>
        みなさん、<emphasis level="strong">こんにちは</emphasis>！
        <break time="0.3s"/>
        今日は<prosody pitch="+15%">とっても</prosody>楽しい
        <prosody rate="75%">お話</prosody>をしますよ！
        <break time="0.5s"/>
    </prosody>
</speak>
```

おお…

ぜひ皆様もお手元でお試しいただきたいんですが…やりたいことはわかるけど、なんか全然違うな。

ピッチを調整して「とっても」を強調している点は、なかなかそれっぽい。  
あとニューラルではなくスタンダードを薦めるのもある意味「ぽさ」がある、ニューラルではピッチ調整ができない点を考慮してくれただけかもしれないけど。

ただ、せっかく流暢な音声モードがあるんだから、やっぱりニューラル使ってみたいなー。ニューラルだとどう？

```xml
<speak>
    <prosody rate="90%" volume="x-loud">
        えー！
        <break time="0.2s"/>
        <prosody rate="120%">それはすごいですね！</prosody>
        <break time="0.3s"/>
        <prosody rate="120%" volume="medium">
            もっと詳しく教えてください！
        </prosody>
    </prosody>
</speak>
```

おっ、こっちのほうが良さそうだけどやっぱりピッチがなぁ。  
よし、これはできあがったmp3をffmpegで編集して、ピッチをあげてみよう。

## ffmpegによる編集の検証

### ffmpegのセットアップ

こちらの記事を参考にさせていただき、ひとまずEC2でffmpegを使えるようにしました。

使用したOSは `Amazon Linux 2023 AMI 2023.9.20250929.0 x86_64 HVM kernel-6.1` です。  
私の場合、上記の記事をそのままコピペするとシンボリックリンクで指定しているファイルパスのバージョンが異なっていたので、適宜読み替える必要がありそうです。ただそれ以外はそのままでOKで、記事のおかげですんなりセットアップできました。

### ffmpegを利用した編集

では早速、Pollyで生成したmp3ファイルを編集してみます。

```xml
ffmpeg -i ./1611187f-3836-4876-ba7e-6367123d6ad1.mp3 -af "asetrate=44100*2^(400/1200),aresample=44100" output.mp3
```

実行結果のコンソールログ

\[ec2-user@ip-172-31-135-247 ~\]$ ffmpeg -i./1611187f-3836-4876-ba7e-6367123d6ad1.mp3 -af "asetrate=44100\*2^(400/1200),aresample=44100" output.mp3  
ffmpeg version 7.0.2-static [https://johnvansickle.com/ffmpeg/](https://johnvansickle.com/ffmpeg/) Copyright (c) 2000-2024 the FFmpeg developers  
built with gcc 8 (Debian 8.3.0-6)  
configuration: --enable-gpl --enable-version3 --enable-static --disable-debug --disable-ffplay --disable-indev=sndio --disable-outdev=sndio --cc=gcc --enable-fontconfig --enable-frei0r --enable-gnutls --enable-gmp --enable-libgme --enable-gray --enable-libaom --enable-libfribidi --enable-libass --enable-libvmaf --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librubberband --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libvorbis --enable-libopus --enable-libtheora --enable-libvidstab --enable-libvo-amrwbenc --enable-libvpx --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-libdav1d --enable-libxvid --enable-libzvbi --enable-libzimg  
libavutil 59. 8.100 / 59. 8.100  
libavcodec 61. 3.100 / 61. 3.100  
libavformat 61. 1.100 / 61. 1.100  
libavdevice 61. 1.100 / 61. 1.100  
libavfilter 10. 1.100 / 10. 1.100  
libswscale 8. 1.100 / 8. 1.100  
libswresample 5. 1.100 / 5. 1.100  
libpostproc 58. 1.100 / 58. 1.100  
\[mp3 @ 0x2948dcc0\] Estimating duration from bitrate, this may be inaccurate  
Input #0, mp3, from './1611187f-3836-4876-ba7e-6367123d6ad1.mp3':  
Metadata:  
encoder: Lavf62.0.100  
Duration: 00:00:05.78, start: 0.000000, bitrate: 48 kb/s  
Stream #0:0: Audio: mp3 (mp3float), 24000 Hz, mono, fltp, 48 kb/s  
Stream mapping:  
Stream #0:0 -> #0:0 (mp3 (mp3float) -> mp3 (libmp3lame))  
Press \[q\] to stop, \[?\] for help  
Output #0, mp3, to 'output.mp3':  
Metadata:  
TSSE: Lavf61.1.100  
Stream #0:0: Audio: mp3, 44100 Hz, mono, fltp  
Metadata:  
encoder: Lavc61.3.100 libmp3lame  
\[out#0/mp3 @ 0x29492c00\] video:0KiB audio:20KiB subtitle:0KiB other streams:0KiB global headers:0KiB muxing overhead: 1.114893%  
size= 20KiB time=00:00:02.49 bitrate= 65.6kbits/s spe

とりあえずffmpegが動かせたけど、4音はあげすぎだったみたい。しかもテンポも上がっちゃうみたいで、どうぶつの森みたいになってしまった。わはは。

気を取り直して調整したコマンドがこちら。

```xml
ffmpeg -i ./input.mp3 -filter:a "rubberband=pitch=1.122:tempo=0.9" -c:a libmp3lame output.mp3
```

よし、細かい調整はともかく、ffmpegでそれっぽい音声に合成できることが確認できたぞ。これで、今回の音声作成の大まかなステップが決まりました。

1. 発言中における相対的な話す早さや間はAmazon PollyのSSMLで調整し、ベースとなるmp3ファイルを生成する
2. できあがったmp3ファイルをffmpegでピッチ修正して、それっぽい声に仕上げる。

## Amazon Polly + ffmpegの自動化

あとはSSMLでどんな調整をしていくかだけど、今検証していた手順だと手作業が多く入っているので、Try & Errorに時間がかかってしまいそうです。

**手作業でAmazon Pollyの音声ファイルを編集する流れ**

1. マネコンのAmazon Pollyで音声を合成し、S3に保存。
2. EC2にSSMで接続する。
3. AWS CLIでS3のmp3ファイルをダウンロードする。
4. ffmpegコマンドを実行する。
5. 再度CLIでS3に編集後のmp3ファイルをアップロードする。

そこで、AWSサービスを組み合わせて半自動化することにしました。（マネコンのインターフェースは使いやすいのでそのまま使う。）

**Amazon Pollyで生成したら自動で変換まで処理する**

1. マネコンのAmazon Pollyで音声を合成し、S3に保存。
2. S3のイベントトリガでLambdaを呼び出す。
3. Lambdaでffmpegを使用した変換を実行する。
4. 出力結果をS3にアップロードする。

ということで、下図のようなパイプラインを用意しました。

![](https://storage.googleapis.com/zenn-user-upload/b60c6e00047b-20251005.png)

Lambdaでffmpegを利用するためにはLayerが必要なので、このあたりを参考に関数を用意しました。

Lambda自体のコードはこんな感じです。記事中たびたび登場しますが、このコードもQ Devに作ってもらったので中身はほぼいじってません。助かる〜。

ffmpegで変換処理をするLambdaのコード

```python
import json
import boto3
import subprocess
import os
import tempfile
import shlex
from urllib.parse import unquote_plus

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # S3イベントから情報取得
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        # パラメータ設定
        pitch_ratio = float(os.environ.get('PITCH_RATIO', '1.189'))  # 1.5音上げる
        tempo_ratio = float(os.environ.get('TEMPO_RATIO', '1.1'))    # 少しゆっくり
        
        # 一時ファイル作成
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, 'input.mp3')
            output_path = os.path.join(temp_dir, 'output.mp3')
            
            # S3からダウンロード
            s3_client.download_file(bucket, key, input_path)

            # FFmpegでピッチ・テンポ変更
            cmd = [
                '/opt/ffmpeg-layer/bin/ffmpeg',
                '-i', input_path,
                '-filter:a', f'rubberband=pitch={pitch_ratio}:tempo={tempo_ratio}',
                '-c:a', 'libmp3lame',
                '-y', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg error: {result.stderr}")
            
            # 出力ファイル名生成
            output_key = key.replace('origin', 'modified')
            
            # S3にアップロード
            s3_client.upload_file(output_path, bucket, output_key)
            
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Audio processing completed',
                'input': f's3://{bucket}/{key}',
                'output': f's3://{bucket}/{output_key}'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

## SSMLの調整

これでSSMLの調整に移れるわけですが、仮にでも台本がないと判断が難しい。  
そこで、週刊AWSの記事から一つ抜粋して、そのアップデートに関して二人のキャラクターがお喋りする台本を作ることにします。  
記事は一番新しい [こちら](https://aws.amazon.com/jp/blogs/news/aws-weekly-20250922/) の中から、説明しやすそうな [Amazon EC2 R8gb インスタンスが一般提供](https://aws.amazon.com/jp/about-aws/whats-new/2025/09/amazon-ec2-r8gb-instances/) を選びました。

次はふたりがどんなふうな会話を繰り広げるか、キャラクター設定が必要ですね。（どんどん本筋から離れていく気がする。）  
ちょうど日本語の女性の音声はKazuhaとTomokoの2パターンがあるので、それぞれに割り当てるつもりで考えていきます。

キャラ名はAmazon Web Servicesをもじったりして考えた結果、アンバー（Amber）とゾーイ（Zoe）という名前に決まり、キャラ設定を考えていきます。その結果がこちら。

キャラ設定：アンバー

## 一人目:アンバー(Amber)

### 基本プロフィール

- **年齢**: 17歳
- **身長**: 158cm
- **誕生日**: 8月15日(しし座)
- **イメージカラー**: オレンジ&ゴールド

### バックグラウンド

- 地方の商業高校に通う高校2年生
- 将来はWebデザイナーになりたいと思っている
- 最近プログラミングに興味を持ち始めたばかり
- 父親が小さなIT企業を経営していて、その影響でクラウドに興味を持った
- 3人姉妹の末っ子で、甘えん坊な性格

### 性格・特徴

- 好奇心旺盛で何でも「すごーい!」と感動する
- 失敗を恐れず、とりあえずやってみる行動派
- 素直で裏表がなく、感情表現が豊か
- 少しおっちょこちょいで、よく早とちりする
- ポジティブ思考で、難しいことも「なんとかなる!」精神

### 話し方の特徴

- 語尾に「〜だね!」「〜なんだ!」をよく使う
- 「えっ、マジで!?」「やばい!」など若者言葉が多い
- 「つまり〜ってこと?」と確認する癖がある
- 驚いた時は「うわぁぁ!」と大げさにリアクション
- 「わかんない〜」「難しい〜」を素直に言える

### 好きなもの

- **食べ物**: パンケーキ、タピオカドリンク、チーズケーキ
- **趣味**: SNS巡り、カフェ巡り、スマホゲーム、イラスト描き
- **好きな色**: パステルカラー全般
- **好きな動物**: 柴犬、ハムスター

### 口癖・特徴的な発言

- 「ねえねえ、これってさ〜」(話を切り出す時)
- 「なるほどわからん!」(理解できない時)
- 「ゾーイ先輩、助けて〜!」(困った時)
- 「あ、それ知ってる!...気がする!」(曖昧な知識)
- 「クラウドって雲じゃないんだよね?」(初心者あるある)

### ビジュアルイメージ

- ふわふわのセミロングヘア(オレンジブラウン)
- 大きな琥珀色の瞳
- 元気な印象のカジュアルファッション
- リボンやヘアピンなどの小物が好き
- 表情豊かで、コロコロ変わる表情が魅力

### 動画での役割

- 情報提示・進行役
- 感情表現・リアクション役
- 学習者としての役割
- 視聴者の代弁者として素朴な疑問を投げかける

---

キャラ設定：ゾーイ

## 二人目:ゾーイ(Zoe)

### 基本プロフィール

- **年齢**: 19歳
- **身長**: 165cm
- **誕生日**: 12月3日(いて座)
- **イメージカラー**: ブルー&シルバー

### バックグラウンド

- 都内の情報系大学1年生
- 高校時代からプログラミングコンテストで入賞経験あり
- AWS認定資格(クラウドプラクティショナー)を既に取得済み
- 中学時代から個人でWebサービスを開発している
- 一人っ子で、両親は研究者という環境で育った

### 性格・特徴

- 論理的思考が得意で、物事を体系的に理解する
- 冷静沈着だが、実は面倒見が良い
- 完璧主義な一面があり、細かいことが気になる
- クールに見えるが、好きなことには熱くなる
- ツッコミが的確で、でも優しさがある

### 話し方の特徴

- 「正確には〜」「厳密に言うと〜」と補足する癖
- 「それは違うよ」とはっきり訂正するが、優しい口調
- 「つまりこういうことだね」とまとめるのが上手
- 専門用語を使った後、「簡単に言うと〜」と言い換える
- 「なるほど、いい質問だね」と相手を認める

### 好きなもの

- **食べ物**: ブラックコーヒー、ダークチョコレート、和菓子(特に羊羹)
- **趣味**: プログラミング、技術書読書、ボードゲーム、天体観測
- **好きな色**: 青系、モノトーン
- **好きな動物**: 猫、フクロウ

### 口癖・特徴的な発言

- 「ちょっと待って、それは〜」(訂正する時)
- 「アンバー、落ち着いて」(暴走を止める時)
- 「実はね...」(豆知識を披露する時)
- 「図で説明すると〜」(視覚的に説明する時)
- 「まあ、そういうこともあるよね」(フォローする時)

### ビジュアルイメージ

- さらさらのロングストレートヘア(ダークブルー)
- 知的な印象の青い瞳
- シンプルで洗練されたファッション
- 眼鏡をかけていることもある(伊達眼鏡)
- 微笑むと柔らかい印象になるギャップが魅力

### 動画での役割

- 知識補完・解説役
- 分析・考察役
- 進行管理・まとめ役
- エンターテイメント役(適度なツッコミ)

話題にする記事とキャラ設定が固まったので、SSMLを調整するためのリアルな台本をQ Devに生成してもらいました。生成時にはキャラ設定をコンテキストとして与えるとともに、MCPサーバを適宜使用して事実確認をしながら作ってもらいました。

そうしてできあがった台本をもとにSSMLをいじりながらTry & Errorを繰り返し、結果的にSSMLで次のような工夫をするとキャラっぽくなる（※筆者の主観）ことがようやくわかってきました。

**ffmpegでアニメキャラっぽい音声に編集するコツ**

- ピッチは +1.5 音 (1.189) あげるとちょうど良い。
- 話す早さはTEMPOを 1.1 倍にするとちょうど良い。SSML側でrateを指定してもいいけど、SSMLはボリューム少ないほうが可読性がいいし、部分的に早く話させたい時に書くのが面倒になる。
- このTEMPOだと行間に `break time="200ms"` を入れるとちょうど良い。
- 挨拶や最初の掛け声は `rate="120%" volume="loud"` を入れておくと元気がいいし、軽快な感じが出て自然に感じる。

これでひとまずSSMLでキャラボイスを生成する検証は完了です。

## キャラクターの立ち絵

次に、今回はラジオではなく動画なので、もちろんキャラクターのビジュアルが必要です。  
これにはBedrockの `Stable Diffusion 3.5 Large` を使用しました。キャラ設定をもとに画像生成のプロンプトを作成してもらいます。英語のほうが細かいニュアンスが伝わりやすいので英語で用意しました。

画像生成のプロンプト

## アンバー (Amber) - 個別イラスト

```xml
A cute anime-style illustration of a 17-year-old girl named Amber, cheerful and energetic expression, fluffy semi-long orange-brown hair with hair ribbons and hairpins, large amber-colored eyes, wearing casual trendy fashion, bright and friendly smile, youthful and approachable appearance, pastel color scheme with orange and gold accents, high quality digital art, clean anime art style, white background, full body portrait
```

## ゾーイ (Zoe) - 個別イラスト

```xml
A sophisticated anime-style illustration of a 19-year-old girl named Zoe, calm and intelligent expression, long straight dark blue hair, blue eyes with intellectual charm, simple and refined fashion style, gentle smile showing warmth, elegant and composed appearance, blue and silver color scheme, optional stylish glasses, high quality digital art, clean anime art style, white background, full body portrait
```

出来上がったそれぞれの画像がこちら。

#### Amber

![](https://storage.googleapis.com/zenn-user-upload/55271b03d9c1-20251003.jpeg)

#### Zoe

![](https://storage.googleapis.com/zenn-user-upload/99daba21ddc6-20251003.jpeg)

おおっ、絵になるとキャラの解像度もあがっていい〜。

ただ、この絵だと動画に登場していただくにはちょっとキレイすぎるっていうか、もうちょっとデフォルメしたいな…。  
と思い、このあと色々試行錯誤したんですが、あまり画像生成に関するノウハウが私になく、結局思ったような画像にはなりませんでした…うまくできるよ！って方いたら教えてください！

ということで、今回は妥協してさきほどの絵を参考にアマチュアのイラストレーターの方（妻）に制作をお願いしました。

出来上がりがこちら。

#### Amber & Zoe

![](https://storage.googleapis.com/zenn-user-upload/068eabf2499a-20251004.png)

おお！まさにこういう感じ！さすが〜。ありがとうございます。

## 台本をSSMLに変換していく

先ほどのSSML検証では台本の一部しかSSMLに変換していなかったので、残っていた部分もまとめてSSMLに変換してもらったんですが、そのままSSMLにするだけでは不十分でした。すぐに行き当たった問題はふたつです。

**ローマ字や数字の読み上げがおかしい時がある**  
例えば、EC2を「イー・シー・ニ」って読んじゃうんですよね。あってるちゃあってるんですが…。  
与えるテキストを「EC2」から「イー・シー・ツー」にするか、 `<sub alias="イーシーツー">EC2</sub>` のようなSSMLによる変換が必要です。

**イントネーションが不自然な時がある**  
例えばタイトルコールで「カッコ仮」と読み上げるんですが、"コ"のほうにイントネーションがいってしまいます。これは、 `<phoneme alphabet="x-amazon-pron-kana" ph="カ'ッコ">カッコ</phoneme>` で解決する必要があります。

ということで、作った台本をもとに次のようなプロンプトを実行し、SSMLへ一括で変換してもらいました。

台本からSSMLを生成するプロンプト

```xml
あなたは与えられた原稿をもとにAmazon Pollyで音声化するためのSSMLを生成してください。
音声はニューラルで生成するので、一部のSSMLタグがサポートされていない点に注意してください。
原稿はpollyフォルダのaws_video_script_r8gb.mdに記載されています。
一行ごとにSSMLを生成してください。SSMLを生成する際には、<rule> タグの内容に従ってください。

<rule>
* 一行に読点で別れた複数の文章がある場合は、間に <break time="200ms"> を入れてください。
* 相手の名前を読んだり、リアクションを発生するような短いリアクションの文章は、 <prosody rate="120%" volume="loud"> を指定して下さい。
* AWSのサービス名など、英文字で表記された単語を正しく発音する必要があります。例えば、 <sub alias="イーシーツー">EC2</sub> のように正確な読み方に変換する指示をしてください。
* この音声はYouTubeで投稿する動画で利用する予定です。視聴者が気持ちよく視聴できることを第一に考えてください。
</rule>
```

そしてできあがったSSMLがこちら。概ね期待通りの出力結果になりました。

Q Devで生成したSSML

## AWS解説動画台本 SSML版: Amazon EC2 R8gbインスタンス

## タイトルコール

**アンバー**:

```xml
<speak>Amber & Zoe's Tech Talk (仮)</speak>
```

**ゾーイ**:

```xml
<speak>Amber & Zoe's Tech Talk (仮)</speak>
```

## オープニング

**アンバー**:

```xml
<speak><prosody rate="120%" volume="loud">ねえねえゾーイ先輩!</prosody> <sub alias="エーダブリューエス">AWS</sub>から新しい<sub alias="イーシーツー">EC2</sub>インスタンスが出たって聞いたんだけど!</speak>
```

**ゾーイ**:

```xml
<speak>そうだね、<prosody rate="120%" volume="loud">アンバー</prosody>。<sub alias="アールハチジービー">R8gb</sub>インスタンスのことだね。<break time="200ms"/>2025年9月23日に正式リリースされたばかりだよ。</speak>
```

**アンバー**:

```xml
<speak><sub alias="アールハチジービー">R8gb</sub>...? <break time="200ms"/>えっと、Rってメモリ最適化のやつだよね? <break time="200ms"/>gbって何?</speak>
```

**ゾーイ**:

```xml
<speak>いい質問だね。<break time="200ms"/>gbは「<sub alias="グラビトンフォー">Graviton4</sub> + ブロックストレージ最適化」の略。<break time="200ms"/>つまり、<sub alias="グラビトンフォー">Graviton4</sub>プロセッサを使っていて、特にストレージ性能が強化されたインスタンスってこと。</speak>
```

## メインコンテンツ

**アンバー**:

```xml
<speak>ストレージ性能が強化...? <break time="200ms"/>どのくらいすごいの?</speak>
```

**ゾーイ**:

```xml
<speak>最大で150<sub alias="ギガビーピーエス">Gbps</sub>の<sub alias="イービーエス">EBS</sub>バンド幅を提供するんだ。<break time="200ms"/>同じサイズの他の<sub alias="グラビトンフォー">Graviton4</sub>ベースのインスタンスと比べて、ストレージのパフォーマンスが大幅に向上してるよ。</speak>
```

**アンバー**:

```xml
<speak>150<sub alias="ギガビーピーエス">Gbps</sub>...! <break time="200ms"/><prosody rate="120%" volume="loud">うわぁ、数字が大きすぎてピンとこない!</prosody></speak>
```

**ゾーイ**:

```xml
<speak>(微笑んで) 簡単に言うと、データベースみたいに大量のデータを読み書きするアプリケーションが、すごく速く動くようになるってこと。</speak>
```

**アンバー**:

```xml
<speak><prosody rate="120%" volume="loud">なるほど!</prosody> じゃあ、データベース使ってるサービスにぴったりなんだね!</speak>
```

**ゾーイ**:

```xml
<speak>その通り。<break time="200ms"/>特に高性能データベースや<sub alias="ノーエスキューエル">NoSQL</sub>データベースに最適だよ。<break time="200ms"/>しかも、<sub alias="グラビトンフォー">Graviton4</sub>プロセッサのおかげで、<sub alias="グラビトンスリー">Graviton3</sub>と比べて最大30%も計算性能が向上してる。</speak>
```

**アンバー**:

```xml
<speak><prosody rate="120%" volume="loud">えっ、マジで!?</prosody> 性能上がってコストも最適化できるって、いいとこ取りじゃん!</speak>
```

## スペック紹介

**ゾーイ**:

```xml
<speak>スペックも見ておこうか。<break time="200ms"/>最大サイズは24xlargeで、メモリは最大768<sub alias="ギガバイト">GiB</sub>。<break time="200ms"/>ネットワーク帯域幅は最大200<sub alias="ギガビーピーエス">Gbps</sub>まで対応してる。</speak>
```

**アンバー**:

```xml
<speak>768ギガバイト...! <break time="200ms"/>スマホの容量とは桁が違う...</speak>
```

**ゾーイ**:

```xml
<speak>(クスッと笑って) そうだね。<break time="200ms"/>あと、16xlarge、24xlarge、metal-24xlサイズでは、<sub alias="イーエフエー">EFA</sub>っていう特別なネットワーク機能も使えるんだ。</speak>
```

**アンバー**:

```xml
<speak><sub alias="イーエフエー">EFA</sub>? それって何?</speak>
```

**ゾーイ**:

```xml
<speak>Elastic Fabric Adapterの略で、複数のサーバーを密に連携させる必要がある場合に、低遅延で高性能なクラスター通信ができる機能だよ。</speak>
```

**アンバー**:

```xml
<speak>つまり、チームワークが必要な処理に強いってこと?</speak>
```

**ゾーイ**:

```xml
<speak>まさにその通り。<break time="200ms"/>いい例えだね、<prosody rate="120%" volume="loud">アンバー</prosody>。</speak>
```

## 利用可能リージョン

**アンバー**:

```xml
<speak>で、これってもう使えるの?</speak>
```

**ゾーイ**:

```xml
<speak>使えるよ。<break time="200ms"/>現在は米国東部(バージニア北部)と米国西部(オレゴン)リージョンで利用可能。<break time="200ms"/>ただし、metalサイズはバージニア北部だけだから注意してね。</speak>
```

**アンバー**:

```xml
<speak>日本リージョンはまだなんだ...<prosody rate="120%" volume="loud">残念!</prosody></speak>
```

**ゾーイ**:

```xml
<speak>今後展開される可能性は高いから、期待して待とう。</speak>
```

## クロージング

**アンバー**:

```xml
<speak>じゃあ、まとめると...データベースとか、ストレージをたくさん使うアプリに最適で、性能もコスパも良いインスタンスってことだね!</speak>
```

**ゾーイ**:

```xml
<speak>完璧なまとめだね。<break time="200ms"/><sub alias="グラビトンフォー">Graviton4</sub>の高性能と、<sub alias="イービーエス">EBS</sub>最適化による高速ストレージアクセスが特徴。<break time="200ms"/>データベースのパフォーマンスを上げたい人は要チェックだよ。</speak>
```

**アンバー**:

```xml
<speak><prosody rate="120%" volume="loud">ゾーイ先輩、今日もありがとう!</prosody> すごくわかりやすかった!</speak>
```

**ゾーイ**:

```xml
<speak>どういたしまして。<break time="200ms"/>詳しくは<sub alias="エーダブリューエス">AWS</sub>の公式ドキュメントもチェックしてみてね。</speak>
```

**アンバー**:

```xml
<speak>はーい! じゃあまた次回!</speak>
```

**二人**:

```xml
<speak><prosody rate="120%" volume="loud">ばいばーい!</prosody></speak>
```

---

## 使用したSSMLタグの説明

- `<prosody rate="120%" volume="loud">`: 短いリアクションや名前呼びで使用
- `<sub alias="読み方">元テキスト</sub>`: AWS用語の正確な発音指定
- `<break time="200ms">`: 読点で区切られた文章間の自然な間
- ニューラル音声対応: `<emphasis>` タグは使用せず、 `<prosody>` で代替

ところどころ怪しいですが、イントネーションの確認もあるので、一通り生成しながら確認してみましょう。（結果として、イントネーションは細かく気にし始めるとキリがないので、あまり指定しませんでした。「ちょっと機械っぽいんだよな〜」も、こういう動画の醍醐味だと思うことにしました。）

## 動画にする

筆者は動画制作なんかしたことないので、パワーポイントのアニメーションを組み合わせるだけのお手軽手法を採用しました。採用というか、これ以外の方法が思いつかなかった。  
（せっかくパワポを採用したので、パワポ自体も生成AIを組み合わせて作る、という選択肢もあったんですが、これは次回への宿題にしました。）

そうしてようやく！完成〜〜！！

<iframe src="https://www.youtube-nocookie.com/embed/Ka-3MrIaX9I" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen=""></iframe>

## まとめ

今回の記事執筆で、AWSのマネージドサービスを組み合わせることで個人でもバーチャルキャラクター解説動画 **っぽいもの** を制作できることが実証できました。  
（当たり前ですが、本業の方々には及ばない点が多々ありますからね…）

- 体験できて良かったこと
	- SSMLによる細かな音声制御とffmpegによるピッチ調整の組み合わせで、製品なしでもアニメキャラクター風の音声が作れる
	- 初期の検証は手作業だけど試行錯誤しやすいEC2で行い、自動化のタイミングでマネージドサービスへ移行するとスムーズ
	- 至る所でAmazon Q Developer CLIによる作業自動化が開発を加速してくれた。というかなかったら作れなかった

さらなる展望を考えると、AWSのnews記事が投稿されたと同時に、ふたりが解説する動画を全自動で制作・投稿なんてこともできそうですね。文字を読むより動画のほうがいいんだよな〜って方にはお役に立てるかもしれない。例えばこんなパイプラインを作ることができれば…？？

![](https://storage.googleapis.com/zenn-user-upload/646d99e89b18-20251005.png)

今回一番時間がかかってしまったのは結局パワポに貼り付けていったりする作業だったので、せめてここの自動化には日を改めてチャレンジしたい。

今回も単なる思いつきから始めたトライアルでしたが、こういった動画作りにチャレンジしてみたい方はぜひお試しください。AWSアカウントさえあれば始められるので、まさにスモールスタートにぴったりです。  
特に言及しておきたいのは比較的短時間で実現できることですね。検証や準備には3~4時間かかりましたが、あとは半自動な部分もあるのでだいたい2時間ぐらいで動画を完成させる事ができました。

また、今回ffmpegは初歩的な利用方法のみでしたが、高度なオプションも駆使すればさらにクオリティをあげることもできるっぽいです。（そこに労力をかけるか、製品を活用するか、は考えた方が良いかもしれませんが…。）

いや〜面白かった。もう日曜日が終わりかけているけど、楽しく遊べたので満足です。  
技術の民主化ってこういうことも可能にしてくれるんですね。

63

21