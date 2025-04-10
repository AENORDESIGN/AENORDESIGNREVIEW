
import streamlit as st
from app.home import render_home
from app.analysis import render_analysis
from app.about import render_about
from app.contact import render_contact

st.set_page_config(layout="wide", page_title="AENOR DESIGN")

PAGES = {
    "Home": render_home,
    "Analysis": render_analysis,
    "About": render_about,
    "Contact": render_contact
}

selection = st.selectbox("메뉴를 선택하세요", list(PAGES.keys()), index=0)
PAGES[selection]()
