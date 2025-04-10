
import streamlit as st

def render_about():
    st.markdown("<small style='font-size: 14px;'>About</small>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 48px; font-weight: bold;'>AENOR DESIGN</h1>", unsafe_allow_html=True)
    st.write("도면과 아이디어 사이에서 고민하는 기획자와 실무자를 위해 시작되었습니다.")
