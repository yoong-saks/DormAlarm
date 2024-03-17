import requests
from urllib import parse

from bs4 import BeautifulSoup

import pandas as pd
import sqlite3

"""
import telegram
# 텔레그램 셋팅 ************************************************************
token = "### TOKEN_KEY ###" # 텔레그램 Bot 토근

bot = telegram.Bot(token)
chat_ID = '### CHAT_ID ###' # 수신자 ID

# 텔레그램 메시지 전송 함수
def Sendmsg(msg):
    bot.send_message(chat_ID, msg)
# ************************************************************************
"""

# 디스코드 셋팅 ************************************************************
discordwebhook="### WEBHOOK_URL ###"

def Sendmsg(msg, myurl, mytitle, mywriter, mydate):     
    data = {
        "content" : msg,
    }

    data["embeds"] = [
        {
            "description" : "작성자 : " + mywriter + "\n작성일 : " + mydate,
            "title" : mytitle,
            "url" : myurl
        }
    ]

    result = requests.post(discordwebhook, json = data)

# ************************************************************************

# 신규 데이터 DB 저장 함수
def DatatoSQL(df):
    con = sqlite3.connect("plus.db") # db 파일명 사용자 임의 선정
    df.to_sql('ITEM', con, if_exists='append', index=False)
    con.close()


# 이전에 저장한 DB와 비교를 위해 불러옴
def Check():
    try:
        con = sqlite3.connect("plus.db") # db 파일명 사용자 임의 선정
        df = pd.read_sql("SELECT * from ITEM ", con=con)
        con.close()

        item_name = df['ID'].tolist() # 동일 매물은 제외시키기 위해서 작성자만 리스트로 받음
        return item_name

    except Exception as e:
        return []


# 검색
def Search():
    # 크롤링 결과 저장 변수
    data = {'Title': [],
            'Writer': [],
            'Date': [],
            'Link': [],
            'ID': []}

    url = 'https://dorm.daegu.ac.kr/hakgwa_home/dorm/sub.php?menu=page&menu_id=32'

    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html.parser')

    contents = soup.find('tbody').find_all('tr')

    for i in contents:
        if not i.select('th') :
            title = i.select('td')[1]   # 제목
            writer = i.select('td')[2]  # 글쓴이
            rdate = i.select('td')[3]   # 날짜
            link = 'https://dorm.daegu.ac.kr/hakgwa_home/dorm/sub.php' + i.find('a')['href'] # 링크
        else :
            title = i.select('td')[0]   # 제목
            writer = i.select('td')[1]  # 글쓴이
            rdate = i.select('td')[2]   # 날짜
            link = 'https://dorm.daegu.ac.kr/hakgwa_home/dorm/sub.php' + i.find('a')['href'] # 링크

        data['Title'].append(title.text.strip())
        data['Writer'].append(writer.text.strip())
        data['Date'].append(rdate.text.strip())
        data['Link'].append(link)
        data['ID'].append(link.split('&')[1][4:]) # DB의 기존 자료와 비교하기 위한 식별자

    df = pd.DataFrame(data)
    print(df)

    check_list = Check() # 기존 저장된 링크 주소 리스트 불러오기

    for idx in data['ID']: #data['id']의 리스트를 하나씩 idx로 반복문을 돌림
        # 크롤링으로 받은 데이터의 링크의 마지막 주소가 기존 리스트에 없으면 메시지 전송/데이터 저장
        if idx not in check_list:
            # 메시지 내용 : 게시글 제목 + 작성자 + 날짜 + 링크 URL
            pos = data['ID'].index(idx)

            """텔레그램 메시지 전용 주석
            #텔레그램 메세지 전송 function
            msg = '기숙사에 공지 게시판에 새로운 글이 올라왔어요! \n\n{}\n{}\n{}\n{}'.format(data['Title'][pos], data['Writer'][pos], data['Date'][pos], data['Link'][pos])
            print(msg)

            Sendmsg(msg) # 메시지 전송
            """

            #******************************************************** 디스코드 메세지 전송 function
            
            msg2 = '기숙사에 공지 게시판에 새로운 글이 올라왔어요! \n\n{}\n{}\n{}\n{}'.format(data['Title'][pos], data['Writer'][pos], data['Date'][pos], data['Link'][pos])
            print(msg2)

            msg = '기숙사 공지 게시판에 새로운 글이 올라왔어요!'
            dcurl = data['Link'][pos]
            dctitle = data['Title'][pos]
            dcwriter = data['Writer'][pos]
            dcdate = data['Date'][pos]

            Sendmsg(msg, dcurl, dctitle, dcwriter, dcdate)
            #********************************************************
            
            DatatoSQL(df.loc[df['ID']==idx]) # 데이터 DB를 SQL에 저장


if __name__ == '__main__':
    Search()