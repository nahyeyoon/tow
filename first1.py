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

# 📊 선 그래프
st.subheader("📈 연령별 인구 선 그래프 (상위 5개 행정구역)")
st.line_chart(age_only_df)

# 📋 전처리된 상위 5개 행정구역 데이터
st.subheader("🏙️ 상위 5개 행정구역 인구 데이터")
st.dataframe(top5)
