import discord

#tokenファイルからtokenを取得
f = open('token', 'r')
token = f.read()
f.close()
#クラアントオブジェクトを生成
client = discord.Client()

#サーバー参加時処理
@client.event
async def on_guild_join(guild):
    print(f'I joined {guild.name} as {client.user}')
    await guild.system_channel.send('Hi.')

#起動時処理
@client.event
async def on_ready():
    print(f'Logged on as {client.user}')

#メッセージ受信時処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

client.run(token)