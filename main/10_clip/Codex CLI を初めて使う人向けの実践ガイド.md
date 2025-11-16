---
title: "Codex CLI を初めて使う人向けの実践ガイド"
source: "https://zenn.dev/hokuto_tech/articles/97fa88f7805a23"
author:
  - "[[Zenn]]"
published: 2025-09-30
created: 2025-11-17
description:
tags:
  - "clippings"
---
198

104[tech](https://zenn.dev/tech-or-idea)

この記事は「 [Claude Code を初めて使う人向けの実践ガイド](https://zenn.dev/hokuto_tech/articles/86d1edb33da61a) 」を [OpenAI Codex CLI](https://openai.com/ja-JP/codex/) 前提で全面的に書き直したものです。

Codex は [Claude Code](https://claude.com/product/claude-code) のようにターミナルで動作するローカルのコーディングエージェントで、コードの生成・編集、テストの実行、各種ツール（MCP）連携まで自然言語で指示できます。

## 導入手順

```bash
npm install -g @openai/codex

# mise (https://mise.jdx.dev/)を使っている場合
mise install npm:@openai/codex
mise use -g npm:@openai/codex
```

ワークディレクトリで以下のコマンドを実行。

## 過去のセッション(会話)を再開したい場合

過去のセッション(会話)を再開したい場合は以下のコマンドで実行

```bash
codex resume # 対象のセッションを選択
codex resume --last  #　最新のセッションで起動
codex resume <SESSION_ID> # 指定したセッションで起動
```

## Cursor / VS Code への設定

以下のURLから、自分自身のIDEの拡張機能をダウンロードしてください。

## セッション内コマンド

`codex` のセッション内で実行できるコマンドでよく使うものです。

```bash
/init — 初期化テンプレートや設定のブートストラップ

/new — 新しい会話に切り替え(セッション状態のクリア)

/model — AIモデルの切り替え

/compact - これまでの会話履歴のトークンを要約・圧縮

/help – ヘルプを表示

/quit — セッション(codex)を終了
```

### 認証モードの切り替え

```bash
/mode — セッション内の「承認モード」を切り替えるため
```

- `suggest` - 読み取りのみ。提案は行うが編集やコマンドは承認が必要）
- `auto-edit` - ファイル編集は自動で行うがシェルコマンドは承認が必要）
- `full-auto` - ファイルの編集もコマンドの実行も自動化。承認不要）

> ちなみに、 `/mode` は自動処理の許可レベルを切り替え、 `/approvals` は個別の操作に対する承認の管理・確認を行うコマンドという違いがあります。

## ルール/メモリ（AGENTS.md）

Codex は起動時に `AGENTS.md` を読み込み、ふるまいの基準として使う。  
(Claude Code の CLAUDE.md に近いもののようです)

- **リポジトリのルート** ： `AGENTS.md` は自動検出・読み込みの対象。
- **作業中ディレクトリ/サブフォルダ** ：同名ファイルがあれば併用可。近いものが優先。
- **`~/.codex/AGENTS.md`**: 全てのプロジェクトで共通の設定になります。
- 複数見つかった場合は、 **近い階層が優先** しつつマージされます。

## カスタムプロンプト

`~/.codex/prompts/` (`$CODEX_HOME/prompts/`) にマークダウンファイル(`.md`)を設置すると、カスタムコマンドとして設置されます。

プロジェクト固有の prompts ディレクトリは用意されていないので全プロジェクト共通のカスタムコマンドになります。

何度も繰り返し入力するような内容をあらかじめマークダウンとして登録しておくと便利です。

> カスタムコマンドと一緒にContextを渡しても受け取ってもらえないことがありました😹  
> (次のタイミングでContextを渡すとちゃんと解釈してくれたので発展途上な部分もまだまだあるなと思います)

[Custom Prompts - Codex ドキュメント](https://github.com/openai/codex/blob/main/docs/prompts.md)

## 設定（~/.codex/config.toml）

```toml
model = "gpt-5-codex"
model_verbosity = "medium" # 詳細な応答の冗長さ（情報量の多さ）
sandbox_mode = "read-only"  # 最も安全（必要時のみ緩める）

# コマンド実行を承認するかどうかをプロンプトで確認すべきタイミング
# - untrusted: 「信頼済み」でないコマンド（危険操作など）は実行前に都度承認を求め
# - on-request: モデル（Codex）が判断して承認を要求する場合
# - on-failure: コマンドが失敗した場合のみ承認にエスカレート
# - never: いかなる場合も承認を求めず、すべての操作を自動で実行
approval_policy = "untrusted"

file_opener = "cursor" # or vscode
notify = ["bash","-lc","afplay /System/Library/Sounds/Ping.aiff"]

# trueにすると、npmのインストールや外部APIへのリクエストが可能 (デフォルトは false)
network_access = false

[tui]
#　デスクトップ通知に関する設定
# - "agent-turn-complete": エージェントの１ターン処理が完了した際に通知
# - "approval-requested": ユーザーの操作や承認が必要な時に通知
notifications = ["agent-turn-complete","approval-requested"]

[shell_environment_policy]
inherit = "core"
include_only = ["PATH","HOME","USER"]
exclude = ["AWS_*","AZURE_*","*TOKEN*","*SECRET*","*KEY*"]
```

### model\_reasoning\_effort

```toml
model_reasoning_effort = "medium" # モデルがどれだけ「考える」かの深さ
```

`model_reasoning_effort` については思考の長さはある程度自動で調整されるので `medium` がベストという話もあるっぽいです。

```toml
[tools]
web_search = true # Web 検索を許可 (デフォルトは false)
```

Prompt Injection のようなセキュリティリスクを防ぐための [Exa.ai](https://exa.ai/) といったソリューションもあるようです。

### 詳細な設定

詳細な設定についてはこちら：

## MCP

### MCP の設定方法

Codex は MCP サーバを利用できる。

**定義方法** （どちらか）：

1. `~/.codex/config.toml` に書く

この場合は全てのプロジェクト共通のMCP設定となります。

```toml
[mcp_servers.playwright]
command = "npx"
args    = ["-y", "@playwright/mcp"]
```

1. CLI で登録

```bash
# 登録
codex mcp add <id> -- <command> <args...>

# 確認
codex mcp list
```

> 注意: Codex は stdio 型の MCP を前提とします。SSE 型はそのままでは不可なので、mcp-proxy 等のブリッジ経由で登録してください。

1. CLI で一時的に上書きして起動

特定のプロジェクトだけで使う場合はこちらを使う (alias を作る) のが2025/9/29時点でおすすめです。

```bash
codex -c 'mcp_servers={"playwright"={command="npx",args=["-y","@playwright/mcp"]}}'
```

## よく使われる MCP

### Serena

コード検索・編集ツールとして機能し、コーディングエージェント(Codex等)のトークンの節約に役立ちます。

**TOML**

```toml
[mcp_servers.serena]
command = "uvx"
args = ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "codex", "--enable-web-dashboard=false", "--project", "$(pwd)"]
```

**CLIから追加**

```bash
codex mcp add serena -- uvx --from git+https://github.com/oraios/serena \
serena start-mcp-server --context codex --enable-web-dashboard=false \
--project $(pwd)
```

**CLIで起動時に渡す**

```bash
codex -c 'mcp_servers={"serena"={command="uvx",args=["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "codex", "--enable-web-dashboard=false", "--project", "$(pwd)"]}}'
```

### Context7

ライブラリ/フレームワークのドキュメントを検索し、API 仕様を参照できます。

**TOML**

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]
```

**CLIから追加**

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

**CLIで起動時に渡す**

```bash
codex -c 'mcp_servers={"context7"={command="npx",args=["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]}}'
```

`YOUR_API_KEY` のところは [https://context7.com/](https://context7.com/) にサインインして取得。

### Notion MCP

Notion のページ/データベースへ読み取りアクセスできます。

**TOML**

```toml
[mcp_servers.notion]
command = "npx"
args = ["-y", "mcp-remote", "https://mcp.notion.com/mcp"]
```

**CLIから追加**

```bash
codex mcp add notion -- npx -y mcp-remote https://mcp.notion.com/mcp
```

**CLIで起動時に渡す**

```bash
codex -c 'mcp_servers={"notion"={command="npx",args=["-y", "mcp-remote", "https://mcp.notion.com/mcp"]}}'
```

### Markitdown

PDF/Office/HTML などを Markdown に変換して取り込みやすくする。

**TOMLに設定**

```toml
[mcp_servers.markitdown]
command = "uvx"
args = ["markitdown-mcp"]
```

**CLIから追加**

```bash
codex mcp add markitdown -- uvx markitdown-mcp
```

**CLIで起動時に渡す**

```bash
codex mcp add markitdown -- uvx markitdown-mcp

codex -c 'mcp_servers={"markitdown"={command="uvx",args=["markitdown-mcp"]}}'
```

### Chrome DevTools

ブラウザでのデバック作業、パフォーマンスのインサイトの取得、puppeteer を使った自動化などを支援してくれます。

**TOML**

```toml
[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp"]
```

**CLIから追加**

```bash
codex mcp add chrome-devtools -- npx chrome-devtools-mcp
```

**CLIで起動時に渡す**

```bash
codex -c 'mcp_servers={"chrome-devtools"={command="npx",args=["chrome-devtools-mcp"]}}'
```

### Playwright

ブラウザの自動操作・E2E テスト生成・スクリーンショット取得などを支援してくれます。

**TOML**

```toml
[mcp_servers.playwright]
command = "npx"
args = ["-y", "@playwright/mcp"]
```

**CLIから追加**

```bash
codex mcp add playwright -- npx -y @playwright/mcp
```

**CLIで起動時に渡す**

```bash
codex -c 'mcp_servers={"playwright"={command="npx",args=["-y","@playwright/mcp"]}}'
```

### Figma Dev Mode MCP

Dev Mode 情報（コンポーネント仕様・アセットなど）を取得し、デザイン→実装の橋渡しを支援。

事前にFigmaのデスクトップアプリを起動しておく必要があります。

**TOML**

```toml
[mcp_servers.figma]
command = "npx"
args = ["-y", "mcp-proxy", "http://127.0.0.1:3845/mcp"]
```

**CLIから追加**

```bash
codex mcp add figma -- npx -y mcp-remote "http://127.0.0.1:3845/mcp"
```

**CLIで起動時に渡す**

```bash
codex -c 'mcp_servers={"figma"={command="npx",args=["-y", "mcp-remote", "http://127.0.0.1:3845/mcp"]}}'
```

### GitHub MCP

GitHub のリポジトリ/Issue/PR へのクエリや操作を行います。(動作確認できていないのでリンクのみ掲載)

### その他の MCP リスト

## CI(GitHub Actions等)での実行

**ポイント**

- CI では **API キーでログイン** して実行（ `codex login --api-key ...`）。
- 解析のみなら既定の `read-only` のまま、 **変更を書き込む場合は** `--config sandbox_mode="workspace-write"` を付与。

**GitHub Actions（例）**

## Codex のキーバインド

Codex のセッション内でのキーバインドです。

- セッション内での改行 -> `Ctrl + J`
- 進行している処理の途中終了 -> `Ctrl + C`

## CodexとClaude Codeの比較

私個人の所感ですが、 Claude Code と Codex との比較は「 [Claude CodeからCodexをMCPで呼び出せるようになった話](https://zenn.dev/tmasuyama1114/articles/cdfd4562bdce78) 」の著者さんのご意見に近い感想です。

- Claude Code (Ops 4.1)の方が向いているタスク
	- 複雑度が高すぎない、探索的ではない (要件を全部伝えられる)
	- スピーディにサクッと解決したい
- Codex (gpt-5-codex)の方が向いているタスク
	- 複雑度が高く、調べてもらいながら要件を補完していきたい
	- 時間がかかってもいいので正解を目指したい

こちらはあくまで2025/9/29時点での手持ちのタスクに基づく個人の感想です。参考程度でお願いします。

## Codex にしかない特徴

Codex では複雑で時間のかかる開発タスクを、クラウド上の隔離されたサンドボックス環境でコード編集やテスト、ビルドコマンドの実行ができます。

クラウド上にサンドボックス環境が揃っている場合は、スマホからもコードの変更を依頼することができます。

![](https://storage.googleapis.com/zenn-user-upload/cd65fcf90d1d-20250929.png)

1度の依頼に対して1-4個の処理を並列して行うことができ、複数の実行結果の中から一番いい成果物を選ぶこともできます。

## Codex に追加してほしい機能

- 「sudo」「git」「rm」等の個別に禁止コマンド(ワード)を明示的に列挙して直接ブロックする公式サポートは2025/9/29では見られません。
- プロジェクトごとの MCP 設定が2025/9/29時点ではサポートされていないようです
- Claude Code の SubAgent のように個別のタスクに対して、役割や利用するモデルを指定する機能は2025/9/29時点では見られません

## 補足：音声入力で効率化

音声入力には明確な利点があります：

- **入力速度**: 平均的な話速は150-200語/分、タイピングは40-60語/分
- **情報量**: 音声では背景・理由・期待結果を自然に含めて話す傾向がある
- **認知負荷**: キーボード操作を考えずに、問題解決に集中できる

タイピングでは「バグ修正」と書くところを、音声では「2ページ目でデータが表示されないバグを修正」のように具体的に伝えやすくなる。結果として、Claude Codeはより正確な解決策を提示できる。

### おすすめツール:　Superwhisper

- 文字起こしツールで、その後に Claude Sonnet4 などであと処理ができる
- 日本語でしゃべったものを、LLMプロンプトで英語翻訳できる
- 英語・日本語両方をセットでClaude Codeに渡すのがおすすめ

![](https://storage.googleapis.com/zenn-user-upload/b3e83c741a1a-20250620.png)

![](https://storage.googleapis.com/zenn-user-upload/f2c87e7c3ecc-20250620.png)

### おすすめツール:　WispFlow

- 喋ったことを精度高く日本語文字起こしするツール
- フィラー(「えー」など)を除去して、読みやすい日本語にする
- 無料でも問題なく使える

## 補足: Ultracite

Ultraciteはbiome上で動作し、非常に高速なコード整形、ほぼ設定不要ですぐ使える導入の簡単さ、一貫したコードスタイルの維持、豊富な自動修正オプションなどがメリットです。Codex 等を使う場合には導入しておいて損はないと思います。

詳しい導入の手順などは上の記事がとっても参考になりました。

ただし、すでにあるプロジェクトで導入するとかなりエラーが出る可能性があるので、最初は全てのチェックルールを `off` にして、一つずつチェックルールを有効にしていきながら修正していくのがおすすめです。

### codex MCP 設定

**TOML**

```toml
[mcp_servers.ultracite]
command = "npx"
args = ["-y", "mcp-remote", "https://www.ultracite.ai/api/mcp/mcp"]
```

**CLIから追加**

```bash
codex mcp add ultracite -- npx -y mcp-remote "https://www.ultracite.ai/api/mcp/mcp"
```

## 参考にさせて頂いた記事

198

104