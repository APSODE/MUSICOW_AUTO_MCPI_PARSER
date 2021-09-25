
from discord import channel, embeds
from discord import client
from discord.client import Client
from discord.embeds import Embed
from selenium import webdriver
import selenium#
from selenium.webdriver.chrome.options import Options#
from discord.ext import commands # from discord.ext import tasks, commands
from discord.ext import tasks #
import urllib.request as URLRQ
import discord, sys, asyncio, time, random, datetime, os, numpy, json, bs4, urllib
from Class.USER_JSON_RW.rw_json import READ_WRITE
from Class.AUTO_DATA_REFRESH.AUTO_REFRESH_DATA import AUTO_REFRESH
sys.path.append("C:\\Users\\leegu\\AppData\\Local\\Programs\\Python\\Python38\\Scripts")



bot = commands.Bot(command_prefix='!')
BOT_TOKEN = "YOUR_BOT_TOKEN"
MAIN_CONFIG_DIR = ".\\MAIN_CONFIG\\MAIN_CONFIG.json"
CLASS_CONFIG_DIR = ".\\Class\\AUTO_DATA_REFRESH\\AUTO_DATA_REFRESH_CONFIG\\AUTO_DATA_REFRESH_CONFIG.json"
CH_DRIVER_DIR = ".\\chromedriver_win32\\chromedriver.exe"
UTF_8_ENCODING = "utf-8"

READ_CONFIG_DATA = READ_WRITE.READ_JSON(MAIN_CONFIG_DIR)
MCPI_VALUE_CHANNEL_ID = READ_CONFIG_DATA["SEND_CHANNEL_LIST"]["MCPI_CHANNEL"]


@bot.event
async def on_ready():
    print("=============")
    print(" 실 행 완 료 ")
    print("=============")
    # AUCTION_CHANNEL_ID = READ_CONFIG_DATA["SEND_CHANNEL_LIST"]["AUCTION_CHANNEL"]
    
    AUTO_DATA_REFRESH.start(MCPI_VALUE_CHANNEL_ID)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("저작권 수익 계산"))  

@tasks.loop(seconds = 1)
async def AUTO_DATA_REFRESH(self):
    CURRENT_TIME_CHECK = AUTO_REFRESH.TIME_CHECK()
    if CURRENT_TIME_CHECK == True:
        print(f"TIME_CHECK = {CURRENT_TIME_CHECK}")
        RT_FILE = AUTO_REFRESH.REFRESH_DATA(TIME_CHECK = CURRENT_TIME_CHECK)
        CHANNEL = bot.get_channel(MCPI_VALUE_CHANNEL_ID)

        await CHANNEL.purge(limit = 100)
        await CHANNEL.send(file = RT_FILE)

@bot.command(aliases = ["audfuddj", "afd", "cmd", "command", "ㅁㄹㅇ", "ㅋㅁㄷ", "커멘드", "층", "명령오"])
async def 명령어(ctx):
    RT_EMBED = discord.Embed(title = f":clipboard: 명령어 리스트 :clipboard:", description = "")
    RT_EMBED.add_field(name = f"`!채널변경`", value = "`!채널변경 <옥션 / MCPI> <변경할 채널ID>`")

    await ctx.send(embed = RT_EMBED)

@bot.command()
async def 채널변경(ctx, *arg):
    READ_CONFIG_DATA = READ_WRITE.READ_JSON(MAIN_CONFIG_DIR)
    AUCTION_CHANNEL_ID = READ_CONFIG_DATA["SEND_CHANNEL_LIST"]["AUCTION_CHANNEL"]
    MCPI_VALUE_CHANNEL_ID = READ_CONFIG_DATA["SEND_CHANNEL_LIST"]["MCPI_CHANNEL"]

    ALTERATION_CHANNEL_ID_TYPE = arg[0]
    ALTERATION_CHANNEL_ID = int(arg[1])


    if ALTERATION_CHANNEL_ID_TYPE in ["옥션", "auction", "dt", "ㅇㅅ"]:
        KEY_NAME = "AUCTION_CHANNEL"
        PRINT_NAME = "옥션"
    elif ALTERATION_CHANNEL_ID_TYPE in ["MCPI", "mcpi" "ㅡ체ㅑ"]:
        KEY_NAME = "MCPI_CHANNEL"
        PRINT_NAME = "MCPI"

    

    try:
        if ALTERATION_CHANNEL_ID == AUCTION_CHANNEL_ID or ALTERATION_CHANNEL_ID == MCPI_VALUE_CHANNEL_ID:
            if ALTERATION_CHANNEL_ID == AUCTION_CHANNEL_ID:
                CHECKING_CHANNEL_ID = AUCTION_CHANNEL_ID
            elif ALTERATION_CHANNEL_ID == MCPI_VALUE_CHANNEL_ID:
                CHECKING_CHANNEL_ID = MCPI_VALUE_CHANNEL_ID

            await ctx.send(f"입력하신 {PRINT_NAME} 채널ID `{ALTERATION_CHANNEL_ID}`는 기존 {PRINT_NAME} 채널ID `{CHECKING_CHANNEL_ID}`와 동일합니다.")

        else:
            READ_CONFIG_DATA = READ_WRITE.READ_JSON(MAIN_CONFIG_DIR)
            with open(MAIN_CONFIG_DIR, "w", encoding = UTF_8_ENCODING) as WRITE_CONFIG_PROFILE:
                READ_CONFIG_DATA["SEND_CHANNEL_LIST"][KEY_NAME] = ALTERATION_CHANNEL_ID
                json.dump(READ_CONFIG_DATA, WRITE_CONFIG_PROFILE, indent = 4)

            await ctx.send(f"입력하신 {PRINT_NAME} 채널ID `{ALTERATION_CHANNEL_ID}`로 변경하였습니다.")
    except Exception as ERROR_MSG:
        await ctx.send(f"오류가 발생하였습니다. 제작자를 호출하여 주십시오.")
        print(ERROR_MSG)

@bot.command(aliases = ["MCPI", "mcpi", "저작권", "wjwkrrnjs", "ㅡ체ㅑ", "ㅡ쳬ㅑ"])
async def 저작권지수(ctx):
    RT_EMBED = AUTO_REFRESH.CURRENT_MCPI_DATA()
    await ctx.send(embed = RT_EMBED)

@bot.command()
async def 기능테스트(ctx):
    # CURRENT_TIME_CHECK = AUTO_REFRESH.TIME_CHECK(TEST_RUN = True)
    # RT_DATA_IMG = AUTO_REFRESH.REFRESH_DATA(TIME_CHECK = CURRENT_TIME_CHECK)
    RT_EMBED = AUTO_REFRESH.CURRENT_MCPI_DATA()
    await ctx.send(embed = RT_EMBED)


#heroku서버에 이식


    
bot.run(BOT_TOKEN)
