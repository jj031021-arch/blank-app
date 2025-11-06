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

import branca.colormap as cm

colormap = cm.linear.YlOrRd_09.scale(latest[metric_type].min(), latest[metric_type].max())
colormap.caption = "확진자 수"

for _, row in latest.iterrows():
    region = row["region"]
    if region in coords:
        val = int(row[metric_type])
        folium.CircleMarker(
            location=coords[region],
            radius=max(5, math.log(val + 1) * 2),
            popup=f"{region}: {val:,}",
            color=colormap(val),
            fill=True,
            fill_color=colormap(val),
            fill_opacity=0.7,
        ).add_to(m)

m.add_child(colormap)

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

