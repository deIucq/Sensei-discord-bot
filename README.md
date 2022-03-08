# Sensei-discord-bot

## 概要

discordサーバー「FPS Dojo」用に開発されたdiscord.pyを用いたいろいろできるdiscord botです．

## 主な機能
### [実装済み]
- 一時的なサーバーを建てる機能
- Twitch配信通知機能
- ランダム機能(VC参加者から一人指名，1から指定した数値までのランダムな値，TRPG等用ダイス)

### [実装予定]
- ゲームサジェスト機能

## 実行方法

1. Discord.pyをインストール
    ```
    python3 -m pip install -U discord.py
    sudo apt install libffi-dev libnacl-dev python3-dev
    ```
2. DiscordとTwitchのAPIToken等を入手したらsettings.jsonを生成し，以下の形式で設定
    (TwitchAuthorizationは次の手順で自動で埋めるので手動で取得する必要はありません)
    ```json
    {
        "discordToken": "XXX",
        "TwitchClientId": "XXX",
        "TwitchClinetSecret": "XXX",
        "TwitchAuthorization": "",
        "TwitchAPIInterval": XX,
        "StreamAnnouncementChannelID": XX,
        "streamer": [
            "XXX",
            "YYY",
            "ZZZ"
        ]
    }
    ```
3. `refresh_api_token.py`を実行
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
2. random
  - /random

    引数に数字を入れた場合，1以上その数字以下ののランダムな数字を返します．
    memberと入れた場合，コマンドを送信した人が参加しているVCの参加者をランダムに選んで返します．
  - /dice nDm
    1以上m以下の値をn回返します
