import requests
import pandas as pd
import os
from datetime import datetime

API_KEY = os.getenv("DATA_API_KEY")  # 환경변수로 관리
API_URL = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire"

def fetch_data(page_no=1, num_of_rows=100):
    params = {
        "serviceKey": API_KEY,
        "STAGE1": "서울특별시",  # 지역 단위로 반복 가능
        "pageNo": page_no,
        "numOfRows": num_of_rows,
        "_type": "json"
    }
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()
    items = data['response']['body']['items']['item']
    return pd.DataFrame(items)

def save_data():
    df = fetch_data()
    df['update_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/cached_data.csv", index=False)
    print(f"[{datetime.now()}] Data saved with {len(df)} records")

if __name__ == "__main__":
    save_data()

import pandas as pd

def load_data():
    df = pd.read_csv("data/cached_data.csv")
    grades = pd.read_csv("data/hospital_grades.csv")
    df = df.merge(grades, on="hpid", how="left")
    df["avail_rate"] = (df["hvec"] / (df["hvec"] + df["hvoc"])).fillna(0)
    return df
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(page_title="응급실 병상 대시보드", layout="wide")

st.title("🏥 전국 응급실 병상 가용률 실시간 대시보드")

df = load_data()

# 필터
col1, col2 = st.columns(2)
with col1:
    grade_filter = st.multiselect("병원 등급", ["2차", "3차"], default=["2차", "3차"])
with col2:
    region_filter = st.selectbox("지역 선택", sorted(df["dutyAddr"].str[:2].unique()))

filtered = df[(df["grade"].isin(grade_filter)) & (df["dutyAddr"].str.startswith(region_filter))]

st.metric("병원 수", len(filtered))
st.metric("평균 가용률", f"{filtered['avail_rate'].mean()*100:.1f}%")

# 차트
fig = px.bar(filtered, x="dutyName", y="avail_rate", color="grade",
             title=f"{region_filter} 지역 병상 가용률",
             labels={"avail_rate": "가용률", "dutyName": "병원명"})
st.plotly_chart(fig, use_container_width=True)

# 지도
st.subheader("🗺️ 병원 위치 및 가용률 지도")
st.map(filtered.rename(columns={"wgs84Lat": "lat", "wgs84Lon": "lon"}))

name: Update Data

on:
  schedule:
    - cron: "*/30 * * * *"   # 30분마다 실행
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Fetch and Save Data
        env:
          DATA_API_KEY: ${{ secrets.DATA_API_KEY }}
        run: python fetch_data.py

      - name: Commit Updated Data
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add data/cached_data.csv
          git commit -m "Auto-update data"
          git push
