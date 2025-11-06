import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(page_title="한국 코로나19 확진자 대시보드", layout="wide")
st.markdown("""
    <style>
    .main-title { font-size:2.2em; font-weight:bold; color:#2C3E50; }
    .section-title { font-size:1.4em; margin-top:30px; color:#34495E; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🦠 한국 코로나19 확진자 추이 대시보드</p>', unsafe_allow_html=True)
st.write("출처: Johns Hopkins University (datasets/covid-19)")

# -----------------------------
# 데이터 불러오기
# -----------------------------
DATA_URL = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df = df[df["Country"] == "Korea, South"]
    df["Date"] = pd.to_datetime(df["Date"])
    df["DailyConfirmed"] = df["Confirmed"].diff().fillna(0)
    df["DailyDeaths"] = df["Deaths"].diff().fillna(0)
    df["DailyRecovered"] = df["Recovered"].diff().fillna(0)
    return df

df = load_data(DATA_URL)

# -----------------------------
# 사이드바 필터
# -----------------------------
st.sidebar.header("⚙️ 필터 설정")

start_date = st.sidebar.date_input("시작 날짜", df["Date"].min())
end_date = st.sidebar.date_input("종료 날짜", df["Date"].max())

metric_mode = st.sidebar.radio("표시 방식 선택", ["누적 (Cumulative)", "일별 (Daily Increase)"])

filtered = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

# -----------------------------
# 주요 지표
# -----------------------------
st.markdown('<p class="section-title">📊 주요 지표</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("총 확진자", f"{filtered['Confirmed'].iloc[-1]:,}",
            f"+{int(filtered['DailyConfirmed'].iloc[-1]):,}")
col2.metric("총 사망자", f"{filtered['Deaths'].iloc[-1]:,}",
            f"+{int(filtered['DailyDeaths'].iloc[-1]):,}")
col3.metric("총 회복자", f"{filtered['Recovered'].iloc[-1]:,}",
            f"+{int(filtered['DailyRecovered'].iloc[-1]):,}")

# -----------------------------
# 그래프 섹션
# -----------------------------
st.markdown('<p class="section-title">📈 코로나19 추이</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["확진자", "사망자", "회복자"])

if metric_mode == "누적 (Cumulative)":
    y_cols = ["Confirmed", "Deaths", "Recovered"]
else:
    y_cols = ["DailyConfirmed", "DailyDeaths", "DailyRecovered"]

# 확진자 탭
with tab1:
    st.line_chart(filtered.set_index("Date")[[y_cols[0]]])

# 사망자 탭
with tab2:
    st.line_chart(filtered.set_index("Date")[[y_cols[1]]])

# 회복자 탭
with tab3:
    st.line_chart(filtered.set_index("Date")[[y_cols[2]]])

# -----------------------------
# 추가 시각화 (Matplotlib 커스텀)
# -----------------------------
st.markdown('<p class="section-title">📉 확진자 및 사망자 추이 비교</p>', unsafe_allow_html=True)

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(filtered["Date"], filtered["Confirmed"], label="확진자", color="tomato")
ax.plot(filtered["Date"], filtered["Deaths"], label="사망자", color="black")
ax.set_title("확진자 vs 사망자 추이", fontsize=13)
ax.set_xlabel("날짜")
ax.set_ylabel("인원 수")
ax.legend()
st.pyplot(fig)

# -----------------------------
# 데이터 미리보기
# -----------------------------
st.markdown('<p class="section-title">📋 데이터 미리보기</p>', unsafe_allow_html=True)
st.dataframe(filtered.tail(10))
