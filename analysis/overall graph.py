import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import xmltodict
from google.cloud import storage
from firebase import firebase
import os
import numpy as np
from os import path

# 한글폰트 적용
from matplotlib import font_manager, rc
import matplotlib
font_location="C:\Windows\Fonts\malgun.ttf"
font_name=font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font',family=font_name)

# 코로나 감염 현황 OpenAPI 불러오기
url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson?serviceKey=k51O9cWrRrewvevw09zB1zRdWQgEKSJl8%2BsSYWdZlm1z1d2wsbhTydoMAOQWTfDVp4NDwzWrC83oNUQdUzU71Q%3D%3D&pageNo=1&numOfRows=100&startCreateDt=&endCreateDt=&'

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
rescode = response.getcode()
response_body = response.read()
data=response_body.decode('utf-8')
dict_data = xmltodict.parse(data)
json_data = json.dumps(dict_data)
result = json.loads(json_data)

rdata=result['response']['body']['items']['item']

# df_week(DataFrame)으로 정의
df_week=pd.DataFrame(rdata)
print(df_week)

# 데이터 전처리
df_week=df_week.groupby('stateDt', sort=True).head(1)
df_week=df_week.iloc[::7]        # 일주일 단위로 데이터 추출

df_week2 = df_week.sort_values(by='stateDt' ,ascending=False)

df_week3=df_week2.loc[0:29]

df_week4=df_week3.sort_values(by='stateDt' ,ascending=True)
print(df_week4)

# float형으로 변환
df_week4['decideCnt']=df_week4['decideCnt'].astype(float)
df_week4['clearCnt']=df_week4['clearCnt'].astype(float)
df_week4['deathCnt']=df_week4['deathCnt'].astype(float)

# 함수 정의-자연수 백의 자리 내림, 올림
def rounddown(val) :
    val = int(val / 100) * 100
    return val

def roundup(val) :
    val = val + 90
    val = int(val / 10) * 10
    return val

# 함수 정의-자연수 일의 자리 내림, 올림
def unit_down(val) :
    val = int(val / 10) * 10
    return val

def unit_up(val) :
    val = val + 9
    val = int(val / 10) * 10
    return val

# 확진자수 그래프 yticks 값 조정
dec_start_num=df_week4.iloc[0,7]
dec_end_num=df_week4.iloc[-1,7]
dec_start_num=rounddown(dec_start_num)
dec_end_num=roundup(dec_end_num)+3200

# 격리해제수 그래프 yticks 값 조정
clear_start_num=df_week4.iloc[0,4]
clear_end_num=df_week4.iloc[-1,4]
clear_start_num=rounddown(clear_start_num)
clear_end_num=roundup(clear_end_num)+1500

# 사망자수 그래프 yticks 값 조정
death_start_num=df_week4.iloc[0,6]
death_end_num=df_week4.iloc[-1,6]
death_start_num=unit_down(death_start_num)
death_end_num=unit_up(death_end_num)+30

# figure 기본 설정 (크기 조정, 그래프 배경 투명하게 만들기)
fig = plt.figure(figsize=(8, 6))
fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
fig.patch.set_alpha(0)
ax = fig.add_subplot()

# 확진자수 그래프 출력 및 저장
plt.title('확진자수', fontsize=18, pad=15)
line_plot=ax.plot(df_week4.stateDt,df_week4.decideCnt, color='#FF5A5A', linewidth=2, marker='o',markersize=5, alpha=.75)
line_plot = line_plot[0]
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.yticks(np.arange(dec_start_num, dec_end_num, step=3200))
for coord in list(line_plot.get_xydata()):      # 값 표시
    ax.text(coord[0],coord[1]+230 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/test1.png')
plt.clf()

# 격리해제수 그래프 출력 및 저장
ax = fig.add_subplot()
plt.title('격리해제수', fontsize=18, pad=13)
line_plot=ax.plot(df_week4.stateDt,df_week4.clearCnt, color='#2478FF', linewidth=2, marker='o',markersize=5, alpha=.75)
line_plot=line_plot[0]
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.yticks(np.arange(clear_start_num, clear_end_num, step=1500))
for coord in list(line_plot.get_xydata()):      # 값 표시
    ax.text(coord[0],coord[1]+110 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#2478FF')
plt.savefig('images/test2.png')
plt.clf()

# 사망자수 그래프 출력 및 저장
ax = fig.add_subplot()
plt.title('사망자수', fontsize=18, pad=13)
line_plot=ax.plot(df_week4.stateDt,df_week4.deathCnt, color='#000000', linewidth=2, marker='o',markersize=5, alpha=.75)
line_plot=line_plot[0]
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.yticks(np.arange(death_start_num, death_end_num, step=30))
for coord in list(line_plot.get_xydata()):      # 값 표시
    ax.text(coord[0],coord[1]+1.6 ,f'{int(coord[1])}',fontsize=11, ha='center')
plt.savefig('images/test3.png')

# Firebase Storage 연결
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="mykey.json"
firebase = firebase.FirebaseApplication('https://project-48b89.firebaseio.com/')
client = storage.Client()
bucket = client.get_bucket('project-48b89.appspot.com')

imageBlob = bucket.blob("/")

# Storage에 저장된 그래프 사진파일 저장
# 확진자수 그래프
imagePath1 = "images/test1.png"
imageBlob1 = bucket.blob("overview1.png")
imageBlob1.upload_from_filename(imagePath1)

# 격리해제수 그래프
imagePath2 = "images/test2.png"
imageBlob2 = bucket.blob("overview2.png")
imageBlob2.upload_from_filename(imagePath2)

# 사망자수 그래프
imagePath3 = "images/test3.png"
imageBlob3 = bucket.blob("overview3.png")
imageBlob3.upload_from_filename(imagePath3)