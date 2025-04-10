
import streamlit as st

def render_home():
    st.markdown("<div class='centered'><h1>건축·경관 심의대상<br>자동 분석기</h1><p>실시간 데이터를 기반으로 심의 가능성을 분석합니다.</p></div>", unsafe_allow_html=True)
    if st.button("분석 시작하기"):
        st.experimental_set_query_params(page="분석기")
        st.rerun()
