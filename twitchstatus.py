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
        for i in online:
            offline.append(i)
        for i in data['data']:
            if i['user_login'] not in online:
                online.append(i['user_login'])
                msg = '{}\'s stream goes online \n {}({}) \n https://www.twitch.tv/{}'.format(i['user_login'],i['title'],i['game_name'],i['user_login'])
                print(msg)
                await client.get_channel(channelid).send(msg)
            else:
                offline.remove(i['user_login'])
        for j in offline:
            online.remove(j)
            print(j + "\'s Stream goes Offline")
            await client.get_channel(channelid).send(j + "\'s Stream goes Offline")
        await asyncio.sleep(interval)