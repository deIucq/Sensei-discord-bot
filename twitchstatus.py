import json
import asyncio
import requests

#twitch通知用関数
async def twitch_getchannelstatus(client):
    interval = 100
    channelid = ''
    with open('settings.json') as f:
        json_dict = json.load(f)
        interval = json_dict['TwitchAPIInterval']
        channelid = json_dict['StreamAnnouncementChannelID']
    url = 'https://api.twitch.tv/helix/streams'
    payload = {}
    headers = {}
    with open('settings.json') as f:
        json_dict = json.load(f)
        payload = {'user_login' : json_dict['streamer']}
        headers = {'Client-Id': json_dict["TwitchClientId"], 'Authorization':json_dict["TwitchAuthorization"]}

    online = []
    while True:
        data = json.loads(requests.get(url, params=payload, headers=headers).text)
        offline = []
        onlineUser_login = []
        for i in online:
            onlineUser_login.append(i['user_login'])
        #onlineをofflineにコピー
        for i in online:
            offline.append(i)
        for i in data['data']:
            #取得したデータがonlineにない場合通知を送信し，onlineリストにuser_loginとmessageの辞書を追加
            if i['user_login'] not in onlineUser_login:
                msgContent = '{}\'s stream goes online \n {}({}) \n https://www.twitch.tv/{}'.format(i['user_login'],i['title'],i['game_name'],i['user_login'])
                print(msgContent)
                msg = await client.get_channel(channelid).send(content = msgContent)
                online.append({'user_login':i['user_login'], 'msg':msg})
            #取得したデータがofflineにある場合，offlineから取得したデータを削除
            else:
                for j in offline:
                    if i['user_login'] == j['user_login']:
                        offline.remove(j)
        #残ったofflineについて，onlineからそのデータを削除し，messasgeの内容を書き換える．
        for i in offline:
            online.remove(i)
            msgContent = str(i['user_login'] + "\'s stream goes offline")
            print(msgContent)
            await i['msg'].edit(content = msgContent)
        await asyncio.sleep(interval)