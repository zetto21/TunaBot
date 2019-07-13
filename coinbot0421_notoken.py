import discord
import asyncio
import random
import datetime
import os
import requests
from bs4 import BeautifulSoup
import bs4
from pyowm import OWM
from difflib import SequenceMatcher
import aiohttp

token = "디스코드 봇 토큰"
#NEWS = 3
'''!참치봇 공지 < :loudspeaker: **2019-04-04 업데이트 내역** :loudspeaker: >
```ini
[ 추가 된 기능 ]
- 참치봇 나무위키 <검색어> - 나무위키에서 검색 (BGM봇 코드 참고)
- 참치봇 태그 <사진 파일> - 사진을 인식하고 태그를 생성
[ 수정 된 기능 ]
- 참치봇 검색 <검색어> -> 참치봇 블로그 <검색어>
- 참치봇 공지의 우선순위 채널이름 변경
```'''
news = ["```19/03/30 충격실화, 참치봇이 이상한 테스트 메세지를 보내...```", "```19/03/30 보상으로 원하는 기능과 도움을 주신 서버에 이름 추가...```", "```19/03/27 참치봇, 이제 정보충의 시대로...```"]
embed_color = 0x141464
app = discord.Client()
API_key = 'OWM API키'
owm = OWM(API_key)
version = "v0421"
embed_footer = "참치봇 | "
logo = "https://cdn.discordapp.com/attachments/535391660138299395/543409080551735314/coinbot_logo.png"
path = "C:/Users/juha/Desktop/coinbot"
wise_saying = ["```자신의 몸, 정신, 영혼에 대한 자신감이야말로 새로운 모험, 새로운 성장 방향, 새로운 교훈을 계속 찾아나서게 하는 원동력이며, 바로 이것이 인생이다.```\n**- 오프라 원프리**",
               "```접대의 비결은 다음과 같다. 손님을 환대하고 마음을 편안하게 하라. 진심으로 그렇게 하면, 나머지는 일사천리다.```\n**- 바바라 홀**",
               "```자존심은 강력한 마약이지만, 자가면역 체계에는 별 도움이 되지 않는다.```\n**- 스튜어스 스티븐스**",
               "```너 자신을 알라.```\n**- 소크라테스**",
               "```나를 알고 적을 알면 백전백승이다.```\n**- 나폴레옹**",
               "```죽느냐, 사느냐 그것이 문제로다!```\n**- 햄릿**",
               "```상상력이 지식보다 중요하다.```\n** 아인슈타인**",
               "```자유와 정의 다음으로 중요한 것은 대중 교육인데, 대중 교육 없이는 자유도 정의도 영원히 유지될 수 없다.```\n**- 제임스 A. 가필드**",
               "```교육은 양날의 칼과 같다. 제대로 다루지 못하면 위험한 용도로 쓰일 수 있다.```\n**- 우 팅-팡**",
               "```나는 모든 논리적 잣대로 따져보았을 때, 절대 영화 배우가 되지 말았어야 하는 배우라는 특이성을 갖고 있는 듯 있다. 내 경력의 모든 단계에서 나는 경험이 부족했다.```\n**- 오드리 햅번**",
               "```친구라면 친구의 결점을 참고 견뎌야 한다.```\n**- 셰익스피어**"]
               

def embed_text(title, description):
    now = datetime.datetime.now()
    embed = discord.Embed(title=title, description=description, color=embed_color)
    if now.hour >= 13:
        pmhour = str(now.hour-12)
        embed_time = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | 오후" + pmhour + ":" + str(now.minute) + ":" + str(now.second)
    else:
        amhour = str(now.hour)
        embed_time = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일 | 오전" + amhour + ":" + str(now.minute) + ":" + str(now.second)
    footer = embed_footer + embed_time
    embed.set_footer(text=footer, icon_url=logo)
    return embed

@app.event
async def on_ready():
    await app.change_presence(game=discord.Game(name=(version+" | "+"참치봇 도움말"), type=0))
    print("정상적으로 로그인되었습니다")
    print(app.user.name)
    print("v"+version)
    print(app.user.id)
    print("=========================")

@app.event
async def on_message(message):
    if message.content.startswith("참치봇 랜덤문자"):
        channel = message.channel
        random_len = len(message.content[9:].split())
        if random_len == 0 or random_len == 1:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **랜덤문자 명령어는 최소 2개 이상의 인수가 필요합니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
        else:
            random_text = random.choice(message.content[9:].split(" "))
            embed = embed_text("**TUNA BOT - 랜덤문자**", (":capital_abcd: "+str(random_len)+"개의 문자중 선택된 문자 -\n```"+random_text+"```"))
            await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 계산"):
        channel = message.channel
        math = message.content[7:]
        if math == "":
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **계산 명령어는 계산식이 필요합니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
        elif len(message.mentions) >= 1 or len(message.role_mentions) >= 1 or len(message.channel_mentions) >= 1:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **계산 명령어의 계산식이 올바르지 않습니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
        else:
            mathtext = ""
            allowed = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ".", "+", "-", "*", "/", "(", ")"]
            for i in math:
                if i in allowed:
                    mathtext += i
                else:
                    mathtext += ""
            try:
                value = eval(mathtext)
                embed = embed_text("**TUNA BOT - 계산**",(":1234: **"+mathtext+"**식의 결과 -\n```"+str(value)+"```"))
                await app.send_message(channel, embed=embed)
            except:
                embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **계산 명령어의 계산식이 올바르지 않습니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
                await app.send_message(channel, embed=embed)

    elif message.content == "참치봇 멜론":
        channel = message.channel
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        url = "https://www.melon.com/chart/index.htm"
        res = requests.get(url, headers = header)
        html = res.text
        bs = bs4.BeautifulSoup(html, 'html.parser')
        title = bs.select('#lst50 > td > div > div > div.ellipsis.rank01 > span > a')
        artist = bs.select('#lst50 > td > div > div > div.ellipsis.rank02 > span')
        titles = {}
        artists = {}
        for x in range(0, 20):
            titles[x+1] = title[x].text
            artists[x+1] = artist[x].text
        time = bs.select('#real_conts > div.multi_row > div.calendar_prid > span.yyyymmdd > span')[0].text + ". " + bs.select('#real_conts > div.multi_row > div.calendar_prid > span.hhmm > span')[0].text
        embed = embed_text("**TUNA BOT - 멜론**", ("<:kakaomelon:565142037150826537> "))
        desc = ""
        for i in range(0, 20):
            desc += str(i+1) + "위 **" + titles[i+1] + " - " + artists[i+1] + "**\n"
            embed = embed_text("**TUNA BOT - 멜론**", ("<:kakaomelon:565142037150826537> "+time+"기준\n"+desc))
        await app.send_message(channel, embed=embed)

    elif message.content == "참치봇 영화":
        channel = message.channel
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
        url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn"
        res = requests.get(url, headers = header)
        html = res.text
        bs = bs4.BeautifulSoup(html, 'html.parser')
        title = bs.select("#old_content > table > tbody > tr > td.title > div > a")
        titles = {}
        for x in range(0, 20):
            titles[x+1] = title[x].text
        embed = embed_text("**TUNA BOT - 영화**", ("<:kakaomelon:565142037150826537> "))
        desc = ""
        for i in range(0, 20):
            desc += str(i+1) + "위 **" + titles[i+1] + "**\n"
        embed = embed_text("**TUNA BOT - 영화**", (":movie_camera: **1주일 간의 영화 순위 -**\n"+desc))
        await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 타이머"):
        channel = message.channel
        if len(message.content[8:].split()) == 0:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **타이머 명령어는 1~2개의 인수가 필요합니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
        else:
            time = message.content[8:].split()[0]
            if len(message.content[8:].split()) >= 2:
                reason = message.content[8:].split()[1]
            else:
                reason = "사유 없음"
            try:
                time = int(time)
                embed = embed_text("**TUNA BOT - 타이머**", (":alarm_clock: **"+reason+" | "+str(time)+"초**(이)라는 타이머가 등록되었습니다."))
                await app.send_message(channel, embed=embed)
                await asyncio.sleep(time)
                try:
                    embed = embed_text("**TUNA BOT - 타이머**", (":alarm_clock: " + reason))
                    await app.send_message(channel, embed=embed)
                except:
                    embed = embed_text("**TUNA BOT - 타이머**", (":alarm_clock: " + reason))
                    await app.send_message(message.author, embed=embed)
            except:
                embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **계산 명령어의 시간(초)는 숫자여야만 합니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
                await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 나무위키"):
        channel = message.channel
        a = message.content[9:]
        title = "http://namu.wiki/w/" + a.replace(" ", "%20")
        async with aiohttp.ClientSession() as session:
            async with session.get(title) as r:
                if r.status == 404:
                    embed = embed_text("**TUNA BOT - 나무위키**",("<:namuwiki:563297655757733888> **" + a + "**에 대한 나무위키 검색결과가 없습니다."))
                    await app.send_message(channel, embed=embed)
                else:
                    data = await r.text()
                    soup = BeautifulSoup(data, "html.parser")
                    d = soup.find("div", {"class": "wiki-inner-content"}).text
                    content = d[:200]
                    embed = embed_text("**TUNA BOT - 나무위키**",("<:namuwiki:563297655757733888> **" + a + "**에 대한 나무위키 검색결과 -\n" + content + "...\n\n[[ 자세히 보기 ]]("+title+")"))
                    await app.send_message(channel, embed=embed)

    #elif message.content.startswith("참치봇 유튜브"):
        #channel = message.channel
        #a = message.content[8:]
        #url = "https://www.youtube.com/results?search_query=" + a.replace(" ", "%20") + "&sp=EgIQAQ%253D%253D"
        #res = requests.get(url)
        #html = res.text
        #bs = bs4.BeautifulSoup(html, 'html.parser')
        #titles = {}
        #for x in range(0, 10):
        #    titles[x] = bs.select("#video-title")[0].text
        #print(titles)

    elif message.content.startswith("참치봇 위키백과"):
        channel = message.channel
        a = message.content[9:]
        title = "https://ko.wikipedia.org/wiki/" + a.replace(" ", "%20")
        async with aiohttp.ClientSession() as session:
            async with session.get(title) as r:
                if r.status == 404:
                    embed = embed_text("**TUNA BOT - 위키백과**",("<:wikipedia:565552985896255488> **" + a + "**에 대한 위키백과 검색결과가 없습니다."))
                    await app.send_message(channel, embed=embed)
                else:
                    data = await r.text()
                    soup = BeautifulSoup(data, "html.parser")
                    d = soup.find("div", {"class": "mw-content-ltr", "id":"mw-content-text", "lang":"ko", "dir":"ltr"}).text
                    content = d[:200]
                    embed = embed_text("**TUNA BOT - 위키백과**",("<:wikipedia:565552985896255488> **" + a + "**에 대한 위키백과 검색결과 -\n" + content + "...\n\n[[ 자세히 보기 ]]("+title+")"))
                    await app.send_message(channel, embed=embed)

    elif message.content == "참치봇 미세먼지":
        channel = message.channel
        url = "https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80"
        res = requests.get(url)
        html = res.text
        bs = bs4.BeautifulSoup(html, 'html.parser')
        mise = {}
        city = ['서울', '경기', '인천', '강원', '세종', '충북' ,'충남', '대전', '경북', '경남', '대구', '울산', '부산', '전북', '전남', '광주', '제주']
        num = 0
        for x in city:
            mise[x] = bs.select(
                "#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.main_box > div.detail_box > div.tb_scroll > table > tbody > tr > td > span")[num].text
            num += 3
        level = {}
        for x in city:
            if int(mise[x]) <= 30:
                level[x] = "좋음"
            elif int(mise[x]) >= 31 and int(mise[x]) <= 80:
                level[x] = "보통"
            elif int(mise[x]) >= 81 and int(mise[x]) <= 150:
                level[x] = "**나쁨**"
            elif int(mise[x]) >= 151:
                level[x] = "**매우나쁨**"
            else:
                level[x] = "오류"
        time = bs.select("#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.info_box > div.guide_bx > div > span.update > em")[0].text
        embed = embed_text("**TUNA BOT - PM10 미세먼지**", (":dash: "+time+"기준"))
        for i in city:
            embed.add_field(name="**"+i+"**", value=(mise[i]+"㎍/m³ | "+level[i]))
        await app.send_message(channel, embed=embed)

    elif message.content == "참치봇 초미세먼지":
        channel = message.channel
        url = "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&query=%EC%B4%88%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80"
        res = requests.get(url)
        html = res.text
        bs = bs4.BeautifulSoup(html, 'html.parser')
        mise = {}
        city = ['서울', '경기', '인천', '강원', '세종', '충북' ,'충남', '대전', '경북', '경남', '대구', '울산', '부산', '전북', '전남', '광주', '제주']
        num = 0
        for x in city:
            mise[x] = bs.select(
                "#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.main_box > div.detail_box > div.tb_scroll > table > tbody > tr > td > span")[num].text
            num += 3
        level = {}
        for x in city:
            if int(mise[x]) <= 15:
                level[x] = "좋음"
            elif int(mise[x]) >= 16 and int(mise[x]) <= 35:
                level[x] = "보통"
            elif int(mise[x]) >= 36 and int(mise[x]) <= 75:
                level[x] = "**나쁨**"
            elif int(mise[x]) >= 76:
                level[x] = "**매우나쁨**"
            else:
                level[x] = "오류"
        time = bs.select("#main_pack > div.content_search.section._atmospheric_environment > div > div.contents03_sub > div > div > div.info_box > div.guide_bx > div > span.update > em")[0].text
        embed = embed_text("**TUNA BOT - PM2.5 초미세먼지**", (":dash: "+time+"기준"))
        for i in city:
            embed.add_field(name="**"+i+"**", value=(mise[i]+"㎍/m³ | "+level[i]))
        await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 태그"):
        channel = message.channel
        url = message.attachments[0]['url']
        request_url = "https://kapi.kakao.com/v1/vision/multitag/generate"
        headers= {"Authorization": "카카오 토큰"}
        params = {"image_url": url}
        response = requests.post(request_url, headers=headers, data=params)
        result = response.json()
        resulttext = ""
        result = result['result']['label_kr']
        for i in result:
            resulttext += ("#"+i+" ")
        if resulttext == "":
            embed = embed_text("**TUNA BOT - 태그**", (":hash: **생성된 태그가 없습니다.**"))
            embed.set_thumbnail(url=url)
            await app.send_message(channel, embed=embed)
        else:
            resulttext = resulttext[:(len(resulttext)-1)]
            embed = embed_text("**TUNA BOT - 태그**", (":hash: **생성된 태그 -**\n```"+resulttext+"```"))
            embed.set_thumbnail(url=url)
            await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 랜덤숫자"):
        channel = message.channel
        random_len = len(message.content[9:].split())
        if not random_len == 2:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **랜덤숫자 명령어는 2개의 인수가 필요합니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
        else:
            try:
                random_first = int(message.content[9:].split(" ")[0])
                random_second = int(message.content[9:].split(" ")[1])
                random_number = str(random.randrange(random_first, random_second))
                embed = embed_text("**TUNA BOT - 랜덤숫자**", (":1234: "+str(random_first)+"~"+str(random_second)+"중 선택된 숫자 -\n```"+random_number+"```"))
                await app.send_message(channel, embed=embed)
            except ValueError:
                embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **랜덤숫자 명령어의 인수는 꼭 숫자여야 합니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
                await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 매치"):
        channel = message.channel
        mlen = len(message.content[7:].split())
        if not mlen == 2:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **매치 명령어는 2개의 인수가 필요합니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
        else:
            first = message.content[7:].split()[0]
            second = message.content[7:].split()[1]
            match = SequenceMatcher(None, first, second).ratio()*100
            embed = embed_text("**TUNA BOT - 매치**", ("**"+first+" & "+second+" 의 비슷한 정도 -**\n```"+str(int(match))+"%```"))
            await app.send_message(channel, embed=embed)

    elif message.content == "참치봇 클리어":
        channel = message.channel
        if message.author.server_permissions.administrator:
            try:
                messages = []
                async for i in app.logs_from(channel, limit=100):
                    messages.append(i)
                await app.delete_messages(messages)
            except:
                embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **참치봇의 메시지 삭제 권한이 없거나 메시지가 너무 오래 됬습니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
                await app.send_message(channel, embed=embed)
        else:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **클리어 명령어는 관리자 권한이 필요합니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)

    elif message.content == "참치봇 소식":
        channel = message.channel
        embed = embed_text("**TUNA BOT - 소식**", (":newspaper: **코인일보**\n"+news[0]+news[1]+news[2]))
        rmessage = await app.send_message(channel, embed=embed)
        await app.add_reaction(rmessage, "👍")
        await app.add_reaction(rmessage, "👎")
        
    elif message.content == "참치봇 정보":
        channel = message.channel
        members = str(len(set(app.get_all_members())))
        embed = embed_text("**TUNA BOT - 정보**", "")
        embed.add_field(name="**이름**", value="TUNA BOT")
        embed.add_field(name="**사용자**", value=(str(len(app.servers))+"서버 "+members+"명"))
        embed.add_field(name="**개발자**", value="@[ COIN ]#7338")
        embed.add_field(name="**버전**", value=version)
        embed.add_field(name="**도움을 주신 분**", value="MAKER7777 & ZEON & BGM & ARPAAP & DACOON & MANGO & GOJUWON")
        embed.add_field(name="**도움을 주신 팀**", value="INFINITY TEAM & TEAM HERMES & TEAM FREETIME")
        embed.add_field(name="**도움을 주신 서버**", value="사람이 없어 & 디스코드 랜드 & HANGEUL & 엔트리유치원 2호점 & FLEET LABORATORY & ENTRY DISCORD & TEAM COMPRO & TEAM FT OFFICIAL")
        embed.add_field(name="**서포트 센터**", value="[[ COKE 공식 서포트 센터 ]](https://discord.gg/WzrdB49)")
        embed.set_thumbnail(url=logo)
        await app.send_message(channel, embed=embed)
    
    elif message.content == "참치봇 내정보":
        channel = message.channel
        member = discord.utils.get(app.get_all_members(), id=message.author.id)
        voice = message.author.voice
        if voice.voice_channel == None:
            voice = "None"
        elif voice.deaf == True:
            voice = "deaf" + " | " + voice.voice_channel.mention
        elif voice.mute == True:
            voice = "mute" + " | " + voice.voice_channel.mention
        elif voice.self_deaf == True:
            voice = "self_deaf" + " | " + voice.voice_channel.mention
        elif voice.self_mute == True:
            voice = "self_mute" + " | " + voice.voice_channel.mention
        else:
            voice = "online" + " | " + voice.voice_channel.mention
        username = member.name
        nickname = message.author.nick
        avatar = member.avatar_url
        usercreated = member.created_at
        userid = member.id
        userroles = message.author.roles
        admin = str(message.author.server_permissions.administrator)
        userrole = ""
        for x in range(0, len(userroles)):
            userrole += (userroles[x].name + ", ")
        userrole = userrole[:(len(userrole)-2)]
        userjoin = member.joined_at
        userstatus = member.status
        usergame = member.game
        embed = embed_text("**TUNA BOT - 내정보**", (""))
        embed.add_field(name="**이름**", value=username)
        embed.add_field(name="**별명**", value=nickname)
        embed.add_field(name="**프로필 사진**", value=("[[ 사진 보기 ]]("+avatar+")"))
        embed.add_field(name="**계정 생성일**", value=usercreated)
        embed.add_field(name="**서버 가입일**", value=userjoin)
        embed.add_field(name="**유저 ID**", value=userid)
        embed.add_field(name="**역할**", value=userrole)
        embed.add_field(name="**서버 관리자**", value=admin)
        embed.add_field(name="**상태**", value=userstatus)
        embed.add_field(name="**음성**", value=voice)
        embed.add_field(name="**게임**", value=usergame)
        embed.set_thumbnail(url=avatar)
        await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 유저정보"):
        channel = message.channel
        try:
            member = message.mentions[0]
            voice = message.author.voice
            if voice.voice_channel == None:
                voice = "None"
            elif voice.deaf == True:
                voice = "deaf" + " | " + voice.voice_channel.mention
            elif voice.mute == True:
                voice = "mute" + " | " + voice.voice_channel.mention
            elif voice.self_deaf == True:
                voice = "self_deaf" + " | " + voice.voice_channel.mention
            elif voice.self_mute == True:
                voice = "self_mute" + " | " + voice.voice_channel.mention
            else:
                voice = "online" + " | " + voice.voice_channel.mention
            username = member.name
            nickname = member.nick
            avatar = member.avatar_url
            usercreated = member.created_at
            userid = member.id
            userroles = message.author.roles
            admin = str(message.author.server_permissions.administrator)
            userrole = ""
            for x in range(0, len(userroles)):
               userrole += (userroles[x].name + ", ")
            userrole = userrole[:(len(userrole)-2)]
            userjoin = member.joined_at
            userstatus = member.status
            usergame = member.game
            embed = embed_text("**TUNA BOT - 유저정보**", (""))
            embed.add_field(name="**이름**", value=username)
            embed.add_field(name="**별명**", value=nickname)
            embed.add_field(name="**프로필 사진**", value=("[[ 사진 보기 ]]("+avatar+")"))
            embed.add_field(name="**계정 생성일**", value=usercreated)
            embed.add_field(name="**서버 가입일**", value=userjoin)
            embed.add_field(name="**유저 ID**", value=userid)
            embed.add_field(name="**역할**", value=userrole)
            embed.add_field(name="**서버 관리자**", value=admin)
            embed.add_field(name="**상태**", value=userstatus)
            embed.add_field(name="**음성**", value=voice)
            embed.add_field(name="**게임**", value=usergame)
            if member.bot:
                embed.add_field(name="**봇**", value=("[[ 초대 링크 ]](https://discordapp.com/api/oauth2/authorize?client_id="+member.id+"&permissions=8&scope=bot)"))
            embed.set_thumbnail(url=avatar)
            await app.send_message(channel, embed=embed)
            
        except:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **유저정보 명령어의 언급은 1개여야만 합니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)

    elif message.content == "참치봇 서버정보":
        channel = message.channel
        if True:
            server = message.server
            avatar = server.icon_url
            ver = server.verification_level
            name = server.name
            region = server.region
            sid = server.id
            created = server.created_at
            created2 = str(created)
            count = server.member_count
            owner = server.owner.mention
            channellen = 0
            for i in server.channels:
                channellen += 1
            channellen = str(channellen)
            roles = server.roles
            role = ""
            for x in range(0, len(roles)):
                role += (roles[x].name + ", ")
            role = role[:(len(role)-2)]
            emojis = server.emojis
            if len(emojis) <= 0:
                emoji = "없음"
            else:
                emoji = ""
                for i in range(0, len(emojis)):
                    emoji += ("<:"+emojis[i].name+":"+emojis[i].id+">, ")
                emoji = emoji[:(len(emoji)-2)]
            if server.afk_channel == None:
                afk = (str(int(server.afk_timeout/60))+"분")
            else:
                afk = ("**"+str(server.afk_timeout/60)+"**분 "+server.afk_channel.mention)
            embed = embed_text("**TUNA BOT - 서버정보**", (""))
            embed.add_field(name="**이름**", value=name)
            embed.add_field(name="**국가**", value=region)
            embed.add_field(name="**서버 생성일**", value=created2)
            embed.add_field(name="**멤버 수**", value=count)
            embed.add_field(name="**소유자**", value=owner)
            embed.add_field(name="**잠수**", value=afk)
            embed.add_field(name="**역할**", value=role)
            embed.add_field(name="**이모지**", value=emoji)
            embed.add_field(name="**채널 수**", value=channellen)
            embed.add_field(name="**서버 ID**", value=sid)
            embed.add_field(name="**보안 수준**", value=ver)
            if avatar == "":
                embed.add_field(name="**아이콘**", value=("없음"))
            else:
                embed.add_field(name="**아이콘**", value=("[[ 사진 보기 ]]("+avatar+")"))
                embed.set_thumbnail(url=avatar)
            await app.send_message(channel, embed=embed)
        #except:
            #embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **서버정보 명령어는 서버에서만 사용할 수 있습니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            #await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 채널정보"):
        if len(message.channel_mentions) == 0:
            channel = message.channel
        else:
            channel = message.channel_mentions[0]
        name = channel.name
        cid = channel.id
        topic = channel.topic
        if topic == "" or topic == None:
            topic = "없음"
        private = str(channel.is_private)
        pos = str(channel.position+1) + "번"
        ctype = str(channel.type)
        created = str(channel.created_at)
        embed = embed_text("**TUNA BOT - 채널정보**", (""))
        embed.add_field(name="**이름**", value=name)
        embed.add_field(name="**채널 ID**", value=cid)
        embed.add_field(name="**주제**", value=topic)
        embed.add_field(name="**비공개**", value=private)
        embed.add_field(name="**채널 순서**", value=pos)
        embed.add_field(name="**채널 종류**", value=ctype)
        embed.add_field(name="**채널 생성일**", value=created)
        await app.send_message(message.channel, embed=embed)

    elif message.content.startswith("참치봇 역할정보"):
        channel = message.channel
        rname = message.content[9:]
        if not len(message.mentions) == 0 or not len(message.role_mentions) == 0 or message.mention_everyone:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **존재하지 않는 역할 이름입니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
            return
        try:
            if rname == "everyone":
                role = discord.utils.get(message.server.roles, name="@everyone")
            else:
                role = discord.utils.get(message.server.roles, name=rname)
                rid = role.id
        except:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **존재하지 않는 역할 이름입니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
            return
        rid = role.id
        name = role.name
        admin = str(role.permissions.administrator)
        color = str(role.colour)
        pos = str(role.position+1) + "번"
        men = str(role.mentionable)
        hoist = str(role.hoist)
        created = str(role.created_at)
        managed = str(role.managed)
        ev = str(role.is_everyone)
        embed = embed_text("**TUNA BOT - 역할정보**", (""))
        embed.add_field(name="**이름**", value=name)
        embed.add_field(name="**역할 ID**", value=rid)
        embed.add_field(name="**역할 생성일**", value=created)
        embed.add_field(name="**색**", value=color)
        embed.add_field(name="**역할 순서**", value=pos)
        embed.add_field(name="**언급 가능**", value=men)
        embed.add_field(name="**분리 표시**", value=hoist)
        embed.add_field(name="**플랫폼 매니지드**", value=managed)
        embed.add_field(name="**에브리원 여부**", value=ev)
        embed.add_field(name="**관리자 권한**", value=admin)
        await app.send_message(message.channel, embed=embed)
        
            
    elif message.content.startswith("참치봇 도움말"):
        channel = message.channel
        if message.content == "참치봇 도움말":
            embed = embed_text("**TUNA BOT - 도움말**", (""))
            embed.add_field(name="**참치봇 도움말 기능**", value="```참치봇의 기능 명령어를 안내합니다```", inline=False)
            embed.add_field(name="**참치봇 도움말 정보**", value="```참치봇의 정보 명령어를 안내합니다```", inline=False)
            await app.send_message(message.author, embed=embed)
        elif message.content[8:] == "기능":
            help = ("**참치봇 도움말 (<기능/정보>)** - 참치봇의 명령어를 안내합니다\n" +
                    "**참치봇 랜덤문자 <문자> <문자> ...** - 문자 인수 중 하나를 랜덤으로 뽑습니다\n" +
                    "**참치봇 랜덤숫자 <최소값> <최대값>** - 숫자 하나를 랜덤으로 뽑습니다\n" +
                    "**참치야 <메세지>** - 인공지능 모드로 대답합니다\n" +
                    "**참치봇 슛골인 <정보/쉬움/어려움>** - 참치봇과 슛골인 게임을 진행합니다\n" +
                    "**참치봇 매직8볼 <질문>** -  질문에 대해 여러가지 메세지로 대답합니다\n" +
                    "**참치봇 시각** -  현재 시각을 알려줍니다\n" +
                    "**참치봇 마크 <닉네임>** -  해당 유저의 마인크래프트 스킨을 불러옵니다\n" +
                    "**참치봇 영한번역 <번역문장>** -  영어 문장을 한국어로 번역합니다\n" +
                    "**참치봇 영일번역 <번역문장>** -  영어 문장을 일본어로 번역합니다\n" +
                    "**참치봇 영중번역 <번역문장>** -  영어 문장을 중국어로 번역합니다\n" +
                    "**참치봇 한영번역 <번역문장>** -  한국어 문장을 영어로 번역합니다\n" +
                    "**참치봇 한일번역 <번역문장>** -  한국어 문장을 일본어로 번역합니다\n" +
                    "**참치봇 한중번역 <번역문장>** -  한국어 문장을 중국어로 번역합니다\n" +
                    "**참치봇 실검** -  현재 네이버의 실시간 검색어 1위~20위를 불러옵니다\n" +
                    "**참치봇 명언** -  도움이 되는 명언을 랜덤으로 안내합니다\n" +
                    "**참치봇 블로그 <검색어>** -  네이버 블로그에서 검색어를 검색합니다\n" +
                    "**참치봇 카이썬 <코드>** -  전용 언어인 카이썬 코드를 실행합니다\n" +
                    "**참치봇 슬롯** - 참치봇과 슬롯 게임을 진행합니다\n" +
                    "**참치봇 날씨** -  전국의 날씨를 불러옵니다\n" +
                    "**참치봇 공지** -  서버에 공지를 보냅니다\n" +
                    "**참치봇 클리어** -  해당 채널의 메세지 100개를 삭제합니다\n" +
                    "**참치봇 찾기 <검색어>** -  해당 채널의 메세지에서 검색어를 검색합니다\n" +
                    "**참치봇 매치 <문자> <문자>** -  두 문자의 비슷한 정도를 안내합니다\n" +
                    "**참치봇 나무위키 <검색어>** -  나무위키에서 검색어를 검색합니다\n" +
                    "**참치봇 태그 <사진 파일>** -  해당 사진의 태그를 생성합니다\n" +
                    "**참치봇 미세먼지** -  전국의 미세먼지를 불러옵니다\n" +
                    "**참치봇 초미세먼지** -  전국의 초미세먼지를 불러옵니다\n" +
                    "**참치봇 타이머 <시간(초)> (<사유>)** -  타이머를 실행합니다\n" +
                    "**참치봇 멜론** -  현재 멜론차트 1위~10위를 불러옵니다\n" +
                    "**참치봇 영화** -  현재 영화 순위를 불러옵니다\n" +
                    "**참치봇 위키백과 <검색어>** -  위키백과에서 검색어를 검색합니다")
            embed = embed_text("**TUNA BOT - 기능 도움말**", help)
            await app.send_message(message.author, embed=embed)
            return
        elif message.content[8:] == "정보":
            embed = embed_text("**TUNA BOT - 정보 도움말**", (""))
            help = ("**참치봇 정보** - 참치봇의 정보를 안내합니다\n" +
                    "**참치봇 내정보** -  자신의 정보를 불러옵니다\n" +
                    "**참치봇 유저정보 <언급>** -  언급된 유저의 정보를 불러옵니다\n" +
                    "**참치봇 서버정보** -  해당 서버의 정보를 불러옵니다 (DM일 시 작동 불가)\n" +
                    "**참치봇 채널정보 (<채널언급>)** -  본 채널 또는 해당 채널의 정보를 불러옵니다\n" +
                    "**참치봇 역할정보 <역할이름>** -  해당 역할의 정보를 불러옵니다\n" +
                    "**참치봇 상세정보 <명령어이름>** -  해당 명령어의 사용법 또는 정보를 불러옵니다 (개발중)")
            embed = embed_text("**TUNA BOT - 기능 도움말**", help)
            await app.send_message(message.author, embed=embed)
            return
            await app.send_message(message.author, embed=embed)
            return
        else:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **도움말 명령어의 인수는 기능 / 정보 여야만 합니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
            return
        embed = embed_text("**TUNA BOT - 도움말**", (":question: 참치봇의 도움말을 DM으로 전송하였습니다."))
        await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치봇 찾기"):
        channel = message.channel
        query = message.content[7:]
        if query == "":
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **찾기 명령어의 인수는 1개 여야만 합니다!**\n```" + message.content + "```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
        else:
            ms = ""
            async for i in app.logs_from(channel, limit=1000):
                try:
                    if query in i.content and not i.id == message.id:
                        ms += ("**"+i.author.name+" - "+str(i.timestamp)[:(len(str(i.timestamp))-7)]+"**```"+i.content+"```")
                except:
                    continue
            if ms == "":
                embed = embed_text("**TUNA BOT - 찾기**", (":mag_right: **" + query + "**에 대한 메세지 검색결과가 없습니다."))
                await app.send_message(channel, embed=embed)
            else:
                embed = embed_text("**TUNA BOT - 찾기**", (":mag_right: **" + query + "**에 대한 메세지 검색결과 -\n"+ms))
                await app.send_message(channel, embed=embed)
    
    elif message.content == "참치봇 명언":
        channel = message.channel
        wise = random.choice(wise_saying)
        embed = embed_text("**TUNA BOT - 명언**", wise)
        await app.send_message(channel, embed=embed)
    
    elif message.content == "참치봇 슬롯":
        channel = message.channel
        first = random.choice([":tada:", ":seven:", ":heavy_dollar_sign:", ":star:", ":crown:"])
        second = random.choice([":tada:", ":seven:", ":heavy_dollar_sign:", ":star:", ":crown:"])
        third = random.choice([":tada:", ":seven:", ":heavy_dollar_sign:", ":star:", ":crown:"])
        if first == second and first == third:
            message = (message.author.mention+"님, 성공! 축하드립니다!")
        else:
            message = (message.author.mention+"님, 아쉽지만 실패했습니다.")
        embed = embed_text("**TUNA BOT - 슬롯**", (":slot_machine: 3개의 이모지가 모두 같을시 승리합니다.\n**[ " + first + " | " + second + " | " + third + " ]**\n" + message))
        await app.send_message(channel, embed=embed)
        
    
    elif message.content.startswith("참치봇 블로그"):
        query = message.content[8:]
        channel = message.channel
        req = requests.get(("https://search.naver.com/search.naver?where=post&sm=tab_jum&query="+query))
        source = req.text
        soup = BeautifulSoup(source, "html.parser")
        last = ""
        try:
            for i in range(1, 10):
                titles = soup.select("#sp_blog_"+str(i)+" > dl > dt > a")[0].text
                links = soup.select("#sp_blog_"+str(i)+" > dl > dd.txt_block > span > a.url")[0].text
                final = ("["+titles+"](https://"+links+")\n")
                last += final
            embed = embed_text("**TUNA BOT - 검색**", ("<:naverblog:563328265268363265> **"+query+"**에 대한 네이버 블로그 검색결과 -\n"+last))
            await app.send_message(channel, embed=embed)
        except:
            embed = embed_text("**TUNA BOT - 검색**", ("<:naverblog:563328265268363265> **"+query+"**에 대한 네이버 블로그 검색결과가 없습니다."))
            await app.send_message(channel, embed=embed)
    
    elif message.content.startswith("참치봇 슛골인"):
        channel = message.channel
        if str(message.content[8:].split(" ")[0]) == "정보":
            embed = embed_text("**TUNA BOT - 슛골인**", (":soccer: **난이도 선택**\n\n**쉬움** - 1m~100m중 1m~50m이 나오면 승리\n**어려움** - 1m~100m중 1m~10m이 나오면 승리"))
            await app.send_message(channel, embed=embed)
        elif str(message.content[8:].split(" ")[0]) == "쉬움":
            dif = str(message.content[8:].split(" ")[0])
            randnum = random.randint(1, 100)
            if randnum >= 1 and randnum <= 50:
                embed = embed_text("**TUNA BOT - 슛골인**", ("```"+str(randnum)+"m```\n"+message.author.mention+"님, **쉬움 난이도** 성공! 축하드립니다!"))
                await app.send_message(channel, embed=embed)
            else:
                embed = embed_text("**TUNA BOT - 슛골인**", ("```"+str(randnum)+"m```\n"+message.author.mention+"님, 아쉽지만 실패했습니다."))
                await app.send_message(channel, embed=embed)
        elif str(message.content[8:].split(" ")[0]) == "어려움":
            dif = str(message.content[8:].split(" ")[0])
            randnum = random.randint(1, 100)
            if randnum >= 1 and randnum <= 10:
                embed = embed_text("**TUNA BOT - 슛골인**", ("```"+str(randnum)+"m```\n"+message.author.mention+"님, **어려움 난이도** 성공! 축하드립니다!"))
                await app.send_message(channel, embed=embed)
            else:
                embed = embed_text("**TUNA BOT - 슛골인**", ("```"+str(randnum)+"m```\n"+message.author.mention+"님, 아쉽지만 실패했습니다."))
                await app.send_message(channel, embed=embed)
        else:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **슛골인 명령어의 인수는 정보 / 쉬움 / 어려움 이여야만 합니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(channel, embed=embed)
    
    
    elif message.content.startswith("참치봇 매직8볼"):
        channel = message.channel
        answer = random.choice(["절대 안돼.", "마음대로 해.", "안돼. 절대 하지마.", "그래.", "하든지 말든지.", "절대 안돼.", "안돼. 절대 하지마.", "절대 안돼.", "안돼. 절대 하지마."])
        embed = embed_text("**TUNA BOT - 매직8볼**", (":8ball: ```"+answer+"```"))
        await app.send_message(channel, embed=embed)
  
    elif message.content.startswith("참치봇 영한번역"):
        channel = message.channel
        url="https://openapi.naver.com/v1/papago/n2mt?source=en&target=ko&text="
        text = message.content[9:]
        request_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": "네이버 클라이언트 아이디", "X-Naver-Client-Secret":"네이버 클라이언트 시크릿"}
        params = {"source": "en", "target": "ko", "text": text}
        response = requests.post(request_url, headers=headers, data=params)
        result = response.json()
        result = result['message']['result']['translatedText']
        embed = embed_text("**TUNA BOT - 영한번역**", (":flag_us::flag_kr: **번역된 문장 -**\n```"+result+"```"))
        await app.send_message(channel, embed=embed)
    
    
    elif message.content.startswith("참치봇 영일번역"):
        channel = message.channel
        url="https://openapi.naver.com/v1/papago/n2mt?source=en&target=ja&text="
        text = message.content[9:]
        request_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": "네이버 클라이언트 아이디", "X-Naver-Client-Secret":"네이버 클라이언트 시크릿"}
        params = {"source": "en", "target": "ja", "text": text}
        response = requests.post(request_url, headers=headers, data=params)
        result = response.json()
        result = result['message']['result']['translatedText']
        embed = embed_text("**TUNA BOT - 영일번역**", (":flag_us::flag_jp: **번역된 문장 -**\n```"+result+"```"))
        await app.send_message(channel, embed=embed)
    
    
    elif message.content.startswith("참치봇 영중번역"):
        channel = message.channel
        url="https://openapi.naver.com/v1/papago/n2mt?source=en&target=zh-CN&text="
        text = message.content[9:]
        request_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": "네이버 클라이언트 아이디", "X-Naver-Client-Secret":"네이버 클라이언트 시크릿"}
        params = {"source": "en", "target": "zh-CN", "text": text}
        response = requests.post(request_url, headers=headers, data=params)
        result = response.json()
        result = result['message']['result']['translatedText']
        embed = embed_text("**TUNA BOT - 영중번역**", (":flag_us::flag_cn: **번역된 문장 -**\n```"+result+"```"))
        await app.send_message(channel, embed=embed)
    
    
    elif message.content.startswith("참치봇 한영번역"):
        channel = message.channel
        url="https://openapi.naver.com/v1/papago/n2mt?source=ko&target=en&text="
        text = message.content[9:]
        request_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": "네이버 클라이언트 아이디", "X-Naver-Client-Secret":"네이버 클라이언트 시크릿"}
        params = {"source": "ko", "target": "en", "text": text}
        response = requests.post(request_url, headers=headers, data=params)
        result = response.json()
        result = result['message']['result']['translatedText']
        embed = embed_text("**TUNA BOT - 한영번역**", (":flag_kr::flag_us: **번역된 문장 -**\n```"+result+"```"))
        await app.send_message(channel, embed=embed)
    
    
    elif message.content.startswith("참치봇 한일번역"):
        channel = message.channel
        url="https://openapi.naver.com/v1/papago/n2mt?source=ko&target=ja&text="
        text = message.content[9:]
        request_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": "네이버 클라이언트 아이디", "X-Naver-Client-Secret":"네이버 클라이언트 시크릿"}
        params = {"source": "ko", "target": "ja", "text": text}
        response = requests.post(request_url, headers=headers, data=params)
        result = response.json()
        result = result['message']['result']['translatedText']
        embed = embed_text("**TUNA BOT - 한일번역**", (":flag_kr::flag_jp: **번역된 문장 -**\n```"+result+"```"))
        await app.send_message(channel, embed=embed)
    
    
    elif message.content.startswith("참치봇 한중번역"):
        channel = message.channel
        url="https://openapi.naver.com/v1/papago/n2mt?source=ko&target=zh-CN&text="
        text = message.content[9:]
        request_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {"X-Naver-Client-Id": "네이버 클라이언트 아이디", "X-Naver-Client-Secret":"네이버 클라이언트 시크릿"}
        params = {"source": "ko", "target": "zh-CN", "text": text}
        response = requests.post(request_url, headers=headers, data=params)
        result = response.json()
        result = result['message']['result']['translatedText']
        embed = embed_text("**TUNA BOT - 한중번역**", (":flag_kr::flag_cn: **번역된 문장 -**\n```"+result+"```"))
        await app.send_message(channel, embed=embed)
        
    
    elif message.content == "참치봇 시각":
        channel = message.channel
        now = datetime.datetime.now()
        if now.hour >= 13:
            pmhour = str(now.hour-12)
            time = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일\n오후 " + pmhour + "시 " + str(now.minute) + "분 " + str(now.second) + "초"
        else:
            amhour = str(now.hour)
            time = str(now.year) + "년 " + str(now.month) + "월 " + str(now.day) + "일\n오전 " + amhour + "시 " + str(now.minute) + "분 " + str(now.second) + "초"
        embed = embed_text("**TUNA BOT - 시각**", (":clock3: **현재 시각**\n```"+time+"```"))
        await app.send_message(channel, embed=embed)
    
    
    elif message.content.startswith("참치봇 마크"):
        nickname = message.content[7:]
        channel = message.channel
        embed = embed_text("**TUNA BOT - 마크**", ("**"+nickname+"님의 스킨**\n[[ 아바타 ]](https://minotar.net/helm/"+nickname+"/100.png)\n[[ 큐브 아바타 ]](https://minotar.net/cube/"+nickname+"/100.png)\n[[ 전신 ]](https://minotar.net/armor/body/"+nickname+"/100.png)\n[[ 반신 ]](https://minotar.net/armor/bust/"+nickname+"/100.png)\n[[ 스킨 다운로드 ]](https://minotar.net/download/"+nickname+")"))
        embed.set_thumbnail(url="https://minotar.net/armor/bust/"+nickname+"/100.png")
        await app.send_message(channel, embed=embed)
    
    
    elif message.content == "참치봇 실검":
        channel = message.channel
        html = requests.get("https://www.naver.com/").text
        soup = BeautifulSoup(html, "html.parser")
        desc = "" 
        title_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')
        for idx, title in enumerate(title_list, 1):
            idx = str(idx)
            desc += (idx + "위 [**" + title.text.replace(" ","") + "**](https://search.naver.com/search.naver?query=+"+title.text.replace(" ","%20")+")\n")
        embed = embed_text("**TUNA BOT - 실검**", desc)
        await app.send_message(channel, embed=embed)


    elif message.content.startswith("참치봇 카이썬"):
        channel = message.channel
        kython = message.content[8:]
        kython = kython.strip()
        if "/" in kython: 
            kython = kython.split("/")
        else:
            kython = [kython]
        codeline = 0
        ifcode = {0:"O"}
        for i in kython:
            if ifcode[codeline] == "O":
                if i.startswith("PRINT<") and i.endswith(">"):
                    text = i[6:(i.find(">"))]
                    result = "```"+text+"```"
                    embed = embed_text("**TUNA BOT - 카이썬**", result)
                    await app.send_message(channel, embed=embed)
                    codeline += 1
                    ifcode[codeline] = "O"
                if i.startswith("IF<") and i.endswith(">"):
                    i = i.replace("IF<", "")
                    how = i[:(i.find(">"))]
                    i = i.replace(how, "")
                    i = i[2:]
                    i = i[:(len(i)-1)]
                    if not "><" in i:
                        result = "**:no_entry_sign: 코드 중 오류 발생**\n```IF문에는 2개 이상의 인수가 필요합니다!```"
                        embed = embed_text("**TUNA BOT - 카이썬**", result)
                        await app.send_message(channel, embed=embed)
                        break
                    else:
                        i = i.split("><")
                        first = i[0]
                        second = i[1]
                        if how == "==":
                            codeline += 1
                            if first == second:
                                ifcode[codeline] = "O"
                            else:
                                ifcode[codeline] = "X"
                        elif how == "!=":
                            codeline += 1
                            if first != second:
                                ifcode[codeline] = "O"
                            else:
                                ifcode[codeline] = "X"
                        else:
                            result = "**:no_entry_sign: 코드 중 오류 발생**\n```IF문의 비교연산자는 '==' 또는 '!=' 여야만 합니다!```"
                            embed = embed_text("**TUNA BOT - 카이썬**", result)
                            await app.send_message(channel, embed=embed)
                            break

    elif message.content.startswith("참치봇 공지"):
        if message.author.id == "474094390441410561":
            for server in app.servers:
                servers = []
                for channel in server.channels:
                    if "봇-공지" in channel.name or "봇_공지" in channel.name or "bot-announcement" in channel.name or "bot_announcement" in channel.name:
                        try:
                            embed = embed_text("**TUNA BOT - 공지**", (message.content[7:]))
                            await app.send_message(channel, embed=embed)
                            servers.append(server.id)
                            break
                        except:
                            continue
                if not server.id in servers:
                    for channel in server.channels:
                        if "bot-notice" in channel.name or "bot_notice" in channel.name:
                            try:
                                embed = embed_text("**TUNA BOT - 공지**", (message.content[7:]))
                                await app.send_message(channel, embed=embed)
                                servers.append(server.id)
                                break
                            except:
                                continue
                if not server.id in servers:
                    for channel in server.channels:
                        if  "notice" in channel.name or "공지" in channel.name or "announcement" in channel.name:
                            try:
                                embed = embed_text("**TUNA BOT - 공지**", (message.content[7:]))
                                await app.send_message(channel, embed=embed)
                                servers.append(server.id)
                                break
                            except:
                                continue
                if not server.id in servers:
                    for channel in server.channels:
                        try:
                            embed = embed_text("**TUNA BOT - 공지**", (message.content[7:]))
                            await app.send_message(channel, embed=embed)
                            servers.append(server.id)
                            break
                        except:
                            continue
        else:
            embed = embed_text("**TUNA BOT - 오류**", (":no_entry_sign: **공지 명령어는 개발자 권한이 있는 유저만 사용할 수 있습니다!**\n```"+message.content+"```\n**자세한 정보는** `참치봇 도움말`**을 통해 확인해주세요!**"))
            await app.send_message(message.channel, embed=embed)

    elif message.content == "참치봇 날씨":
        channel = message.channel
        incheonobs = owm.weather_at_place("Incheon")
        incheonweather = incheonobs.get_weather()
        incheontemperature = int(incheonweather.get_temperature(unit='celsius')['temp'])
        ulsanobs = owm.weather_at_place("Ulsan")
        ulsanweather = ulsanobs.get_weather()
        ulsantemperature = int(ulsanweather.get_temperature(unit='celsius')['temp'])
        gwangjuobs = owm.weather_at_place("Gwangju")
        gwangjuweather = gwangjuobs.get_weather()
        gwangjutemperature = int(gwangjuweather.get_temperature(unit='celsius')['temp'])
        daejeonobs = owm.weather_at_place("Daejeon")
        daejeonweather = daejeonobs.get_weather()
        daejeontemperature = int(daejeonweather.get_temperature(unit='celsius')['temp'])
        jejuobs = owm.weather_at_place("Jeju, KR")
        jejuweather = jejuobs.get_weather()
        jejutemperature = int(jejuweather.get_temperature(unit='celsius')['temp'])
        daeguobs = owm.weather_at_place("Daegu")
        daeguweather = daeguobs.get_weather()
        daegutemperature = int(daeguweather.get_temperature(unit='celsius')['temp'])
        busanobs = owm.weather_at_place("Busan")
        busanweather = busanobs.get_weather()
        busantemperature = int(busanweather.get_temperature(unit='celsius')['temp'])
        seoulobs = owm.weather_at_place("Seoul")
        seoulweather = seoulobs.get_weather()
        seoultemperature = int(seoulweather.get_temperature(unit='celsius')['temp'])
        embed = embed_text("**TUNA BOT - 날씨**", (":white_sun_cloud: **전국 날씨**"))
        embed.add_field(name="**인천**", value=(str(incheontemperature) + "°C"))
        embed.add_field(name="**울산**", value=(str(ulsantemperature) + "°C"))
        embed.add_field(name="**광주**", value=(str(gwangjutemperature) + "°C"))
        embed.add_field(name="**대전**", value=(str(daejeontemperature) + "°C"))
        embed.add_field(name="**제주**", value=(str(jejutemperature) + "°C"))
        embed.add_field(name="**대구**", value=(str(daegutemperature) + "°C"))
        embed.add_field(name="**부산**", value=(str(busantemperature) + "°C"))
        embed.add_field(name="**서울**", value=(str(seoultemperature) + "°C"))
        embed.add_field(name="**제공**", value="OpenWeatherMap")
        await app.send_message(channel, embed=embed)

    elif message.content.startswith("참치야"):
        name = message.author.name
        channel = message.channel
        channel_id = message.channel.id
        channel_name = message.channel.name
        argtext = message.content[4:]
        if "안녕" in argtext or "하이" in argtext or "반가" in argtext or "반갑" in argtext or "헬로" in argtext or "hello" in argtext or "Hello" in argtext or "hi" in argtext or "Hi" in argtext:
            answer = random.choice(["안녕하세요, 주인님.", "반가워요. 주인님.", ("안녕하세요,"+name+"님."), ("반가워요,"+name+"님.")])
            embed = embed_text("**TUNA BOT - 인공지능**", (":levitate: **"+argtext+"** 에 대한 답변 -\n```"+answer+"```"))
            await app.send_message(channel, embed=embed)
        elif "너" in argtext and "누구" in argtext or "넌" in argtext and "누구" in argtext or "넌" in argtext and "누구" in argtext or "너" in argtext and "이름" in argtext or "네" in argtext and "이름" in argtext or "넌" in argtext and "이름" in argtext:
            answer = random.choice(["저는 참치봇입니다.", "저는 참치봇이에요."])
            embed = embed_text("**TUNA BOT - 인공지능**", (":levitate: **"+argtext+"** 에 대한 답변 -\n```"+answer+"```"))
            await app.send_message(channel, embed=embed)
        elif "사랑해" in argtext or "너" in argtext and "사랑" in argtext or "널" in argtext and "사랑" in argtext:
            answer = random.choice(["저도 사랑해요. 주인님."])
            embed = embed_text("**TUNA BOT - 인공지능**", (":levitate: **"+argtext+"** 에 대한 답변 -\n```"+answer+"```"))
            await app.send_message(channel, embed=embed)
        elif "바보" in argtext or "멍청이" in argtext or "닥쳐" in argtext:
            answer = random.choice(["죄송해요. 더 노력할게요."])
            embed = embed_text("**TUNA BOT - 인공지능**", (":levitate: **"+argtext+"** 에 대한 답변 -\n```"+answer+"```"))
            await app.send_message(channel, embed=embed)
        elif "너" in argtext and "똑똑" in argtext or "넌" in argtext and "똑똑" in argtext or "넌" in argtext and "착해" in argtext or "너" in argtext and "착해" in argtext:
            answer = random.choice(["칭찬은 더 좋은 저를 만들어요.", "칭찬 해주셔서 감사합니다!"])
            embed = embed_text("**TUNA BOT - 인공지능**", (":levitate: **"+argtext+"** 에 대한 답변 -\n```"+answer+"```"))
            await app.send_message(channel, embed=embed)
        elif "예뻐" in argtext or "잘생겼" in argtext:
            answer = random.choice(["주인님이 더요."])
            embed = embed_text("**TUNA BOT - 인공지능**", (":levitate: **"+argtext+"** 에 대한 답변 -\n```"+answer+"```"))
            await app.send_message(channel, embed=embed)
        elif "예뻐" in argtext or "잘생겼" in argtext:
            answer = random.choice(["주인님이 더요."])
            embed = embed_text("**TUNA BOT - 인공지능**", (":levitate: **"+argtext+"** 에 대한 답변 -\n```"+answer+"```"))
            await app.send_message(channel, embed=embed)

app.run(token)
