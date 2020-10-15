import discord
import random
import time
import asyncio
import discord.ext
from discord.ext import commands
import os
import traceback
import random
import urllib.request
import json
import re
import urllib.request
from googletrans import Translator
from datetime import datetime, timedelta
from discord.ext import tasks

bot = commands.Bot(command_prefix="mus:", help_command=None)
token = os.environ['DISCORD_BOT_TOKEN']
client = discord.Client()
translator = Translator()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(f"ヘルプは mu:help | 導入サーバー数: {len(bot.guilds)}"))
    
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
    embed = discord.Embed(title="ヘルプ", description="このヘルプコマンドにはプレフィックスを書いていないため、\n実行には全て`mu:コマンド名`とする必要があります。",color=0x4169e1)
    #↑ここのテキストは自分で修正よろしく
    embed.add_field(name="help", value="このコマンドです。",inline=False)
    embed.add_field(name="newinfo", value="新着情報を確認します。",inline=False)
    embed.add_field(name="wiki", value="開発者が知っていること、関係することについてwiki形式で見ることができます。",inline=False)
    embed.add_field(name="dice", value="サイコロを振ることができます。",inline=False)
    embed.add_field(name="omikuji", value="おみくじを引くことができます。",inline=False)
    embed.add_field(name="ping", value="botのメッセージ送信速度をチェックします。",inline=False)
    embed.add_field(name="about", value="botについてや、botの招待リンクを確認できます。",inline=False)
    embed.add_field(name="support", value="この botのサポートサーバーを表示できます。",inline=False)
    embed.add_field(name="partnerserver", value="提携サーバーを表示します。",inline=False)
    await ctx.send(embed=embed)#Contextにはいろいろな情報が入っており、そこから様々な関数、情報にアクセスできる。ctx.sendがその一つ

@bot.command()
async def about(ctx):
    embed = discord.Embed(title="このbotについて...", description="Mumeinosato bot/ むめいのさと　ぼっと",color=0x4169e1)
    embed.add_field(name="製作者", value="Mumeinosato#7252",inline=True)
    embed.add_field(name="バージョン", value="Ver.1.2\nおみくじ実装版",inline=False)
    embed.add_field(name="このbotを招待", value="[こちら](https://discord.com/api/oauth2/authorize?client_id=729668738877620255&permissions=272103536&scope=bot)から招待できます",inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def support(ctx):
    embed = discord.Embed(title="サポートサーバーについて...", description="以下のリンクから参加できます。",color=0x4169e1)
    embed.add_field(name="招待リンク:", value="https://discord.gg/csJHtxZ")
    await ctx.send(embed=embed)

@bot.command()
async def partnerserver(ctx):
    embed = discord.Embed(title="提携サーバー一覧", description="以下のリンクから申請できます。",color=0x4169e1)
    embed.add_field(name="申請ページ:", value="https://forms.gle/53okyZb9L6MXztzq6")
    await ctx.send(embed=embed)
    embed = discord.Embed(title="提携サーバー", description="\n以下のリンクから参加できます。\n@@@ ",color=0x4169e1)
    embed.add_field(name="招待リンク:", value="https://discord.gg/csJHtxZ")
    await ctx.send(embed=embed)
    
@bot.command()
async def newinfo(ctx):
    await embox("新着情報","\n**2020 8/13** おみくじ内容追加。　\n**2020 8/12** おみくじ機能実装。　\n**2020 7/9** 試験運用開始。\n**2020 7/9 **  BOTの稼働を開始しました。",0x4169e1,ctx.message) 
 
@bot.command()
async def emsay(ctx,*,arg):
  await ctx.send(embed=discord.Embed(description=arg))

@bot.command()
async def test(ctx):
    await embox("これはテストコマンドです。","特に意味はありません。",0x4169e1,ctx.message)

@bot.command(pass_context = True) 
async def kick(ctx, userName: discord.User): 
    await bot.kick(userName)     
    
@bot.command()
async def ping(ctx):
    starttime = time.time()
    msg = await ctx.send("Pingを測定しています。\nしばらくお待ちください...")
    ping = time.time() - starttime
    await msg.edit(content=f"測定結果:{round(ping * 1000)}ms")
    #float(ping * 1000)

@bot.command()
async def user(ctx,uid):
    print(f"-user\n|<Author>{ctx.author}")
    user = await bot.fetch_user(int(uid))
    s = ""
    if user.bot:
        s = "`BOT`"
    embed = discord.Embed(title=f"{user}{s}",color=color)
    time = user.created_at+timedelta(hours=9)
    embed.add_field(name="アイコンURL",value=user.avatar_url_as(format="png"),inline=False)
    embed.add_field(name="タグ",value=user.discriminator)
    embed.add_field(name="ID",value=user.id)
    embed.set_footer(text=f"Discord参加日：{time.strftime('%Y-%m-%d')}")
    embed.set_thumbnail(url=user.avatar_url_as(format="png"))
    await ctx.send(embed=embed)    
    
@bot.command()
async def gban(ctx,mode,uid,reason):
    if ctx.author.id in [706373590869606431]:
        if mode == "add":
            try:
                user = await bot.fetch_user(int(uid))
            except:
                user = None
            if user is not None:
                if td["gban"].get(uid) is None:
                    async with ctx.typing():
                        td["gban"][uid] = reason
                        await rtutil.jwrite("data.json",td)
                        embed = discord.Embed(
                            title=f"GBANリストにユーザーが追加されました",
                            description=f"追加ユーザー：{user} ({user.id})",
                            color=0xf78279)
                        embed.add_field(name="理由",value=td["gban"][uid])
                        embed.set_thumbnail(url=user.avatar_url_as(format="png"))
                        for tg in bot.guilds:
                            for tc in tg.text_channels:
                                if tc.name == "tsuna-gban":
                                    if user in tc.guild.members:
                                        await tc.guild.ban(user,reason=f"<TUNA-GBAN>{td['gban'][uid]}")
                                    await tc.send(embed=embed)
                    await ctx.send(f"`{uid}`のユーザーをGBANに追加しました。")
                else:
                    await ctx.send(f"`{uid}`のユーザーは既に追加されています。")
            else:
                await ctx.send(f"`{uid}`のユーザーが見つかりませんでした。")
        elif mode == "rm":
            if td["gban"].get(uid) is not None:
                del td["gban"][uid]
                await rtutil.jwrite("data.json",td)
                await ctx.send(f"`{uid}`のユーザーをGBANから削除しました。")
            else:
                await ctx.send(f"`{uid}`のユーザーはまだ追加されていません。")
    else:
        await ctx.send("はっ？何勝手にGBANできると思っているの？何様のつもり？")
 

@client.event
async def on_message(message):
    if message.content.startswith("/kick"):
        args = message.content.split()
        user = discord.utils.get(message.guild.members, name=args[1])
        await user.kick()
        embed=discord.Embed(title="キックが正常に実行されました", color=0xff0000)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="対象", value=user, inline=False)
        embed.add_field(name="実行", value=message.author, inline=False)
        await message.channel.send(embed=embed)
    
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!trans'):
        say = message.content 
        print(say)
        say = say[7:]
        if say.find('-') == -1:
            str = say
            detact = translator.detect(str)
            befor_lang = detact.lang
            if befor_lang == 'ja':
                convert_string = translator.translate(str, src=befor_lang, dest='en')
                embed = discord.Embed(title='変換結果', color=0xff0000)
                embed.add_field(name='Befor', value=str)
                embed.add_field(name='After', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
            else:
                convert_string = translator.translate(str, src=befor_lang, dest='ja')
                embed = discord.Embed(title='変換結果', color=0xff0000)
                embed.add_field(name='Befor', value=str)
                embed.add_field(name='After', value=convert_string.text, inline=False)
                await message.channel.send(embed=embed)
        else:
            trans, str = list(say.split('='))
            befor_lang, after_lang = list(trans.split('-'))
            convert_string = translator.translate(str, src=befor_lang, dest=after_lang)
            embed = discord.Embed(title='変換結果', color=0xff0000)
            embed.add_field(name='Befor', value=str)
            embed.add_field(name='After', value=convert_string.text, inline=False)
            await message.channel.send(embed=embed)

    if message.content.startswith('!detect'):
        say = message.content 
        print(say)
        s = say[8:]
        detect = translator.detect(s)
        m = 'この文字列の言語はたぶん ' + detect.lang + ' です。'
        await message.channel.send(m)


@client.event
async def on_ready():
  print("logged in as " + client.user.name)

citycodes = {
    "土浦": '080020',
    "水戸": '080010',
    "札幌": '016010',
    "仙台": '040010',
    "東京": '130010',
    "横浜": '140010',
    "名古屋": '230010',
    "大阪": '270000',
    "広島": '340010',
    "福岡": '400010',
    "鹿児島": '460010',
    "那覇": '471010'
}

@client.event
async def on_message(message):
  if message.author != client.user:

    reg_res = re.compile(u"Bot君、(.+)の天気は？").search(message.content)
    if reg_res:

      if reg_res.group(1) in citycodes.keys():

        citycode = citycodes[reg_res.group(1)]
        resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
        resp = json.loads(resp.decode('utf-8'))

        msg = resp['location']['city']
        msg += "の天気は、\n"
        for f in resp['forecasts']:
          msg += f['dateLabel'] + "が" + f['telop'] + "\n"
        msg += "です。"

        await client.send_message(message.channel, message.author.mention + msg)

      else:
        await client.send_message(message.channel, "そこの天気はわかりません...")

@client.event
async def on_message(message):
    if message.author.bot:
        # もし、送信者がbotなら無視する
        return
    GLOBAL_CH_NAME = "hoge-global" # グローバルチャットのチャンネル名

    if message.channel.name == GLOBAL_CH_NAME:
        # hoge-globalの名前をもつチャンネルに投稿されたので、メッセージを転送する

        await message.delete() # 元のメッセージは削除しておく

        channels = client.get_all_channels()
        global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_NAME]
        # channelsはbotの取得できるチャンネルのイテレーター
        # global_channelsは hoge-global の名前を持つチャンネルのリスト

        embed = discord.Embed(title="hoge-global",
            description=message.content, color=0x00bfff)

        embed.set_author(name=message.author.display_name, 
            icon_url=message.author.avatar_url_as(format="png"))
        embed.set_footer(text=f"{message.guild.name} / {message.channel.name}",
            icon_url=message.guild.icon_url_as(format="png"))
        # Embedインスタンスを生成、投稿者、投稿場所などの設定

        for channel in global_channels:
            # メッセージを埋め込み形式で転送
            await channel.send(embed=embed)
                                                           
@bot.command()
async def wiki(ctx, *,arg:str=""):
    """
    コマンドには引数を指定できる。
    例えばこの場合は「tb:wiki Switch」と送信すると引数argに"Switch"が渡される。
    ちなみに引数が無いときは空の文字列が自動で入るようになっているけどここの説明は難しいので省略
    """
    if not arg:#こうしておくと、文字列が空であるとき(つまりこの場合は引数が渡されなかったとき)にifの中が実行される
        embed = discord.Embed(title="MumeinosatoのWikiへようこそ！", description="開発者が知っていることや関係することについてwiki形式で紹介します。\n(実行は全て`mu:wiki カテゴリー名又は単語名`というように行ってください。)",color=0x4169e1)
        embed.add_field(name="現在登録されているもの:", value="\nSNS\nゲーム\nTJAPlayer3")
        await ctx.send(embed=embed)

    elif arg =="ゲーム":
        await embox("ゲームカテゴリー","登録されているもの \nアスファルト 9: Legends\nTJAPlayer3",0x4169e1,ctx.message)

    elif arg =="SNS":
        await embox("SNSカテゴリー","登録されているもの　\nDiscord",0x4169e1,ctx.message)
            
    elif arg == "アスファルト 9: Legends":#スペースまで一字一句一致してないとifの中が実行されないので変えた方がいいかも
        await embox("アスファルト 9: Legends","アスファルト 9: Legends とは、\nゲームロフトが開発した\niOS、Android、Windows、Nintendo Switch、MacOS で\nプレイできるカーアクションレースゲームのこと。\nアスファルトシリーズ13作目(ナンバリングでは9作目)で、\n実在する車(マシン)を操作し、様々なロケーションでレースを行う。",0x4169e1,ctx.message)
    
    elif arg == "Nintendo Switch":
        await embox("Nintendo Switch","Nintendo Switch とは、\n任天堂が開発・販売をしている、\n据え置き型ゲーム機のこと。",0x4169e1,ctx.message)

    elif arg == "TJAPlayer3":
        await embox("TJAPlayer3","TJAPlayer3 とは、\nWindows向けの太鼓の達人エミュレーターの一つ。\n現在は配布を終了している。(Waybackmachineというツールを使用すればDL可)\n.tja 形式の譜面データと音源ファイルを用意することでプレイ可能。",0x4169e1,ctx.message)

    elif arg== "Discord":
        await embox("Disxord","https://ja.wikipedia.org/wiki/Discord_(ソフトウェア)",0x4169e1,ctx.message)
        
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
        await message.channel.send(f"{message.author.mention} ヘルプが必要なのか？\nmu:help でヘルプを表示しろよ")
        
    elif message.content == "mu:dice":
        await embox("サイコロコマンドが実行されました",f"サイコロぐらい自分でやれよ　今回だけだぞ　分かったなしっかり覚えておけよ\n\n実行者:{message.author.name}",0x4169e1,message)
        await asyncio.sleep(2)
        x = random.randint(1,6) # 50から100の乱数をxに代入
        await embox("結果は、、",f"結果は {str(x)} だよ　分かったか",0x4169e1,message)
        return

    elif message.content == "mu:omikuji":
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢は！",
                              color=0x4169e1)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.add_field(name="[運勢] ", value=random.choice(('大大吉', '大吉', '向大吉', '末大吉', '吉', '中吉', '小吉', '後吉', '吉凶未分末大吉', '吉凶相交末吉', '吉凶相半', '吉凶相央', '小凶後吉', '凶後吉', '凶後大吉', '凶', '大凶')), inline=False)
        await message.channel.send(embed=embed)
    
    elif message.content.startswith("こんにち"):
        await message.channel.send("こん")

    elif message.content.startswith("こんちゃ"):
        await message.channel.send("こん")

    elif message.content.startswith("ども"):
        await message.channel.send("どーもです")

    elif message.content.startswith("よろし"):
        await message.channel.send("よろ")

    elif message.content.startswith("ただいま"):
        await message.channel.send("おか")

    elif message.content.startswith("飯落ち"):
        await message.channel.send("いってら")

    elif message.content.startswith("落ち"):
        await message.channel.send("おつ〜")

    elif message.content.startswith("ばい"):
        await message.channel.send("ばーい")

    elif message.content.startswith("死ね"):
        await message.channel.send("そういうのよくないよ")

    elif message.content.startswith("おはよ"):
        await message.channel.send("おは")
        
    elif message.content.startswith("暇"):
        await message.channel.send("俺も暇だな〜")
        
    elif message.content.startswith("初めまして"):
        await message.channel.send("よろ〜")
        
    elif message.content.startswith("草"):
        await message.channel.send("草")
        
    elif message.content.startswith("無名の里"):
        await message.channel.send("無名の里(ムメイノサト)は、YouTuber、ゲーム開発者です。　是非YouTubeチャンネルを登録してね！https://www.youtube.com/channel/UCpb92184AP2Ffhyf7u2bD3w?view_as=subscriber")
        
    elif message.content.startswith("利用規約"):
        await message.channel.send("無名の里のコンテンツ利用規約です。https://mumeinosato.wixsite.com/lfkf/白紙ページ")
        
    elif message.content.startswith("オーナーのサイト"):
        await message.channel.send("無名の里のサイトです。https://mumeinosato.wixsite.com/lfkf")
        
    elif message.content.startswith("だろ"):
        await message.channel.send("そうだよ")
        
    elif message.content.startswith("そうだよ"):
        await message.channel.send("そうだよ")
        
    elif message.content.startswith("こんばん"):
        await message.channel.send("こんばんわんこそば")
                                 
       
    await bot.process_commands(message)#on_messageの定義内の最後にこれを入れないと定義したコマンドが動かなくなる。注意

bot.run(token)

