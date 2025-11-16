---
title: "Markdownをプログラミング言語として用いる仕様駆動開発の可能性 ——GitHub Blogより"
source: "https://gihyo.jp/article/2025/10/spec-driven-development-example"
author:
  - "[[gihyo.jp]]"
published: 2025-10-02
created: 2025-11-17
description: "GitHubは2025年9月30日、ブログ記事「Spec-driven development: Using Markdown as a programming language when building with AI」を公開し、Markdownをプログラミング言語として用いる仕様駆動開発の可能性の一端が紹介された。"
tags:
  - "clippings"
  - raw
---
GitHubは2025年9月30日、ブログ記事  「Spec-driven development: Using Markdown as a programming language when building with AI」  を公開し、Markdownをプログラミング言語として用いる仕様駆動開発の可能性の一端が紹介された。

- [GitHub Blog: Spec-driven development: Using Markdown as a programming language when building with AI - GitHub Blog](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-using-markdown-as-a-programming-language-when-building-with-ai/)

プログラムを作成するときにコーディングエージェント利用する場合、もっとも基礎的な使い方として  「Xをおこなうアプリを作成」  といった指示から開始し、逐次  「機能Yを追加」  「 ⁠バグZを修正」  といった指示を反復する方法がある。しかしこの方法は、エージェントがアプリの目的や過去の決定を忘れ、説明の再提示や指示に対する矛盾が発生するといった課題がある。

その対応の一つに、エージェントの振る舞いをあらかじめ設定できるカスタムインストラクションがある  （GitHub Copilotではcopilot-instructions. mdなどが使われることになる⁠ ） ⁠。ただ、カスタムインストラクションは開発中に更新する必要が出てくることもしばしばあり、忙しいときなどはその更新を忘れてしまう問題が挙げられている。

さらなる候補として、仕様駆動開発  （Spec-driven development）  が挙げられている状況がある。GitHubでは仕様駆動開発のツールキット  「 [Spec Kit](https://gihyo.jp/article/2025/09/github-spec-kit) 」  がオープンソースで継続的に開発されている。

仕様駆動開発では、アプリの実装仕様と文脈をMarkdownに集約し、それをコーディングエージェントがコードへ変換することでコンテキストの損失を防ぎ、仕様と実装を同期させる狙いがある。

では実際に、仕様駆動開発でどの程度のことができるのか。ブログ著者のGitHubのTomas Vesely氏は実験を兼ねて、今回 [GitHub Brain MCP Server](https://github.com/wham/github-brain)  （Go言語製）  の開発において、Go言語のプログラムファイルを書かずに、Markdownファイルのみを使ってプログラムを生成してみることにした。開発環境としてはVS CodeとGitHub Copilotを利用している。

なおGitHub Brain MCPサーバーは、GitHub上のDiscussions、Issues、プルリクエストを要約するためものであり、  「 ⁠ユーザーXの先月の貢献は？」  「 ⁠今月の議論を要約して」  といった質問に答えるのに役立つという。

ブログでは、以下のファイル構成を示して解説した。

```
.
├── .github/
│   └── prompts/
│       └── compile.prompt.md
├── main.go
├── main.md
└── README.md
```

README. mdはユーザー向けドキュメントであり、簡単な概要とワークフロー、インストール方法、CLIの利用方法を記述する。

main. mdは実質的にソースコードの仕様になる。形式的に定義できる部分は見出しや箇条書き・  コードブロックで明示し、振る舞いなどの高レベルな意図は自然言語で宣言的に書く。また、README. mdのインポートもおこなう。なお、機能追加やバグ修正への対応もこのMarkdownを編集するかたちになる。

このmain. mdの記述は仕様としての要求を明確にする必要があり、著者にとって直接Goを書くよりも難しい場合があったという。その際、Copilotを使った支援も利用して解決したとのこと。データベースにはSQLiteを使っており、この仕様もmain. mdに記述している。なお、外部リソース取得はGraphQLクエリとタイムスタンプ停止条件により効率化するようにしたという。

compile. prompt. mdは仕様をmain. goに変換させるための繰り返し利用可能なプロンプトファイルであり、  「 ⁠仕様へ従いアプリを更新」  「 ⁠VS Codeタスクでビルド  （手動の `go build` / `go test` 指示の回避⁠ ） ⁠ 」 ⁠ 「 ⁠使用ライブラリごとにGitHubホームページを取得しドキュメントと例を得る」  といった指示が含まれている。

さらに、main. mdの明確化と簡潔化を目的としてlint. prompt. mdが作られた。このファイルでは  「仕様の明確化・  簡潔化」  「 ⁠英語をプログラミング言語として扱う」  「 ⁠用語統一」  「 ⁠重複削除・  重要詳細保持」  「 ⁠Goコードは変更せずMarkdownのみ最適化」  「 ⁠プロンプト自身は変更しない」  などいった指示が含まれている。

作業の流れとしては、README. mdとmain. mdを編集し、コーディングエージェントに `/` コマンドで `compile.prompt.md` を使った変換を指示し、Goのコード生成するかたちになる。なお随時 `/` コマンドで `lint.prompt.md` を呼び出し、main. mdを整理する。

そしてプログラムの実行と動作テストをおこない、期待する動作と一致しない場合には仕様を更新して再変換する……といった反復がおこなわれた。なお、仕様が大きくなってからは、 `focus on <変更点>` といった文脈を追加することで、コーディングエージェントの焦点を誘導できたという。

こうして、仕様をみたすGitHub Brain MCPサーバーができたとのこと。GitHub Copilotのコーディングエージェントのアップデートのたびに、ワークフローの改善ができていることも付け加えられている。

今後は、main. goが肥大化するとコンパイル速度が低下するので各 `##` セクションをモジュールに分割する指示を追加することや、テストファイルの追加などを検討したいという。また、Go言語のコードではなく、他のプログラミング言語で生成する案にも言及がある。

おすすめ記事

- [![](https://gihyo.jp/assets/images/admin/serial/01/ubuntu-recipe/0877/wlk00.png)
	第877回  リアルタイム文字起こしを  ローカルマシンで  実現できる  WhisperLiveKitを  使ってみよう
	](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0877)
- [![](https://gihyo.jp/assets/images/ICON/2024/2211_python-in-excel.png)
	Excelに  Pythonコードを  埋め込める  「Python in Excel」  の  紹介
	](https://gihyo.jp/article/2024/02/monthly-python-2402)

記事・ニュース一覧

- [![](https://gihyo.jp/assets/images/ICON/2022/1903_ubuntu-topics.png)
	Ubuntu 14. 04 LTSへの  15年サポート⁠ ⁠ ・  DNSSECの  デフォルト化テストと  失敗⁠ ⁠ ・  Ubuntu 25. 10リリース記念オフラインミーティング25. 11
	吉田史
	](https://gihyo.jp/admin/clip/01/ubuntu-topics/202511/14?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2687_hcd2025.png)
	専門性が  高く  ライフサイクルの  長い  医療機器の  ユーザビリティを  向上させる  ために
	\[取材・文・構成\]森川裕美
	](https://gihyo.jp/article/2025/11/hcd-net-2025?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2686_gpt-5.1.png)
	OpenAI⁠ ⁠ 、  GPT-5. 1を  リリース —⁠—親しみやすさとの  両立へ⁠ ⁠ 。  応答性能も  向上し⁠ ⁠ 、  応答の  トーンも  さらに  選択できるように
	](https://gihyo.jp/article/2025/11/gpt-5.1?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2685_dotnet10-release.png)
	Microsoft⁠ ⁠ 、 .NET 10を  リリース —⁠— Visual Studio 2026も  一般提供開始
	](https://gihyo.jp/article/2025/11/dotnet-10?summary)
- [![](https://gihyo.jp/assets/images/admin/serial/01/ubuntu-recipe/0887/seedvc03.png)
	第887回  AIボイスチェンジャーである  Seed-VC用に⁠ ⁠ 、  任意の  音声ファイルを  トレーニングしてみよう
	柴田充也
	](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0887?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2684_mtddc2025.png)
	今回の  テーマは  「Future of Web Creation」  ――MTDDC Meetup TOKYO 2025⁠ ⁠ 、  11/  29に  開催
	馮富久
	](https://gihyo.jp/article/2025/11/mtddc2025?summary)
- [![](https://gihyo.jp/assets/images/ICON/2022/1898_mysql_rcn_new.png)
	第258回  MySQL 8. 4で  厳格化された  外部キー制約仕様
	佐伯拓哉
	](https://gihyo.jp/article/2025/11/mysql-rcn0258?summary)
- [![](https://gihyo.jp/assets/images/article/2025/11/mastodon-4.5-with-quote-post-feature/mastodon-4.5-1.jpg)
	Mastodon⁠ ⁠ 、  バージョン4. 5を  リリース —⁠—元投稿者の  引用ポリシーを  尊重する  引用投稿の  投稿が  可能に
	](https://gihyo.jp/article/2025/11/mastodon-4.5-with-quote-post-feature?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2681_gitlab.png)
	3年以内に  訪れる⁠ ⁠ 、  ソフトウェアの  自律型AIの  未来 —⁠—CISOが  今すぐ  備えるべき  理由
	小澤正治
	](https://gihyo.jp/article/2025/11/the-future-of-autonomous-ai-in-software?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2683_vscode-inline-suggest-oss.png)
	Visual Studio Code⁠ ⁠ 、  GitHub Copilotの  インラインサジェスト機能を  オープンソース化
	](https://gihyo.jp/article/2025/11/vscode-inline-suggest-oss?summary)
- [![](https://gihyo.jp/assets/images/ICON/2022/1903_ubuntu-topics.png)
	Steam Snapの  Core24版の  テスト開始⁠ ⁠ 、  Dell PowerEdge XR8000を  中心に  した  エッジAIや  ネットワーキング, Azure VM utils
	吉田史
	](https://gihyo.jp/admin/clip/01/ubuntu-topics/202511/07?summary)
- [![](https://gihyo.jp/assets/images/ICON/2022/1897_linux_daily_new.png)
	systemdフリーの  Devuan “Excalibur” 6が  リリース
	階戸アキラ
	](https://gihyo.jp/article/2025/11/daily-linux-251106?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2682_storybook-10.png)
	Storybook 10リリース ―モジュールシステムを  ESMに  統一し  コンパクト化
	](https://gihyo.jp/article/2025/11/storybook-10?summary)
- [![](https://gihyo.jp/assets/images/ICON/2022/1908_AndroidWeeklyTopics.png)
	「Swift SDK for Android」  の  プレビュー版が  リリース
	傍島康雄
	](https://gihyo.jp/article/2025/11/android-weekly-topics-251106?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2680_rubyprocon.jpg)
	「中高生Rubyプログラミングコンテスト2025」  の  最終審査会進出者10組が  決定⁠ ⁠ 、  2025年11月29日三鷹で  最終審査会を  開催
	](https://gihyo.jp/article/2025/11/ruby-procon2025-11?summary)
- [![](https://gihyo.jp/assets/images/admin/serial/01/ubuntu-recipe/0886/seedvc03.png)
	第886回  AIボイスチェンジャーである  Seed-VCで  自分の  声を  変えてみよう
	柴田充也
	](https://gihyo.jp/admin/serial/01/ubuntu-recipe/0886?summary)
- [![](https://gihyo.jp/assets/images/article/2025/11/chrome-142-devtools-updates/chrome-142-devtools-1-2.png)
	Chrome 142⁠ ⁠ 、  DevToolsの  AIアシスタンス機能を  強化 —⁠—コード提案機能の  追加や⁠ ⁠ 、  トレース情報を  渡すだけで  パフォーマンス調査が  可能に
	](https://gihyo.jp/article/2025/11/chrome-142-devtools-updates?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2679_kiro-0-5.png)
	Kiro v0. 5.0リリース⁠ ⁠ 、  リモートMCPサーバー⁠ ⁠ 、  AGENTS. mdを  サポート
	](https://gihyo.jp/article/2025/11/kiro-0-5?summary)
- [![](https://gihyo.jp/assets/images/article/2025/11/get-started-claude-code-02/2-6.jpg)
	Claude Codeの  料金体系と  インストールから  セットアップまで
	平川知秀
	書籍関連
	](https://gihyo.jp/article/2025/11/get-started-claude-code-02?summary)
- [![](https://gihyo.jp/assets/images/ICON/2025/2663_gitlab-strategic-growth-guidelines-for-engineering-team.png)
	エンジニアリングチームを  戦略的に  成長させる  ための  行動指針
	サブリナ・ファーマー
	](https://gihyo.jp/article/2025/10/gitlab-strategic-growth-guidelines-for-engineering-teams?summary)

[→記事一覧](https://gihyo.jp/list/article)