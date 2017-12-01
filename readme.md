# 概要

Twitterのリプライで送られてきた画像の説明文を生成して返信するbotです。AzureのComputer Vision APIを利用します。

## 必要なライブラリ
- tweepy

## 必要なAPIキー
- Azure Computer Vision API
- Twitter API

## ファイル構成
- main.py
メインのプログラムです
- keys.json
ここに各種APIキーを記述します（新規作成してください）

# 使い方
1. keys.jsonを作成する

    中身

        {
        "CONSUMER_KEY": "XXXXXXXXXXXXX",
        "CONSUMER_SECRET": "XXXXXXXXXXXXX",
        "ACCESS_TOKEN": "XXXXXXXXXXXXXXX",
        "ACCESS_SECRET": "XXXXXXXXXXXXX",
        "AZURE_KEY": "XXXXXXXXXXXXXX"
        }

2. main.pyを実行する
    
        python main.py

    「接続しました」と表示されれば正常に動作しています。