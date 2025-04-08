
import streamlit as st

def render_about():
    st.title("About AENOR DESIGN")
    st.markdown("이 앱은 AENOR DESIGN에 의해 개발된 건축·경관 심의 대상 자동 분석 도구입니다.")
    st.image("static/building_line.png", use_column_width=True)
