import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="한국 병원 현황 대시보드", layout="wide")

st.title("🏥 한국 병원 현황 대시보드")

@st.cache_data
def load_data():
    return pd.read_csv("hospitals.csv")

df = load_data()

# 사이드바 필터
cities = st.sidebar.multiselect("도시 선택", df["city"].unique(), default=df["city"].unique())
types = st.sidebar.multiselect("병원 유형 선택", df["type"].unique(), default=df["type"].unique())

filtered = df[df["city"].isin(cities) & df["type"].isin(types)]

# 통계
st.subheader("📊 병원 통계 요약")
col1, col2, col3 = st.columns(3)
col1.metric("총 병원 수", len(filtered))
col2.metric("총 병상 수", int(filtered["beds"].sum()))
col3.metric("총 환자 수", int(filtered["patients"].sum()))

# 시각화 1: 도시별 병상 수
st.subheader("🏙️ 도시별 병상 수")
st.bar_chart(filtered.groupby("city")["beds"].sum())

# 시각화 2: 병원 유형별 환자 수
st.subheader("🧑‍⚕️ 병원 유형별 환자 수")
st.bar_chart(filtered.groupby("type")["patients"].sum())

# 데이터 미리보기
st.subheader("📋 병원 데이터 미리보기")
st.dataframe(filtered)

