from bs4 import BeautifulSoup
import requests
from konlpy.tag import Twitter
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from google.cloud import storage
from firebase import firebase
import os

# 검색어 지정
search_word = "코로나"
title_list = []

# 함수 정의-뉴스 제목 가져오기
def get_titles(start_num, end_num):
    # 네이버 뉴스 start_num페이지부터 end_num페이지까지 크롤링
    while 1:
        if start_num > end_num:
            break

        url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={}&start={}'.format(search_word,
                                                                                                     start_num)
        req = requests.get(url)

        # request 확인
        if req.ok:
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')

            # 뉴스 제목 추출
            titles = soup.select(
                'div.news_wrap.api_ani_send > div > a'
            )

            # title_list에 넣기
            for title in titles:
                title_list.append(title['title'])
        start_num += 10
    # title_list 확인하기
    print(title_list)

# 함수 정의-워드클라우드 만들기
def make_wordcloud(word_count):
    # 형태소 분석기
    twitter = Twitter()

    sentences_tag = []
    # 형태소 분석하여 리스트에 저장
    for sentence in title_list:
        morph = twitter.pos(sentence)
        sentences_tag.append(morph)

    noun_list = []
    # 명사만 리스트에 저장
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun']:
                if len(word) == 1:      # 글자수 하나일 경우 리스트 저장X
                    continue
                else:
                    noun_list.append(word)

    # 명사의 수 count
    counts = Counter(noun_list)
    tags = counts.most_common(word_count)
    print(tags)

    # 배경 mask 지정
    icon_path = "icon.jpg"
    icon = Image.open(icon_path)
    mask = Image.new("RGB", icon.size, (255, 255, 255))
    mask.paste(icon, icon)
    mask = np.array(mask)

    # WordCloud 생성
    wc = WordCloud(font_path='c:/Windows/Fonts/SeoulNamsanM.ttf', background_color='white', width=800, height=800,
                   mask=mask, colormap='gist_earth')
    print(dict(tags))
    cloud = wc.generate_from_frequencies(dict(tags))
    # figure 기본 설정
    fig = plt.figure(figsize=(5, 5))
    fig.patch.set_alpha(0)
    plt.axis('off')
    plt.imshow(cloud)
    plt.savefig('images/word.png')  # 사진 파일로 저장


if __name__ == '__main__':
    # 1~300 게시글까지 크롤링
    get_titles(1, 300)

    # 단어 100개까지 WordCloud로 출력
    make_wordcloud(100)

    # Firebase Storage 연결
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "mykey.json"
    firebase = firebase.FirebaseApplication('https://project-48b89.firebaseio.com/')
    client = storage.Client()
    bucket = client.get_bucket('project-48b89.appspot.com')

    imageBlob = bucket.blob("/")

    # Storage에 저장된 그래프 사진파일 저장
    imagePath = "images/word.png"
    imageBlob = bucket.blob("word.png")
    imageBlob.upload_from_filename(imagePath)


