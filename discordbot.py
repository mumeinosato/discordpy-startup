import discord
import random
import time
import asyncio
import discord.ext
from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix="wb:", help_command=None)
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(f"ヘルプは wb:help | 導入サーバー数: {len(bot.guilds)}"))
    
    #status=discord.Status.idle で退席状態に
    
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
   

async def embox(title,description,color,message):
      embed = discord.Embed(title=title,description=description,color=color)
      await message.channel.send(embed=embed)

@bot.command()
async def help(ctx):#コマンドを定義するときの関数は必ずContextという引数が渡される。つまり引数を最低一つだけでも書いておかないと動かないので注意
    embed = discord.Embed(title="ヘルプ", description="このヘルプコマンドにはプレフィックスを書いていないため、\n実行には全て`wb:コマンド名`とする必要があります。",color=0x77aa27)
    #↑ここのテキストは自分で修正よろしく
    embed.add_field(name="help", value="このコマンドです。",inline=False)
    embed.add_field(name="newinfo", value="新着情報を確認します。",inline=False)
    embed.add_field(name="wiki", value="開発者が知っていること、関係することについてwiki形式で見ることができます。",inline=False)
    embed.add_field(name="dice", value="サイコロを振ることができます。",inline=False)
    embed.add_field(name="ping", value="botのメッセージ送信速度をチェックします。",inline=False)
    embed.add_field(name="about", value="botについてや、botの招待リンクを確認できます。",inline=False)
    embed.add_field(name="serverintroduction", value="開発者が運営しているサーバーについて表示できます。",inline=False)
    await ctx.send(embed=embed)#Contextにはいろいろな情報が入っており、そこから様々な関数、情報にアクセスできる。ctx.sendがその一つ

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="このbotについて...", description="Weabot / うぇあぼっと",color=0x77aa27)
    embed.add_field(name="製作者", value="うぇあChannel#6928",inline=True)
    embed.add_field(name="バージョン", value="Ver.1.6b\nコマンドフレームワーク移行版",inline=False)
    embed.add_field(name="このbotを招待", value="[こちら](https://discord.com/oauth2/authorize?client_id=699585993988374628&permissions=379968&scope=bot)から招待できます",inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def serverintroduction(ctx):
    embed = discord.Embed(title="開発者のサーバーについて...", description="以下のリンクから参加できます。",color=0x77aa27)
    embed.add_field(name="招待リンク:", value="https://discord.gg/9ayfU9K")
    await ctx.send(embed=embed)

@bot.command()
async def newinfo(ctx):
    await embox("新着情報","\n**2020 6/24** コマンドフレームワークへ移行しました。\n**2020 5/15** 一般公開を開始しました。\n**2020 5/14** help等のコマンドを3つ実装しました。\n**2020 5/2 **  BOTの稼働を開始しました。",0x77aa27,ctx.message)

@bot.command()
async def test(ctx):
    await embox("これはテストコマンドです。","特に意味はありません。",0x77aa27,ctx.message)

@bot.command()
async def ping(ctx):
    starttime = time.time()
    msg = await ctx.send("Pingを測定しています。\nしばらくお待ちください...")
    ping = time.time() - starttime
    await msg.edit(content=f"測定結果:{round(ping * 1000)}ms")
    #float(ping * 1000)

@bot.command()
async def wiki(ctx, *,arg:str=""):
    """
    コマンドには引数を指定できる。
    例えばこの場合は「tb:wiki Switch」と送信すると引数argに"Switch"が渡される。
    ちなみに引数が無いときは空の文字列が自動で入るようになっているけどここの説明は難しいので省略
    """
    if not arg:#こうしておくと、文字列が空であるとき(つまりこの場合は引数が渡されなかったとき)にifの中が実行される
        embed = discord.Embed(title="WeaのWikiへようこそ！", description="開発者が知っていることや関係することについてwiki形式で紹介します。\n(実行は全て`wb:wiki 単語名`というように行ってください。)",color=0x77aa27)
        embed.add_field(name="現在登録されているもの:", value="アスファルト 9: Legends\nNintendo Switch\nTJAPlayer3")
        await ctx.send(embed=embed)

    elif arg == "アスファルト 9: Legends":#スペースまで一字一句一致してないとifの中が実行されないので変えた方がいいかも
        await embox("アスファルト 9: Legends","アスファルト 9: Legends とは、\nゲームロフトが開発した\niOS、Android、Windows、Nintendo Switch、MacOS で\nプレイできるカーアクションレースゲームのこと。\nアスファルトシリーズ13作目(ナンバリングでは9作目)で、\n実在する車(マシン)を操作し、様々なロケーションでレースを行う。",0x77aa27,ctx.message)
    
    elif arg == "Nintendo Switch":
        await embox("Nintendo Switch","Nintendo Switch とは、\n任天堂が開発・販売をしている、\n据え置き型ゲーム機のこと。",0x77aa27,ctx.message)

    elif arg == "TJAPlayer3":
        await embox("TJAPlayer3","TJAPlayer3 とは、\nWindows向けの太鼓の達人エミュレーターの一つ。\n現在は配布を終了している。(Waybackmachineというツールを使用すればDL可)\n.tja 形式の譜面データと音源ファイルを用意することでプレイ可能。",0x77aa27,ctx.message)

@bot.event
async def on_message(message):
    """
    if message.author == bot.user:
        return
    """#Bot判定は下のif文で十分。ちなみにこれは複数行コメントアウト
    if message.author.bot:
        return

    if bot.user in message.mentions:
        print(f"{message.author.name}にメンションされました")
        await message.channel.send(f"{message.author.mention} ヘルプが必要ですか？\nwb:help でヘルプを表示します。")
        
    elif message.content == "wb:dice":
        await embox("サイコロコマンドが実行されました",f"何が出るかな？！何が出るかな？！\n\n実行者:{message.author.name}",0x77aa27,message)
        await asyncio.sleep(2)
        x = random.randint(1,6) # 50から100の乱数をxに代入
        await embox("結果は、、",f"結果は {str(x)} でした！",0x77aa27,message)
        return

    elif message.content.startswith("こんにち"):
        await message.channel.send("こんにちは！")

    elif message.content.startswith("こんちゃ"):
        await message.channel.send("こんちゃっちゃ！！")

    elif message.content.startswith("ども"):
        await message.channel.send("どうも！")

    elif message.content.startswith("よろし"):
        await message.channel.send("よろしくお願いします！")

    elif message.content.startswith("ただいま"):
        await message.channel.send("おかえり～")

    elif message.content.startswith("飯落ち"):
        await message.channel.send("いってらっしゃい！")

    elif message.content.startswith("落ち"):
        await message.channel.send("お疲れ～")

    elif message.content.startswith("ばい"):
        await message.channel.send("ばい～")

    elif message.content.startswith("死ね"):
        await message.channel.send("暴言はまずいですよ！！")

    elif message.content.startswith("おはよ"):
        await message.channel.send("おはようございます～")
        
    elif message.content.startswith("暇"):
        await message.channel.send("暇ですねぇ...")
        
    elif message.content.startswith("初めまして"):
        await message.channel.send("初めまして！")                                  

    await bot.process_commands(message)#on_messageの定義内の最後にこれを入れないと定義したコマンドが動かなくなる。注意

bot.run(token)
