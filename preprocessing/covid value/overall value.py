import xmltodict
import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# OpenAPI 불러오기
url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey=k51O9cWrRrewvevw09zB1zRdWQgEKSJl8%2BsSYWdZlm1z1d2wsbhTydoMAOQWTfDVp4NDwzWrC83oNUQdUzU71Q%3D%3D&pageNo=1&numOfRows=100&startCreateDt=&endCreateDt=&'

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
rescode = response.getcode()
response_body = response.read()
data=response_body.decode('utf-8')
dict_data = xmltodict.parse(data)
json_data = json.dumps(dict_data)
result = json.loads(json_data)

data=result['response']['body']['items']['item']

# df_week(DataFrame)으로 정의
df_week=pd.DataFrame(data)

# 데이터 전처리
df_week=df_week.groupby('stateDt', sort=True).head(1)
df_week=df_week.iloc[::7]
df_week2=df_week.sort_values(by='stateDt' ,ascending=False)
df_week3=df_week2.loc[0:29]
df_day=df_week3.head(1)

# 확진자수, 격리해제수, 사망자수
decideCnt=df_day['decideCnt'][0]
clearCnt=df_day['clearCnt'][0]
deathCnt=df_day['deathCnt'][0]

# Firebase Realtime Database 연결
cred = credentials.Certificate('mykey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-48b89.firebaseio.com/'
})

# total 위치를 생성하고 키, 값 형태로 확진자수, 격리해제수, 사망자수 데이터 저장
dir = db.reference('total')
dir.update({'decide': decideCnt})
dir.update({'clear': clearCnt})
dir.update({'death': deathCnt})