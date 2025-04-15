
import streamlit as st

def render_home():
    st.markdown("<h1 style='text-align:center;'>AENOR DESIGN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>건축·경관 심의 자동 분석기</p>", unsafe_allow_html=True)
    if st.button("🔍 분석 시작하기"):
        st.session_state["page"] = "분석기"
        st.experimental_rerun()
