import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="전국 병원 정보 대시보드", layout="wide")

st.title("🏥 전국 병원 정보 대시보드 (샘플 데이터)")
st.write("이 대시보드는 API 없이 CSV 데이터로 작동하는 예시입니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("data/hospitals.csv")
    return df

df = load_data()

# 필터 영역
st.sidebar.header("🔍 필터")
region_filter = st.sidebar.text_input("지역(예: 서울특별시)", "서울")
grade_filter = st.sidebar.multiselect("병원 등급 선택", ["1차", "2차", "3차"], default=["2차", "3차"])

filtered = df[df["address"].str.contains(region_filter)]
filtered = filtered[filtered["grade"].isin(grade_filter)]

# 요약 지표
col1, col2 = st.columns(2)
col1.metric("표시 중인 병원 수", len(filtered))
col2.metric("선택된 등급", ", ".join(grade_filter))

# 병원 목록 표시
st.subheader("🏥 병원 목록")
st.dataframe(filtered[["name", "address", "grade", "open_time", "close_time"]])

# 등급별 병원 수 시각화
st.subheader("📊 병원 등급 분포")
fig = px.histogram(df, x="grade", title="전국 병원 등급 분포")
st.plotly_chart(fig, use_container_width=True)

# 지도 표시
st.subheader("🗺️ 병원 위치")
st.map(filtered.rename(columns={"lat": "latitude", "lon": "longitude"}))
