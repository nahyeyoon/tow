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
import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 경로 (업로드 없이 자동 로딩)
file_path = '202505_202505_연령별인구현황_월간.csv'

# EUC-KR로 인코딩된 CSV 파일 불러오기
df = pd.read_csv(file_path, encoding='euc-kr')

# 연령별 인구 열 추출
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
total_col = '2025년05월_계_총인구수'

# 연령 라벨 추출 (100세 이상 → 100으로 치환)
age_labels = [col.replace('2025년05월_계_', '').replace('세', '').replace('100 이상', '100') for col in age_columns]

# 총인구수 숫자형 변환
df['총인구수'] = df[total_col].str.replace(',', '').astype(int)

# 전처리된 데이터프레임 생성
age_df = df[['행정구역'] + age_columns + [total_col]].copy()
age_df.columns = ['행정구역'] + age_labels + ['총인구수']

# 상위 5개 행정구역 추출
top5 = age_df.sort_values(by='총인구수', ascending=False).head(5)
top5.set_index('행정구역', inplace=True)

# 연령별 인구만 추출하고 숫자 정렬
age_only_df = top5.drop(columns='총인구수').transpose()
age_only_df.index = age_only_df.index.astype(int)
age_only_df.sort_index(inplace=True)

# 🔍 원본 데이터 표시
st.subheader("📄 원본 데이터 (일부)")
st.dataframe(df.head(10))


# 📋 전처리된 상위 5개 행정구역 데이터
st.subheader("🏙️ 상위 5개 행정구역 인구 데이터")
st.dataframe(top5)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌸 인구 분석 리포트 – 빅데이터 인사이트")

# 파일 불러오기
file_path = '202505_202505_연령별인구현황_월간.csv'
df = pd.read_csv(file_path, encoding='euc-kr')

# 전처리
total_col = '2025년05월_계_총인구수'
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
df['총인구수'] = df[total_col].str.replace(',', '').astype(int)
df['행정구역'] = df['행정구역'].str.replace(r'\s*\(.*\)', '', regex=True)

# 연령 라벨 정리
age_labels = [col.replace('2025년05월_계_', '').replace('세', '').replace('100 이상', '100') for col in age_columns]
age_df = df[['행정구역'] + age_columns + [total_col]].copy()
age_df.columns = ['행정구역'] + age_labels + ['총인구수']

# 상위 5개 지역
top5 = age_df.sort_values(by='총인구수', ascending=False).head(5).set_index('행정구역')
age_only_df = top5.drop(columns='총인구수').transpose()
age_only_df.index = age_only_df.index.astype(int)

# 🎯 연령대 그룹핑
bins = [0, 19, 39, 59, 79, 120]
labels = ['0-19세', '20-39세', '40-59세', '60-79세', '80세 이상']
age_groups = pd.cut(age_only_df.index, bins=bins, labels=labels, right=True)

# 📊 각 지역 연령대 비율 시각화
st.subheader("🧁 지역별 연령대 비율 그래프")
for region in age_only_df.columns:
    group_sum = age_only_df[region].groupby(age_groups).sum()
    fig, ax = plt.subplots()
    group_sum.plot(kind='bar', color='pink', ax=ax)
    plt.title(f"{region} 연령대 분포")
    plt.ylabel("인구 수")
    st.pyplot(fig)

# 🧓 고령화 지수 분석
st.subheader("🌟 고령화 지수 분석 (65세 이상 / 14세 이하 × 100)")

results = {}
for region in age_only_df.columns:
    over_65 = age_only_df.loc[age_only_df.index >= 65, region].sum()
    under_15 = age_only_df.loc[age_only_df.index <= 14, region].sum()
    aging_index = round((over_65 / under_15) * 100, 2) if under_15 != 0 else None
    results[region] = aging_index

aging_df = pd.DataFrame.from_dict(results, orient='index', columns=['고령화지수']).sort_values(by='고령화지수', ascending=False)
st.dataframe(aging_df)

# 💡 요약 인사이트
st.subheader("🧠 요약 인사이트")
for region, value in results.items():
    if value is None:
        st.markdown(f"- {region}: 고령화 지수 계산 불가 (14세 이하 인구 0)")
    elif value > 100:
        st.markdown(f"- {region}는 고령 인구가 더 많아요 🧓 (고령화 지수: {value})")
    else:
        st.markdown(f"- {region}는 젊은 층 인구가 많아요 👶 (고령화 지수: {value})")
