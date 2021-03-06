import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

musics = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for music in musics:
    if music is not None:
        rank = music.select_one('td.number')
        if rank is not None:
            rank_nospan = rank.span.decompose()
            title = music.select_one('td.info > a.albumtitle.ellipsis').text
            musician = music.select_one('td.info > a.artist.ellipsis').text
            print(rank.text.strip(),title, musician)
            db.musictop50.insert_one({'rank':rank.text.strip(),'title':title,'musician':musician})