# Sensei-discord-bot

## 概要

このbotはdiscordサーバー「FPS Dojo」用に開発されたdiscord.pyを用いたいろいろできるdiscord botです．

## 主な機能

- ゲームサジェスト機能[未実装]
- 参加ゲーム表示機能[未実装]
- 一時的なサーバーを建てる機能

## 実行方法

1. Discord.pyをインストール

    ```
    python3 -m pip install -U discord.py
    sudo apt install libffi-dev libnacl-dev python3-dev
    ```
2. discordbot.pyと同じディレクトリに`token`ファイルを生成
3. Discord Developer Portalで取得，API Tokenを`token`ファイルに貼り付け
4. `discordbot.py`を実行

## コマンド

1. temp server
  - /mkserver
    
    サーバー作成
  - /rmserver
    
    コマンド実行がされたサーバーを削除
  - /liserver
    
    サーバー一覧
    ✅リアクションで該当サーバーの招待を表示
    🗑️リアクションで該当サーバーを削除
  - /allserverinvite
    
    botが参加中の全サーバーの招待を返します．
2. misc
  - /random [number]
    
    1-numberのランダムな数字を返します．
