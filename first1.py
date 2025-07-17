import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="인구 지도 보기", layout="centered")
st.title("🌸 2025년 5월 업데이트 및 지도 시간 🌸")

# 데이터 로드
file_path = "202505_202505_\uc5f0\ub839\ubcc4\uc778\uad6c\ud604\ud669_\uc6d4\uac04.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 전체 인구수 수집
age_columns = [col for col in df.columns if col.startswith('2025\ub14405\uc6d4_\uacc4_') and '세' in col]
total_col = '2025\ub14405\uc6d4_\uacc4_\ucd1d\uc778\uad6c\uc218'

# 인구수 전처리
age_labels = [col.replace('2025\ub14405\uc6d4_\uacc4_', '').replace('세', '').replace('100 \uc774\uc0c1', '100') for col in age_columns]
df['총인구수'] = df[total_col].str.replace(',', '').astype(int)

# 포함 데이터 만들기
age_df = df[['행정구역'] + age_columns + [total_col]].copy()
age_df.columns = ['행정구역'] + age_labels + ['총인구수']
age_df['행정구역'] = age_df['행정구역'].str.replace(r'\s*\(.*\)', '', regex=True)

# 상위 5개 행정구역
top5 = age_df.sort_values(by='총인구수', ascending=False).head(5).copy()
top5.set_index('행정구역', inplace=True)

# 지도 정보
coords = {
    '경기도': (37.4138, 127.5183),
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경상남도': (35.4606, 128.2132),
    '인천광역시': (37.4563, 126.7052),
}

# 평기적 인구 지도 만들기
m = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles="CartoDB Positron")

for region, row in top5.iterrows():
    if region in coords:
        lat, lon = coords[region]
        pop = row['총인구수']

        # 폴리얼 원 표시
        folium.Circle(
            location=[lat, lon],
            radius=pop / 50,  # 만든 크기 조정
            color='#FF69B4',
            fill=True,
            fill_color='#FFB6C1',
            fill_opacity=0.4,
            tooltip=f"{region}: {pop:,}명"
        ).add_to(m)

        # 인구수 표시
        folium.map.Marker(
            [lat + 0.1, lon],
            icon=folium.DivIcon(html=f"""
                <div style='font-size: 12px; color: #FF1493; text-align: center;'>
                    👥 {pop:,}
                </div>
            """)
        ).add_to(m)

# 지도 보이기
st.subheader("🌸 상위 5개 행정구역 인구 지도 표시")
st_folium(m, width=700, height=500)

# 원본 데이터 보이게 하기
st.subheader("\ud83c\udf38 \uc6d0\ubcf8 \ub370\uc774\ud130 \ud45c\uc2dc")
st.dataframe(df.head())
