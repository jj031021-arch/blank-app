import streamlit as st
import pandas as pd
import plotly.express as px
name,address,grade,open_time,close_time,lat,lon
서울대병원,서울특별시 종로구 대학로 101,3차,08:00,18:00,37.579,126.999
강북삼성병원,서울특별시 종로구 새문안로 29,2차,08:30,17:30,37.570,126.970
서울성모병원,서울특별시 서초구 반포대로 222,3차,09:00,18:00,37.501,127.005
고려대병원,서울특별시 성북구 안암로 145,2차,08:30,17:30,37.589,127.028
중앙의원,서울특별시 마포구 신촌로 12,1차,09:00,16:00,37.551,126.936

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
