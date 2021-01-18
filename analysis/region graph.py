import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import xmltodict
from google.cloud import storage
from firebase import firebase
import os
from os import path

# 한글폰트 적용
from matplotlib import font_manager, rc
import matplotlib
font_location="C:\Windows\Fonts\malgun.ttf"
font_name=font_manager.FontProperties(fname=font_location).get_name()
matplotlib.rc('font',family=font_name)

# 함수-자연수 백의 자리 내림, 올림
def rounddown(val) :
    val = int(val / 100) * 100
    return val

def roundup(val) :
    val = val + 90
    val = int(val / 10) * 10
    return val

# 함수-자연수 일의 자리 내림, 올림
def unit_down(val) :
    val = int(val / 10) * 10
    return val

def unit_up(val) :
    val = val + 9
    val = int(val / 10) * 10
    return val

# 함수-천의 자리 올림
def step_up(val) :
    val = val + 900
    val = int(val / 1000) * 1000
    return val


# 코로나 시,도 발생 현황 OpenAPI 불러오기
url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=pg8wihCfmYf9Euwqa0CoiZfui3IMOfk1kliZfV46KSIm3pDqCHQZBNVRyrNCGvbPYUYwsCmB5ULMPvlH2aT4Ag%3D%3D&pageNo=1&numOfRows=&startCreateDt=&endCreateDt=&'

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
rescode = response.getcode()
response_body = response.read()
data=response_body.decode('utf-8')
dict_data = xmltodict.parse(data)
json_data = json.dumps(dict_data)
result = json.loads(json_data)

rdata=result['response']['body']['items']['item']

# df(DataFrame)으로 정의
df=pd.DataFrame(rdata)


# 데이터 전처리 (원하는 데이터 추출)
df_safe=df[['gubun','defCnt','localOccCnt','overFlowCnt','deathCnt','incDec','isolClearCnt','qurRate','createDt']]

df_safe=df_safe.fillna(0)

df_safe['gubun']=df_safe['gubun'].astype(str)
df_safe['createDt']=df_safe['createDt'].astype(str)

df_safe=df_safe[df_safe.gubun != '검역']
df_safe=df_safe[df_safe.gubun != '합계']

# 날짜 데이터 값 변경하기
date=[]
for one in df_safe['createDt']:
    date.append(one[0:10])

df_safe['createDt']=date

df_safe['createDt'] = df_safe['createDt'].str.replace(pat=r'[-]', repl= r'', regex=True)
df_safe['qurRate'] = df_safe['qurRate'].str.replace(pat=r'[-]', repl= r'0', regex=True)

# 형변환
df_safe['defCnt']=df_safe['defCnt'].astype(int)
df_safe['localOccCnt']=df_safe['localOccCnt'].astype(int)
df_safe['overFlowCnt']=df_safe['overFlowCnt'].astype(int)
df_safe['deathCnt']=df_safe['deathCnt'].astype(int)
df_safe['incDec']=df_safe['incDec'].astype(int)
df_safe['isolClearCnt']=df_safe['isolClearCnt'].astype(int)
df_safe['qurRate']=df_safe['qurRate'].astype(float)
df_safe['createDt']=df_safe['createDt'].astype(int)

# 10개의 지역으로 DataFrame 나누기
df_safe_seoul=df_safe[df_safe['gubun'].str.contains('서울')]
df_safe_gg=df_safe[df_safe['gubun'].str.contains('경기|인천')]
df_safe_chungnam=df_safe[df_safe['gubun'].str.contains('충남|대전|세종')]
df_safe_chungbuk=df_safe[df_safe['gubun'].str.contains('충북')]
df_safe_jeonnam=df_safe[df_safe['gubun'].str.contains('전남|광주')]
df_safe_jeonbuk=df_safe[df_safe['gubun'].str.contains('전북')]
df_safe_gyeongnam=df_safe[df_safe['gubun'].str.contains('경남|부산|울산')]
df_safe_gb=df_safe[df_safe['gubun'].str.contains('경북|대구')]
df_safe_gangwon=df_safe[df_safe['gubun'].str.contains('강원')]
df_safe_jeju=df_safe[df_safe['gubun'].str.contains('제주')]

# 서울
# 서울 df 전처리
df_safe_seoul=df_safe_seoul.groupby('createDt', sort=True).head(1)

df_safe_seoul_week=df_safe_seoul.iloc[::7]      # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_seoul_month=df_safe_seoul_week.head(5)  # 일주일 단위로 한달(5주) 데이터 추출  (누적 확진자수 그래프에 사용)
df_safe_seoul_day=df_safe_seoul.head(5)         # 하루 단위로 5일  데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_seoul_month=df_safe_seoul_month.sort_values(by='createDt', ascending=True)
df_safe_seoul_day=df_safe_seoul_day.sort_values(by='createDt', ascending=True)

df_safe_seoul_month['createDt']=df_safe_seoul_month['createDt'].astype(str)

# 서울 확진자수 그래프 yticks 값 조정
start_num=df_safe_seoul_month.iloc[0,1]
end_num=df_safe_seoul_month.iloc[-1,1]
start_num=rounddown(start_num)-500
end_num=roundup(end_num)+1000

# figure 기본 설정(크기 조정)
fig = plt.figure(figsize=(8, 6))
fig.subplots_adjust(left=0.1, right=0.9, top=0.94, bottom=0.1)
fig.patch.set_alpha(0)
ax = fig.add_subplot()

# 서울 확진자수 그래프 출력
line_plot=ax.plot(df_safe_seoul_month.createDt,df_safe_seoul_month['defCnt'], color='#FF5A5A', linewidth=2, marker='o',markersize=5, alpha=.75 )
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=1000))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+100 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_seoul_1.png')
plt.clf()

# 서울 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_seoul_day_c=df_safe_seoul_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_seoul_day_c['localOccCnt'].idxmax()
end_num_c=(df_safe_seoul_day_c['localOccCnt'][end_num_idx])+50

# 서울 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_seoul_day.createDt))
plt.bar(x-0.0, df_safe_seoul_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_seoul_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_seoul_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=50))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_seoul_2.png')
plt.clf()

# 경기도
# 경기도 df 전처리
df_safe_gg=df_safe_gg.groupby('createDt', sort=True).head(1)

df_safe_gg_week=df_safe_gg.iloc[::7]        # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_gg_month=df_safe_gg_week.head(5)    # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_gg_day=df_safe_gg.head(5)           # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_gg_month=df_safe_gg_month.sort_values(by='createDt', ascending=True)
df_safe_gg_day=df_safe_gg_day.sort_values(by='createDt', ascending=True)

df_safe_gg_month['createDt']=df_safe_gg_month['createDt'].astype(str)

# 경기도 확진자수 그래프 yticks 값 조정
start_num=df_safe_gg_month.iloc[0,1]
end_num=df_safe_gg_month.iloc[-1,1]
start_num=roundup(start_num)-100
end_num=rounddown(end_num)+800

# 경기도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_gg_month.createDt,df_safe_gg_month['defCnt'], color='#FF5A5A', alpha=.75, linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=800))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+68 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_gg_1.png', dpi=300)
plt.clf()

# 경기도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_gg_day_c=df_safe_gg_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_gg_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_gg_day_c['localOccCnt'][end_num_idx]+50

# 경기도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_gg_day.createDt))
plt.bar(x-0.0, df_safe_gg_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_gg_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_gg_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=40))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_gg_2.png', dpi=300)
plt.clf()

# 충청남도
# 충청남도 df 전처리
df_safe_chungnam=df_safe_chungnam.groupby('createDt', sort=True).head(1)

df_safe_chungnam_week=df_safe_chungnam.iloc[::7]        # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_chungnam_month=df_safe_chungnam_week.head(5)    # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_chungnam_day=df_safe_chungnam.head(5)           # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_chungnam_month=df_safe_chungnam_month.sort_values(by='createDt', ascending=True)
df_safe_chungnam_day=df_safe_chungnam_day.sort_values(by='createDt', ascending=True)

df_safe_chungnam_month['createDt']=df_safe_chungnam_month['createDt'].astype(str)

# 충청남도 확진자수 그래프 yticks 값 조정
start_num=df_safe_chungnam_month.iloc[0,1]
end_num=df_safe_chungnam_month.iloc[-1,1]
start_num=roundup(start_num)-100
end_num=roundup(end_num)

# 충청남도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_chungnam_month.createDt,df_safe_chungnam_month['defCnt'], color='#FF5A5A', alpha=.75, linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=100))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+9 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_chungnam_1.png', dpi=300)
plt.clf()

# 충청남도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_chungnam_day_c=df_safe_chungnam_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_chungnam_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_chungnam_day_c['localOccCnt'][end_num_idx]+10

# 충청남도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_chungnam_day.createDt))
plt.bar(x-0.0, df_safe_chungnam_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_chungnam_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_chungnam_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=5))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_chungnam_2.png', dpi=300)
plt.clf()

# 충청북도
# 충청북도 df 전처리
df_safe_chungbuk=df_safe_chungbuk.groupby('createDt', sort=True).head(1)

df_safe_chungbuk_week=df_safe_chungbuk.iloc[::7]        # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_chungbuk_month=df_safe_chungbuk_week.head(5)    # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_chungbuk_day=df_safe_chungbuk.head(5)           # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_chungbuk_month=df_safe_chungbuk_month.sort_values(by='createDt', ascending=True)
df_safe_chungbuk_day=df_safe_chungbuk_day.sort_values(by='createDt', ascending=True)

df_safe_chungbuk_month['createDt']=df_safe_chungbuk_month['createDt'].astype(str)

# 충청북도 확진자수 그래프 yticks 값 조정
start_num=df_safe_chungbuk_month.iloc[0,1]
end_num=df_safe_chungbuk_month.iloc[-1,1]
start_num=unit_down(start_num)
end_num=unit_up(end_num)+50

# 충청북도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_chungbuk_month.createDt,df_safe_chungbuk_month['defCnt'], color='#FF5A5A', alpha=.75, linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=50))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+6.3 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_chungbuk_1.png', dpi=300)
plt.clf()

# 충청북도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_chungbuk_day_c=df_safe_chungbuk_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_chungbuk_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_chungbuk_day_c['localOccCnt'][end_num_idx]+5

# 충청북도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_chungbuk_day.createDt))
plt.bar(x-0.0, df_safe_chungbuk_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_chungbuk_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_chungbuk_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=5))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_chungbuk_2.png', dpi=300)
plt.clf()

# 전라남도
# 전라남도 df 전처리
df_safe_jeonnam=df_safe_jeonnam.groupby('createDt', sort=True).head(1)

df_safe_jeonnam_week=df_safe_jeonnam.iloc[::7]      # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_jeonnam_month=df_safe_jeonnam_week.head(5)  # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_jeonnam_day=df_safe_jeonnam.head(5)         # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_jeonnam_month=df_safe_jeonnam_month.sort_values(by='createDt', ascending=True)
df_safe_jeonnam_day=df_safe_jeonnam_day.sort_values(by='createDt', ascending=True)

df_safe_jeonnam_month['createDt']=df_safe_jeonnam_month['createDt'].astype(str)

# 전라남도 확진자수 그래프 yticks 값 조정
start_num=df_safe_jeonnam_month.iloc[0,1]
end_num=df_safe_jeonnam_month.iloc[-1,1]
start_num=unit_down(start_num)
end_num=unit_up(end_num)+60

# 전라남도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_jeonnam_month.createDt,df_safe_jeonnam_month['defCnt'], color='#FF5A5A', alpha=.75, linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=60))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+5 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_jeonnam_1.png', dpi=300)
plt.clf()

# 전라남도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_jeonnam_day_c=df_safe_jeonnam_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_jeonnam_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_jeonnam_day_c['localOccCnt'][end_num_idx]+4

# 전라남도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_jeonnam_day.createDt))
plt.bar(x-0.0, df_safe_jeonnam_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_jeonnam_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_jeonnam_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=2))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_jeonnam_2.png', dpi=300)
plt.clf()

# 전라북도
# 전라북도 df 전처리
df_safe_jeonbuk=df_safe_jeonbuk.groupby('createDt', sort=True).head(1)

df_safe_jeonbuk_week=df_safe_jeonbuk.iloc[::7]      # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_jeonbuk_month=df_safe_jeonbuk_week.head(5)  # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_jeonbuk_day=df_safe_jeonbuk.head(5)         # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_jeonbuk_month=df_safe_jeonbuk_month.sort_values(by='createDt', ascending=True)
df_safe_jeonbuk_day=df_safe_jeonbuk_day.sort_values(by='createDt', ascending=True)

df_safe_jeonbuk_month['createDt']=df_safe_jeonbuk_month['createDt'].astype(str)

# 전라북도 확진자수 그래프 yticks 값 조정
start_num=df_safe_jeonbuk_month.iloc[0,1]
end_num=df_safe_jeonbuk_month.iloc[-1,1]
start_num=unit_down(start_num)
end_num=unit_up(end_num)+80

# 전라북도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_jeonbuk_month.createDt,df_safe_jeonbuk_month['defCnt'], color='#FF5A5A', alpha=.75, linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=80))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+5 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_jeonbuk_1.png', dpi=300)
plt.clf()

# 전라북도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_jeonbuk_day_c=df_safe_jeonbuk_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_jeonbuk_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_jeonbuk_day_c['localOccCnt'][end_num_idx]+5

# 전라북도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_jeonbuk_day.createDt))
plt.bar(x-0.0, df_safe_jeonbuk_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_jeonbuk_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_jeonbuk_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=5))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_jeonbuk_2.png', dpi=300)
plt.clf()

# 경상남도
# 경상남도 df 전처리
df_safe_gyeongnam=df_safe_gyeongnam.groupby('createDt', sort=True).head(1)

df_safe_gyeongnam_week=df_safe_gyeongnam.iloc[::7]      # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_gyeongnam_month=df_safe_gyeongnam_week.head(5)  # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_gyeongnam_day=df_safe_gyeongnam.head(5)         # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_gyeongnam_month=df_safe_gyeongnam_month.sort_values(by='createDt', ascending=True)
df_safe_gyeongnam_day=df_safe_gyeongnam_day.sort_values(by='createDt', ascending=True)

df_safe_gyeongnam_month['createDt']=df_safe_gyeongnam_month['createDt'].astype(str)

# 경상남도 확진자수 그래프 yticks 값 조정
start_num=df_safe_gyeongnam_month.iloc[0,1]
end_num=df_safe_gyeongnam_month.iloc[-1,1]
start_num=unit_down(start_num)
end_num=unit_up(end_num)+100

# 경상남도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_gyeongnam_month.createDt,df_safe_gyeongnam_month['defCnt'], color='#FF5A5A', alpha=.75, linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=100))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+7 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_gyeongnam_1.png', dpi=300)
plt.clf()

# 경상남도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_gyeongnam_day_c=df_safe_gyeongnam_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_gyeongnam_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_gyeongnam_day_c['localOccCnt'][end_num_idx]+10

# 경상남도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_gyeongnam_day.createDt))
plt.bar(x-0.0, df_safe_gyeongnam_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_gyeongnam_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_gyeongnam_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=10))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_gyeongnam_2.png', dpi=300)
plt.clf()

# 경상북도
# 경상북도 df 전처리
df_safe_gb=df_safe_gb.groupby('createDt', sort=True).head(1)

df_safe_gb_week=df_safe_gb.iloc[::7]        # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_gb_month=df_safe_gb_week.head(5)    # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_gb_day=df_safe_gb.head(5)           # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_gb_month=df_safe_gb_month.sort_values(by='createDt', ascending=True)
df_safe_gb_day=df_safe_gb_day.sort_values(by='createDt', ascending=True)

df_safe_gb_month['createDt']=df_safe_gb_month['createDt'].astype(str)

# 경상북도 확진자수 그래프 yticks 값 조정
start_num=df_safe_gb_month.iloc[0,1]
end_num=df_safe_gb_month.iloc[-1,1]
start_num=unit_down(start_num)
end_num=unit_up(end_num)+50

# 경상북도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_gb_month.createDt,df_safe_gb_month['defCnt'], color='#FF5A5A', alpha=.75, linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=50))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+4 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_gb_1.png', dpi=300)
plt.clf()

# 경상북도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_gb_day_c=df_safe_gb_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_gb_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_gb_day_c['localOccCnt'][end_num_idx]+4

# 경상북도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_gb_day.createDt))
plt.bar(x-0.0, df_safe_gb_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_gb_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_gb_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=3))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_gb_2.png', dpi=300)
plt.clf()

# 강원도
# 강원도 df 전처리
df_safe_gangwon=df_safe_gangwon.groupby('createDt', sort=True).head(1)

df_safe_gangwon_week=df_safe_gangwon.iloc[::7]      # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_gangwon_month=df_safe_gangwon_week.head(5)  # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_gangwon_day=df_safe_gangwon.head(5)         # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_gangwon_month=df_safe_gangwon_month.sort_values(by='createDt', ascending=True)
df_safe_gangwon_day=df_safe_gangwon_day.sort_values(by='createDt', ascending=True)

df_safe_gangwon_month['createDt']=df_safe_gangwon_month['createDt'].astype(str)

# 강원도 확진자수 그래프 yticks 값 조정
start_num=df_safe_gangwon_month.iloc[0,1]
end_num=df_safe_gangwon_month.iloc[-1,1]
start_num=unit_down(start_num)
end_num=unit_up(end_num)+100

# 강원도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_gangwon_month.createDt,df_safe_gangwon_month['defCnt'], color='#FF5A5A', alpha=.75, linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=100))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+7.5 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_gangwon_1.png', dpi=300)
plt.clf()

# 강원도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_gangwon_day_c=df_safe_gangwon_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_gangwon_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_gangwon_day_c['localOccCnt'][end_num_idx]+8

# 강원도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_gangwon_day.createDt))
plt.bar(x-0.0, df_safe_gangwon_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_gangwon_day.overFlowCnt, label='해외유입수', width=0.2,color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_gangwon_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=4))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_gangwon_2.png', dpi=300)
plt.clf()

# 제주도
# 제주도 df 전처리
df_safe_jeju=df_safe_jeju.groupby('createDt', sort=True).head(1)

df_safe_jeju_week=df_safe_jeju.iloc[::7]        # 일주일 단위로 데이터 추출 (누적 확진자수 그래프에 사용)

df_safe_jeju_month=df_safe_jeju_week.head(5)    # 일주일 단위로 한달(5주) 데이터 추출 (누적 확진자수 그래프에 사용)
df_safe_jeju_day=df_safe_jeju.head(5)           # 하루 단위로 5일 데이터 추출 (지역발생수, 해외유입수 그래프에 사용)

df_safe_jeju_month=df_safe_jeju_month.sort_values(by='createDt', ascending=True)
df_safe_jeju_day=df_safe_jeju_day.sort_values(by='createDt', ascending=True)

df_safe_jeju_month['createDt']=df_safe_jeju_month['createDt'].astype(str)

# 제주도 확진자수 그래프 yticks 값 조정
start_num=df_safe_jeju_month.iloc[0,1]
end_num=df_safe_jeju_month.iloc[-1,1]
start_num=unit_down(start_num)
end_num=unit_up(end_num)+10

# 제주도 확진자수 그래프 출력
ax = fig.add_subplot()
line_plot=ax.plot(df_safe_jeju_month.createDt,df_safe_jeju_month['defCnt'], color='#FF5A5A', alpha=.75,  linewidth=2, marker='o',markersize=5)
line_plot=line_plot[0]
plt.yticks(np.arange(start_num, end_num, step=10))
plt.xlabel('날짜 (단위: 주)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
for coord in list(line_plot.get_xydata()):
    ax.text(coord[0],coord[1]+0.7 ,f'{int(coord[1])}',fontsize=11, ha='center', color='#FF5A5A')
plt.savefig('images/fig_jeju_1.png', dpi=300)
plt.clf()

# 제주도 지역발생수, 해외유입수 그래프 yticks 값 조정
df_safe_jeju_day_c=df_safe_jeju_day.sort_values(by='localOccCnt', ascending=True)
end_num_idx=df_safe_jeju_day_c['localOccCnt'].idxmax()
end_num_c=df_safe_jeju_day_c['localOccCnt'][end_num_idx]+4

# 제주도 지역발생수, 해외유입수 그래프 출력
x=np.arange(len(df_safe_jeju_day.createDt))
plt.bar(x-0.0, df_safe_jeju_day.localOccCnt, label='지역발생수', width=0.2, color='#ff8a3c', alpha=.75)
plt.bar(x+0.2, df_safe_jeju_day.overFlowCnt, label='해외유입수', width=0.2, color='#3a8d65', alpha=.75)
plt.xticks(x, df_safe_jeju_day.createDt)
plt.yticks(np.arange(0, end_num_c, step=2))
plt.xlabel('날짜 (단위: 일)')
plt.ylabel('명', position=(0,1.05), verticalalignment='top', horizontalalignment='left', rotation='horizontal')
plt.legend()
plt.savefig('images/fig_jeju_2.png', dpi=300)


# Firebase Storage 연결
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="mykey.json"
firebase = firebase.FirebaseApplication('https://project-48b89.firebaseio.com/')
client = storage.Client()
bucket = client.get_bucket('project-48b89.appspot.com')

imageBlob = bucket.blob("/")

# Storage에 저장된 그래프 사진파일 저장
# 서울 그래프
imagePath_s1 = "images/fig_seoul_1.png"
imageBlob_s1 = bucket.blob("seoul1.png")
imageBlob_s1.upload_from_filename(imagePath_s1)

imagePath_s2 = "images/fig_seoul_2.png"
imageBlob_s2 = bucket.blob("seoul2.png")
imageBlob_s2.upload_from_filename(imagePath_s2)

# 경기도 그래프
imagePath_g1 = "images/fig_gg_1.png"
imageBlob_g1 = bucket.blob("gyeounggi1.png")
imageBlob_g1.upload_from_filename(imagePath_g1)

imagePath_g2 = "images/fig_gg_2.png"
imageBlob_g2 = bucket.blob("gyeounggi2.png")
imageBlob_g2.upload_from_filename(imagePath_g2)

# 충청남도 그래프
imagePath_cn1 = "images/fig_chungnam_1.png"
imageBlob_cn1 = bucket.blob("chungnam1.png")
imageBlob_cn1.upload_from_filename(imagePath_cn1)

imagePath_cn2 = "images/fig_chungnam_2.png"
imageBlob_cn2 = bucket.blob("chungnam2.png")
imageBlob_cn2.upload_from_filename(imagePath_cn2)

# 충청북도 그래프
imagePath_cb1 = "images/fig_chungbuk_1.png"
imageBlob_cb1 = bucket.blob("chungbuk1.png")
imageBlob_cb1.upload_from_filename(imagePath_cb1)

imagePath_cb2 = "images/fig_chungbuk_2.png"
imageBlob_cb2 = bucket.blob("chungbuk2.png")
imageBlob_cb2.upload_from_filename(imagePath_cb2)

# 전라남도 그래프
imagePath_jn1 = "images/fig_jeonnam_1.png"
imageBlob_jn1 = bucket.blob("jeonnam1.png")
imageBlob_jn1.upload_from_filename(imagePath_jn1)

imagePath_jn2 = "images/fig_jeonnam_2.png"
imageBlob_jn2 = bucket.blob("jeonnam2.png")
imageBlob_jn2.upload_from_filename(imagePath_jn2)

# 전라북도 그래프
imagePath_jb1 = "images/fig_jeonbuk_1.png"
imageBlob_jb1 = bucket.blob("jeonbuk1.png")
imageBlob_jb1.upload_from_filename(imagePath_jb1)

imagePath_jb2 = "images/fig_jeonbuk_2.png"
imageBlob_jb2 = bucket.blob("jeonbuk2.png")
imageBlob_jb2.upload_from_filename(imagePath_jb2)

# 경상남도 그래프
imagePath_gn1 = "images/fig_gyeongnam_1.png"
imageBlob_gn1 = bucket.blob("gyeongnam1.png")
imageBlob_gn1.upload_from_filename(imagePath_gn1)

imagePath_gn2 = "images/fig_gyeongnam_2.png"
imageBlob_gn2 = bucket.blob("gyeongnam2.png")
imageBlob_gn2.upload_from_filename(imagePath_gn2)

# 경상북도 그래프
imagePath_gb1 = "images/fig_gb_1.png"
imageBlob_gb1 = bucket.blob("gyeongbuk1.png")
imageBlob_gb1.upload_from_filename(imagePath_gb1)

imagePath_gb2 = "images/fig_gb_2.png"
imageBlob_gb2 = bucket.blob("gyeongbuk2.png")
imageBlob_gb2.upload_from_filename(imagePath_gb2)

# 강원도 그래프
imagePath_gw1 = "images/fig_gangwon_1.png"
imageBlob_gw1 = bucket.blob("gangwon1.png")
imageBlob_gw1.upload_from_filename(imagePath_gw1)

imagePath_gw2 = "images/fig_gangwon_2.png"
imageBlob_gw2 = bucket.blob("gangwon2.png")
imageBlob_gw2.upload_from_filename(imagePath_gw2)

# 제주도 그래프
imagePath_j1 = "images/fig_jeju_1.png"
imageBlob_j1 = bucket.blob("jeju1.png")
imageBlob_j1.upload_from_filename(imagePath_j1)

imagePath_j2 = "images/fig_jeju_2.png"
imageBlob_j2 = bucket.blob("jeju2.png")
imageBlob_j2.upload_from_filename(imagePath_j2)



