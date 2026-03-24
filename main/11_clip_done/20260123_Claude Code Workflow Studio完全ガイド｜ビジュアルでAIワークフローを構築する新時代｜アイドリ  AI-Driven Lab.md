---
title: "Claude Code Workflow Studio完全ガイド｜ビジュアルでAIワークフローを構築する新時代｜アイドリ | AI-Driven Lab"
source: "https://note.com/ai_driven/n/nce437c34242f"
author:
  - "[[アイドリ | AI-Driven Lab]]"
published: 2026-01-02
created: 2026-01-23
description: "本記事の対象者    主な対象者: Claude Codeを使っているがワークフロー機能を活用しきれていない方、AIエージェントによる自動化に興味がある開発者・ビジネスパーソンを想定しています。    技術レベル: 初級〜中級を想定しています。    前提知識: Claude Codeの基本的な使い方（ターミナルでの対話）とVS Codeの操作を理解していることを前提としますが、ワークフロー機能の知識は不要です。    この記事で得られるもの: Claude Code Workflow Studioのインストールから実践的なワークフロー構築まで一通り習得でき、複雑なAIエージェント連携"
tags:
  - "clippings"
  - "raw"
---
![見出し画像](https://assets.st-note.com/production/uploads/images/240832352/rectangle_large_type_2_71f2a4f682337ae9646c86662bf84116.png?width=1280)

## Claude Code Workflow Studio完全ガイド｜ビジュアルでAIワークフローを構築する新時代

[アイドリ | AI-Driven Lab](https://note.com/ai_driven)

## 本記事の対象者

![画像](https://assets.st-note.com/img/1767347760-SMbZedyJtf2LN9iu5P7YgCHq.png?width=1200)

- **主な対象者**: Claude Codeを使っているがワークフロー機能を活用しきれていない方、AIエージェントによる自動化に興味がある開発者・ビジネスパーソンを想定しています。
- **技術レベル**: 初級〜中級を想定しています。
- **前提知識**: Claude Codeの基本的な使い方（ターミナルでの対話）とVS Codeの操作を理解していることを前提としますが、ワークフロー機能の知識は不要です。
- **この記事で得られるもの**: Claude Code Workflow Studioのインストールから実践的なワークフロー構築まで一通り習得でき、複雑なAIエージェント連携を自力で設計できるようになります。

## 要約

![画像](https://assets.st-note.com/img/1767347838-EVxuNvtFoi56abrs7cO928AT.png?width=1200)

- **本記事の主要トピック**: 本記事はClaude Code Workflow Studioの概要と解決する課題、具体的なインストール・操作方法、実践的なユースケースの三点を中心に解説します。
- **記事の構成と学習の流れ**: 前半でツールの位置づけと技術的な仕組みを理解し、中盤でインストールから基本操作までをハンズオン形式で学び、後半で実際のワークフロー設計パターンと活用事例を通じて実践力を身につけます。
- **ゴール**: 読了後にClaude Code Workflow Studioを使って独自のAIワークフローを構築でき、チームへの導入メリットを説明できるようになります。

---

「Claude Codeのワークフロー機能、なんだか難しそうで手を出せていない...」

そんな経験はありませんか？実は私もそうでした。Claude Codeには強力なカスタムコマンドやサブエージェント機能があるのに、設定ファイルをゼロから書くのはハードルが高い。YAMLやMarkdownの構文を調べながら、複数のエージェントがどう連携するのか頭の中で想像しながら...。正直、めんどうですよね。

そこに登場したのが **Claude Code Workflow Studio** です。このVS Code拡張機能を使えば、ノードをドラッグ＆ドロップするだけで複雑なAIワークフローを設計できます。まるで「AIワークフローのFigma」のような体験で、GitHubでは **1,100以上のスター** を獲得し、開発者コミュニティで大きな注目を集めています。

この記事では、Claude Code Workflow Studioとは何か、なぜ今これが必要とされているのか、そして具体的にどう使えばいいのかを、初心者の方にもわかりやすく徹底解説していきます。

## Claude Code Workflow Studioとは何か

### 一言でいうと「AIワークフローのビジュアルエディタ」

![画像](https://assets.st-note.com/img/1767344468-tnAwEDUr8GJNs429p6du0VWK.png?width=1200)

https://github.com/breaking-brake/cc-wf-studio/blob/main/resources/hero.png

[Claude Code Workflow Studio](https://github.com/breaking-brake/cc-wf-studio) は、Claude Codeのワークフロー機能をビジュアルに設計・編集できるVS Code拡張機能です。東京在住の開発者「breaking-brake」氏によって開発され、AGPL-3.0ライセンスで公開されています。2025年12月29日にv3.10.0がリリースされ、活発に開発が続けられています。

従来、Claude Codeでワークフローを作るには.claudeディレクトリにMarkdownファイルを手動で作成する必要がありました。Workflow Studioは、この作業を **ノードベースのビジュアルキャンバス** に置き換えます。

![画像](https://assets.st-note.com/img/1767344537-wBf51M2XvdUSumLnFJr9I6cy.png?width=1200)

### プロジェクトの現状と信頼性

このツールの信頼性を示すいくつかの数字をご紹介しましょう。

\\begin{array}{|l|r|} \\hline \\textbf{指標} &amp; \\textbf{数値} \\\\ \\hline \\text{GitHubスター数} &amp; \\text{1,100+} \\\\ \\hline \\text{マージ済みPR} &amp; \\text{297件} \\\\ \\hline \\text{最新バージョン} &amp; \\text{v3.10.0} \\\\ \\hline \\text{最終更新} &amp; \\text{2025年12月29日} \\\\ \\hline \\text{対応言語} &amp; \\text{日本語を含む多言語} \\\\ \\hline \\end{array}

活発なコミュニティと継続的な開発により、安心して使えるツールといえます。

## このツールが解決する3つの課題

Claude Code Workflow Studioは、従来のワークフロー構築における3つの大きな課題を解決します。

### 課題1: 設定ファイルの複雑さ

Claude Codeのワークフロー機能自体は非常に強力です。しかし、その設定には独自の構文とディレクトリ構造を理解する必要があります。

![画像](https://assets.st-note.com/img/1767344711-CyMv9qrXJfkpF6tKaBx2jThl.png?width=1200)

たとえば、コードレビュー用のカスタムコマンドを作るには、以下のようなMarkdownファイルを正確に記述する必要があります。

```python
# .claude/commands/review.md
---
description: Comprehensive code review
allowed-tools: Bash(git diff:*), Read
---

Perform a comprehensive code review focusing on:
1. TypeScript/React conventions
2. Error handling and accessibility
3. Test coverage and security
```

フロントマターの構文、allowed-toolsの書き方、適切なプロンプトの構成...覚えることが多いですよね。

### 課題2: 複雑なフローの可視化が困難

複数のエージェントが条件分岐しながら連携するワークフローを想像してみてください。「もしコードに問題があればセキュリティチェッカーに回して、なければドキュメント生成へ...」といった流れを、テキストファイルだけで管理するのは至難の業です。

### 課題3: 非エンジニアの参加障壁

ビジネスサイドのメンバーが「こういうワークフローがあれば便利なのに」と思っても、設定ファイルを書けなければ実現できません。アイデアを持つ人と実装する人が分断されてしまいます。

Workflow Studioは、これらすべての課題を **ビジュアルエディタ** という解決策で一気に解消します。

## Claude Code標準機能との関係性

「Workflow Studioを使うと、Claude Codeの標準機能は使えなくなるの？」という疑問を持つ方もいるかもしれません。答えは **No** です。

![画像](https://assets.st-note.com/img/1767344736-3U9tpLlbHZnrk05mPXTJ6wfq.png?width=1200)

Workflow Studioは、Claude Code標準機能の **上に乗るGUIレイヤー** です。ツール内で設計したワークフローは、最終的に.claude/agents/\*.mdや.claude/commands/\*.mdとして出力されます。つまり、出力フォーマットは完全に標準準拠なので、Workflow Studioを使っていないチームメンバーとも問題なく共有できます。

### 標準機能のおさらい

Workflow Studioを効果的に使うために、Claude Codeの標準機能を整理しておきましょう。

\\begin{array}{|l|l|l|} \\hline \\textbf{機能} &amp; \\textbf{場所} &amp; \\textbf{役割} \\\\ \\hline \\text{カスタムスラッシュコマンド} &amp; \\text{.claude/commands/.md} &amp; \\text{/command名で呼び出せる再利用可能なプロンプト} \\\\ \\hline \\text{サブエージェント} &amp; \\text{.claude/agents/.md} &amp; \\text{特定タスク専用のAIエージェント定義} \\\\ \\hline \\text{スキル} &amp; \\text{.claude/skills/} &amp; \\text{複数ファイルを含む包括的なワークフロー} \\\\ \\hline \\text{CLAUDE.md} &amp; \\text{プロジェクトルート} &amp; \\text{プロジェクト固有コンテキストの永続化} \\\\ \\hline \\text{Hooks} &amp; \\text{settings.json} &amp; \\text{ツール実行前後の自動処理} \\\\ \\hline \\end{array}

Workflow Studioは、これらの設定ファイルを **ビジュアルに作成・編集するツール** という位置づけです。

## 技術的な仕組みを理解する

ここからは、Workflow Studioがどのように動作するのかを見ていきましょう。技術的な詳細を知ることで、より効果的に活用できるようになります。

### アーキテクチャ概要

Workflow StudioはVS Code拡張機能として動作し、TypeScript/React 18.2で構築されています。

![画像](https://assets.st-note.com/img/1767344931-oA9uydJxLGMQSXclgTzPDnEt.png?width=1200)

### ノードタイプの全体像

Workflow Studioでは、8種類以上のノードを組み合わせてワークフローを設計します。

![画像](https://assets.st-note.com/img/1767344882-5i69IoypfCHPLcxW3GugKXSU.png?width=1200)

それぞれのノードをもう少し詳しく見てみましょう。

**(1) Promptノード**

最も基本的なノードで、AIへの指示を定義します。{{variableName}}形式のテンプレート変数を使用でき、動的な入力を受け付けられます。

**(2) Sub-Agentノード**

特定のタスクを担当する専門エージェントを定義します。使用するモデル（Haiku/Sonnet/Opus）の選択、ツール権限の設定、カスタムプロンプトの指定が可能です。

**(3) IfElseノード**

条件に基づく二択分岐を実現します。True/FalseやSuccess/Errorなど、シンプルな分岐ロジックに適しています。

**(4) Switchノード**

2つ以上の選択肢がある場合に使用します。たとえば「フロントエンド/バックエンド/インフラ」のような多分岐が必要なケースで活躍します。

**(5) AskUserQuestionノード**

ワークフローの途中でユーザーに選択を求めます。2〜4つのオプションを提示し、選択結果に応じて異なるパスに分岐できます。

**(6) Skillノード**

Claude Codeのスキル機能と連携します。既存のスキルを参照したり、新しいスキルを作成したりできます。

**(7) MCPノード**

Model Context Protocolを通じて外部サービスと連携します。データベースやAPI、GitHubなど様々なサービスとの接続が可能です。

### AI支援編集機能

Workflow Studioの特徴的な機能のひとつが、 **AI支援編集** です。ツールバーの✨アイコンをクリックすると、自然言語でワークフローを編集できます。

たとえば「入力データを検証するSub-Agentノードを追加して」と入力すると、AIがノードの追加と接続を自動で実行してくれます。会話履歴を維持しながら反復的に改善できるので、試行錯誤しながらワークフローを磨き上げることができます。

## インストールとセットアップ

ここからは実際にWorkflow Studioを使ってみましょう。

### 前提条件

まず、必要な環境を確認しておきます。

\\begin{array}{|l|l|} \\hline \\textbf{要件} &amp; \\textbf{詳細} \\\\ \\hline text{OS} &amp; \\text{Windows, macOS, Linux} \\\\ \\hline \\text{VS Code} &amp; \\text{1.80.0以上} \\\\ \\hline \\text{Node.js} &amp; \\text{18.0以上} \\\\ \\hline \\text{RAM} &amp; \\text{最低2GB（推奨4GB以上）} \\\\ \\hline \\text{Claude Code CLI} &amp; \\text{AI支援機能に必要} \\\\ \\hline \\text{Anthropic APIキー} &amp; \\text{claude.aiから取得} \\\\ \\hline \\end{array}

### インストール手順

最も簡単なのは、VS Code Marketplaceからのインストールです。

![画像](https://assets.st-note.com/img/1767345094-bgGPMWzX1IsDQUkBY3At9Tuq.png?width=1200)

## 基本的な操作方法

### エディタのインターフェース

Workflow Studioのエディタを開くと、以下のようなレイアウトが表示されます。

![画像](https://assets.st-note.com/img/1767345541-RnuZVXU4NGJ26tcxh79QkSdH.png?width=1200)

https://github.com/breaking-brake/cc-wf-studio/blob/main/resources/hero.png

画面は大きく3つのエリアに分かれています。

**(1) 左パネル（ノードパレット）**: 使用可能なノードタイプが並んでいます。ここからキャンバスにドラッグ＆ドロップでノードを追加します。

**(2) 中央（キャンバス）**: ワークフローを設計するメインエリアです。ノードを配置し、接続線で繋いでいきます。グリッドに沿って自動整列される機能もあります。

**(3) 右パネル（プロパティ）**: 選択中のノードの詳細設定を行います。ノード名、使用モデル、プロンプト内容、ツール権限などを編集できます。

### ワークフロー作成の5ステップ

実際にワークフローを作る流れを見ていきましょう。

![画像](https://assets.st-note.com/img/1767345221-TpMuRlBch4kWPGbOvasK70Xi.png?width=1200)

**(1) ノード追加**

左のパレットから必要なノードをドラッグして、キャンバス上にドロップします。

**(2) プロパティ設定**

ノードをクリックすると、右パネルに詳細設定が表示されます。プロンプト内容、モデルの選択、ツール権限などを設定します。

**(3) 接続作成**

ノードの右側にある出力ポート（小さな丸）から、別のノードの左側にある入力ポートへドラッグすると、接続線が作成されます。

**(4) 保存**

Ctrl+S（MacはCmd+S）でワークフローを保存します。.vscode/workflows/ディレクトリにJSON形式で保存されます。

**(5) エクスポート**

ツールバーの「Export」ボタンをクリックすると、.claude/agents/と.claude/commands/にMarkdownファイルが生成されます。

### エクスポート後の実行

エクスポートしたワークフローは、通常のClaude Codeコマンドとして実行できます。

```python
# ターミナルから直接実行
claude my-workflow "入力データ"

# Claude Code内からスラッシュコマンドとして実行
claude > /my-workflow
```

### 知っておきたい制限事項

Workflow Studioにはいくつかの制限があります。事前に把握しておきましょう。

\\begin{array}{|l|l|} \\hline \\textbf{制限項目} &amp; \\textbf{値} \\\\ \\hline \\text{ワークフローあたりの最大ノード数} &amp; \\text{50ノード} \\\\ \\hline \\text{AI処理タイムアウト} &amp; \\text{デフォルト90秒（30秒〜5分で設定可能）} \\\\ \\hline \\text{リクエスト文字数制限} &amp; \\text{2,000文字} \\\\ \\hline \\text{会話履歴} &amp; \\text{アクティブセッション中のみ保持} \\\\ \\hline \\end{array}

## 実践的なユースケース

ここからは、実際にどのようなワークフローが作れるのかを具体的に見ていきます。

### ユースケース1: ドキュメント要約パイプライン

長いドキュメントを自動で要約するワークフローです。

![画像](https://assets.st-note.com/img/1767345658-60rzNbPTLaV7AkdHoJQGmUug.png?width=1200)

各ノードの具体的な設定を見ていきましょう。

**(1) Document Input（Promptノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Document Input} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Prompt} \\\\ \\hline \\text{テンプレート変数} &amp; \\text{{{documentPath}}, {{outputFormat}}} \\\\ \\hline \\end{array}

```python
# プロンプト内容
以下のドキュメントを分析対象として読み込んでください。

ドキュメントパス: {{documentPath}}
希望する出力形式: {{outputFormat}}

ドキュメントの内容を次のエージェントに渡してください。
```

**(2) Key Extractor（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Key Extractor} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Haiku（高速処理優先）} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(cat:\*)} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたはドキュメント分析の専門家です。
渡されたドキュメントから以下の要素を抽出してください：

1. **主要なトピック**: 文書が扱う中心的なテーマ（3-5個）
2. **キーポイント**: 各トピックの重要な論点や主張
3. **データ・数値**: 文書内の具体的な数値や統計
4. **結論・提言**: 文書の結論部分の要点

出力形式はJSON形式で、次のエージェントが処理しやすい構造にしてください。
```

**(3) Summarizer（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Summarizer} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet（品質重視）} \\\\ \\hline \\text{allowed-tools} &amp; \\text{なし（テキスト処理のみ）} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたは要約作成のエキスパートです。
Key Extractorから渡された構造化データを基に、包括的な要約を作成してください。

要約の構成：
1. **エグゼクティブサマリー**（100字以内）
   - 文書の本質を一文で表現
2. **主要ポイント**（各50字以内×3-5項目）
   - 箇条書きで重要点を列挙
3. **詳細要約**（500字程度）
   - 論理的な流れを維持した要約文
4. **注目すべきデータ**
   - 重要な数値や統計を強調

読者が原文を読まなくても内容を把握できる品質を目指してください。
```

**(4) Formatter（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Formatter} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Haiku（整形処理）} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Write, Bash(mkdir:\*)} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたはドキュメント整形の専門家です。
Summarizerから渡された要約を、指定された出力形式に整形してください。

対応フォーマット：
- **markdown**: 見出しと箇条書きを活用した読みやすい形式
- **html**: スタイル付きのWebページ形式
- **json**: APIレスポンス向けの構造化形式

出力要件：
- ファイルとして保存する場合は適切な拡張子を付与
- 日本語の場合はUTF-8エンコーディングを使用
- 作成日時をメタデータとして含める
```

各ステージが独立したノードとして定義されているため、たとえば「Summarizerだけをより高性能なOpusに変更する」といった調整が簡単に行えます。

### ユースケース2: コード分析・修復ワークフロー

バグ検出から修正提案までを自動化するワークフローです。

![画像](https://assets.st-note.com/img/1767346921-2TrypAwF5SueIz4HtjKOBoaV.png?width=1200)

各ノードの具体的な設定を詳しく見ていきましょう。

**(1) Code Input（Promptノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Code Input} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Prompt} \\\\ \\hline \\text{テンプレート変数} &amp; \\text{{{targetPath}}, {{filePattern}}, {{excludeDirs}}} \\\\ \\hline \\end{array}

```python
# プロンプト内容
以下の条件でコードベースを読み込み、分析対象として準備してください。

対象パス: {{targetPath}}
ファイルパターン: {{filePattern}}  # 例: "*.ts,*.tsx,*.js"
除外ディレクトリ: {{excludeDirs}}  # 例: "node_modules,dist,build"

読み込んだファイルの一覧と総行数を次のエージェントに渡してください。
```

**(2) Analyzer（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Code Analyzer} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet（精度重視）} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(grep:, find:, wc:\*)} \\\\ \\hline \\end{array}

```php
# プロンプト内容
あなたは経験豊富なシニアエンジニアです。
渡されたコードベースを以下の観点で分析してください。

## 分析項目

### 1. バグ・エラー検出
- 潜在的なランタイムエラー
- 型の不整合
- null/undefined参照の可能性
- 無限ループのリスク

### 2. コードスタイル
- 命名規則の一貫性
- 関数の複雑度（循環的複雑度が高すぎないか）
- コードの重複

### 3. ベストプラクティス
- エラーハンドリングの適切さ
- 非同期処理のパターン
- セキュリティ上の懸念

## 出力形式
分析結果をJSON形式で出力してください：
{
  "hasBugs": boolean,
  "severity": "critical" | "high" | "medium" | "low" | "none",
  "issues": [
    {
      "file": "ファイルパス",
      "line": 行番号,
      "type": "bug" | "style" | "security",
      "description": "問題の説明",
      "suggestion": "修正案"
    }
  ]
}
```

**(3) HasBugs?（IfElseノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{HasBugs?} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{IfElse} \\\\ \\hline \\text{条件} &amp; \\text{hasBugs === true} \\\\ \\hline \\text{Trueの出力先} &amp; \\text{Security Checker} \\\\ \\hline \\text{Falseの出力先} &amp; \\text{DocGen} \\\\ \\hline \\end{array}

```php
# 条件判定ロジック
前のエージェントから渡されたJSONの "hasBugs" フィールドを評価します。

- hasBugs が true → Security Checker へルーティング
- hasBugs が false → DocGen へルーティング

追加条件（オプション）:
- severity が "critical" または "high" の場合は必ず True パスへ
```

**(4a) Security Checker（Sub-Agentノード）- バグありパス**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Security Checker} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(grep:, npm audit:)} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたはセキュリティ専門のエンジニアです。
Analyzerが検出した問題に対して、セキュリティの観点から追加分析を行ってください。

## チェック項目

### 脆弱性チェック
- SQLインジェクションの可能性
- XSS（クロスサイトスクリプティング）
- CSRF（クロスサイトリクエストフォージェリ）
- 機密情報のハードコーディング
- 安全でない依存関係

### 認証・認可
- 認証バイパスの可能性
- 権限昇格のリスク
- セッション管理の問題

## 出力形式
{
  "securityIssues": [...],
  "riskLevel": "critical" | "high" | "medium" | "low",
  "recommendations": ["推奨アクション1", "推奨アクション2"]
}
```

**(4a続) Fix Proposer（Sub-Agentノード）- バグありパス**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Fix Proposer} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Opus（高品質な修正案）} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Write, Bash(git diff:\*)} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたは熟練のソフトウェアエンジニアです。
AnalyzerとSecurity Checkerの分析結果を基に、具体的な修正案を作成してください。

## 修正案の要件

### 各問題に対して以下を提供
1. **問題の要約**: 何が問題なのかを簡潔に説明
2. **影響範囲**: この問題が引き起こす可能性のある影響
3. **修正コード**: 実際に適用可能なコード差分
4. **テスト案**: 修正を検証するためのテストケース

### 出力形式
修正案は以下の形式で出力：
- unified diff形式で修正内容を表示
- 各修正に優先度（P0〜P3）を付与
- 修正適用の推奨順序を提示

### 注意事項
- 既存の機能を破壊しない修正を心がける
- コードスタイルは既存のコードベースに合わせる
- 必要に応じてコメントを追加
```

**(4b) DocGen（Sub-Agentノード）- バグなしパス**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{DocGen} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Write} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたはテクニカルライターです。
分析したコードベースのドキュメントを生成してください。

## 生成するドキュメント

### 1. README.md
- プロジェクト概要
- セットアップ手順
- 使用方法
- ディレクトリ構造

### 2. API ドキュメント
- 公開関数/メソッドの説明
- パラメータと戻り値
- 使用例

### 3. アーキテクチャ図
- Mermaid記法でのコンポーネント図
- データフロー図

## 出力
生成したドキュメントをMarkdown形式で出力してください。
```

このワークフローのポイントは、IfElseノードによる条件分岐です。問題が見つかった場合のみセキュリティチェックと修正提案を行い、問題がなければドキュメント生成に進みます。処理の無駄を省きつつ、必要なケースでは徹底的な分析を行う効率的な設計です。

### ユースケース3: PRコードレビュー自動化

GitHub連携を活用したコードレビュー自動化ワークフローです。

![画像](https://assets.st-note.com/img/1767346777-M6Ql3ecwtJpvsHO5UyFEd8Ih.png?width=1200)

各ノードの具体的な設定を見ていきましょう。

**(1) GitHub MCP - PR検知（MCPノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{GitHub PR Detector} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{MCP} \\\\ \\hline \\text{MCPサーバー} &amp; \\text{@modelcontextprotocol/server-github} \\\\ \\hline \\text{認証} &amp; \\text{GITHUB\\\_TOKEN環境変数} \\\\ \\hline \\end{array}

```ruby
# MCP設定
サーバー: @modelcontextprotocol/server-github
操作: pull_request.get

# 取得するデータ
- PRのタイトルと説明
- 変更されたファイルの一覧
- 差分（diff）の内容
- PRの作成者情報
- ベースブランチとヘッドブランチ

# 出力形式
{
  "prNumber": 123,
  "title": "PRタイトル",
  "description": "PR説明",
  "files": [
    {
      "filename": "src/components/Button.tsx",
      "status": "modified",
      "additions": 10,
      "deletions": 5,
      "patch": "差分内容"
    }
  ],
  "author": "username"
}
```

**(2) File Type Router（Switchノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{File Type Router} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Switch} \\\\ \\hline \\text{分岐数} &amp; \\text{3（Frontend / Backend / Infra）} \\\\ \\hline \\text{デフォルト} &amp; \\text{Backend Reviewer} \\\\ \\hline \\end{array}

```python
# 分岐条件

## Branch 1: Frontend
ファイル拡張子が以下のいずれかに該当:
- .tsx, .ts（src/components/, src/pages/配下）
- .css, .scss, .less
- .html, .jsx

## Branch 2: Backend  
ファイル拡張子が以下のいずれかに該当:
- .py, .go, .java, .rs
- .sql
- src/api/, src/services/配下の.ts

## Branch 3: Infrastructure
ファイル拡張子が以下のいずれかに該当:
- .tf, .tfvars（Terraform）
- .yaml, .yml（kubernetes/, .github/配下）
- Dockerfile, docker-compose.yml
- .env.example

# 複数カテゴリに該当する場合
ファイルごとに適切なレビュアーにルーティング
（1つのPRで複数のレビュアーが動作する可能性あり）
```

**(3a) Frontend Reviewer（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Frontend Reviewer} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(npm:, eslint:)} \\\\ \\hline \\end{array}

**(3b) Backend Reviewer（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Backend Reviewer} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(pytest:, go test:)} \\\\ \\hline \\end{array}

**(3c) Infrastructure Reviewer（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Infrastructure Reviewer} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(terraform validate:\*)} \\\\ \\hline \\end{array}

**(4) GitHub MCP - コメント投稿（MCPノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{GitHub Comment Poster} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{MCP} \\\\ \\hline \\text{MCPサーバー} &amp; \\text{@modelcontextprotocol/server-github} \\\\ \\hline \\text{操作} &amp; \\text{pull\\\_request.createReview} \\\\ \\hline \\end{array}

```cs
# MCP設定
サーバー: @modelcontextprotocol/server-github
操作: pull_request.createReview

# 投稿内容の構成
1. サマリーコメント（PRの全体評価）
2. インラインコメント（各ファイルの特定行へのコメント）
3. レビューステータス（APPROVE / REQUEST_CHANGES / COMMENT）

# 投稿形式
レビュアーごとの結果を統合し、以下の形式で投稿:

## 🤖 AI Code Review Summary

### Frontend Review
[Frontend Reviewerの結果]

### Backend Review  
[Backend Reviewerの結果]

### Infrastructure Review
[Infrastructure Reviewerの結果]

---
*This review was automatically generated by Claude Code Workflow Studio*
```

### ユースケース4: インタラクティブなデータ分析

ユーザーの選択に応じて分析内容を変えるワークフローです。

![画像](https://assets.st-note.com/img/1767346733-faBQ5yY7LelZOtSkT6mgb9od.png?width=1200)

各ノードの具体的な設定を見ていきましょう。

**(1) Data Input（Promptノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Data Input} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Prompt} \\\\ \\hline \\text{テンプレート変数} &amp; \\text{{{dataSource}}, {{dataFormat}}} \\\\ \\hline \\end{array}

```python
# プロンプト内容
以下のデータソースを分析対象として読み込んでください。

データソース: {{dataSource}}
データ形式: {{dataFormat}}  # csv, json, excel, database

データの基本情報を取得してください：
- 行数・列数
- 各カラムのデータ型
- 欠損値の有無
- 基本統計量（数値列の場合）

この情報を次のステップに渡してください。
```

**(2) Analysis Type?（AskUserQuestionノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Analysis Type Selector} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{AskUserQuestion} \\\\ \\hline \\text{選択肢数} &amp; \\text{3} \\\\ \\hline \\end{array}

```python
# 質問内容
データの概要を確認しました。どのような分析を行いますか？

## 選択肢

### 選択肢1: 📈 統計分析
データの統計的特性を深掘りします。
- 相関分析
- 分布の確認
- 外れ値検出
- 仮説検定

### 選択肢2: 📊 可視化
データを視覚的に表現します。
- グラフ・チャートの生成
- ダッシュボード作成
- トレンド可視化

### 選択肢3: 🔮 予測モデル
機械学習モデルを構築します。
- 回帰分析
- 分類モデル
- 時系列予測

# ルーティング
選択肢1 → Statistical Analyzer
選択肢2 → Visualization Generator  
選択肢3 → Prediction Model
```

**(3a) Statistical Analyzer（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Statistical Analyzer} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(python:\*), Write} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたはデータサイエンティストです。
渡されたデータに対して統計分析を実行してください。

## 分析項目

### 記述統計
- 中心傾向（平均、中央値、最頻値）
- 散布度（分散、標準偏差、範囲、四分位範囲）
- 歪度と尖度

### 相関分析
- ピアソン相関係数
- スピアマン順位相関
- 相関行列のヒートマップ

### 分布分析
- ヒストグラム
- Q-Qプロット
- 正規性検定（Shapiro-Wilk）

### 外れ値検出
- IQR法
- Zスコア法
- 外れ値の影響評価

## 出力
Pythonスクリプトを生成・実行し、結果をJSON形式で出力：
{
  "descriptive_stats": {...},
  "correlations": {...},
  "distribution_tests": {...},
  "outliers": {...},
  "insights": ["洞察1", "洞察2"]
}
```

**(3b) Visualization Generator（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Visualization Generator} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(python:\*), Write} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたはデータビジュアライゼーションの専門家です。
渡されたデータを視覚的に表現してください。

## 生成するビジュアライゼーション

### 必須グラフ
1. **データ概要ダッシュボード**
   - KPIカード（主要指標）
   - 分布ヒストグラム
   - 時系列トレンド（該当する場合）

2. **相関可視化**
   - 散布図マトリクス
   - 相関ヒートマップ

3. **カテゴリ分析**（カテゴリ変数がある場合）
   - 棒グラフ
   - 円グラフ
   - ボックスプロット

### 使用ライブラリ
- matplotlib / seaborn（静的グラフ）
- plotly（インタラクティブグラフ）

### 出力形式
- PNG画像（静的グラフ）
- HTML（インタラクティブグラフ）
- 各グラフの解釈コメント

## 出力
{
  "charts": [
    {
      "title": "グラフタイトル",
      "type": "histogram",
      "file": "output/chart1.png",
      "interpretation": "このグラフから読み取れること"
    }
  ]
}
```

**(3c) Prediction Model（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Prediction Model Builder} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Opus（複雑なモデリング）} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Bash(python:\*), Write} \\\\ \\hline \\end{array}

```ruby
# プロンプト内容
あなたは機械学習エンジニアです。
渡されたデータに対して予測モデルを構築してください。

## モデリングプロセス

### 1. データ前処理
- 欠損値処理（補完 or 削除）
- カテゴリ変数のエンコーディング
- 特徴量スケーリング
- 訓練/テスト分割（80/20）

### 2. モデル選択
データの特性に応じて適切なモデルを選択：

**回帰タスクの場合:**
- 線形回帰
- ランダムフォレスト回帰
- XGBoost回帰

**分類タスクの場合:**
- ロジスティック回帰
- ランダムフォレスト分類
- XGBoost分類

### 3. モデル評価
**回帰:** RMSE, MAE, R²
**分類:** Accuracy, Precision, Recall, F1, AUC-ROC

### 4. 特徴量重要度
- 各特徴量の予測への寄与度
- SHAP値（解釈可能性）

## 出力
{
  "model_type": "XGBoost Regressor",
  "metrics": {
    "rmse": 0.123,
    "r2": 0.89
  },
  "feature_importance": [...],
  "predictions_sample": [...],
  "model_file": "output/model.pkl"
}
```

**(4) Report Generator（Sub-Agentノード）**

\\begin{array}{|l|l|} \\hline \\textbf{設定項目} &amp; \\textbf{値} \\\\ \\hline \\text{ノード名} &amp; \\text{Report Generator} \\\\ \\hline \\text{ノードタイプ} &amp; \\text{Sub-Agent} \\\\ \\hline \\text{使用モデル} &amp; \\text{Claude Sonnet} \\\\ \\hline \\text{allowed-tools} &amp; \\text{Read, Write} \\\\ \\hline \\end{array}

```python
# プロンプト内容
あなたはビジネスアナリストです。
前のステップで得られた分析結果を、ビジネス向けのレポートにまとめてください。

## レポート構成

### 1. エグゼクティブサマリー
- 分析の目的と範囲
- 主要な発見事項（3点以内）
- 推奨アクション

### 2. データ概要
- データソースの説明
- 分析対象期間
- データ品質の評価

### 3. 分析結果
- 実施した分析の詳細
- 図表を含む結果の説明
- 統計的な裏付け

### 4. 洞察と提言
- ビジネスインパクトの解釈
- 具体的なアクションプラン
- リスクと注意点

### 5. 付録
- 詳細な統計データ
- 使用した手法の説明
- 再現手順

## 出力形式
- Markdownレポート
- PDF版（オプション）
- プレゼンテーション用スライド要約
```

AskUserQuestionノードを使うことで、ワークフローの途中でユーザーに選択を求めることができます。同じデータに対して、ユーザーのニーズに応じた異なる分析を提供できる柔軟なワークフローです。

## 従来手法との比較

Workflow Studioを使うことで、具体的にどのようなメリットがあるのでしょうか。

![画像](https://assets.st-note.com/img/1767347081-9lnctAhFE7SGk3zojWfYxQrO.png?width=1200)

### 具体的なメリットまとめ

**(1) 開発効率の向上**

「アイデアをスケッチして、いくつかのノードを接続し、数時間ではなく数分で動作するプロトタイプを作成できる」というユーザーフィードバックが示すように、設定ファイルを直接編集する方式と比較して大幅な時間短縮が期待できます。

**(2) エラー削減と可視化**

YAML/JSON構文エラーのデバッグから解放され、複雑なエージェント間の相互作用を視覚的に把握できます。ノード間の接続関係が明確に表示されるため、論理的な問題を発見しやすくなります。

**(3) 非プログラマーへのアクセシビリティ**

「プログラミング経験不要でAIワークフローを構築可能」という設計思想により、エンジニア以外のチームメンバーもワークフロー設計に参加できます。ビジネスサイドの知見をワークフローに直接反映できる点は大きなメリットです。

**(4) チーム協業の促進**

ワークフローがJSON形式で保存されGit管理できるため、変更履歴の追跡やコードレビューが容易です。エクスポートされたMarkdownファイルは標準準拠のため、Workflow Studioを使用していないメンバーとも共有可能です。

## 効果的に活用するためのポイント

最後に、Workflow Studioを効果的に活用するためのポイントをお伝えします。

### 事前に身につけておくと良い知識

\\begin{array}{|l|l|l|} \\hline \\textbf{知識} &amp; \\textbf{必要度} &amp; \\textbf{説明} \\\\ \\hline \\text{Claude Codeの基本操作} &amp; \\text{必須} &amp; \\text{ターミナルでの対話、基本コマンド} \\\\ \\hline \\text{.claudeディレクトリ構造} &amp; \\text{推奨} &amp; \\text{commands, agents, skillsの役割} \\\\ \\hline \\text{プロンプトエンジニアリング基礎} &amp; \\text{推奨} &amp; \\text{効果的なプロンプトの書き方} \\\\ \\hline \\text{VS Code操作} &amp; \\text{必須} &amp; \\text{拡張機能のインストール、コマンドパレット} \\\\ \\hline \\end{array}

ただし、公式ドキュメントとインタラクティブツアーが充実しているため、Claude Code初心者でも段階的に学習できる設計になっています。

### 学習のロードマップ

![画像](https://assets.st-note.com/img/1767347202-vSYeT45R61UyMchVqm2JWrBO.png?width=1200)

最初から複雑なワークフローを作ろうとせず、まずはシンプルなものから始めて徐々にステップアップしていくことをおすすめします。

## まとめ

Claude Code Workflow Studioは、Claude Codeの強力なワークフロー機能を **ビジュアルエディタという新しいインターフェース** で解放するツールです。

従来は設定ファイルを手動で書く必要があり、複雑なマルチエージェントワークフローの設計は技術的なハードルが高いものでした。Workflow Studioは、ドラッグ＆ドロップでノードを配置し接続するだけで、誰でも直感的にAIワークフローを設計できる環境を提供します。

**1,100以上のGitHubスター** と活発な開発活動（297件のマージ済みPR）は、コミュニティからの支持を示しています。日本語を含む多言語対応、AI支援編集機能、VS Codeとの深い統合など、実用性を重視した機能設計が特徴的です。

AIワークフローの構築を「コマンドライン専用」から「ユニバーサルアクセシビリティ」へと進化させるこのツール。Claude Codeを活用している方、これからAIエージェントによる自動化に取り組みたい方は、ぜひ一度試してみてはいかがでしょうか。

---

**参考リンク**

- GitHub: [https://github.com/breaking-brake/cc-wf-studio](https://github.com/breaking-brake/cc-wf-studio)
- VS Code Marketplace: [https://marketplace.visualstudio.com/items?itemName=breaking-brake.cc-wf-studio](https://marketplace.visualstudio.com/items?itemName=breaking-brake.cc-wf-studio)
- 公式ドキュメント: [https://breaking-brake.com/](https://breaking-brake.com/)

---

**この記事が役に立ったら、ぜひスキ❤️やコメントをお願いします！質問があれば、コメント欄でお気軽にどうぞ。**

## テクノロジーで、あなたのビジネスに革新を

![画像](https://assets.st-note.com/img/1767347704-MEFWUKDmbAk7BGOjRiCV9qdf.png?width=1200)

この記事をお読みいただき、ありがとうございます。「システムを作りたいけど、初期投資が高すぎる」「IoT製品を開発したいが、技術とコストの両面で不安」とお悩みではありませんか?

### ✨ 初期費用0円でSaaSを開発。ポノテクのマイクロSaaSサービス

私たちポノテク株式会社は、 **お客様専用のSaaSを初期費用0円で開発** します。

![画像](https://assets.st-note.com/img/1767347704-cAbe6sjnoxGUO7Rg0hM5qtCD.png?width=1200)

**マイクロSaaS開発の特徴**

- **初期費用0円**: Webアプリ、モバイルアプリ、デスクトップアプリを無料で開発
- **月額サブスクで提供**: 必要な機能に応じた月額料金で利用開始
- **買取オプション**: サブスク利用中に、システムを自社所有物として買い取ることも可能

「自社専用のSaaSが欲しいけど、数百万円の初期投資は厳しい」そんな企業様に最適なソリューションです。

[**マイクロSaaS開発｜初期費用0円で最短2–6週間｜SDK＋AI｜ポノテク** *SDK＋AIで貴社専用SaaSを短期構築。初期費用0円の「マイクロSaaS開発」。まずは無料Fit診断で現状とゴールを整理* *zero-saas.ponotech.work*](https://zero-saas.ponotech.work/)

### 🔧 IoT受託開発 × 補助金活用で、ものづくりを支援

ハードウェアからソフトウェアまで一貫して開発可能。IoTシステムの構築を、補助金を活用して最大66%のコスト削減で実現します。

![画像](https://assets.st-note.com/img/1767347704-iKDX2SU7NbtycfGQlA3xWHPn.png?width=1200)

**補助金活用でシステム開発コスト削減**

経済産業省認定のIT導入支援事業者として、以下のサービスをワンストップで提供。

- **補助金診断・申請サポート**: 採択率82.8%の実績で、最適な補助金をご提案
- **要件定義から開発まで一貫支援**: 補助金要件に100%準拠した開発体制
- **省力化補助金・ものづくり補助金など**: 最大8,000万円の補助金活用をサポート

[**補助金活用システム開発 | 開発コスト最大66%削減** *補助金獲得のプロとシステム開発のプロがタッグを組み、DX推進や新規ビジネスに必要なシステム開発を低コストで実現します。採択* *hojokin-dev.ponotech.net*](https://hojokin-dev.ponotech.net/)

### 📚 最新刊『ComfyUIマスターガイド』5月9日発売！

AI技術に関する深い知見を持つ私たちの代表・早野康寛が共著者として参加した画像生成AI書籍『ComfyUIマスターガイド』が、2025年5月9日にSBクリエイティブ社より発売されました。AI画像生成の最前線を理解したい方は、ぜひご覧ください。

### 📈 こんな課題をお持ちの企業様に最適です

- 「専用SaaSが欲しいが、初期投資を抑えたい」
- 「IoT製品を開発したいが、ハードとソフト両方の知見が必要」
- 「補助金を活用したいが、申請方法がわからない」
- 「サブスクで始めて、必要なら買い取りたい」

### 🌟 三つの強みで、確かな未来を共に創る

1. **マイクロSaaS開発**: 初期費用0円で専用システムを構築
2. **IoT受託開発**: ハードウェアからソフトウェアまで一貫対応
3. **補助金活用**: 開発コストを最大66%削減

ぜひ初回無料相談をご利用ください。技術と経営の両面から、貴社の成長戦略を共に考えましょう。  
ポノテク株式会社へのお問い合わせはこちらから！

[**CONTACT - PONOTECH** *ポノテク株式会社へのお問い合わせはこちらから！生成AIから組み込みソフトウェアまで、幅広い開発に対応いたします。* *www.ponotech.net*](https://www.ponotech.net/contact)

▶ [**テクノロジーで成長を加速する第一歩を踏み出す**](https://www.ponotech.net/)

― 技術で未来を創る。ポノテク株式会社

Claude Code Workflow Studio完全ガイド｜ビジュアルでAIワークフローを構築する新時代｜アイドリ | AI-Driven Lab