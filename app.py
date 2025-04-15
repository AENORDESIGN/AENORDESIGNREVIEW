
import streamlit as st
from pages.home import render_home
from pages.analysis import render_analysis
from pages.about import render_about
from pages.contact import render_contact

st.set_page_config(page_title="AENOR DESIGN", layout="wide")

PAGES = {
    "홈": render_home,
    "분석기": render_analysis,
    "어바웃": render_about,
    "문의": render_contact,
}

selection = st.sidebar.radio("메뉴를 선택하세요", list(PAGES.keys()))
PAGES[selection]()
