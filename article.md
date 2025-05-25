# Amazon Q CLIでゲーム開発：ぷよぷよ風ゲームの作成体験

## はじめに

「[Build Games with Amazon Q CLI and score a T shirt 🏆👕](https://community.aws/content/2xIoduO0xhkhUApQpVUIqBFGmAc/build-games-with-amazon-q-cli-and-score-a-t-shirt)」というキャンペーンを知りましたのでキャンペーンの概要とゲーム作成のノウハウなどを紹介します。

## キャンペーン概要

https://community.aws/content/2xIoduO0xhkhUApQpVUIqBFGmAc/build-games-with-amazon-q-cli-and-score-a-t-shirt

このイベントは、Amazon Q CLIを使ってゲームを開発することで、**特性Tシャツが貰える**というキャンペーンです。

開催期間は、**2025年5月20日から6月20日まで**です。

対象国は次のようになっています。

```text
オーストラリア、バングラデシュ、ブータン、ブルネイ、カンボジア、中国、フィジー、香港、インド、インドネシア、日本、ラオス、マレーシア、モルディブ、ミャンマー、ネパール、ニュージーランド、パキスタン、パプアニューギニア、フィリピン、シンガポール、韓国、スリランカ、台湾、タイ、ベトナム
```

参加するために必要なステップは次の４つだけです。

- Step1：Amazon Q CLIをマシンにインストールする
- Step2：Amazon Q CLIのチャットでゲームを作る
- Step3：Amazon Q CLIで作ったものをブログまたはソーシャルメディアで共有する。投稿は母国語でよい。
- Step4：Tシャツ引き換えフォームに記入する

### Amazon Q CLIとは？

Amazon Q CLIは、AWSが提供するAI支援ツールで、コマンドラインから直接AIと対話しながらコーディングができます。従来のコーディング方法と異なり、自然言語で要望を伝えるだけで、AIがコードを生成・修正してくれるため、開発効率が大幅に向上します。

## 1. 開発環境の構築：Windows + WSL + VSCode + devcontainer

Amazon Q CLIを効率的に使うため、Windows環境でWSLとVSCodeのdevcontainerを組み合わせた開発環境を構築しました。

### 1-1. 工夫したポイント

- ローカル環境での実施例はあるので、Windows(WSL) + VSCode + devcontainerでの構築に挑戦しました。
- devcontainer での実行のため、[GUIを使用せずにインストールする方法](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html#command-line-installing-ubuntu)を実施しました。
- Amazon Q CLI はルートユーザーでのインストールをサポートしていないため、今回は`--force`オプションで強制的にインストールしました。

### 1-2. Dockerfileの設定

```dockerfile
FROM ubuntu:22.04

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Amazon Q CLIをインストール
RUN curl --proto '=https' --tlsv1.2 -sSf "https://desktop-release.q.us-east-1.amazonaws.com/latest/q-x86_64-linux-musl.zip" -o "/tmp/q.zip" && \
    cd /tmp && \
    unzip q.zip && \
    cd q && \
    ./install.sh --no-confirm --force && \
    cd / && \
    rm -rf /tmp/q && \
    rm -f /tmp/q.zip
```

### 1-3. devcontainer.jsonの設定

```json
{
  "name": "Amazon Q CLI Environment",
  "build": {
      "dockerfile": "Dockerfile",
      "context": ".."
  },
  "features": {
      "ghcr.io/devcontainers/features/git:1": {},
      "ghcr.io/devcontainers/features/aws-cli:1": {},
  },      
  "customizations": {
    "vscode": {
      "extensions": [
        // Install your preferred extensions
      ]
    }
  },
  // Command to run after container creation
  "postCreateCommand": "bash .devcontainer/postCreateCommand.sh",
  // Workspace folder path
  "workspaceFolder": "/workspaces/${localWorkspaceFolderBasename}"
}
```

## 2. 開発プロセス

### 2-1. 基本機能の実装

[ぷよぷよ](https://puyo.sega.jp/portal/index.html)風ゲームを作ることにしました。

最初に、ゲームの基本機能を実装しました。Amazon Q のチャットで以下のような簡単な指示を行いました。

これだけの指示で、かなりの完成度の**ぷよぷよ風ゲーム**が実装されました。

```text
ぷよぷよのようなゲームを作成します。
pygame 2.6.1を使用します。仕様は次の通りです。

## 基本仕様

落ちてくる「ぷよぷよ」は、AWSサービスのアイコンにしてください。黄色のサービスがないので、EC2で代用します。

赤：CloudTrail
青：Aurora
黄→オレンジ：EC2
緑：S3
紫：Amazon VPC

## 操作

キーボードで操作します。

- ←と→で左右に移動
- ↑またはスペースで回転
- ↓で落下
```

```python
# ゲームの基本構造
import pygame
import sys
import random
import math

# 初期化
pygame.init()
screen = pygame.display.set_mode((600, 700))
```

### 2-2. 機能の拡張と改良

基本機能ができた後は、より細かい要望を伝えて機能を拡張していきました。

- 加速落下機能：「↓で落下」という指示ではぷよぷよの機能である加速落下が実装できていませんでしたので、明示的に加速落下と指示をして実装させました。
- 落下予測機能: 「落下予測地点を半透明の円で表示したい」として実装させました。
- 連鎖システム: 初期の実装では一気に消えてしまい、ぷよぷよの特徴である「連鎖」の演出がありませんでした。「連鎖が発生したら順番に消えるようにしたい」という要望に対して、アニメーション付きの連鎖システムを実装させました。
- UI改善: 「スコア表示を日本語にしたい」、「最大れんさ数」、などの表示改善も指示することで柔軟に対応できました。
- ゲームタイトル画面の実装と、コンティニュー

### 2-3. バグ修正と最適化

開発中に発生したバグも、Amazon Q CLIの助けを借りて効率的に修正できました：

- **関数定義順序の問題**: 関数が使用される前に定義されていないエラーを検出し、コード構造を最適化
- **落下ロジックの修正**: 「ぷよ」が空中で止まる問題を解決するアルゴリズムを提案
- **日本語表示の問題**: フォント設定を調整して日本語文字化けを解消

## 3. Amazon Q CLIの活用テクニック

### 3-1. 効果的な指示の出し方

Amazon Q CLIを使う際は、具体的で明確な指示を出すことが重要です。

- ❌ 「ゲームを改善して」→ 抽象的すぎる
- ✅ 「落下後のアイコンが空中で止まる問題を修正して」→ 具体的で明確

### 3-2. 段階的な開発アプローチ

複雑な機能は一度に実装しようとせず、小さな単位に分けて段階的に開発すると効率的です。

1. まず基本機能を実装
2. 動作確認をしながら機能を追加
3. 最後に視覚効果やアニメーションを調整

### 3.3. エラー対応のコツ

エラーが発生した場合は、エラーメッセージを正確に伝えることで、Amazon Qがより適切な解決策を提案してくれます。devcontainer環境では、エラーログを直接コピー＆ペーストできるため、正確な情報伝達が容易です。

### 3-4. WSL + devcontainer環境のメリット

- **環境の再現性**: チーム全体で同じ開発環境を共有できる
- **クロスプラットフォーム**: WindowsでもLinuxネイティブの環境で開発可能
- **VSCode統合**: エディタとターミナルを行き来せずに開発できる
- **Amazon Q CLI互換性**: WSLを通じてLinux版のAmazon Q CLIをスムーズに実行

## まとめ

Amazon Q CLIとdevcontainer環境を組み合わせたゲーム開発は、従来のコーディング方法と比べて非常に効率的でした。特に、自然言語でのやり取りを通じて複雑な機能を実装できる点が魅力です。初心者でも専門的なゲーム開発の知識がなくても、AIの支援を受けながら自分のアイデアを形にすることができます。

そして、WSLとdevcontainerを活用することで、Windows環境でもAmazon Q CLIを簡単に実行できます。rootユーザーを使用した場合は、`--force`オプションの活用など、いくつかの工夫は必要ですが、一度環境を構築してしまえば、スムーズな開発体験が得られます。

今回のイベントを通じて、Amazon Q CLIを利用した開発の可能性を実感しました。Amazon Q CLIは単なるコード生成ツールではなく、開発パートナーとして一緒に問題を解決してくれる心強い味方だと感じました。皆さんもぜひ、Amazon Q CLIを使った開発に挑戦してみてください！

---

*この記事は「Build Games with Amazon Q CLI and score a T shirt」イベントへの参加体験をもとに作成されました。*
