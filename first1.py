import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 🎨 페이지 설정
st.set_page_config(page_title="🌸 2025년 5월 인구 지도", layout="centered")

# 🐻‍❄️ 타이틀
st.title("🌸 2025년 5월 기준 연령별 인구 현황 분석")
st.caption("🧁 상위 5개 행정구역의 인구를 귀여운 핑크 원으로 지도에 표시해봤어요!")

# 📂 파일 경로
file_path = '202505_202505_연령별인구현황_월간.csv'

# 📥 데이터 불러오기 (EUC-KR 인코딩)
df = pd.read_csv(file_path, encoding='euc-kr')

# 🧹 전처리: 연령별 컬럼, 총인구수
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
total_col = '2025년05월_계_총인구수'
age_labels = [col.replace('2025년05월_계_', '').replace('세', '').replace('100 이상', '100') for col in age_columns]
df['총인구수'] = df[total_col].str.replace(',', '').astype(int)

# 🧼 괄호 숫자 제거한 행정구역 컬럼 생성
df['행정구역_정제'] = df['행정구역'].str.replace(r'\s*\(.*\)', '', regex=True)

# 📊 전처리 테이블
age_df = df[['행정구역', '행정구역_정제'] + age_columns + [total_col]].copy()
age_df.columns = ['행정구역', '행정구역_정제'] + age_labels + ['총인구수']

# 👑 상위 5개 행정구역
top5 = age_df.sort_values(by='총인구수', ascending=False).head(5)
top5.set_index('행정구역_정제', inplace=True)

# 📈 연령별 인구 테이블
age_only_df = top5.drop(columns=['행정구역', '총인구수']).transpose()
age_only_df.index = age_only_df.index.astype(int)
age_only_df.sort_index(inplace=True)

# 📍 수동 위치 설정 (괄호 제거된 이름 기준)
region_coords = {
    '경기도': (37.4138, 127.5183),
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경상남도': (35.4606, 128.2132),
    '인천광역시': (37.4563, 126.7052),
}

# 🗺️ folium 지도 생성
m = folium.Map(location=[36.5, 127.8], zoom_start=7)

for region in top5.index:
    if region in region_coords:
        lat, lon = region_coords[region]
        pop = top5.loc[region, '총인구수']
        folium.CircleMarker(
            location=[lat, lon],
            radius=15,
            color='pink',
            fill=True,
            fill_color='pink',
            fill_opacity=0.4,
            tooltip=folium.Tooltip(f"🌆 <b>{region}</b><br>👥 인구: <b>{pop:,}명</b>", sticky=True)
        ).add_to(m)

# 💗 지도 출력
st.subheader("🗺️ 귀여운 인구 지도")
st_folium(m, width=700, height=500)

# 📈 그래프 출력
st.subheader("📊 연령별 인구 선 그래프 (상위 5개 행정구역)")
for region in age_only_df.columns:
    st.markdown(f"### 🏙️ {region}")
    st.line_chart(age_only_df[[region]])

# 📋 원본 데이터
with st.expander("📄 원본 데이터 일부 보기"):
    st.dataframe(df[['행정구역', total_col]].head(10))

# 🧾 전처리된 상위 5개 데이터
st.subheader("🌟 전처리된 상위 5개 행정구역 인구 데이터")
st.dataframe(top5[['총인구수']])
