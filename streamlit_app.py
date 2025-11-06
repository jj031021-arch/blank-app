import os
import pandas as pd
from zipfile import ZipFile

# 폴더 구조 만들기
os.makedirs("hospital-dashboard/data", exist_ok=True)

# 가짜 병원 데이터 생성
data = [
    ["서울중앙의원", "서울특별시 종로구 종로 1", "1차", "09:00", "17:00", 37.572, 126.978],
    ["강남삼성병원", "서울특별시 강남구 테헤란로 123", "3차", "08:30", "18:00", 37.504, 127.048],
    ["한강의료원", "서울특별시 영등포구 여의대로 24", "2차", "09:00", "17:30", 37.527, 126.933],
    ["서울시민병원", "서울특별시 서초구 반포대로 45", "2차", "08:00", "17:30", 37.500, 127.010],
    ["동서울의원", "서울특별시 광진구 능동로 90", "1차", "09:00", "16:00", 37.547, 127.073],
    ["은평중앙병원", "서울특별시 은평구 통일로 715", "3차", "08:00", "18:00", 37.617, 126.922],
    ["서대문메디컬", "서울특별시 서대문구 연세로 12", "1차", "09:00", "17:00", 37.560, 126.940],
    ["강서성심병원", "서울특별시 강서구 공항대로 213", "2차", "09:00", "17:30", 37.561, 126.821],
    ["도봉의료센터", "서울특별시 도봉구 도봉로 612", "2차", "08:30", "17:30", 37.668, 127.045],
    ["양천서울병원", "서울특별시 양천구 목동로 330", "3차", "08:30", "18:00", 37.527, 126.870],
    ["송파우리의원", "서울특별시 송파구 중대로 65", "1차", "09:00", "16:30", 37.505, 127.116],
    ["노원성심병원", "서울특별시 노원구 동일로 1345", "2차", "08:30", "17:30", 37.653, 127.061],
    ["종로메디컬센터", "서울특별시 종로구 대학로 20", "1차", "09:00", "17:00", 37.579, 126.999],
    ["마포성모병원", "서울특별시 마포구 마포대로 44", "3차", "08:30", "17:30", 37.544, 126.950],
    ["동대문서울병원", "서울특별시 동대문구 왕산로 25", "2차", "09:00", "18:00", 37.574, 127.039],
    ["성북중앙의원", "서울특별시 성북구 보문로 37", "1차", "09:00", "17:00", 37.589, 127.018],
    ["관악서울의료원", "서울특별시 관악구 남부순환로 1636", "2차", "09:00", "17:30", 37.478, 126.951],
    ["서초서울병원", "서울특별시 서초구 서초대로 333", "3차", "08:00", "18:00", 37.495, 127.016],
    ["성동서울병원", "서울특별시 성동구 왕십리로 240", "2차", "09:00", "17:30", 37.563, 127.037],
    ["중랑의료원", "서울특별시 중랑구 신내로 156", "3차", "08:30", "17:30", 37.613, 127.098]
]

cols = ["name", "address", "grade", "open_time", "close_time", "lat", "lon"]
pd.DataFrame(data, columns=cols).to_csv("hospital-dashboard/data/hospitals.csv", index=False)

# Streamlit 코드 작성
app_code = """\
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="서울 병원 대시보드", layout="wide")
st.title("🏥 서울 병원 정보 대시보드 (샘플 데이터)")

@st.cache_data
def load_data():
    return pd.read_csv("data/hospitals.csv")

df = load_data()

st.sidebar.header("🔍 필터")
grade_filter = st.sidebar.multiselect("병원 등급", ["1차", "2차", "3차"], default=["2차", "3차"])
region_filter = st.sidebar.text_input("지역 검색", "서울")

filtered = df[df["address"].str.contains(region_filter)]
filtered = filtered[filtered["grade"].isin(grade_filter)]

st.metric("표시 중 병원 수", len(filtered))

st.subheader("🏥 병원 목록")
st.dataframe(filtered[["name", "address", "grade", "open_time", "close_time"]])

st.subheader("📊 병원 등급 분포")
fig = px.histogram(df, x="grade", title="병원 등급 분포")
st.plotly_chart(fig, use_container_width=True)

st.subheader("🗺️ 지도 보기")
st.map(filtered.rename(columns={"lat": "latitude", "lon": "longitude"}))
"""
with open("hospital-dashboard/app.py", "w") as f:
    f.write(app_code)

# requirements.txt
with open("hospital-dashboard/requirements.txt", "w") as f:
    f.write("streamlit\npandas\nplotly\n")

# README
with open("hospital-dashboard/README.md", "w") as f:
    f.write("# 🏥 서울 병원 대시보드\n\n"
            "이 프로젝트는 Streamlit Cloud에서 바로 실행 가능한 예시입니다.\n\n"
            "1️⃣ GitHub에 업로드\n\n"
            "2️⃣ Streamlit Cloud에서 app.py 지정하여 Deploy\n\n"
            "3️⃣ URL로 접속하여 대시보드 확인\n")

# zip 묶기
with ZipFile("hospital-dashboard.zip", "w") as z:
    for root, dirs, files in os.walk("hospital-dashboard"):
        for file in files:
            path = os.path.join(root, file)
            z.write(path, arcname=os.path.relpath(path, "hospital-dashboard"))

print("✅ hospital-dashboard.zip 생성 완료!")
