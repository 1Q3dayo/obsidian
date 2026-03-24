---
title: "【西川和久の不定期コラム】 画像生成AIの「ノード地獄」にサヨナラ。ComfyUIを快適に使う技と超簡単インストール法"
source: "https://pc.watch.impress.co.jp/docs/column/nishikawa/2070854.html"
author: ""
published: "2025-12-16"
created: "2025-12-19"
description: "ComfyUIを使っているといろいろなnodeが並び、全体が見れるようにするとPrompt入力枠が小さかったり、画像を大きくするとほかが小さかったりで、ズームイン/アウトが結構発生。何だか見にくかったりする。それをスッキリ表示に変え気分的に効率アップを図りたい……というのが今回のお題となる。"
tags:
  - ""
  - "raw"
---

西川和久の不定期コラム

## 画像生成AIの「ノード地獄」にサヨナラ。ComfyUIを快適に使う技と超簡単インストール法

2025年12月16日 06:06

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C00_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C00_o.jpg.html)

　ComfyUIを使っているといろいろなnodeが並び、全体が見れるようにするとPrompt入力枠が小さかったり、画像を大きくするとほかが小さかったりで、ズームイン/アウトが結構発生。何だか見にくかったりする。それをスッキリ表示に変え気分的に効率アップを図りたい……というのが今回のお題となる。

## たまには軽めな話を

　ここのところ重め(？)な内容が続いたので、今回はちょっと箸休め。生成AI画像/動画を作る場合、ComfyUIがほぼデファクトスタンダードになっているが、Workflowが固まった後、多くのnodeが並んでいる画面をあまり見たくなく、Promptと出力結果に集中したい……と思う人も多いのではないだろうか？

　筆者もそのうちの一人。Workflowを作る作業はそれはそれでもちろん面白いのだが、終わった後は、できればスッキリした画面で操作したい。もちろん、nodeのレイアウトを工夫すればできなくもないが、もっと根本的に変えたい。

　今回は、これを実現できる方法を2パターン紹介する。

　そして最後は+αとして、ComfyUIやってみたいけど、pip installなど、コマンドプロンプトでコマンドを入力するのが面倒……っと思ってる人に、exe一発でインストールできる方法もご紹介する。

## 複数のnodeをブラックボックス化するSubgraph

　Subgraph(サブグラフ)は一言でいえば、“複数のnodeを1つのnodeにまとめブラックボックス化”する手法で、ComfyUIの標準機能となる。

　試す方法は簡単！テンプレートの検索枠へ“Subgraph”と入れると、いくつか出るので1つ選択(ここではText to image/Z-Image-Turbo)。項目を入力するnodeと、画像表示用のnode、2つだけのWorkflowが現れる。

　通常、画像生成のWorkflowは、少なくともcheckpointのロード、CLIP Text Encode、Empty Latent、KSampler、VAE Decode、Save Image……といったnodeが必要になるのが、たった2つでスッキリ！これだと適度な倍率で表示して、Promptとその結果の画像に集中できるわけだ。

　もちろん、nodeが2つになったのではなく、中間のnodeをブラックボックス化しただけで、実際は右上のアイコンをクリックすると、中身を表示することができる。

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C03_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C03_o.jpg.html)

Subgraphの中身。Load Model/CLIP/VAE、Empty Latent、CLIP Text Encode、KSampler、VAE Decode……と、いつものnodeが並び、出力がIMAGEになっている。ピンク色の枠が外部に表示される項目

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C04_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C04_o.jpg.html)

stepsも表示したい時は、右クリックでPromote Widget stepsを選べば、表側に表示される

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C05_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C05_o.jpg.html)

Load LoRA nodeを追加、LoRAファイル名選択、strength\_modelとstrength\_clipをPromote Widget

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C06_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C06_o.jpg.html)

下に項目が追加されている

　見ると、普段のLoad Model/CLIP/VAE、Empty Latent、CLIP Text Encode、KSampler、VAE Decodeが並び、出力がIMAGEとなっている。つまりSubgraph化することで、実際のWorkflowをブラックボックス化することが可能となる。

　この時、ピンク色の枠が外部に表示する項目となり、ここではEmpty Latentのwidth/height、CLIP Text EncoderのPrompt部分、KSamplerのseed/control after generate。

　stepsも表で変えたいと思った時は、stepsの項目で右クリック、Promote Widget stepsを選べば、表側にstepsの項目が追加される。

　さらにLoRAを使いたい時はLoad LoRA nodeを追加、各項目をPromote Widgetすれば表側の項目が増える。

　Qwen-Image-Edit-2509のように、リファレンス画像がある時は、その設定も表に出したい。これは左側にタップを作ればOKだ。

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C07_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C07_o.jpg.html)

Qwen-Image-Edit-2509のSubgraph側。左側のタップに画像入力が出ている。Text Encode部分も表に出るよう、タップへ接続

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C08_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C08_o.jpg.html)

表側の表示、入力にLoad Image nodeを接続する

　通常のWorkflowをSubgraph化する時は、Subgraph化したいnodeをすべて選択し、右クリックでConvert Subgraphとする。なお、Text Encodeのテキスト部分は左側のタップへ接続すると表で入力可能になる。

　いかがだろうか？これならスッキリと必要な項目だけを表示、画像生成などに集中でき、編集中にラインやnodeをたまたま動かしてしまったり、消してしまったり……というミスもなくなる。すでにWorkflowが確定している時にお勧めの手法となる。

## 懐かしいA1111風にComfyUIを操作できるMinimalistic-Comfy-Wrapper-WebUI

　先のSubgraphは元々ComfyUIが持ってる機能だが、次はcustom nodeだ。Minimalistic-Comfy-Wrapper-WebUIを使用する。これは名前の通り、ComfyUIのインターフェイスから離れ、昔懐かしのAUTOMATIC1111風UIで操作可能となる優れものだ。

　インストールは、

```
cd ComfyUI/custom_nodes
git clone https://github.com/light-and-ray/Minimalistic-Comfy-Wrapper-WebUI
cd Minimalistic-Comfy-Wrapper-WebUI
pip install -r requirements.txt
```

　これでComfyUIを再起動すればOK。左側、一番下にアイコンが増えているのでクリックすると以下のようなWebUIを表示する。ただし、何も設定ができていないため空の状態となる。

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C09_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C09_o.jpg.html)

何も設定されていない状態のMinimalistic-Comfy-Wrapper-WebUI

　では画像生成で必須なPromptと画像出力のUIを付けてみたい。実際動作するWorkflowを開き(ここではZ-Image-Turbo)、UIとして表示したいnodeのタイトルを編集する(タイトルをダブルクリックすると編集状態になる)。ここで修正するのは以下2つのタイトル。

```
CLIP Text Encode (Prompt)　→　<Prompt:prompt:1>
Save Image　→　<Output:output:1>
```

　WebUI化するには、タイトルに以下のようなルールがありこれに従う。ただし、上記のSubgraphのあるWorkflowには対応していない。

```
<Label:category[/tab]:sortRowNumber[/sortColNumber]>
Categories are: "prompt", "output", "important", "advanced"
```

　Workflow保存後、WebUIの右上にある\[Refresh\]をクリックすると、先ほど設定した内容が反映されたWebUIになる。

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C10_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C10_o.jpg.html)

とりあえずPromptと出力画像のみを表示するように設定したWorkflow

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C11_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C11_o.jpg.html)

Promptと生成画像を表示できるWebUIに。\[RUN\]を押せば生成する

　昔A1111を使っていた人からすれば「お！」っという感じではないだろうか。ただこれだと、WorkflowのKSamplerでSeedをランダムにしていても固定になってしまうため、最低限、Seedの項目を追加する必要がある。ついでに解像度も入力可能にしたい。

　まずWorkflowの該当項目から線を引っ張り出し、そこへ数値を入力できるnodeを追加する。この時、Comfy CoreのPrimitive属性のものに限られる。ここではSeedも解像度もINTなので、INTのnodeを3つ追加(赤いnode)。そしてタイトルを編集する。

```
int　→　<seed:advanced:1>
int　→　<width:advanced:2>
int　→　<height:advanced:3>
```

※ 各項目には初期値を入れ、widthとheightはfixedへ

　こうすると3つの項目が縦並びになる。

```
int　→　<seed:advanced/Seed:1>
int　→　<width:advanced/Resolution:1>
int　→　<height:advanced/Resolution:2>
```

　こうするとSeedとResolutionのタブが2つ並び、Resolutionはwidthが1番目、heightが2番目となる。またSeedに関しては乱数アイコンとリサイクルアイコンが自動的に追加される。

　Qwen-Image-Edit-2509などリファレンス画像がある場合は、たとえば3つだと、Load Imageのタイトルを以下のようにすれば、画像入力のパネルも表示する。

```
<Image 1:prompt/Image 1:1>
<Image 2:prompt/Image 2:2>
<Image 3:prompt/Image 3:3>
```

　これをそのままTextEncodeQwenImageEditPlusのimage1/2/3へ接続した場合は、画像1枚、2枚、3枚を自動的に判断、画像のない部分は接続しないロジックが入っているが、たとえばLoad Imageの後ろにリサイズnodeがあり、それがimage1/2/3に入力している場合は、制御ができず、全部の画像をセットしないとエラーになるので注意が必要だ。このようなケースでは少し面倒だが、使わないnodeをバイパスして保存、\[refresh\]するのが一番手っ取り早い。

　現在モデルの切り替えには未対応(TODOにあり)。生成の元となるモデルはほぼ固定なので問題ないが、LoRAはさすがにそうはいかない。仕方ないので普段使うLoRAをLora Loader Stack (rgthree)にセット、strengthにComfy CoreのPrimitive属性FLOATを接続、使わないものは0(効果なし)として切り替えている。

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C16_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C16_o.jpg.html)

Lora Loader Stack (rgthree)で、普段使うLoRAを並べ、strengthにComfy CoreのPrimitive属性FLOATを接続、使わないものは0として切り替え

[![](https://asset.watch.impress.co.jp/img/pcw/docs/2070/854/C17_l.jpg)](https://pc.watch.impress.co.jp/img/pcw/docs/2070/854/html/C17_o.jpg.html)

WebUI上ではこんな感じとなり、使うLoRAだけstrengthを0以外にする

　いかがだろうか？タイトルの編集が少し面倒といえば面倒だが、それだけでComfyUIの世界から離れ、普通のWebUIとして操作可能となる優れものcustom nodeだ。これだとWebブラウザの%拡大でPromptの部分の文字も大きくできるため、筆者世代にも優しいUIとなる(笑)。

　ほかにもいろいろルールや機能があるので、興味のある人はgithubの [README.md](https://github.com/light-and-ray/Minimalistic-Comfy-Wrapper-WebUI/blob/master/Readme.md) をご覧いただきたい。

## ComfyUI Desktopならexe一発起動！

　最後はおまけ。

　Windowsにおける一般的なComfyUIのインストールは、まずpythonの環境を作り、git clone。でもその前にgit for Windowsをインストール。cloneしたらpip install、そしてpythonとCUDAのバージョンに合わせてPyTorchもインストール……といった手順を踏む必要がある。

　これらの作業は、分かってる人であれば大したことないのだが、pythonやgitを使ったことがない人にとってはかなりハードルが高い。

　とはいえ、PCにはちょっとしたNVIDIAのGPUが乗ってるし、面白そうだから使ってみたい……でもコマンドラインでの設定が難しいという人にピッタリな純正環境、ComfyUI Desktopがあるのだ。

　ダウンロードは [ここ](https://www.comfy.org/download) から。Windows版とMac版があり、Windows版の場合はNVIDIAのGPUが必須。前者をダウンロードすると ComfyUI Setup 0.6.0 - x64.exe(執筆時)があるのでそれをクリックすればOK。何も事前に用意する必要はない。

　筆者は初期版の頃少し触ったことはあるものの、最近のは今回が初。呆気に取られるほど簡単だった(アンインストールは、設定のアプリからとWindowsの作法に準拠)。これなら誰でもインストールできるわけだ。お！っと思った人は、ぜひ試してほしい。

---

　以上、今回は、ComfyUIをシンプルなUIで使う方法2つ。そしてWindows環境ならEXE一発でComfyUIをインストールできる方法をご紹介した。実はクラウド版 [ComfyUI](https://cloud.comfy.org/) もあるので(20ドル/月)、GPUのない普通のPCからでも使えたりする。

　ComfyUIは、いろいろなnodeを組み合わせてWorkflowを作るという特性上、生成AIによる画像/動画だけでなく、LLMや音楽、そしてAIに無関係なものまで含め、さまざまなものを扱うことができる。興味があればぜひ使って遊んでほしい。