import discord

#tokenファイルからtokenを取得
f = open('token', 'r')
token = f.read()
f.close()
#クラアントオブジェクトを生成
client = discord.Client()

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
        invite = await (await guild.create_text_channel("default")).create_invite()
        await message.channel.send(invite.url)
        self.sync()

    async def rmserver(self, message):
        await message.guild.delete()
        self.sync()

    async def liserver(self, message):
        await message.channel.send(self.servers)

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
servers = servers(client)

#サーバー参加時処理
@client.event
async def on_guild_join(guild):
    print(f'I joined {guild.name} as {client.user}')
    await guild.system_channel.send('Hi.')

#起動時処理
@client.event
async def on_ready():
    print(f'Logged on as {client.user}')
    servers.sync()
    for i in servers.servers:
        print(i)
        await i.system_channel.send('I\'m online')

#メッセージ受信時処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')
    if message.content == '/where':
        if message.author.voice == None: await message.channel.send('You don\'t join voice channel')
        else: print(message.author.voice.channel)

    # /mkserver でサーバー作成，招待発行
    if message.content == '/mkserver':
        await servers.mkserver(message)
    # /rmserver でメッセージが発せられたサーバーを削除
    if message.content == '/rmserver':
        await servers.rmserver(message)
    # /liserver で参加中サーバーの招待リンク
    if message.content == '/liserver':
        await servers.liserver(message)
    if message.content == '/allseverinvite':
        await servers.getallinvite(message)

client.run(token)