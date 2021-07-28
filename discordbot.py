import discord
#tokenファイルからtokenを取得
f = open('token', 'r')
token = f.read()
f.close()
#クラアントオブジェクトを生成
client = discord.Client()


client.run(token)
