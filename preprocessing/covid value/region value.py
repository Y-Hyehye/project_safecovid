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
url='http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=pg8wihCfmYf9Euwqa0CoiZfui3IMOfk1kliZfV46KSIm3pDqCHQZBNVRyrNCGvbPYUYwsCmB5ULMPvlH2aT4Ag%3D%3D&pageNo=1&numOfRows=&startCreateDt=&endCreateDt=&'

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
rescode = response.getcode()
response_body = response.read()
data=response_body.decode('utf-8')
dict_data = xmltodict.parse(data)
json_data = json.dumps(dict_data)
result = json.loads(json_data)

data=result['response']['body']['items']['item']

# df(DataFrame)으로 정의
df=pd.DataFrame(data)

# 데이터 전처리 (필요한 부분만 추출)
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

# 서울 확진자(누적), 지역발생수, 해외유입수
seoul_deicdeCnt=df_safe_seoul['defCnt'].iloc[0]
seoul_local_defCnt=df_safe_seoul['localOccCnt'].iloc[0]
seoul_overflow_defCnt=df_safe_seoul['overFlowCnt'].iloc[0]

# 경기도 확진자(누적), 지역발생수, 해외유입수
gg_deicdeCnt=df_safe_gg['defCnt'].iloc[0]
gg_local_defCnt=df_safe_gg['localOccCnt'].iloc[0]
gg_overflow_defCnt=df_safe_gg['overFlowCnt'].iloc[0]

# 충남 확진자(누적), 지역발생수, 해외유입수
chungnam_deicdeCnt=df_safe_chungnam['defCnt'].iloc[0]
chungnam_local_defCnt=df_safe_chungnam['localOccCnt'].iloc[0]
chungnam_overflow_defCnt=df_safe_chungnam['overFlowCnt'].iloc[0]

# 충북 확진자(누적), 지역발생수, 해외유입수
chungbuk_deicdeCnt=df_safe_chungbuk['defCnt'].iloc[0]
chungbuk_local_defCnt=df_safe_chungbuk['localOccCnt'].iloc[0]
chungbuk_overflow_defCnt=df_safe_chungbuk['overFlowCnt'].iloc[0]

# 전남 확진자(누적), 지역발생수, 해외유입수
jeonnam_deicdeCnt=df_safe_jeonnam['defCnt'].iloc[0]
jeonnam_local_defCnt=df_safe_jeonnam['localOccCnt'].iloc[0]
jeonnam_overflow_defCnt=df_safe_jeonnam['overFlowCnt'].iloc[0]

# 전북 확진자(누적), 지역발생수, 해외유입수
jeonbuk_deicdeCnt=df_safe_jeonbuk['defCnt'].iloc[0]
jeonbuk_local_defCnt=df_safe_jeonbuk['localOccCnt'].iloc[0]
jeonbuk_overflow_defCnt=df_safe_jeonbuk['overFlowCnt'].iloc[0]

# 경남 확진자(누적), 지역발생수, 해외유입수
gyeongnam_deicdeCnt=df_safe_gyeongnam['defCnt'].iloc[0]
gyeongnam_local_defCnt=df_safe_gyeongnam['localOccCnt'].iloc[0]
gyeongnam_overflow_defCnt=df_safe_gyeongnam['overFlowCnt'].iloc[0]

# 경북 확진자(누적), 지역발생수, 해외유입수
gb_deicdeCnt=df_safe_gb['defCnt'].iloc[0]
gb_local_defCnt=df_safe_gb['localOccCnt'].iloc[0]
gb_overflow_defCnt=df_safe_gb['overFlowCnt'].iloc[0]

# 강원 확진자수(누적), 지역발생수, 해외유입수
gangwon_deicdeCnt=df_safe_gangwon['defCnt'].iloc[0]
gangwon_local_defCnt=df_safe_gangwon['localOccCnt'].iloc[0]
gangwon_overflow_defCnt=df_safe_gangwon['overFlowCnt'].iloc[0]

# 제주 확진자수(누적), 지역발생수, 해외유입수
jeju_deicdeCnt=df_safe_jeju['defCnt'].iloc[0]
jeju_local_defCnt=df_safe_jeju['localOccCnt'].iloc[0]
jeju_overflow_defCnt=df_safe_jeju['overFlowCnt'].iloc[0]


# Firebase Realtime Database 연결
cred = credentials.Certificate('mykey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://project-48b89.firebaseio.com/'
})

# 각 위치를 생성하고 키, 값형태로 확진자수, 지역발생수, 해외유입수 데이터 저장
# 서울
dir = db.reference('local/seoul')
dir.update({'decide': seoul_deicdeCnt})
dir.update({'local_decide': seoul_local_defCnt})
dir.update({'overflow_decide': seoul_overflow_defCnt})

# 경기
dir = db.reference('local/gyeounggi')
dir.update({'decide': gg_deicdeCnt})
dir.update({'local_decide': gg_local_defCnt})
dir.update({'overflow_decide': gg_overflow_defCnt})

# 충남
dir = db.reference('local/chungnam')
dir.update({'decide': chungnam_deicdeCnt})
dir.update({'local_decide': chungnam_local_defCnt})
dir.update({'overflow_decide': chungnam_overflow_defCnt})

# 충북
dir = db.reference('local/chungbuk')
dir.update({'decide': chungbuk_deicdeCnt})
dir.update({'local_decide': chungbuk_local_defCnt})
dir.update({'overflow_decide': chungbuk_overflow_defCnt})

# 전남
dir = db.reference('local/jeonnam')
dir.update({'decide': jeonnam_deicdeCnt})
dir.update({'local_decide': jeonnam_local_defCnt})
dir.update({'overflow_decide': jeonnam_overflow_defCnt})

# 전북
dir = db.reference('local/jeonbuk')
dir.update({'decide': jeonbuk_deicdeCnt})
dir.update({'local_decide': jeonbuk_local_defCnt})
dir.update({'overflow_decide': jeonbuk_overflow_defCnt})

# 경남
dir = db.reference('local/gyeongnam')
dir.update({'decide': gyeongnam_deicdeCnt})
dir.update({'local_decide': gyeongnam_local_defCnt})
dir.update({'overflow_decide': gyeongnam_overflow_defCnt})

# 경북
dir = db.reference('local/gyeongbuk')
dir.update({'decide': gb_deicdeCnt})
dir.update({'local_decide': gb_local_defCnt})
dir.update({'overflow_decide': gb_overflow_defCnt})

# 강원
dir = db.reference('local/gangwon')
dir.update({'decide': gangwon_deicdeCnt})
dir.update({'local_decide': gangwon_local_defCnt})
dir.update({'overflow_decide': gangwon_overflow_defCnt})

# 제주
dir = db.reference('local/jeju')
dir.update({'decide': jeju_deicdeCnt})
dir.update({'local_decide': jeju_local_defCnt})
dir.update({'overflow_decide': jeju_overflow_defCnt})