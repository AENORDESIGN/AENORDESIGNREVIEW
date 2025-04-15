
import streamlit as st
import time

def render_analysis():
    st.header("심의 대상 분석기")
    with st.form("analysis_form"):
        area = st.number_input("연면적 (㎡)", min_value=0.0)
        floors = st.number_input("지상 층수", min_value=1)
        households = st.number_input("세대 수", min_value=0)
        submitted = st.form_submit_button("분석하기")

    if submitted:
        with st.spinner("분석 중입니다..."):
            time.sleep(1.5)
            result = []
            if area >= 10000 or floors >= 10:
                result.append("건축심의 대상")
            if households >= 500:
                result.append("공동위원회 심의 대상")
            if not result:
                st.info("심의 대상이 아닐 수 있습니다.")
            else:
                for item in result:
                    st.success(item)
