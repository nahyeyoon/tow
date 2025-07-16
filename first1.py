import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 경로
file_path = '202505_202505_연령별인구현황_월간.csv'

# 데이터 불러오기 (EUC-KR 인코딩)
df = pd.read_csv(file_path, encoding='euc-kr')

# 연령별 인구 컬럼 추출
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
total_col = '2025년05월_계_총인구수'

# 연령 라벨 정리 (100세 이상 → 100)
age_labels = [col.replace('2025년05월_계_', '').replace('세', '').replace('100 이상', '100') for col in age_columns]

# 총인구수 숫자형으로 변환
df['총인구수'] = df[total_col].str.replace(',', '').astype(int)

# 전처리된 데이터프레임 생성
age_df = df[['행정구역'] + age_columns + [total_col]].copy()
age_df.columns = ['행정구역'] + age_labels + ['총인구수']

# 총인구수 기준 상위 5개 행정구역 추출
top5 = age_df.sort_values(by='총인구수', ascending=False).head(5)
top5.set_index('행정구역', inplace=True)

# 연령별 인구만 추출 후 전치(transpose)
age_only_df = top5.drop(columns='총인구수').transpose()
age_only_df.index = age_only_df.index.astype(int)
age_only_df.sort_index(inplace=True)

# 🔍 원본 데이터 출력
st.subheader("📄 원본 데이터 (일부 보기)")
st.dataframe(df.head(10))

# 📈 행정구역별 개별 그래프 출력
st.subheader("📊 상위 5개 행정구역의 연령별 인구 선 그래프")

for region in age_only_df.columns:
    st.markdown(f"### 🏙️ {region}")
    st.line_chart(age_only_df[[region]])

# 📋 전처리된 데이터도 출력
st.subheader("🏙️ 상위 5개 행정구역 인구 데이터 (전처리 완료)")
st.dataframe(top5)
