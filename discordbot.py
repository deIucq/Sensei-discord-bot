import discord
import random
import json
import time
import asyncio
from discord import message
import requests

#serversクラスを定義
class servers():
    def __init__(self, client):
        self.sync()
    def sync(self):
        self.servers = client.guilds
    async def mkserver(self, message):
        f = open('logo/sensei.png', 'rb')
        im = f.read()
        f.close()
        guild = await client.create_guild("temporary server " + str(len(client.guilds)), icon=im)
        perm = discord.Permissions(administrator=True)
        await guild.create_role(name='op',permissions=perm)
        invite = await (await guild.create_text_channel("default")).create_invite()
        await message.channel.send(invite.url)
        self.sync()
    async def rmserver(self, message):
        await message.guild.delete()
        self.sync()
    async def liserver(self, message):
        self.message = []
        for i in self.servers:
            self.message.append(await message.channel.send(i.name))
        for i in self.message:
            await i.add_reaction('✅')
            await i.add_reaction('🗑️')
    async def reaction(self, reaction):
        if reaction.emoji == '✅':
            for i in self.servers:
                if i.name == reaction.message.content:
                    if i == reaction.message.guild:continue
                    invites = await i.invites()
                    if invites == None:
                        await reaction.message.channel.send(invites[0].url)
                    else:
                        if i.text_channels[0] == None:
                            invite = await (await i.create_text_channel("default")).create_invite()
                            await reaction.message.channel.send(invite.url)
                        else:
                            invite = await i.text_channels[0].create_invite()
                            await reaction.message.channel.send(invite.url)
        elif reaction.emoji == '🗑️':
            for i in self.servers:
                if i.name == reaction.message.content:
                    try:
                        await i.delete()
                        await reaction.message.edit(content=i.name + '- deleted')
                    except discord.HTTPException:
                        await reaction.message.channel.send(f'I could\'nt delete {i.name}. There\'s some errors.')
                    except discord.Forbidden:
                        await reaction.message.channel.send(f'I could\'nt delete {i.name}. I don\'t have permission for this.')
                    self.sync()
    async def getallinvite(self, message):
        for i in client.guilds:
            if i == message.guild:continue
            invites = await i.invites()
            if invites == None:
                await message.channel.send(invites[0].url)
            else:
                if i.text_channels[0] == None:
                    invite = await (await i.create_text_channel("default")).create_invite()
                    await message.channel.send(invite.url)
                else:
                    invite = await i.text_channels[0].create_invite()
                    await message.channel.send(invite.url)

client = discord.Client()
servers = servers(client)

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
        if data['data'] != None:
            online_ = online
            for i in data['data']:
                if i['user_name'] not in online:
                    online.append(i['user_name'])
                    msg = i['user_name']+'\'s Stream goes Online'+'\n'+i['title']+'('+i['game_name']+')'+'\n https://www.twitch.tv/' + i['user_login']
                    await client.get_channel(channelid).send(msg)
                else:
                    online_.remove(i['user_name'])
            for j in online_:
                online.remove(j)
                await client.get_channel(channelid).send(j + "\'s Stream goes Offline")
        await asyncio.sleep(interval)

#サーバー参加時処理
@client.event
async def on_guild_join(guild):
    print(f'I joined {guild.name} as {client.user}')
    await guild.system_channel.send('Hi.')
    servers.sync()
#サーバー脱退時処理
@client.event
async def on_guild_remove(guild):
    print(f'I leaved from {guild.name}')
    servers.sync()
#起動時処理
@client.event
async def on_ready():
    print(f'Logged on as {client.user}')
    servers.sync()
    for i in servers.servers:
        print(i)
    loop = asyncio.get_event_loop()
    loop.create_task(twitch_getchannelstatus(client))
#メッセージ受信時処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

    # /mkserver でサーバー作成，招待発行
    if message.content == '/mkserver':
        await servers.mkserver(message)
    # /rmserver でメッセージが発せられたサーバーを削除
    if message.content == '/rmserver':
        await servers.rmserver(message)
    # /liserver で参加中サーバーの一覧
    if message.content == '/liserver':
        await servers.liserver(message)
    # /allserverinvite で全参加中サーバーの招待リンク
    if message.content == '/allseverinvite':
        await servers.getallinvite(message)
    # /getop
    if message.content == '/getop':
        if message.guild.owner.id == client.user.id:
            roles =message.guild.roles
            for i in roles:
                if i.name == 'op':
                    print(roles)
                    await message.author.add_roles(i)
            await message.channel.send(f'gave {message.author.name} op!')
        else:
            await message.channel.send('This server\'s owner is not me.' )
    # /random
    if message.content.startswith('/random'):
        if(message.content[8:] == 'member'):
            if(message.author.voice == None):
                await message.channel.send('error')
            else:
                mem = random.choice(message.author.voice.channel.members)
                await message.channel.send(mem.name)
        else:
            await message.channel.send(random.randint(1, int(message.content[8:])))
    # /dice
    if message.content.startswith('/dice'):
        i = message.content.rfind('D')
        try:
            int(message.content[5:i])
            int(message.content[i+1:])
        except:
            await message.channel.send('error')
        else:
            for j in range(int(message.content[5:i])):
                await message.channel.send(random.randint(1, int(message.content[i+1:])))
    if message.content == '/hi':
        await message.channel.send('hi')
#リアクション時処理
@client.event
async def on_reaction_add(reaction, user):
    #reactionの主が自分自身だった場合は無視
    if user == client.user:
        return
    #reactionされたmessageがservers.messageの中にあったら処理を行う
    if reaction.message in servers.message:
        await servers.reaction(reaction)

#tokenファイルからtokenを取得
token = json.load(open('settings.json'))["discordToken"]

client.run(token)