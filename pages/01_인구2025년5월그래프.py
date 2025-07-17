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
