import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- 파일 로딩 및 전처리 ---
@st.cache_data
def load_data():
    file_path = "202505_202505_연령별인구현황_월간.csv"
    df = pd.read_csv(file_path, encoding='euc-kr')
    df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(",", "").astype(int)
    return df

df = load_data()
top5 = df.sort_values(by='총인구수', ascending=False).head(5)

coords = {
    '경기도  (4100000000)': (37.4138, 127.5183),
    '서울특별시  (1100000000)': (37.5665, 126.9780),
    '부산광역시  (2600000000)': (35.1796, 129.0756),
    '경상남도  (4800000000)': (35.4606, 128.2132),
    '인천광역시  (2800000000)': (37.4563, 126.7052),
}

# --- 페이지 선택 ---
st.sidebar.title("페이지 선택")
page = st.sidebar.radio("원하는 화면을 선택하세요:", ["지도 보기", "데이터 보기"])

# --- 지도 페이지 ---
if page == "지도 보기":
    st.title("🗺️ 인구수 상위 5개 지역 지도 시각화")
    m = folium.Map(location=[36.5, 127.8], zoom_start=7)

    for _, row in top5.iterrows():
        region = row['행정구역']
        if region in coords:
            lat, lon = coords[region]
            folium.CircleMarker(
                location=(lat, lon),
                radius=15,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.4,
                tooltip=f"{region}<br>총인구수: {row['총인구수']:,}명"
            ).add_to(m)

    st_folium(m, width=700, height=500)

# --- 데이터 페이지 ---
elif page == "데이터 보기":
    st.title("📊 인구수 상위 5개 행정구역 데이터")
    st.dataframe(top5[['행정구역', '총인구수']])
