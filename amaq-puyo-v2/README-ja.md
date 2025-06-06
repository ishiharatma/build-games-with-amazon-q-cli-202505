# AWS Puyo Puyo Game

[![🇯🇵 日本語](https://img.shields.io/badge/%F0%9F%87%AF%F0%9F%87%B5-日本語-white)](./README-ja.md)
[![🇺🇸 English](https://img.shields.io/badge/%F0%9F%87%BA%F0%9F%87%B8-English-white)](./README.md)

このゲームは、AWSサービスのアイコンを使用したぷよぷよ風の落ちものパズルゲームです。

![overview](../images/game-v2-x4.gif)

## ゲームの特徴

- AWSサービスのアイコンがぷよぷよのように落ちてきます
- 同じサービスのアイコンが4つ以上つながると消えてスコアが加算されます
- アイコンは着地したときにぷるぷると揺れます
- 落下予測地点が薄く表示されます
- 連鎖反応が発生すると順番に消えていきます
- 消えるときは点滅してからはじけるようなアニメーションで消えます
- 連鎖数に応じてボーナススコアが加算されます
- レベルが上がると落下速度が速くなります
- ゲームオーバー時には「Amazon Q～」の文字が左右にゆらゆら揺れます

## 使用しているAWSサービスアイコン

- 赤：CloudTrail
- 青：Aurora
- 黄：EC2
- 緑：S3
- 紫：Amazon VPC

## 操作方法

- 左右矢印キー (←→)：ピースを左右に移動
- 上矢印キー (↑) またはスペースキー：ピースを回転
- 下矢印キー (↓)：押している間、ピースが高速で落下
- スペースキー：ハードドロップ（一気に落とす）
- ゲームオーバー時：Rキーでリスタート

## 必要なライブラリ

- Python 3.x
- Pygame

## インストール方法

```bash
pip install pygame
```

## 実行方法

```bash
python main.py
```

## ゲームの目的

できるだけ多くのAWSサービスアイコンを消して、高得点を目指しましょう！連鎖を狙うとより高得点が獲得できます！
