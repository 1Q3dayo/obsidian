---
title: "Everything Claude Codeを眺めてみる | oikon48"
source: "https://oikon48.dev/ja/blog/everything-claude-code/"
author:
published: 2026-03-21
created: 2026-03-23
description: "Anthropicハッカソン優勝者のリポジトリEverything Claude Codeを眺めてみる"
tags:
  - "clippings"
  - "raw"
---
[Everything Claude Code](https://github.com/affaan-m/everything-claude-code) はAnthropicのハッカソンの優勝者が公開したリポジトリとして2026年1月に話題になりました。

[

GitHub - affaan-m/everything-claude-code: The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.

The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond. - affaan-m/everything-cla...

github.com

![](https://opengraph.githubassets.com/41412e7bdad648896033b84bb8a5743cd5d9b4296e70e5695fd964bb45914adf/affaan-m/everything-claude-code)](https://github.com/affaan-m/everything-claude-code)

作者のcogsec (X:[@affaanmustafa](https://x.com/affaanmustafa))氏もXでClaude CodeのTipsを公開していたため多くの人が読んだのではないでしょうか？私もそのうちの1人で実践的で分かりやすい内容だと思いました。

そこから2ヶ月経過して、先日Claude Codeの公式GitHubリポジトリのスター数をEverything Claude Codeが抜いたようです。このことからも注目度の高さが伺えます。

タイミング良く先日「 [ハッカソン優勝者はこう使うのか！「Everything Claude Code」から学ぶ 基本と実践](https://offers-jp.connpass.com/event/385385/) 」という企画の登壇をしてきました。今見るとまるでOikonがハッカソン優勝者のようなタイトルでとても恐れ多いですね。

登壇するからには最新のEverything Claude Codeの勉強をしようと思いリポジトリを覗いたのですが、1月に拝見した時とは全く別のリポジトリになっていたのが印象的でした。登壇スライドも置いておきます。

[

Everything Claude Code を眺める

X: https://x.com/oikon48 Event link: https://offers-jp.connpass.com/event/385385/ Everything Claude Code: https://github.com/affaan-m/everything-c&hellip;

speakerdeck.com

![](https://files.speakerdeck.com/presentations/73f4cc6aeb1e49ff91e4e011c562c2a5/slide_0.jpg?38757592)](https://speakerdeck.com/oikon48/every-claude-code-wotiao-meru)

せっかくなので個人的に面白いと思った最新のEverything Claude Code (通称: ECC)の内容をこの記事でまとめたいと思います。ちなみにこの記事では、ECCのインストール方法やどうやって使うべきかなどについては言及するつもりはありません。Tips的な内容の記事は探せばたくさんあるのでそちらを読むのをお勧めします。

## Everything Claude Codeに何が入っているか

![Everything Claude Code の構成（Rules / Agents / Skills / Commands / Hooks / Scripts）](https://oikon48.dev/images/everything-claude-code/architecture.png)

ECCには何が含まれているか確認してみましょう。

| カテゴリ | 数量 | 概要 |
| --- | --- | --- |
| Rules | common 9 + 9言語別 | coding-style / security / testing / git-workflow など全言語共通 + TypeScript・Python・Go・Swift・Kotlin・Perl・PHP・C++・Rust |
| Agents | 25 | 設計・計画 / 品質・レビュー / 実装支援 / 言語別（Go/Kotlin/Python/C++/Rust/Java）/ 運用・文書 |
| Skills | 108 | ワークフロー定義（コア・多言語・フレームワーク・テスト・DB・インフラ・セキュリティ・AI等） |
| Commands | 57 | `/plan` `/tdd` `/orchestrate` などスラッシュコマンド群 |
| Hooks | 23 | セッション管理 / コード品質 / 安全ガード / コンテキスト / ビルド / 外部連携 |
| Scripts | 997テスト | Node.js ベース、Windows・macOS・Linux クロスプラットフォーム対応 |

とてつもなく多いですね。最近Claude Codeを触り始めた初学者の方は圧倒されるんじゃないでしょうか？

とりあえずプラグインインストールする方も多いと思いますが、READMEには「自分に必要なものだけ選んでカスタマイズしてね」という意図の文章が書かれているので全てを入れる必要はないと思います。

> ### Customization
> 
> These configs work for my workflow. You should:
> 
> 1. Start with what resonates
> 2. Modify for your stack
> 3. Remove what you don’t use
> 4. Add your own patterns

全ての機能をインストールすると、コンテキストの圧迫や冗長なハーネスになってしまうので注意が必要です。

一方で、ECCのリポジトリには複数のコンポーネントを組み合わせて使うものもありました。

### Agents + Skills combination (Agents + Skillsの連携)

Subagentsのdoc-updater agentsは以下のようなフロントマターが存在しています。

```yaml
---
name: doc-updater
description: Documentation and codemap specialist. Use PROACTIVELY for updating codemaps and documentation. Runs /update-codemaps and /update-docs, generates docs/CODEMAPS/*, updates READMEs and guides.
tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
model: haiku
---
```

このSubagentsのDescriptionには以下の2つのSkillsが含まれています。

- /update-codemaps
- /update-docs

つまりこのSubagentsを使用する際には、Skillsも呼び出されるということです。

### Short Description (短いDescription)

ECCのCommandsやSkills、AgentsなどのDescriptionの短いのも特徴的だと思います。

```yaml
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediatel after writing or modifying code. MUST BE USED for all code changes.
tools: ["Read", "Grep", "Glob", "Bash"]
model: sonnet
---
```

たとえば上記のようなcode-reviewer agentsを見ても先ほどのdoc-updater同様にDescriptionが短いです。実際にECCを使ってみるとわかると思いますが、このcode-reviewer agentsはコードに変更があるとよく呼ばれます。DescriptionにMUST BE USEDという文言があるのはもちろんのこと、呼び出される確率が高いのもdescriptionが簡潔であることも理由の一つだと思います。経験上長すぎるDescriptionはあまり効果的ではありません。

### Model choice (モデルの選択)

ECCを眺めていると面白いCommandsもいくつか見つかります。

![/model-route コマンドのイメージ](https://oikon48.dev/images/everything-claude-code/model-route.png)

`/model-route` コマンドはタスクを引数として与えると、Haiku / Sonnet / Opus のClaudeモデルの中から「どのモデルを使うべきか」「なぜそのモデルを選択するか」を提案してくれます。

個人的にECCで興味深かったのはモデルをinheritではなく細かく設定していること、またほとんどのタスクはSonnetで十分だという思想を感じました。

Sonnetで十分な理由を私なりに考察すると、ECCはタスクのドメインを細分化しており、AgentやCommandの実行するべきタスクがはっきりしていることが多いです。適切な粒度でワークフローが分割されていれば、実行するモデルは必ずしもOpusの最上位モデルでなくても問題ないのだと思います。

## Orchestrate（/orchestrate）

![Agent Orchestration Pipeline（feature と Handoff）](https://oikon48.dev/images/everything-claude-code/diagram3-orchestration.png)

ECCの中のコマンドの一つである `/orchestrate` コマンドを見てみます。たとえば以下のような複数のSubagentsでワークフローを作っています。

- feature: planner（opus）→ tdd-guide → code-reviewer → security-reviewer

ほかにも

- bugfix: planner → tdd-guide → code-reviewer
- refactor: architect → code-reviewer → tdd-guide
- security: security-reviewer → code-reviewer → architect

など複数のオーケストレーションに対応しています。

ここから一つ分かるのは、エージェントワークフローを組む際にはエージェントごとに責務を切り分けており、オーケストレーションの目的に応じてエージェントの並べ替えを行っていることです。汎用タスクを実行できるgeneral-purposeを指示によって責務を与えるよりも、特化したエージェントをあらかじめ用意して利用する方が効果的というECCの考えが伺えます。

## Instinct model（continuous-learning-v2）

![Instinct モデルの流れ（Continuous Learning Pipeline）](https://oikon48.dev/images/everything-claude-code/diagram4-learning.png)

現在のECCには自動学習システムが盛り込まれています。以下のような流れです。

```bash
Session Activity (in a git repo)
      |
      | Hooks capture prompts + tool use (100% reliable)
      | + detect project context (git remote / repo path)
      v
+---------------------------------------------+
|  projects/<project-hash>/observations.jsonl  |
|   (prompts, tool calls, outcomes, project)   |
+---------------------------------------------+
      |
      | Observer agent reads (background, Haiku)
      v
+---------------------------------------------+
|          PATTERN DETECTION                   |
|   * User corrections -> instinct             |
|   * Error resolutions -> instinct            |
|   * Repeated workflows -> instinct           |
|   * Scope decision: project or global?       |
+---------------------------------------------+
      |
      | Creates/updates
      v
+---------------------------------------------+
|  projects/<project-hash>/instincts/personal/ |
|   * prefer-functional.yaml (0.7) [project]   |
|   * use-react-hooks.yaml (0.9) [project]     |
+---------------------------------------------+
|  instincts/personal/  (GLOBAL)               |
|   * always-validate-input.yaml (0.85) [global]|
|   * grep-before-edit.yaml (0.6) [global]     |
+---------------------------------------------+
      |
      | /evolve clusters + /promote
      v
+---------------------------------------------+
|  projects/<hash>/evolved/ (project-scoped)   |
|  evolved/ (global)                           |
|   * commands/new-feature.md                  |
|   * skills/testing-workflow.md               |
|   * agents/refactor-specialist.md            |
+---------------------------------------------+
```

(上記は `/continuous-learning-v2` Skillsに記載されているワークフロー)

基本的にはコーディングエージェントがツールを使用するタイミング(PreToolUse/PostToolUse)で、ユーザープロンプト・ツール使用・プロジェクトコンテキストを `~/.claude/homuncles/` に自動で書き込みます(Project設定の場合は `projects/<project-hash>/observations.jsonl` に保存される)。

記録したObservationファイル(jsonl)をBackgroundでClaude Haiku Agentがパターン分析を行います。ここで解析した記録をinstinctsファイル(Global: `instincts/personal/`, Project: `projects/<project-hash>/instincts/personal/`)としてconfidence score付きで記録します。

ある程度instinctファイルが自動で溜まってきたタイミングで、 `/evolve` を実行するとinstinct fileをクラスタ化し、commands, skills, agentsを作成してくれます。また、 `/promote` で複数プロジェクトで再現したconfidence scoreを元にglobal設定に昇格させることができます。

このような自動でエージェントにセッションを記録させて学習させる仕組みは、現在プロトタイプとして実装されている程度ですが、今後自動記憶する仕組みは発達していき、徐々にエージェントの自律運用が進むシステムが成熟していくことを示唆しています。

## OpenClaw とセキュリティ

2026年1月ごろにOpenClaw(旧ClawdBot)が話題になりました。この際、ECCの作者は [`The Hidden Danger of OpenClaw`](https://github.com/affaan-m/everything-claude-code/blob/main/the-openclaw-guide.md) という長文の記事を書いています。

[

https://github.com/affaan-m/everything-claude-code/blob/main/the-openclaw-guide.md

github.com

](https://github.com/affaan-m/everything-claude-code/blob/main/the-openclaw-guide.md)

この記事はOpenClawの危険性を指摘しているのですが、個人的にはECCの思想を理解する上でもかなり重要な文章だと思います。

主張を簡単にまとめると以下のような内容です。

- Telegram / Discord / X / Email などの複数チャネル統合は、そのまま攻撃面の増大につながる
- コミュニティ配布のSkillやPluginは便利だが、未監査のまま導入するとサプライチェーン攻撃の入口になりうる
- 自律エージェントに広い権限を与えるなら、sandbox・最小権限・監査ログが前提であるべき
- 便利さを優先して外部接続を増やすほど、prompt injectionの被害が横展開しやすくなる

ECC全体を見ていると、単に「便利なコマンド集」というより、AIエージェントの実行環境をどう構造化するかに強い関心があることがわかります。 `security-reviewer` のようなAgentや、Hook・memory・instinct の仕組みも、突き詰めると「エージェントにどこまで自由を与えるのか」「その自由をどう制御するのか」という話に繋がっています。

### 技術者は OpenClaw を使うべきか

OpenClawの記事で個人的に面白かったのは、「安全に使える人はそれを必要とせず、必要とする人は安全に使えない」という話です。

記事の中では技術者であれば以下のようなものを自分で管理できると指摘しています。

- SSH / tmux を使った常時接続のセッション
- cron や scheduler による定期実行
- Claude Code や Codex のようなハーネスの直接利用
- Playwright や API を使った限定的な自動化
- 自前で監査したSkills / Hooks / Commands の運用

これに関しては私も同意です。また、この記事を執筆している数日前にClaude Codeも公式でDiscordとTelegramをサポートしました。最近ではRemote Control機能やcronも内蔵されているので、OpenClawの運用をClaude Codeでも実現できるようになっていると思います。

ある程度ターミナルやサーバー運用に慣れている技術者は、オーケストレーションの本質である「複数のタスクをどう分割し、どう監視し、どこまで権限を渡すか」を自分で決められることが可能です。

### ECC に入っている NanoClaw

![nanoclaw](https://oikon48.dev/images/everything-claude-code/nanoclaw.png)

ECCには実はOpenClawを最小限に実装した NanoClaw というエージェントが使えます。ECCのGitHubリポジトリ内の `node scripts/claw.js` ですぐ試すことができます。実装は Node の標準モジュールだけで動き、ランタイムの外部依存は増やさない方針が README や Skill でも繰り返し強調されています。内部では `claude -p` にプロンプトを渡す形で応答を得て、やり取りは Markdown ファイルとして `~/.claude/claw/<session>.md` にターン単位で追記されます。

| 原則 | OpenClaw | MiniClaw |
| --- | --- | --- |
| アクセスポイント | 多数（Telegram、X、Discord、メール、ブラウザ） | 1つ（SSH） |
| 実行 | ホストマシン、広範なアクセス | コンテナ化、制限付き |
| インターフェース | ダッシュボード + GUI | Headless ターミナル（tmux） |
| スキル | ClawdHub（未審査のコミュニティマーケットプレイス） | 手動監査、ローカルのみ |
| ネットワーク露出 | 複数ポート、複数サービス | SSH のみ（Tailscale mesh） |
| Blast radius | エージェントがアクセスできるすべて | プロジェクトディレクトリにサンドボックス化 |
| セキュリティ態勢 | 暗黙的（何に露出しているかわからない） | 明示的（すべての権限を自分で選択） |

(the-openclaw-guide.mdより引用)

ここまで話してきたようにECCの作者もOpenClawについてインターフェースとセキュリティについて言及をしており、AnthropicさえもClaude Codeの機能にOpenClawのアイデアを取り入れているほどです(AnthropicはOpenClawに言及することはないと思いますが)。OpenClaw、もしくはそれに準ずるエージェントについては、一度自分の手で安全な環境で確認して今後のエージェント運用について改めて考える機会を設けるといいでしょう。

## まとめ

Everything Claude Code は、Claude Code のTips集や便利設定集として読むだけでも面白いですが、それ以上にAIエージェント運用の設計思想集として読む価値があるリポジトリだと思いました。

ECCは全部入りの巨大パッケージに見えますが、実際には「全部使え」というより、自分のワークフローを分解し、必要なものだけ選んで構造化していくためのサンプル集として読むのが良いのだと思います。

私自身、Agentの分割の仕方、Descriptionの書き方、HookやSkillの責務の切り方などは今回改めて一通り動かしてみて参考になりました。

OpenClawのようなエージェントも2026年はさらに話題になっていくと思うので、今のうちにエージェントのインターフェースとセキュリティについて考えを整理しておく良い機会だと思います。