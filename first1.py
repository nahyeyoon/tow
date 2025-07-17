import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 🌸 페이지 제목
st.set_page_config(page_title="인구 지도", layout="centered")
st.title("🌸 2025년 5월 상위 5개 지역 인구 지도 🌸")

# 📂 CSV 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 🧼 전처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)
top5 = df.sort_values(by='총인구수', ascending=False).head(5).copy()
top5['행정구역'] = top5['행정구역'].str.replace(r'\s*\(.*\)', '', regex=True)

# 📍 좌표 지정 (직접 입력)
coords = {
    '경기도': (37.4138, 127.5183),
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경상남도': (35.4606, 128.2132),
    '인천광역시': (37.4563, 126.7052),
}

# 🗺️ 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles="CartoDB Positron")

for _, row in top5.iterrows():
    region = row['행정구역']
    if region in coords:
        lat, lon = coords[region]
        pop = row['총인구수']
        
        # 🎀 원형 마커
        folium.CircleMarker(
            location=[lat, lon],
            radius=15,
            color='#FF69B4',
            fill=True,
            fill_color='#FFB6C1',
            fill_opacity=0.4,
            tooltip=f"🌸 {region} - 👩‍👩‍👧‍👦 {pop:,}명"
        ).add_to(m)
        
        # 👩‍👩‍👧‍👦 인구 수 텍스트 표시 (약간 위에)
        folium.map.Marker(
            [lat + 0.12, lon],
            icon=folium.DivIcon(html=f"""
                <div style="font-size: 13px; color: #FF1493; font-weight: bold; text-align: center;">
                    👩‍👩‍👧‍👦 {pop:,}
                </div>
            """)
        ).add_to(m)

# 🎨 지도 출력
st_folium(m, width=700, height=500)
