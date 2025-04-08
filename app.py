
import streamlit as st
from pages.home import render_home
from pages.analysis import render_analysis
from pages.about import render_about
from pages.contact import render_contact

st.set_page_config(page_title="AENOR DESIGN APP", layout="wide")

page = st.experimental_get_query_params().get("page", ["Home"])[0]

# 상단 네비게이션 바
st.markdown("""
    <style>
    .nav-container {
        display: flex; justify-content: center; background-color: #f9f9f9; padding: 10px;
        border-bottom: 1px solid #ccc; margin-bottom: 20px;
    }
    .nav-item {
        margin: 0 15px; text-decoration: none; color: #333; font-weight: bold;
    }
    </style>
    <div class="nav-container">
        <a class="nav-item" href="?page=Home">Home</a>
        <a class="nav-item" href="?page=Analysis">Analysis</a>
        <a class="nav-item" href="?page=About">About</a>
        <a class="nav-item" href="?page=Contact">Contact</a>
    </div>
""", unsafe_allow_html=True)

# 페이지 렌더링
if page == "Home":
    render_home()
elif page == "Analysis":
    render_analysis()
elif page == "About":
    render_about()
elif page == "Contact":
    render_contact()
