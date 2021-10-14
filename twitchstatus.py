import json
import asyncio
import requests

#twitch通知用関数
async def twitch_getchannelstatus(client):
    interval = 100
    channelid = ''
    url = 'https://api.twitch.tv/helix/streams'
    payload = {}
    headers = {}
    with open('settings.json') as f:
        json_dict = json.load(f)
        interval = json_dict['TwitchAPIInterval']
        channelid = json_dict['StreamAnnouncementChannelID']
        payload = {'user_login' : json_dict['streamer']}
        headers = {'Client-Id': json_dict["TwitchClientId"], 'Authorization':json_dict["TwitchAuthorization"]}
    #[[{id:, user_login:, game_name:, title:, ...}, msg], [{}, msg]]
    onlineStream = []
    while True:
        #APIリクエスト，帰ってきた値をjsonに変換
        data = json.loads(requests.get(url, params=payload, headers=headers).text)
        #onlineStreamの要素のidをonlineStreamsIDsとsfflineStreamsIDsにコピー
        onlineStreamIDs = []
        offlineStreamIDs = []
        for i in onlineStream:
            onlineStreamIDs.append(i[0]['id'])
            offlineStreamIDs.append(i[0]['id'])
        #受けたjsonデータに関する処理
        for i in data['data']:
            #取得したデータがonlineStreamIDsにない場合通知を送信し，onlineStreamリストにjsondataとdiscord.messageの配列を追加
            if i['id'] not in onlineStreamIDs:
                msgContent = '{}\'s stream goes online \n {}({}) \n https://www.twitch.tv/{}'.format(i['user_login'],i['title'],i['game_name'],i['user_login'])
                msg = await client.get_channel(channelid).send(content = msgContent)
                onlineStream.append([i, msg])
            #取得したデータがonlineStreamIDsにある場合，offlineから取得したデータを削除
            else:
                for j in offlineStreamIDs:
                    if i['id'] == j:
                        offlineStreamIDs.remove(j)
        #残ったofflineについて，onlineからそのデータを削除し，messasgeの内容を書き換える．
        for i in offlineStreamIDs:
            for j in onlineStream:
                if i == j[0]['id']:
                    msgContent = str(j[0]['user_login'] + "\'s stream goes offline")
                    await j[1].edit(content = msgContent)
                    onlineStream.remove(j)
        await asyncio.sleep(interval)