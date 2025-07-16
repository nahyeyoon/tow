import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 파일 업로드
uploaded_file = st.file_uploader("202505_202505_연령별인구현황_월간.csv (EUC-KR 인코딩)", type=["csv"])
if uploaded_file is not None:
    try:
        # 데이터 불러오기
        df = pd.read_csv(202505_202505_연령별인구현황_월간.csv, encoding='euc-kr')

        st.subheader("원본 데이터")
        st.dataframe(df)

        # 필요한 열 필터링
        # '2025년05월_계_'로 시작하는 열을 연령별 인구 열로 간주
        age_columns = [col for col in df.columns if col.startswith('2025년05월_계_')]
        total_col = '총인구수'

        # 연령 추출: '2025년05월_계_0세' -> '0'
        age_labels = [col.replace('2025년05월_계_', '').replace('세', '') for col in age_columns]

        # 연령별 인구 + 총인구수로 새로운 DataFrame 생성
        age_df = df[['행정구역'] + age_columns + [total_col]].copy()
        age_df.columns = ['행정구역'] + age_labels + ['총인구수']

        # 총인구수 기준 상위 5개 행정구역 선택
        top5 = age_df.sort_values(by='총인구수', ascending=False).head(5)

        # '행정구역'을 인덱스로 설정
        top5.set_index('행정구역', inplace=True)

        # 연령별 데이터만 추출
        age_only_df = top5.drop(columns=['총인구수']).transpose()

        # 연령은 숫자형으로 변환 (정렬을 위해)
        age_only_df.index = age_only_df.index.astype(int)
        age_only_df.sort_index(inplace=True)

        st.subheader("상위 5개 행정구역의 연령별 인구 선 그래프")
        st.line_chart(age_only_df)

        st.subheader("상위 5개 행정구역 데이터 (전처리 완료)")
        st.dataframe(top5)

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
