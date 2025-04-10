
from app.home import render_home
from app.analysis import render_analysis
from app.about import render_about
from app.contact import render_contact

import streamlit as st

PAGES = {
    "홈": render_home,
    "분석기": render_analysis,
    "어바웃": render_about,
    "문의": render_contact,
}

st.set_page_config(page_title="AENOR DESIGN", layout="wide")

# 네비게이션
st.sidebar.title("앱")
selection = st.sidebar.radio("이동", list(PAGES.keys()))
page = PAGES[selection]
page()
