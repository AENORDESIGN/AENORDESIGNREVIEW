
import streamlit as st
def render_home():
    st.markdown("<div class='centered'><h1>건축·경관 심의대상<br>자동 분석기</h1><p>국가법령정보센터 및 국토부 API를 통해 실시간 데이터를 제공합니다.</p></div>", unsafe_allow_html=True)
    st.image("static/city_line.png", use_column_width=True)
    if st.button("분석 시작하기"):
        st.experimental_set_query_params(page="Analysis")
        st.rerun()
