import asyncio
import discord
import random
import json
import twitchstatus

client = discord.Client()

#サーバー参加時処理
@client.event
async def on_guild_join(guild):
    print(f'I joined {guild.name} as {client.user}')
    await guild.system_channel.send('Hi.')
#サーバー脱退時処理
@client.event
async def on_guild_remove(guild):
    print(f'I leaved from {guild.name}')
#起動時処理
@client.event
async def on_ready():
    print(f'Logged on as {client.user}')
    #Twitch通知用の処理を開始
    loop = asyncio.get_event_loop()
    loop.create_task(twitchstatus.twitch_getchannelstatus(client))
#メッセージ受信時処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
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

#tokenファイルからtokenを取得
token = json.load(open('settings.json'))["discordToken"]
client.run(token)