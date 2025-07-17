import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 🧸 페이지 꾸미기
st.set_page_config(page_title="🌸 인구수 지도", page_icon="🗺️", layout="centered")

# 🐥 제목
st.title("🌸 2025년 5월 기준 인구수 상위 5개 지역 지도")
st.markdown("##### 👑 상위 5개 행정구역의 인구를 귀엽게 지도에 표시했어요!")

# 🐰 CSV 파일 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 💖 총인구수 숫자형으로 변환
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(",", "").astype(int)

# 🐣 상위 5개 지역만 추출
top5 = df.sort_values(by='총인구수', ascending=False).head(5).copy()

# 🎀 괄호 안 숫자 제거: '서울특별시  (1100000000)' → '서울특별시'
top5['행정구역'] = top5['행정구역'].str.replace(r'\s*\(.*\)', '', regex=True)

# 📍 좌표 직접 지정
coords = {
    '경기도': (37.4138, 127.5183),
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경상남도': (35.4606, 128.2132),
    '인천광역시': (37.4563, 126.7052),
}

# 🗺️ 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# 💕 핑크색 원형 마커 추가
for _, row in top5.iterrows():
    region = row['행정구역']
    pop = row['총인구수']
    if region in coords:
        lat, lon = coords[region]
        folium.CircleMarker(
            location=(lat, lon),
            radius=15,
            color='#ff69b4',  # 핫핑크
            fill=True,
            fill_color='#ffb6c1',  # 연핑크
            fill_opacity=0.5,
            tooltip=folium.Tooltip(f"<b>{region}</b><br>🧑‍🤝‍🧑 총인구수: <b>{pop:,}명</b>", sticky=True)
        ).add_to(m)

# 🖼️ 지도 출력
st_folium(m, width=720, height=500)

# 🧾 데이터 표시
with st.expander("📊 원본 데이터 보기"):
    st.dataframe(top5[['행정구역', '총인구수']], use_container_width=True)
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 타이틀
st.title("2025년 5월 기준 인구 수 기준 상위 5개 행정구역 지도 시각화")

# CSV 파일 경로
file_path = '202505_202505_연령별인구현황_월간.csv'

# CSV 데이터 읽기
df = pd.read_csv(file_path, encoding='euc-kr')

# 연령별 컬럼 필터링
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
total_col = '2025년05월_계_총인구수'

# 총인구수 숫자화
df['총인구수'] = df[total_col].str.replace(',', '').astype(int)

# 전처리: 총인구수 기준 상위 5개 추출
age_df = df[['행정구역', total_col]].copy()
age_df.columns = ['행정구역', '총인구수']
top5 = age_df.sort_values(by='총인구수', ascending=False).head(5)

# ▶ 위도/경도 수동 지정 (중심 좌표 기준)
coords = {
    '경기도  (4100000000)': (37.4138, 127.5183),
    '서울특별시  (1100000000)': (37.5665, 126.9780),
    '부산광역시  (2600000000)': (35.1796, 129.0756),
    '경상남도  (4800000000)': (35.4606, 128.2132),
    '인천광역시  (2800000000)': (37.4563, 126.7052),
}

# ▶ folium 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

# ▶ 마커 표시
for idx, row in top5.iterrows():
    region = row['행정구역']
    pop = row['총인구수']
    if region in coords:
        lat, lon = coords[region]
        folium.CircleMarker(
            location=(lat, lon),
            radius=15,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.4,
            tooltip=f"{region}<br>총인구수: {pop:,}명"
        ).add_to(m)

# ▶ Streamlit에 지도 출력
st.subheader("📍 지도에서 상위 5개 지역 확인하기")
st_folium(m, width=700, height=500)
