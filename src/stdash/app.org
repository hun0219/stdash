import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime as dt

st.title('CNN JOB MON')

# 데이터 로드
def load_data():
    url = 'http://43.202.66.118:8077/all'
    r = requests.get(url)
    d = r.json()

    return d

# 데이터 가져오기
data = load_data()
# 데이터 프레임 생성
df = pd.DataFrame(data)

df

# TODO
# request_time, prediction_time을 이용해 '%Y-%m-%d %H' 형식
# 즉 시간별 GROUPBY COUNT 하여 plt 차트 그려보기

# request_time 컬럼을 datetime 형식으로 변환
df['request_time'] = pd.to_datetime(df['request_time'])
# 시간별 그룹화를 위해 'request_time' 시간(h) 추출
df['h_time'] = df['request_time'].dt.strftime('%Y-%m-%d %H')
# 시간별 요청 횟수 그룹화
h_counts = df.groupby('h_time').size()

# 데이터 시각화
#plt.figure(figsize=(10, 6))
h_counts.plot(kind='bar')
h_counts.plot(kind='line', color='red', marker='o')
plt.title('Number of Requests by Hour')
plt.xlabel('date time')
plt.ylabel('request time')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# 스트리밋 화면에 그리기
st.pyplot(plt)
