import discord, asyncio
import pymysql
import traceback
import random
import time
import os
import hashlib
import math
from discord.ext import tasks
from discord.ext import commands
from discord import FFmpegPCMAudio
from datetime import datetime, date
from bs4 import BeautifulSoup
import json
import re
import requests
from collections import Counter
from umi import *
# from umi import umi

# 초기화
intents = discord.Intents.default()
intents.members = True
intents.presences = True

token = "NjkyMjYzNDI4MDY4NDc0OTMw.XxnsEA.Ix_nSvIgSlqDP5u2YMVD9QvWKZg"
client = commands.Bot(command_prefix='.', intents=intents)


# global tray
# 자음퀴즈 관련 전역변수들(정답기능 있음, 포기 존재, 미진행 여부 tray 변수로 구분)

tray = ""
logch = None
timer = None
waitch = None
wcmessage = None
htimer1 = None
htimer2 = None
stime = None
ishard = False
jqnowuser = None
channel7 = None
fortestch = None

notallowall = ["dict출력", "off", "단어수정", "단어추가", "랭킹초기화", "아무말", "점수설정", "콤보초기화", "콤보테스트"]


ansnum = []
strike = 0
ball = 0
isout2 = True
baseballremains = 25


combodic = {}
hintmul = 300
nowauto = False
autotag = ""
autouid = ""
autoctx = None
nowdiff = "normal"









# 태그 사전 전역변수
#  "마마마":"마법소녀 마도카 마기카@mamama",

# 음성 재생 관련 전역변수들
isjoined = False
isplaying = False
ctxforglobal = None
elptime = 0
isbooted = False
channel9 = None

# 생일 체크 관련 변수들
allhae = date.today().strftime("%Y")
honoka = [int(allhae), 8, 3]
umi = [int(allhae), 3, 15]
kotori = [int(allhae), 9, 12]
rin = [int(allhae), 11, 1]
hanayo = [int(allhae), 1, 17]
maki = [int(allhae), 4, 19]
nozomi = [int(allhae), 6, 9]
eli = [int(allhae), 10, 21]

musedic = {"honoka":date(int(allhae), 8, 3), "umi":date(int(allhae), 3, 15), "kotori":date(int(allhae), 9, 12),
"rin":date(int(allhae), 11, 1), "maki":date(int(allhae), 4, 19), "hanayo":date(int(allhae), 1, 17),
"nozomi":date(int(allhae), 6, 9), "eli":date(int(allhae), 10, 21) }

# 직접출제 관련 전역변수들(정답기능 있음, 포기 존재, 미진행 여부 gaekdic 배열 길이로 구분)
gaekdic = []
judic = []
mtimer999 = None
remains = 0


@tasks.loop(minutes=1.0)
async def clocksound():
    global ctxforglobal
    global isjoined
    global isbooted
    global elptime
    global channel7

    

    if isbooted == False:
        isbooted = True
    else:
        elptime += 1
        
        if elptime % 20 == 0:
            if elptime % 60 != 0:
                now = datetime.now().strftime("%H:%M:%S")
                print(f"{now} ) 20분 경과")
            else:
                await channel7.send(f"봇 가동 시작 후 {int(elptime / 60)}시간이 경과하였습니다.")

@client.event
async def on_member_update(before, after):
    global channel7
    bs = before.status
    ast = after.status

    ba = before.activity
    aa = after.activity

    if bs != ast:
        if ast == discord.Status.online:
            await channel7.send(f"엌 {after.display_name}님 오심 흑흑", tts=True)
            #return
        if ast == discord.Status.offline:
            await channel7.send(f"엌 {after.display_name}님 가심 흑흑", tts=True)
            #return
        if ast == discord.Status.idle:
            await channel7.send(f"엌 {after.display_name}님 자리비움이심 흑흑", tts=True)
            #return
        if ast == discord.Status.dnd:
            await channel7.send(f"엌 {after.display_name}님 방해금지 모드 켜심 흑흑", tts=True)
            #return
    '''
    if (isinstance(ba, discord.Activity) or ba == None) and (isinstance(aa, discord.Activity) or aa == None):
        if ba != aa:
            if aa != None:
                await channel7.send(f"엌 {after.display_name}님 {aa.name} 켜심 흑흑", tts=True)
            elif ba != None and aa == None:
                await channel7.send(f"엌 {after.display_name}님 {ba.name} 끄심 흑흑", tts=True)
    '''
            
@client.event
async def on_member_join(member):
    global waitch, wcmessage
    newbierole = discord.utils.get(member.guild.roles, name="New")
    await member.add_roles(newbierole)
    wcmessage = await waitch.send("서버에 오신 것을 환영합니다!\n\n\
이 채널은 신규 유저의 규칙 준수 의사를 확인하기 위한 대기용 채널입니다. 아래의 서버 규칙을 잘 읽어보신 다음 모든 내용에 동의하실 경우 아래의 체크 표시를 누르시면 바로 기본적인 채널 출입 권한이 부여됩니다. 동의 시 대기 채널로 다시 돌아올 수 없으니 유의하시기 바랍니다.\n\n\
1. 서버가 매우 시끄럽습니다. - 알림을 끌 수 있거나 적응이 가능하여야 합니다.\n\
2. 서브컬처 문화(일명 덕후 문화)에 대한 거부감이 없어야 합니다. - 단, 만약 자신이 이러한 문화와 거리가 멀다고 하더라도 취향을 존중하실 수 있다면 문제가 되지 않습니다.\n\
3. 이미 활동 중인 유저와 플레이하는 게임이 겹치도록 할 것을 권장합니다. (목록: 끄투, 오스, 롤, 클로, 마기레코, 이사만루, 스쿠스타 등)\n\
4. 이 서버는 카카오톡 오픈채팅방이 아닙니다! - 이 서버와 관련하여 현실 세계에서의 신변 문제가 생기지 않는 이상 가볍게 대화하다 흥미를 잃어 나가실 분은 받지 않습니다.\n\
**5. 서버 내에서 분쟁이 발생할 경우 이에 대한 결론 도출 및 연루된 인원들의 처벌 여부, 수위를 포함한 모든 최종 해석권은 전적으로 서버 관리자에게만 주어집니다.**\n\n\
규칙 1~5항의 위반이 적발되거나 준수 의지가 없다고 판단될 경우 서버 관리자에 의해 추방될 수 있습니다. 참고로 서버 분위기를 파악하는데 도움이 될 수 있도록 메인 채널인 잡담 채널의 읽기 권한을 개방하였으니 10분 이상 해당 채널을 지켜보고 결정하시는 것을 권장드립니다.")
    await wcmessage.add_reaction("\U00002705")
    # await wcmessage.add_reaction("\U0000274E")

@client.event
async def on_raw_reaction_add(payload):
    global waitch, wcmessage
    # 692263428068474930
    if wcmessage != None:
        gd = wcmessage.guild
    else:
        return

    if payload.message_id == wcmessage.id and payload.user_id != client.user.id:
        user3 = gd.get_member(payload.user_id)
        newbierole = discord.utils.get(user3.guild.roles, name="New")
        nncrole = discord.utils.get(user3.guild.roles, name="Normal_NoColor")
        await user3.add_roles(nncrole)
        await user3.remove_roles(newbierole)

def checkgh(passport3, req):
    global notallowall
    if str(passport3) != "630348273730846760" and req in notallowall:
        return False
    else:
        return True

@client.event
async def on_message(msg):
    await client.process_commands(msg)

    if msg.author.bot:
        return

    ngame = getnowgame()

    global timer
    global htimer1
    global htimer2
    global jqnowuser, combodic, hintmul, nowdiff
    global nowauto, autotag, autoctx
    global tray

    # Hit Value + (Hit Value * ((Combo multiplier * Difficulty multiplier * Mod multiplier) / 25))

    if ngame == "자음 퀴즈가":
        if msg.content == tray:
            await asyncio.sleep(0)
            timer.cancel()
            await asyncio.sleep(0)
            htimer1.cancel()
            await asyncio.sleep(0)
            htimer2.cancel()
            uid3 = str(msg.author.id)

            combomul = 1.1 ** max(0, int(combodic[str(msg.author.id)]))

            if combomul == 1:
                combomul = 0

            if nowdiff == "normal":
                modmul = 1
            else:
                modmul = 0.2

            s1 = hintmul + (hintmul * ((combomul * 6 * modmul) / 25))
            final = min(7500, round(s1))
            if hintmul < 300 and uid3 == jqnowuser:
                combodic[uid3] = 0
            elif uid3 != jqnowuser:
                # combodic[jqnowuser] = 0
                final = 400 if nowdiff == "normal" else 80
                # combodic[uid3] += 1
            else:
                if nowdiff == "normal":
                    combodic[uid3] += 1
                elif nowdiff == "easy":
                    final = 80

            hintmul = 300
            tray = ""
            if ((combodic[uid3] < 2 and uid3 == jqnowuser) or (combodic[uid3] < 2 and uid3 != jqnowuser)):
                await msg.channel.send(f"{msg.author}님 정답! {final}점을 획득하였습니다.")
                addscore(int(final), str(msg.author.id))

                if nowauto:
                    await startgamebytag(autotag, autoctx, "normal")

            elif (combodic[uid3] > 1 and uid3 != jqnowuser) or (combodic[uid3] > 1 and uid3 == jqnowuser):
                await msg.channel.send(f"{msg.author}님 정답! {final}점을 획득하였습니다. (현재 {combodic[uid3]}연속)")
                addscore(int(final), str(msg.author.id))

                if nowauto:
                    await startgamebytag(autotag, autoctx, "normal")

                

    # global practag
    # global alreadyqueue
    # global fchr
    # global wmax
    # global wnow
    # global timertray

    
    

    global mtimer999, gaekdic, remains

    trigger = msg.author
    

    if ngame == "객관식 문제가":
        if msg.content == gaekdic[6]:
            mtimer999.cancel()
            gaekdic = []
            await msg.channel.send(f"{trigger}님 정답!")
        elif msg.content == "1" or msg.content == "2" or msg.content == "3" or msg.content == "4" or msg.content == "5":
            remains = remains - 1
            await msg.channel.send(f"{trigger}님 오답.")
            if remains == 0:
                mtimer999.cancel()
                await msg.channel.send(f"답안 제출 횟수를 모두 사용하였습니다. (정답: {gaekdic[6]}번)")
                gaekdic = []

    global judic

    trigger = msg.author

    if ngame == "주관식 문제가":
        if msg.content == judic[1]:
            mtimer999.cancel()
            judic = []
            await msg.channel.send(f"{trigger}님 정답!")

    
    if ngame == "숫자 야구가":
        global ansnum, strike, ball, isout2, baseballremains
        
        if len(msg.content) == 4 and str(msg.content).isdigit():
            useransnum = [int(msg.content[0]), int(msg.content[1]), int(msg.content[2]), int(msg.content[3])]
            if len(useransnum) == len(set(useransnum)):
                isout2 = True
                strike = 0
                ball = 0
                for i, j in enumerate(useransnum):
                    for k, l in enumerate(ansnum):
                        if i == k and j == l:
                            strike = strike + 1
                            isout2 = False
                        elif i != k and j == l:
                            ball = ball + 1
                            isout2 = False

                baseballremains = baseballremains - 1
                if isout2 == False:
                    if strike == 4 and ball == 0:
                        ansnum.clear()
                        await msg.channel.send(f"{trigger}님의 답: {msg.content} -> 홈런! (도전 횟수: {25 - baseballremains}회)")
                        
                    else:
                        await msg.channel.send(f"{trigger}님의 답: {msg.content} -> {strike}스트라이크, {ball}볼")
                        if baseballremains == 0:
                            
                            stransnum = str(ansnum[0]) + str(ansnum[1]) + str(ansnum[2]) + str(ansnum[3])
                            await msg.channel.send(f"도전 횟수를 모두 사용하여 게임이 종료되었습니다. (정답: {stransnum})")
                            ansnum.clear()
                            
                else:
                    await msg.channel.send(f"{trigger}님의 답: {msg.content} -> 아웃!")
                    if baseballremains == 0:
                        
                        stransnum = str(ansnum[0]) + str(ansnum[1]) + str(ansnum[2]) + str(ansnum[3])
                        await msg.channel.send(f"도전 횟수를 모두 사용하여 게임이 종료되었습니다. (정답: {stransnum})")
                        ansnum.clear()



    result = random.randrange(1, 1501)
    if result < 2:
        # await msg.add_reaction('\U0001f4ae')
        await msg.channel.send("엌")

@client.event
async def on_message_delete(msg3):
    global logch
    detail = msg3.content[:300]
    if not msg3.author.bot:
        await logch.send(f"{msg3.author}님이 메시지를 삭제하였습니다. (내용: {detail})")


def getnowgame():
    # practag, skans, hostandclient dupqueue, 
    global gaekdic, judic, tray, ansnum
    if tray != "": # 자음 퀴즈 진행 여부 체크
        return "자음 퀴즈가"

    elif len(gaekdic) != 0: # 객관식 문제 진행 여부 체크
        return "객관식 문제가"
    
    elif len(judic) != 0: # 주관식 문제 진행 여부 체크
        return "주관식 문제가"

    elif len(ansnum) != 0:
        return "숫자 야구가"
    
    else: # 아무것도 진행 중이지 않음
        return -1

async def hinttimer1(a, ans, gamemode):
    global hintmul

    await asyncio.sleep(10)

    hintmul = 100 if gamemode == "normal" else 300
    hint = getrevealed(ans, False, "normal") if gamemode == "normal" else getrevealed(ans, False, "easy")
    print(f"첫 번째 힌트: {hint}")
    embed1 = discord.Embed(title="자음퀴즈 - 힌트 1", color=0x0000ff)
    embed1.set_footer(text="20초 남았습니다.")
    embed1.add_field(name="문제", value=hint, inline=True)
    await a.send(embed=embed1)

async def hinttimer2(a, ans, gamemode):
    global hintmul

    await asyncio.sleep(20)
    
    hintmul = 50 if gamemode == "normal" else 300
        
    hint = getrevealed(ans, False, "normal") if gamemode == "normal" else getrevealed(ans, False, "easy")
    print(f"두 번째 힌트: {hint}")
    embed1 = discord.Embed(title="자음퀴즈 - 마지막 힌트", color=0x0000ff)
    embed1.set_footer(text="10초 남았습니다.")
    embed1.add_field(name="문제", value=hint, inline=True)
    await a.send(embed=embed1)

async def qstclose(a, ans):
    global jqnowuser, hintmul, combodic, nowauto, tray
    await asyncio.sleep(30)
            
    tray = ""
    combodic[jqnowuser] = 0
    hintmul = 300
    await a.send(f"제한시간이 초과되어 문제가 종료되었습니다. (정답: {ans})")

    if nowauto:
        await startgamebytag(autotag, autoctx, "normal")

def getqtyw(tag, where):
    if not tag in tagdic.keys():
        return "-1"
    
    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")
    try:
        with conn.cursor() as cs:
            q = f"select count(*) from {tagdic[tag].split('@')[1]} {where};"
            cs.execute(q)
            rows = cs.fetchall()
            for row in rows:
                tray = row
            return tray
    finally:
        conn.close()


def getqty(tag):
    if not tag in tagdic.keys():
        return "-1"
    
    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")
    try:
        with conn.cursor() as cs:
            q = f"select count(*) from {tagdic[tag].split('@')[1]};"
            cs.execute(q)
            rows = cs.fetchall()
            tray = rows[0][0]
            if tray == "0":
                return "0"
            return tray
    finally:
        conn.close()

def modword(tag, prevw, nextw, uid):
    if not tag in tagdic.keys():
        return "-1"

    if uid != "630348273730846760":
        return "-2"



    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")

    try:
        with conn.cursor() as cs:
            if nextw != "-":
                q = f"update {tagdic[tag].split('@')[1]} set wname='{nextw}' where wname='{prevw}';"
                cs.execute(q)
                conn.commit()

                q = f"select * from {tagdic[tag].split('@')[1]} where wname='{nextw}';"
                cs.execute(q)
                conn.commit()

                if cs.rowcount == 0:
                    return "999"
                else:
                    return "2"
            else:
                q = f"select * from {tagdic[tag].split('@')[1]} where wname='{prevw}';"
                cs.execute(q)
                conn.commit()

                if cs.rowcount == 0:
                    return "99999"

                q = f"delete from {tagdic[tag].split('@')[1]} where wname='{prevw}';"
                cs.execute(q)
                conn.commit()

                return "222"

    finally:
        conn.close()

def addword(w, tag, uid, isoneword=True):
    if not tag in tagdic.keys():
        return "-1"

    if uid != "630348273730846760":
        return "-2"



    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")

    try:
        with conn.cursor() as cs:
            if isoneword:
                q = f"insert into {tagdic[tag].split('@')[1]}(wname) value ('{w}');"
            cs.execute(q)
            conn.commit()
            return "2"
    finally:
        conn.close()




async def startgamebytag(tag, ctx, gamemode="normal"):
    global timer
    global htimer1
    global htimer2
    global stime, ishard, jqnowuser, combodic, tray

    if tag in tagdic.keys():
        uid = str(ctx.message.author.id)
        for i in ctx.message.guild.members:
            if str(i.id) not in combodic.keys():
                combodic[str(i.id)] = 0

        jqnowuser = uid
        
        tray = getword(tag)[0][0]
        fordisp = getrevealed(tray, True, "normal") if gamemode == "normal" else getrevealed(tray, True, "easy")
        embed1 = discord.Embed(title="자음퀴즈", color=0x0000ff)
        embed1.set_footer(text="제한시간: 30초")
        embed1.add_field(name="문제", value=fordisp, inline=True)
        embed1.add_field(name="주제", value=tagdic[tag].split("@")[0], inline=True)
        await ctx.send(embed=embed1)
        stime = datetime.now()

        timer = client.loop.create_task(qstclose(ctx, tray))

        if gamemode == "normal":
            htimer1 = client.loop.create_task(hinttimer1(ctx, tray, "normal"))
            htimer2 = client.loop.create_task(hinttimer2(ctx, tray, "normal"))
        elif gamemode == "easy":
            htimer1 = client.loop.create_task(hinttimer1(ctx, tray, "easy"))
            htimer2 = client.loop.create_task(hinttimer2(ctx, tray, "easy"))
    else:
        await ctx.send("존재하지 않는 주제입니다.")

async def twosel(list2, num, ctx3):
    seldic = {"s1":list2[0], "s2":list2[1]}
    seldic2 = [0, 0]
    
    tried = 0

    while tried < num:
        if random.randrange(0, 2) == 1:
            seldic2[1] += 1
            tried += 1
        else:
            seldic2[0] += 1
            tried += 1
    
    if num > 1:
        await ctx3.send(f"{num}회 선택 결과:\n{seldic['s1']}: {seldic2[0]}회\n{seldic['s2']}: {seldic2[1]}회")
    else:
        await ctx3.send(f"{list2[random.randrange(0, 2)]}가 선택되었습니다.")

def addscore(s, uid):
    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")

    try:
        with conn.cursor() as cs:
            q = f"update jqranking set score = score + ({s}) where mnum='{uid}';"
            cs.execute(q)
            conn.commit()
            return "2"
    finally:
        conn.close()

def setscore(dname, s):
    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")

    try:
        with conn.cursor() as cs:
            q = f"update jqranking set score = {s} where dispname like '%{dname}%';"
            cs.execute(q)
            conn.commit()
            return "2"
    except:
        return "3"
    finally:
        conn.close()

def getfromrank(r):
    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")
    # result = ""
    rankcount = 0

    try:
        with conn.cursor() as cs:
            q = f"select dispname, score from jqranking order by score desc;"
            cs.execute(q)
            row = cs.fetchall()

            for i in row:
                rankcount += 1
                if rankcount == r:
                    return i




            
            return "-1"
                
            
    finally:
        conn.close()

def getrinfo(uid, dtype):
    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")

    try:
        with conn.cursor() as cs:
            if dtype == "score":
                q = f"select score from jqranking where mnum='{uid}';"
                cs.execute(q)
                row = cs.fetchall()
            else:
                q = f"select maxcb from jqranking where mnum='{uid}';"
                cs.execute(q)
                row = cs.fetchall()

            
            return row[0][0]
                
            
    finally:
        conn.close()

def getallranking():
    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")
    result = ""
    rankcount = 0

    try:
        with conn.cursor() as cs:
            q = f"select dispname, score from jqranking order by score desc;"
            cs.execute(q)
            row = cs.fetchall()

            for i in row:
                rankcount += 1
                strscore = "{:,}".format(i[1])
                if cs.rowcount != rankcount:
                    result = result + f"{rankcount}위: {i[0].split('#')[0]} {strscore}점\n"
                else:
                    result = result + f"{rankcount}위: {i[0].split('#')[0]} {strscore}점"




            
            return result
                
            
    finally:
        conn.close()




def setcombo(c, uid):
    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")

    try:
        with conn.cursor() as cs:
            q = f"update jqranking set maxcb = {c} where mnum='{uid}';"
            cs.execute(q)
            conn.commit()
            return "2"
    finally:
        conn.close()




@client.event
async def on_ready():
    global channel7, fortestch, waitch, logch
    channel7 = client.get_channel(719714080486588491) # 잡담 채널
    waitch = client.get_channel(761057012971733030)
    # fortestch = client.get_channel(719738841841533009) # 테스트 채널
    fortestch = client.get_channel(719714080486588491) # 테스트 채널
    logch = client.get_channel(724696646059032608) # 삭제로그 채널
    now = datetime.now().strftime("%H:%M:%S")
    await client.change_presence(status=discord.Status.online, activity=discord.Game("봇 작동"))
    await channel7.send("봇 가동을 시작합니다.")
    print(f"{now} ) 봇 작동 중입니다...")
    print(client.user.name)
    print(client.user.id)

@client.command(pass_context=True)
async def xtts(ctx, num, *args):
    if str(ctx.message.author.id) != "630348273730846760":
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")
        return

    tray = []
    for a in args:
        tray.append(a)
    
    for i in range(0, int(num)):
        await ctx.send(" ".join(tray), tts=True)

@xtts.error
async def onerror977(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .xtts (반복할 횟수) (할말)")

@client.command(pass_context=True)
async def 선택(ctx, number, *args):
    try:
        numforpassing = int(number)
        finalargs = {}
        listforshow = []

        if numforpassing < 0 or numforpassing > 5000:
            await ctx.send("횟수에는 1 이상 5000 이하의 정수만 올 수 있습니다.")
            return

        for i in args:
            finalargs[str(i)] = 0

        for _ in range(0, numforpassing):
            finalargs[str(random.sample(args, 1)[0])] += 1
        if numforpassing > 1:
            listforshow.append(f"{numforpassing}회 선택 결과:")

            for i in finalargs.keys():
                listforshow.append(f"{i}: {finalargs[i]}회")

            await ctx.send("\n".join(listforshow))
        elif numforpassing == 1:
            for i in finalargs.keys():
                if finalargs[i] == 1:
                    await ctx.send(f"{i}(이)가 선택되었습니다.")
                    return





    except ValueError:
        await ctx.send("횟수에는 1 이상 5000 이하의 정수만 올 수 있습니다.")

@선택.error
async def onerror7(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .선택 (횟수) (대상1) (대상2) (대상3)...")

@client.command(pass_context=True)
async def 갯수(ctx, tag):

    res3 = getqty(tag)
    if res3 == "-1":
        await ctx.send("없는 주제입니다.")
    elif res3 == "0":
        await ctx.send("비어있는 주제입니다.")
    else:
        disptag = tagdic[tag].split("@")[0]
        await ctx.send(f"{disptag} 주제의 현재 단어 갯수는 {res3}개입니다.")

@갯수.error
async def onerror(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == "tag":
            await ctx.send("사용법: .갯수 (주제)")

@client.command(pass_context=True)
async def dict출력(ctx):
    for k, v in combodic.items():
        await ctx.send(f"{k}: {v}")

@client.command(pass_context=True)
async def 랜덤단어(ctx, tag):

    response = getword(tag)

    if response == "-1":
        await ctx.send("없는 주제입니다.")
    else:
        tray = getword(tag)[0][0]
        embed1 = discord.Embed(title="랜덤 단어", color=0x0000ff)
        embed1.set_footer(text=f"주제 - {tagdic[tag].split('@')[0]}")
        embed1.add_field(name="단어", value=tray, inline=True)
        embed1.add_field(name="길이", value=len(tray), inline=True)
        await ctx.send(embed=embed1)

@랜덤단어.error
async def onerror2(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == "tag":
            await ctx.send("사용법: .랜덤단어 (주제)")

@client.command(pass_context=True)
async def 검색(ctx, w, tag="deftag"):
    if tag == "deftag":
        response = searchwordfromall(w)
    elif tag != "deftag" and len(w.split("-")) > 1 and w.split("-")[1] != "?" and w.split("-")[0] != "?":
        response = iswordexist(tag, w)
    elif tag != "deftag" and len(w.split("-")) > 1 and (w.split("-")[1] == "?" or w.split("-")[0] == "?"):
        response = getallstartword(tag, w)
        if response == "-1":
            await ctx.send("존재하지 않는 주제입니다.")
            return
        elif response == "-2":
            await ctx.send("일치하는 단어가 없습니다.")
            return
    elif tag != "deftag" and len(w.split("-")) < 2:
        await ctx.send("사용법: .검색 (단어 또는 시작 글자-미션 글자) (주제(-를 사용하여 검색할 경우))")
        return



    if response == "-1":
        await ctx.send("존재하지 않는 주제입니다.")
        return
    elif response == "-2":
        await ctx.send("일치하는 단어가 없습니다.")
        return
    else:
        if tag == "deftag":
            embed1 = discord.Embed(title="단어 검색 결과", color=0x0000ff)
            embed1.add_field(name="단어", value=response[0], inline=True)
            embed1.add_field(name="길이", value=len(response[0]), inline=True)
            embed1.set_footer(text=f"주제 - {', '.join(response[1:])}")
            await ctx.send(embed=embed1)
        elif tag != "deftag" and len(w.split("-")) > 1 and (w.split("-")[1] == "?" or w.split("-")[0] == "?"):
            tempcnt = 0
            for i in response:
                if tempcnt == 5:
                    break
                embed1 = discord.Embed(title="단어 검색 결과", color=0x0000ff)
                embed1.add_field(name="단어", value=i[0], inline=True)
                embed1.add_field(name="길이", value=len(i[0]), inline=True)
                embed1.set_footer(text=f"주제 - {tagdic[tag].split('@')[0]}")
                await ctx.send(embed=embed1)
                tempcnt = tempcnt + 1
        else:
            embed1 = discord.Embed(title="단어 검색 결과", color=0x0000ff)
            embed1.add_field(name="단어", value=response[0], inline=True)
            embed1.add_field(name="길이", value=len(response[0]), inline=True)
            embed1.set_footer(text=f"주제 - {tagdic[tag].split('@')[0]}")
            await ctx.send(embed=embed1)


@검색.error
async def onerror213(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .검색 (단어 또는 시작 글자-미션 글자) (주제(-를 사용하여 검색할 경우))")
    else:
        traceback.print_stack()
        traceback.print_exc()

@client.command(pass_context=True)
async def 곡랭킹(ctx, diffnum, page="1", gmode="태고"):
    try:
        gmodedic = {"스탠": "osu", "태고": "taiko", "캐치": "fruits", "매니아": "mania"}

        if gmode not in gmodedic.keys():
            await ctx.send("올바르지 않은 게임 모드입니다. (스탠, 태고, 캐치, 매니아 중 택일)")
            return

        html2 = requests.get(f"https://osu.ppy.sh/beatmaps/{diffnum}/scores?type=global&mode={gmodedic[gmode]}").text
        s2 = BeautifulSoup(html2, "html.parser")
        strings2 = json.loads(str(s2))

        diffname = strings2["scores"][1]["beatmap"]["version"]
        setnum = strings2["scores"][1]["beatmap"]["beatmapset_id"]

        html3 = requests.get(f"https://osu.ppy.sh/beatmapsets/{setnum}").text
        s3 = BeautifulSoup(html3, "html.parser")

        beatmapsetbox = s3.find("script", id="json-beatmapset")
        strings3 = json.loads(str(beatmapsetbox.string))

        songname = strings3["title"]


        ranktray3 = []
        rankcount = 0

        for i in strings2["scores"]:
            rankcount = rankcount + 1
            mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
            forappend = f"{rankcount}위: {i['rank']} {i['user']['username']} {'{:,}'.format(int(i['score']))} ({mods3})"
            finfor = forappend.replace(" X ", " SS ").replace(" XH ", " SS ").replace(" SH ", " S ")
            ranktray3.append(finfor)
        startidx = (int(page) - 1) * 10
        endidx = startidx + 9
        finalstr = "\n".join(ranktray3[startidx:endidx+1])
        finalstr = f"곡명: {songname}\n" + f"난이도: {diffname}\n\n" + f"곡 랭킹({page}페이지):\n" + finalstr

        await ctx.send(finalstr)
    except:
        traceback.print_stack()
        traceback.print_exc()

def getwindow(od, dthtstring="x"):
    max3 = 20
    min3 = 50
    result = min3 + (max3 - min3) * od / 10
    result = math.floor(result) - 0.5
    
    if "ht" in dthtstring:
        result = result / 0.75
    
    if "dt" in dthtstring:
        result = result / 1.5
    

    return round(result * 100) / 100

def getpp(sr: float, fcombo: int, h100: int, h0: int, rawod: float, odmods="x"):
    try:
        if float(sr) > 20 or float(sr) < 0:
            return "-1"

        if int(fcombo) > 7000 or int(fcombo) < 1:
            return "-2"

        if int(h100) + int(h0) > int(fcombo):
            return "-3"

        if float(rawod) > 10 or float(rawod) < 0:
            return "-4"

        mycombo = fcombo - h0
        newod = float(rawod)

        if "hr" in odmods:
            newod = min(10, newod * 1.4)

        newod = round(newod, 1)

        acc = round((((h100 * 150) + ((fcombo - (h100 + h0)) * 300)) / (fcombo * 300)) * 100, 2)
        '''
        if "dt" in odmods:
            ptiming = getwindow(newod, "dt")
        elif "ht" in odmods:
            ptiming = getwindow(newod, "ht")
        else:
            ptiming = getwindow(newod)
        '''

        ptiming = getwindow(newod)

        strainVal = max(1.0, sr / 0.0075) * 5.0 - 4.0
        strainVal = math.pow(strainVal, 2) / 100000.0

        lenBonus = min(1.0, fcombo / 1500.0) * 0.1 + 1.0
        strainVal *= lenBonus

        strainVal *= math.pow(0.985, h0)

        strainVal *= min(math.sqrt(mycombo) / math.sqrt(fcombo), 1.0)

        if "hd" in odmods:
            strainVal *= 1.025
        
        if "fl" in odmods:
            strainVal *= 1.05 * lenBonus
        
        strainVal *= acc / 100

        accVal = math.pow(150.0 / ptiming, 1.1)
        accVal *= math.pow(acc / 100, 15) * 22.0
        accVal *= min(math.pow(fcombo / 1500.0, 0.3), 1.15)

        multiplier = 1.1

        if "nf" in odmods:
            multiplier *= 0.9
        
        if "hd" in odmods:
            multiplier *= 1.1
        

        res = math.pow(math.pow(strainVal, 1.1) + math.pow(accVal, 1.1), 1.0 / 1.1) * multiplier
        return round(res)
    except Exception:
        traceback.print_stack()
        traceback.print_exc()
        return "-5"

@client.command(pass_context=True)
async def 목표pp(ctx, sr: float, fcombo: int, rawod: float, destpp, odmods="x"):
    res = getpp(sr, fcombo, 0, 0, rawod, odmods)

    if res == "-1":
        await ctx.send("별점에는 0~20 범위의 실수만 입력할 수 있습니다.")
        return

    if res == "-2":
        await ctx.send("콤보에는 1~7000 범위의 정수만 입력할 수 있습니다.")
        return

    if res == "-4":
        await ctx.send("od에는 0~10 범위의 실수만 입력할 수 있습니다.")
        return

    if res == "-5":
        await ctx.send("pp 계산 중 알 수 없는 오류가 발생하였습니다.")
        return

    prevresult = ""

    for i in range(0, fcombo+1):
        res = int(getpp(sr, fcombo, i, 0, rawod, odmods))
        if res >= int(destpp):
            prevresult = "ok"
        elif res < int(destpp):
            if i == 0:
                await ctx.send("해당 조건으로는 주어진 목표 pp를 획득할 수 없습니다.")
                break
            elif prevresult == "ok":
                await ctx.send(f"계산 결과: 100 {i-1}개 이하로 풀콤보 시 {destpp}pp 이상 획득 가능")
                prevresult = ""
                break

    if prevresult == "ok":
        await ctx.send("해당 조건으로는 주어진 목표 pp를 획득할 수 없습니다.")
    
    

@목표pp.error
async def onerror23135595(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .목표pp (별 갯수) (풀콤보시 콤보 수) (논모드 기준 od) (목표 pp) (모드 조합(hr, hd, fl, nf 중 원하는 모드들을 공백 없이 이어서 작성))")
    else:
        traceback.print_stack()
        traceback.print_exc()

@client.command(pass_context=True)
async def pp계산(ctx, sr: float, fcombo: int, h100: int, h0: int, rawod: float, odmods="x"):
    res = getpp(sr, fcombo, h100, h0, rawod, odmods)

    if res == "-1":
            await ctx.send("별점에는 0~20 범위의 실수만 입력할 수 있습니다.")
            return

    if res == "-2":
        await ctx.send("콤보에는 1~7000 범위의 정수만 입력할 수 있습니다.")
        return

    if res == "-3":
        await ctx.send("100 갯수와 미스 갯수는 풀콤보 시 콤보 수보다 클 수 없습니다.")
        return

    if res == "-4":
        await ctx.send("od에는 0~10 범위의 실수만 입력할 수 있습니다.")
        return

    if res == "-5":
        await ctx.send("pp 계산 중 알 수 없는 오류가 발생하였습니다.")
        return

    await ctx.send(f"예상 획득 pp: 약 {res}pp")

@pp계산.error
async def onerror2135595(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .pp계산 (별 갯수) (풀콤보시 콤보 수) (100 갯수) (미스 갯수) (논모드 기준 od) (모드 조합(hr, hd, fl, nf 중 원하는 모드들을 공백 없이 이어서 작성))")
    else:
        traceback.print_stack()
        traceback.print_exc()

@client.command(pass_context=True)
async def pp(ctx, uid, gmode="태고", *page):
    try:
        gmodedic = {"스탠": "osu", "태고": "taiko", "캐치": "fruits", "매니아": "mania"}

        if gmode not in gmodedic.keys():
            await ctx.send("올바르지 않은 게임 모드입니다. (스탠, 태고, 캐치, 매니아 중 택일)")
            return

        uid = str(uid).replace(";", " ")

        page = list(page)

        if len(page) == 0:
            page.append("1")

        if len(page) >= 1 and str(page[0]).isdecimal(): # 모드 뒤로 아무 것도 정하지 않은 경우
            html = requests.get(f"https://osu.ppy.sh/users/{uid}/{gmodedic[gmode]}").text
            s = BeautifulSoup(html, "html.parser")
            forgetid = s.find("script", id="json-user")
            uinfobox = json.loads(str(forgetid.string))
            regex = re.compile(r"\"id\":[^,]+,")
            final1 = str(regex.findall(str(forgetid))[0])
            final2 = str(re.sub(r"[^0-9]+", "", final1)) # 평문 아이디로부터 얻어낸 유저 번호
            # print(final2)

            reqp = 0 + (10 * (int(page[0]) - 1))
            html2 = requests.get(f"https://osu.ppy.sh/users/{final2}/scores/best?mode={gmodedic[gmode]}&offset={reqp}&limit=10").text
            s2 = BeautifulSoup(html2, "html.parser")
            strings2 = json.loads(str(s2))
            # print(strings2[0])

            ranktray3 = []
            rankcount = 0 + (10 * (int(page[0]) - 1))

            ranktray3.append(f"유저명: {uid}")
            ranktray3.append(f"{gmode} 총 pp: {round(uinfobox['statistics']['pp'])}pp\n")
            ranktray3.append(f"{gmode} 개별 pp 랭킹({page[0]}페이지):")
            for i in strings2:
                if rankcount == (0 + (10 * (int(page[0]) - 1))) + 10:
                    break
                mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                convacc = round(float(i['accuracy']) * 100, 2)
                ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                rankcount = rankcount + 1
            
            finalstr = "\n".join(ranktray3)
            await ctx.send(finalstr)

        elif not str(page[0]).isdecimal():
            html = requests.get(f"https://osu.ppy.sh/users/{uid}/{gmodedic[gmode]}").text
            s = BeautifulSoup(html, "html.parser")
            forgetid = s.find("script", id="json-user")
            uinfobox = json.loads(str(forgetid.string))
            regex = re.compile(r"\"id\":[^,]+,")
            final1 = str(regex.findall(str(forgetid))[0])
            final2 = str(re.sub(r"[^0-9]+", "", final1)) # 평문 아이디로부터 얻어낸 유저 번호
            # print(final2)

            html2 = requests.get(f"https://osu.ppy.sh/users/{final2}/scores/best?mode={gmodedic[gmode]}&offset=0&limit=50").text
            s2 = BeautifulSoup(html2, "html.parser")
            strings2 = json.loads(str(s2))

            html3 = requests.get(f"https://osu.ppy.sh/users/{final2}/scores/best?mode={gmodedic[gmode]}&offset=50&limit=50").text
            s3 = BeautifulSoup(html3, "html.parser")
            strings3 = json.loads(str(s3))
            # print(strings2[0])

            ranktray3 = []
            rankcount = 0

            ranktray3.append(f"유저명: {uid}")
            ranktray3.append(f"{gmode} 총 pp: {round(uinfobox['statistics']['pp'])}pp\n")
            ranktray3.append(f"{gmode} 개별 pp 랭킹 검색 결과:")

            if page[0] == "n":
                page = []

            page = [x.upper() for x in page]

            for i in strings2:
                if(page[0] in ["HR", "SD", "PF", "NC", "HD", "FL", "DT", "HT", "NF", "EZ"]):
                    if(Counter(i['mods']) == Counter(page)):
                        mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                        convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                        convacc = round(float(i['accuracy']) * 100, 2)
                        ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                else:
                    if (((page[0] in str(i['beatmapset']['title']).upper()) or (page[0] in str(i['beatmap']['version']).upper()) or (page[0] in str(i['beatmapset']['artist']).upper()))):
                        mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                        convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                        convacc = round(float(i['accuracy']) * 100, 2)
                        ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                

                '''
                if ("%" not in page and ((page.lower() in str(i['beatmapset']['title']).lower()) or (page.lower() in str(i['beatmap']['version']).lower()) or (page.lower() in str(i['beatmapset']['artist']).lower()))):
                    mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                    convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                    convacc = round(float(i['accuracy']) * 100, 2)
                    ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                if ("%" in page and (round(float(i['accuracy']) * 100, 2) >= round(float(page.replace("%", "")), 2))):
                    mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                    convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                    convacc = round(float(i['accuracy']) * 100, 2)
                    ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                '''
                
                rankcount = rankcount + 1

            for i in strings3:
                if(page[0] in ["HR", "SD", "PF", "NC", "HD", "FL", "DT", "HT", "NF", "EZ"]):
                    if(Counter(i['mods']) == Counter(page)):
                        mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                        convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                        convacc = round(float(i['accuracy']) * 100, 2)
                        ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                else:
                    if (((page[0] in str(i['beatmapset']['title']).upper()) or (page[0] in str(i['beatmap']['version']).upper()) or (page[0] in str(i['beatmapset']['artist']).upper()))):
                        mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                        convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                        convacc = round(float(i['accuracy']) * 100, 2)
                        ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                

                '''
                if ("%" not in page and ((page.lower() in str(i['beatmapset']['title']).lower()) or (page.lower() in str(i['beatmap']['version']).lower()) or (page.lower() in str(i['beatmapset']['artist']).lower()))):
                    mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                    convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                    convacc = round(float(i['accuracy']) * 100, 2)
                    ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                if ("%" in page and (round(float(i['accuracy']) * 100, 2) >= round(float(page.replace("%", "")), 2))):
                    mods3 = "None" if ', '.join(i['mods']) == "" else ', '.join(i['mods'])
                    convrank = i['rank'].replace("X", "SS").replace("XH", "SS").replace("SH", "S")
                    convacc = round(float(i['accuracy']) * 100, 2)
                    ranktray3.append(f"{rankcount + 1}위: ({convrank} {convacc}%) {i['beatmapset']['title']} [{i['beatmap']['version']}] - {round(i['pp'])}pp ({mods3})")
                '''
                rankcount = rankcount + 1
            
            finalstr = "\n".join(ranktray3)
            await ctx.send(finalstr)
    except discord.errors.HTTPException:
        traceback.print_stack()
        traceback.print_exc()
        await ctx.send("검색 결과가 너무 많습니다. 조건을 바꿔 다시 검색해보시기 바랍니다.")
    except Exception:
        traceback.print_stack()
        traceback.print_exc()
        await ctx.send("정보 취득 중 오류가 발생하였습니다.")

@pp.error
async def onerror213595(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .pp (아이디(공백은 ;로 입력)) (게임 모드(스탠, 태고, 캐치, 매니아 중 택일)) (페이지 or 검색어(곡명, 가수명, 난이도명) or 모드 조합(두 글자 약칭 사용 / 띄어쓰기로 구분))")
    else:
        traceback.print_stack()
        traceback.print_exc()

@client.command(pass_context=True)
async def 숫자야구(ctx):
    global ansnum, baseballremains

    nowgame = getnowgame()

    if nowgame != -1:
        await ctx.send(f"진행 중인 {nowgame} 있습니다.")
    elif nowgame == -1:
        ansnum = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
        erk = str(ansnum[0]) + str(ansnum[1]) + str(ansnum[2]) + str(ansnum[3])
        baseballremains = 25
        await ctx.send(f"숫자 야구가 시작되었습니다. (도전 기회: 25회)")


@client.command(pass_context=True)
async def 출제(ctx, tag, mode="노말"):
    global hintmul, nowauto, autouid, nowdiff

    nowgame = getnowgame()

    if nowauto:
        await ctx.send("현재 자동 출제 상태입니다.")
        return

    if nowgame != -1:
        await ctx.send(f"진행 중인 {nowgame} 있습니다.")
    elif nowgame == -1:

        if tag == "테스트":
            await ctx.send("선택할 수 없는 주제입니다.")
            return
        
        if mode == "노말":
            hintmul = 300
            nowdiff = "normal"
            await startgamebytag(tag, ctx, "normal")
        elif mode == "이지":
            hintmul = 300
            nowdiff = "easy"
            await startgamebytag(tag, ctx, "easy")
        else:
            await ctx.send("존재하지 않는 부가 모드입니다.")

@출제.error
async def onerror3(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .출제 (주제)")

@client.command(pass_context=True)
async def 콤보테스트(ctx, combo, mtp=1.3):
    result = 300 + (300 * ((float(mtp) ** max(0, int(combo)) * 6 * 1) / 25))
    await ctx.send(f"{int(combo)+1}연속: {result}점")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        emj = client.get_emoji(721968301433159732)
        await ctx.message.add_reaction(emj)

@client.command(pass_context=True)
async def 포기(ctx): # 통합 포기 명령어
    # , clstimer
    global timer, htimer1, htimer2, jqnowuser, combodic, hintmul, nowauto, tray

    # trigger = str(ctx.message.author.id)
    ngame = getnowgame()

    
    if ngame == "자음 퀴즈가":
        if str(ctx.message.author.id) != jqnowuser:
            await ctx.send("출제자만 포기할 수 있습니다.")
            return

        timer.cancel()
        htimer1.cancel()
        htimer2.cancel()
        combodic[str(ctx.message.author.id)] = 0
        hintmul = 300
        
        await ctx.send(f"자음 퀴즈를 포기하였습니다. (정답: {tray})")
        tray = ""
        if nowauto:
            await startgamebytag(autotag, autoctx, "normal")
        return

    # alreadyqueue, fchr, practag, wmax, wnow, global timertray, nowuser1
    
    global mtimer999, judic

    if ngame == "주관식 문제가":
        mtimer999.cancel()
        await ctx.send(f"주관식 문제를 포기하였습니다. (정답: {judic[1]})")
        judic = []
        return

    if ngame == "숫자 야구가":
        global ansnum
        
        await ctx.send(f"숫자 야구를 포기하였습니다. (정답: {str(ansnum[0]) + str(ansnum[1]) + str(ansnum[2]) + str(ansnum[3])})")
        ansnum.clear()
        return

    await ctx.send("진행 중인 게임이 없습니다.")

    
# bhash1 = hashlib.sha256(b1.encode()).hexdigest()
def getone(a: list, expt="-1"):
    aa = a.copy()
    if expt != "-1":
        aa.remove(aa[int(expt)])
        return random.sample(aa, 1)[0]
    else:
        return random.sample(aa, 1)[0]


@client.command(pass_context=True)
async def 아무말(ctx, t: str):
    tt = t.replace(";", " ")
    n = ["출석부", "스피커", "연필", "샤프", "볼펜", "외장하드", "컴퓨터", "스마트폰", "키보드", "마우스", "형광등", "지우개", "간판", "나침반", "의자", "책상", "문제집", "이어폰", "방석", "침대", "쇼파", "건전지", "창문", "텔레비전", "서랍", "시계", "자전거", "우표", "꽃병", "에어컨", "선풍기", "달력", "귀걸이", "목걸이", "책장", "옷장", "계산기", "마이크", "앨범", "체크카드", "신용카드", "통장", "장갑", "모자", "삽", "화분", "줄넘기", "뜀틀", "거울", "머리띠", "머리끈", "학생증", "공유기", "커튼", "체온계", "자물쇠", "열쇠", "도어락", "망원경", "이불", "소나무", "벽지", "그래픽카드", "교과서", "잡지", "야구공", "축구공", "농구공", "색연필", "카메라", "모자", "안경", "액자", "피아노", "바이올린", "첼로", "리코더", "필통", "빗", "열쇠고리", "엘리베이터", "에스컬레이터", "노트북", "메인보드", "오르골", "탁구공", "체중계", "액정보호필름", "프린터", "스마트폰 거치대", "보조배터리", "CPU", "USB 허브", "마우스패드", "커피메이커", "헤어드라이어", "SSD", "물감", "팔레트", "도화지", "이젤", "울타리", "레이저 포인터", "텐트", "무전기", "만년필", "색종이", "클립", "화이트보드", "칠판", "털실", "현미경", "잠망경", "컴퍼스", "버니어 캘리퍼스", "각도기", "돋보기", "주사위", "우산", "파라솔", "바람막이", "독서대", "벼루", "수정테이프", "책갈피", "책받침", "부채", "붓", "캔버스", "스케치북", "스카치테이프", "골판지", "포스트잇", "원고지", "하드보드지", "컴퓨터 사인펜", "수수깡", "지갑", "명함", "기름종이", "알코올 램프", "저울", "드럼", "실로폰", "오르간", "오보에", "콘트라베이스", "랜턴", "물안경", "튜브", "쇼핑카트", "청진기", "샤프심", "영수증", "노트북 쿨링패드", "물총", "패딩", "분필", "보드마카", "주판", "영사기", "스크린도어", "순간접착제", "물로켓", "낙하산", "헬리콥터", "항공모함", "도장", "신디사이저", "오보에", "옷걸이", "분수대", "정글짐", "미끄럼틀", "평행봉", "보풀제거기", "사다리", "스노보드", "스케이트보드", "골프공", "벨트", "잠자리채", "에코백", "크리스마스 트리", "라디오", "사포", "지점토", "찰흙", "철사", "디퓨저", "우체통", "물레방아", "공중전화", "셀카봉", "레이더", "확성기", "에어 서큘레이터", "가로등", "피규어", "벽난로", "무빙워크", "눈사람", "실린더", "스포이드", "누전차단기", "금고", "골드바", "스캐너", "USB 메모리", "기뢰", "어뢰", "ICBM", "비행기", "전투기", "소나", "분젠 버너", "만보기", "하드디스크", "캣타워", "CCTV", "헤드셋", "시소", "롤러코스터", "관람차", "오카리나", "비올라", "하프", "트럼펫", "핸드벨", "전봇대", "제본기", "A4용지", "고무동력기", "NAS", "네오디뮴 자석", "막대자석", "진동벨", "ATM", "지진계", "글루건", "지게차", "포크레인", "연필깎이", "지구본", "런닝머신", "라디에이터", "메트로놈", "팩스", "인공위성", "다리미", "스탠드", "잠수함", "셋톱박스", "풍선", "돗자리"]
    d = ["사온", "놓아둔", "고친", "빌려준", "모은", "찾은", "보낸", "부탁한", "떨어뜨린", "디자인한", "찢어버린", "녹인", "치워버린", "얼린", "부숴버린", "조립한"]
    h1 = ["황홀하고", "부드럽고", "딱딱하고", "둥글고", "파랗고", "크고", "작고", "두껍고", "투명하고", "가볍고", "시원하고", "따뜻하고", "하얗고", "화려하고", "아름답고", "진하고"]
    h2 = ["황홀한", "부드러운", "딱딱한", "둥근", "파란", "큰", "작은", "두꺼운", "투명한", "가벼운", "시원한", "따뜻한", "하얀", "화려한", "아름다운", "진한"]
    c = ["호노카", "우미", "코토리", "하나요", "마키", "에리", "치카", "요우", "리코", "하나마루", "요시코", "루비", "마리", "카난", "시즈쿠", "아유무"]
    bhash1 = hashlib.sha1(tt.encode("utf-8")).hexdigest()

    # tmp = random.randrange(0, 16)
    finalc1 = c[int(bhash1[0], 16)] # 이름1
    finalc2 = c[int(bhash1[1], 16)] # 이름2
    finald = d[int(bhash1[2], 16)] # 동사
    finalh1 = h1[int(bhash1[3], 16)] # 형용사1
    finalh2 = h2[int(bhash1[4], 16)] # 형용사2
    finaln = n[int(bhash1[5:7], 16)] # 명사
    # random.randrange(0, 2)
    tmp1 = "과" if finalc1 == "카난" else "와"
    tmp2 = "이" if finalc2 == "카난" else "가"
    await ctx.send(f"{finalc1}{tmp1} {finalc2}{tmp2} {finald} {finalh1} {finalh2} {finaln}")

@client.command(pass_context=True)
async def 랭킹초기화(ctx):
    if str(ctx.message.author.id) != "630348273730846760":
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")
        return

    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")

    try:
        with conn.cursor() as cs:
            dq = "delete from jqranking;"
            cs.execute(dq)
            conn.commit()
            for i in ctx.message.guild.members:
                if "코딩하는" not in str(i):
                    q = f"insert ignore into jqranking(dispname, mnum, score, maxcb) value ('{str(i)}', '{str(i.id)}', 0, 0);"
                    cs.execute(q)
                    conn.commit()
            await ctx.send("랭킹을 초기화하였습니다.")
    finally:
        conn.close()

@client.command(pass_context=True)
async def 내점수(ctx):

    u = str(ctx.message.author.id)
    stray = "{:,}".format(getrinfo(u, "score"))


    ranktray = 0
    nextuser = None

    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")

    try:
        with conn.cursor() as cs:
            q = f"select dispname, score from jqranking order by score desc;"
            cs.execute(q)
            row = cs.fetchall()

            rankcount = 0

            for i in row:
                rankcount += 1
                if str(ctx.message.author) == i[0]:
                    if rankcount != 1:
                        nextuser = getfromrank(rankcount - 1)
                        ranktray = rankcount
                    elif rankcount == 1:
                        nextuser = getfromrank(rankcount + 1)
                        ranktray = rankcount
                    break
                
            
    finally:
        conn.close()

    if ranktray != 1:
        await ctx.send(f"당신의 점수는 {stray}점입니다. (현재 {ranktray}위, {ranktray - 1}위와의 차이: -{nextuser[1] - getrinfo(u, 'score')}점)")
    else:
        await ctx.send(f"당신의 점수는 {stray}점입니다. (현재 {ranktray}위, 2위와의 차이: +{getrinfo(u, 'score') - nextuser[1]}점)")

@client.command(pass_context=True)
async def 점수설정(ctx, d, score):
    if str(ctx.message.author.id) != "630348273730846760":
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")
        return
    
    res = setscore(d, score)

    if res == "2":
        await ctx.send(f"해당 유저의 점수를 {score}점으로 설정하였습니다.")
    else:
        await ctx.send("점수 설정 중 오류가 발생하였습니다.")

    

@client.command(pass_context=True)
async def 랭킹(ctx):
    res = getallranking()
    await ctx.send(res)



@client.command(pass_context=True)
async def 콤보초기화(ctx):
    global combodic

    if str(ctx.message.author.id) != "630348273730846760":
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")
        return

    combodic = {}
    await ctx.send("콤보를 초기화하였습니다.")

@client.command(pass_context=True)
async def off(ctx):
    if str(ctx.message.author.id) != "630348273730846760":
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")
        return
    
    await ctx.send("봇 가동을 중단합니다.")
    await client.close()

def getpop(kf, sptword):
    q = f"SELECT * FROM gichoingu WHERE wname='{kf}';" # 완전 일치 검색 시도

    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")
    try:
        with conn.cursor() as cs:
            cs.execute(q)
            rows = cs.fetchall()
            if cs.rowcount == 1:
                return [rows[0][0], rows[0][1]]

            q = f"SELECT * FROM gichoingu WHERE wname REGEXP ' {kf}$' AND wname LIKE '%{sptword}%';"
            cs.execute(q)
            rows = cs.fetchall()
            if cs.rowcount == 1:
                return [rows[0][0], rows[0][1]]

            q = f"SELECT * FROM gichoingu WHERE wname REGEXP ' {kf}[시군구읍면동가]{{1}}$' AND wname LIKE '%{sptword}%';"
            cs.execute(q)
            rows = cs.fetchall()
            if cs.rowcount == 1:
                return [rows[0][0], rows[0][1]]

            

            return "notfound"
    finally:
        conn.close()

def getpop2(kf, ks, kt):
    # 시, 군, 구를 뗀 이름 부분만을 입력했다고 먼저 가정
    q = f"select * from gichoingu where wname like '%{kf}';"

    if ks != "not":
        q = f"select * from gichoingu where wname like '%{kf}' and wname like '%{ks}%';"

    conn = pymysql.connect(host="119.193.130.207", user="root", password="96321h", db="korwords", charset="utf8")
    try:
        with conn.cursor() as cs:
            cs.execute(q)
            rows = cs.fetchall()
            if cs.rowcount == 1:
                return [rows[0][0], rows[0][1]]
            elif cs.rowcount == 0:
                return "-2" # 검색 결과 없음
            elif cs.rowcount > 1:
                if ks == "not" and kt == "n":
                    return "-3"
                elif ks != "not" and kt == "n":
                    return "-5"
                elif ks != "not" and kt != "n":
                    q = f"select * from gichoingu where wname like '% {kf}' and wname like '%{ks}%';"
                    cs.execute(q)
                    rows = cs.fetchall()
                    if cs.rowcount == 1:
                        return [rows[0][0], rows[0][1]]
                    elif cs.rowcount > 1:
                        return "-7"
                    else:
                        return "-2"

    finally:
        conn.close()

@client.command(pass_context=True)
async def 인구(ctx, sf, ss=""):
    res = getpop(sf, ss)

    if res == "notfound":
        await ctx.send("검색 결과가 없거나 2건 이상입니다. 검색어가 올바른지 재확인하거나 보조 키워드를 사용해보시기 바랍니다.")
        return

    embed1 = discord.Embed(title="인구 정보", color=0x0000ff)
    embed1.set_footer(text="2020년 10월 기준")
    finalname = res[0]
    finalpop = res[1]
    embed1.add_field(name="명칭", value=finalname, inline=True)
    embed1.add_field(name="인구(명)", value=f"{finalpop}", inline=True)
    await ctx.send(embed=embed1)


@인구.error
async def onerror355991(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .인구 (키워드) (보조 키워드(선택))")

async def mclose(time, dest):
    global gaekdic

    await asyncio.sleep(time)
    
    await dest.send(f"시간 초과로 문제가 종료되었습니다. (정답: {gaekdic[6]}번)")
    gaekdic = []

async def mclose2(time, dest):
    global judic

    await asyncio.sleep(time)
    
    await dest.send(f"시간 초과로 문제가 종료되었습니다. (정답: {judic[1]})")
    judic = []

@client.command(pass_context=True)
async def 사진객관식(ctx, q, a1, a2, a3, a4, a5, ra, t, url):
    global gaekdic, mtimer999, remains, channel7, fortestch

    # 692279080468480020 - 봇테스트채널

    # 692212990631739425 - 잡담채널

    if ctx.message.guild != None:
        await ctx.send("봇과의 개인 메시지를 통해서만 출제할 수 있습니다.")
    else:
        nowgame = getnowgame()
        if nowgame != -1:
            await ctx.send(f"진행 중인 {nowgame} 있습니다.")
            return

        remains = 2

        mtimer999 = client.loop.create_task(mclose(float(t), fortestch))
        gaekdic = [q.replace(";", " "), a1.replace(";", " "), a2.replace(";", " "), a3.replace(";", " "), a4.replace(";", " "), a5.replace(";", " "), ra, float(t), url]
        await fortestch.send(f"{gaekdic[8]}\n\n객관식> {gaekdic[0]} (제한 시간: {int(gaekdic[7])}초)\n1) {gaekdic[1]}\n2) {gaekdic[2]}\n3) {gaekdic[3]}\n4) {gaekdic[4]}\n5) {gaekdic[5]}")
        await ctx.send("성공적으로 출제되었습니다.")

@사진객관식.error
async def onerroraaaaa3559791(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .사진객관식 (문제) (1번 선택지) (2번 선택지) (3번 선택지) (4번 선택지) (5번 선택지) (정답 번호) (제한시간(초)) (사진 URL)\n주의: 띄어쓰기는 ;로 구분")


@client.command(pass_context=True)
async def 지문객관식(ctx, q, a1, a2, a3, a4, a5, ra, t, *at):
    global gaekdic, mtimer999, remains, channel7, fortestch

    # 692279080468480020 - 봇테스트채널

    # 692212990631739425 - 잡담채널

    if ctx.message.guild != None:
        await ctx.send("봇과의 개인 메시지를 통해서만 출제할 수 있습니다.")
    else:
        nowgame = getnowgame()
        if nowgame != -1:
            await ctx.send(f"진행 중인 {nowgame} 있습니다.")
            return

        remains = 2

        mtimer999 = client.loop.create_task(mclose(float(t), fortestch))
        gaekdic = [q.replace(";", " "), a1.replace(";", " "), a2.replace(";", " "), a3.replace(";", " "), a4.replace(";", " "), a5.replace(";", " "), ra, float(t), " ".join(at)]
        await fortestch.send(f"> **다음 글을 읽고 질문에 답하여라.**\n```\n{gaekdic[8]}\n```\n객관식> {gaekdic[0]} (제한 시간: {int(gaekdic[7])}초)\n1) {gaekdic[1]}\n2) {gaekdic[2]}\n3) {gaekdic[3]}\n4) {gaekdic[4]}\n5) {gaekdic[5]}")
        await ctx.send("성공적으로 출제되었습니다.")

@지문객관식.error
async def onerroraaa3559791(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .지문객관식 (문제) (1번 선택지) (2번 선택지) (3번 선택지) (4번 선택지) (5번 선택지) (정답 번호) (제한시간(초)) (지문)\n주의: 지문 이외에는 ;로 띄어쓰기 구분")

@client.command(pass_context=True)
async def 객관식(ctx, q, a1, a2, a3, a4, a5, ra, t):
    global gaekdic, mtimer999, remains, channel7, fortestch

    # 692279080468480020 - 봇테스트채널

    # 692212990631739425 - 잡담채널

    if ctx.message.guild != None:
        await ctx.send("봇과의 개인 메시지를 통해서만 출제할 수 있습니다.")
    else:
        nowgame = getnowgame()
        if nowgame != -1:
            await ctx.send(f"진행 중인 {nowgame} 있습니다.")
            return

        remains = 2

        mtimer999 = client.loop.create_task(mclose(float(t), fortestch))
        gaekdic = [q.replace(";", " "), a1.replace(";", " "), a2.replace(";", " "), a3.replace(";", " "), a4.replace(";", " "), a5.replace(";", " "), ra, float(t)]
        await fortestch.send(f"객관식> {gaekdic[0]} (제한 시간: {int(gaekdic[7])}초)\n1) {gaekdic[1]}\n2) {gaekdic[2]}\n3) {gaekdic[3]}\n4) {gaekdic[4]}\n5) {gaekdic[5]}")
        await ctx.send("성공적으로 출제되었습니다.")

@객관식.error
async def onerror3559791(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .객관식 (문제) (1번 선택지) (2번 선택지) (3번 선택지) (4번 선택지) (5번 선택지) (정답 번호) (제한시간(초))\n주의: 띄어쓰기는 ;로 가능")

@client.command(pass_context=True)
async def tts(ctx, *args):
    if ctx.message.author.is_on_mobile() == False:
        await ctx.send("모바일에서만 사용 가능한 명령어입니다.")
        return

    tray = []
    for a in args:
        tray.append(a)
    await ctx.send(" ".join(tray), tts=True)

@tts.error
async def onerro3r3559791(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .tts (내용)")


@client.command(pass_context=True)
async def 색변경(ctx, ccode):
    triggerrole = ctx.message.author.top_role
    regex = re.compile(r"[a-fA-F0-9]{6}")
    pccode = regex.findall(ccode)
    samples = ["a", "b", "c", "d", "e", "f", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    selected = [random.choice(samples) for i in range(6)]

    if ccode == "랜덤":
        rcolor = "".join(selected)
        await triggerrole.edit(reason=None, colour=discord.Colour(int(rcolor, 16)))
        await ctx.send(f"닉네임 색상을 #{rcolor}로 변경하였습니다.")
        return

    if len(ccode) != 6:
        await ctx.send("유효하지 않은 색상 코드입니다.")
        return

    if len(pccode) != 1:
        await ctx.send("유효하지 않은 색상 코드입니다.")
        return

    if len(pccode[0]) != 6:
        await ctx.send("유효하지 않은 색상 코드입니다.")
        return
    await triggerrole.edit(reason=None, colour=discord.Colour(int(ccode, 16)))
    await ctx.send(f"닉네임 색상을 #{ccode}로 변경하였습니다.")

@색변경.error
async def onerror355979551(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .색변경 (색상코드(# 없이 6자리) 또는 '랜덤')")

@client.command(pass_context=True)
async def 주관식(ctx, q, a, t):
    global judic, mtimer999, remains, channel7, fortestch

    # 692279080468480020 - 봇테스트채널

    # 692212990631739425 - 잡담채널

    if ctx.message.guild != None:
        await ctx.send("봇과의 개인 메시지를 통해서만 출제할 수 있습니다.")
    else:
        nowgame = getnowgame()
        if nowgame != -1:
            await ctx.send(f"진행 중인 {nowgame} 있습니다.")
            return
        try:
            mtimer999 = client.loop.create_task(mclose2(float(t), fortestch))
            judic = [q.replace(";", " "), a.replace(";", " "), float(t)]
            await fortestch.send(f"주관식> {judic[0]} (제한 시간: {int(judic[2])}초)")
            await ctx.send("성공적으로 출제되었습니다.")
        except:
            traceback.print_stack()
            traceback.print_exc()

@주관식.error
async def onerror35359791(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .주관식 (문제) (답) (제한 시간(초))\n주의:띄어쓰기는 ;로 가능.")

@client.command(pass_context=True)
async def 단어추가(ctx, word, tag):
    passport = str(ctx.message.author.id)
    result = addword(word, tag, passport)

    if result == "2":
        await ctx.send("단어가 성공적으로 추가되었습니다.")
    elif result == "-1":
        await ctx.send("존재하지 않는 주제입니다.")
    elif result == "-2":
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")

@단어추가.error
async def onerr3or35359791(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .단어추가 (단어) (주제)")



@client.command(pass_context=True)
async def 단어수정(ctx, pw, nw, tag):
    passport = str(ctx.message.author.id)
    result = modword(tag, pw, nw, passport)

    if result == "2":
        await ctx.send("단어가 성공적으로 수정되었습니다.")
    if result == "222":
        await ctx.send("단어가 성공적으로 삭제되었습니다.")
    elif result == "-1":
        await ctx.send("존재하지 않는 주제입니다.")
    elif result == "-2":
        await ctx.send("이 명령어를 사용할 권한이 없습니다.")
    elif result == "999":
        await ctx.send("수정할 단어가 검색되지 않았습니다.")
    elif result == "99999":
        await ctx.send("삭제할 단어가 검색되지 않았습니다.")

@단어수정.error
async def oxnerr3or35359791(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("사용법: .단어수정 (수정할 단어) (수정 후 단어(- 입력 시 삭제)) (주제)")

'''
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
'''

clocksound.start()

client.run(token)