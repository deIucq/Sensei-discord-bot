# Sensei-discord-bot

## 概要
discordサーバー「FPS Dojo」用に開発されたdiscord.pyを用いたいろいろできるdiscord botです．

## 実行方法
1. Discord.pyをインストール
    ```
    python3 -m pip install -U discord.py
    sudo apt install libffi-dev libnacl-dev python3-dev
    ```
2. DiscordとTwitchのAPIToken等を入手したらsettings.jsonを作成し，以下の形式で各種設定を行う。
    ```json
    {
    "discordToken":"XXX",
    "TwitchClientId":"XXX",
    "TwitchAuthorization": "Bearer XXX",
    "TwitchAPIInterval" : XX,
    "StreamAnnouncementChannelID" : XXX,
    "streamer" : ["XXX", "YYY", "ZZZ"]
    }
    ```
3. `discordbot.py`を実行

## コマンド
1. /twitch
    - adduser [ユーザー名]
    - deluser [ユーザー名]

    通知する対象のTwitchユーザーを追加/削除します
2. /random \
    引数に数字を入れた場合，1以上その数字以下ののランダムな数字を返します．
    memberと入れた場合，コマンドを送信した人が参加しているVCの参加者をランダムに選んで返します．
3. /dice nDm \
    1以上m以下の値をn回返します
4. misc
  - /neko
  "にゃーん"と返します。botの生存確認に使用してください

削除済み
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