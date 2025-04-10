
import streamlit as st

def render_home():
    st.markdown("<h1 style='text-align: center;'>건축·경관 심의 자동 분석기</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>처음 심의를 준비하는 1인 건축가부터, 복잡한 프로젝트를 조율하는 실무자까지</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>누구나 참고할 수 있는 ‘작은 기준서’를 목표로 합니다.</p>", unsafe_allow_html=True)
    if st.button("🔍 분석 시작하기", use_container_width=True):
        st.session_state["navigate"] = "분석기"
        st.experimental_rerun()
