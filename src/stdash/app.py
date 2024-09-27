import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime as dt
import os

st.title('요청자, 처리자 불균형')
st.subheader('Requests & Predictioner 데이터가 같으면 True')

# 데이터 로드
def load_data():
    DB = os.getenv("DB")
    DB_PORT = os.getenv("DB_PORT")
    url = f'http://{DB}:{DB_PORT}/all'
    r = requests.get(url)
    d = r.json()

    return d

# 데이터 가져오기
data = load_data()
# 데이터 프레임 생성
df = pd.DataFrame(data)

#df

# TODO
# request_time, prediction_time을 이용해 '%Y-%m-%d %H' 형식
# 즉 시간별 GROUPBY COUNT 하여 plt 차트 그려보기

# request_time 컬럼을 datetime 형식으로 변환
df['request_time'] = pd.to_datetime(df['request_time'])
# 시간별 그룹화를 위해 'request_time' 시간(h) 추출
df['h_time'] = df['request_time'].dt.strftime('%Y-%m-%d %H')
df['n_model'] = df['prediction_model'].str.contains(r'n[0-9]', regex=True)
# 시간별 요청 횟수 그룹화
h_counts = df.groupby(['h_time', 'n_model']).size()

# 데이터 시각화
plt.figure(figsize=(10, 6))

# 멀티인덱스를 unstack()으로 풀어서 막대그래프 형식에 맞게 변환
grouped_counts_unstacked = h_counts.unstack(fill_value=0)

# 그래프 그리기
ax = grouped_counts_unstacked.plot(kind='bar', figsize=(12, 6))

# 그래프 위에 카운터 숫자 출력
for p in ax.patches:
    ax.annotate(str(p.get_height()),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom',
                fontsize=10,
                color='black',
                rotation=0)

#h_counts.plot(kind='bar')
#h_counts.plot(kind='line', color='red', marker='o')
plt.title('Compare Requester and Predictioner')
plt.xlabel('Requests & Predictioner')
plt.ylabel('comparison Count')
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# 스트리밋 출력
st.pyplot(plt)
