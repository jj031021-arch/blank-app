import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="한국 코로나19 확진자 대시보드", layout="wide")

st.title("🦠 한국 코로나19 확진자 추이 대시보드")

# ✅ 인터넷 CSV URL (예시: 질병관리청 공개데이터)
DATA_URL = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df[df["Country"] == "Korea, South"]

df = load_data(DATA_URL)

# 날짜 형식 변환
df["Date"] = pd.to_datetime(df["Date"])

# 사이드바 필터
start_date = st.sidebar.date_input("시작 날짜", df["Date"].min())
end_date = st.sidebar.date_input("종료 날짜", df["Date"].max())

filtered = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

# 요약 통계
st.subheader("📊 주요 지표")
col1, col2, col3 = st.columns(3)
col1.metric("총 확진자", f"{filtered['Confirmed'].iloc[-1]:,}")
col2.metric("총 사망자", f"{filtered['Deaths'].iloc[-1]:,}")
col3.metric("총 회복자", f"{filtered['Recovered'].iloc[-1]:,}")

# 그래프 1: 확진자 추이
st.subheader("📈 확진자 추이")
st.line_chart(filtered.set_index("Date")[["Confirmed"]])

# 그래프 2: 사망자 추이
st.subheader("☠️ 사망자 추이")
st.line_chart(filtered.set_index("Date")[["Deaths"]])

# 데이터 미리보기
st.subheader("📋 데이터 미리보기")
st.dataframe(filtered.tail(10))

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="한국 코로나19 지도 대시보드", layout="wide")

st.title("🦠 한국 코로나19 확진자 지도 대시보드")

# ✅ 인터넷 URL 예시 (공공데이터포털 대신 공개 CSV 사용)
DATA_URL = "https://raw.githubusercontent.com/jooeungen/coronaboard_kr/master/kr_regional_daily.csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data(DATA_URL)

# 최신 날짜 데이터만 선택
latest_date = df["date"].max()
latest = df[df["date"] == latest_date]

st.sidebar.header("⚙️ 설정")
st.sidebar.write(f"현재 날짜: **{latest_date.date()}** 기준 데이터")
metric_type = st.sidebar.selectbox("표시할 지표 선택", ["confirmed", "deceased"])

# 지역 좌표 (간단 예시)
coords = {
    "서울": [37.5665, 126.9780],
    "부산": [35.1796, 129.0756],
    "대구": [35.8714, 128.6014],
    "인천": [37.4563, 126.7052],
    "광주": [35.1595, 126.8526],
    "대전": [36.3504, 127.3845],
    "울산": [35.5384, 129.3114],
    "세종": [36.4800, 127.2890],
    "경기": [37.4138, 127.5183],
    "강원": [37.8228, 128.1555],
    "충북": [36.6357, 127.4914],
    "충남": [36.5184, 126.8],
    "전북": [35.7175, 127.153],
    "전남": [34.8679, 126.991],
    "경북": [36.4919, 128.8889],
    "경남": [35.4606, 128.2132],
    "제주": [33.4996, 126.5312]
}

# 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 마커 추가
for _, row in latest.iterrows():
    region = row["region"]
    if region in coords:
        val = int(row[metric_type])
        folium.CircleMarker(
            location=coords[region],
            radius=max(5, val / 500),
            popup=f"{region}: {val:,}",
            color="red" if metric_type == "confirmed" else "black",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

# Streamlit에 Folium 지도 표시
st.subheader("🗺️ 지역별 확진자/사망자 지도")
st_folium(m, width=900, height=600)

# 바 차트 표시
st.subheader("📊 지역별 데이터")
chart_data = latest.set_index("region")[[metric_type]]
st.bar_chart(chart_data.sort_values(by=metric_type, ascending=False))

# 데이터 미리보기
st.subheader("📋 원본 데이터 미리보기")
st.dataframe(latest)

import math

radius = max(5, math.log(val + 1) * 2)
