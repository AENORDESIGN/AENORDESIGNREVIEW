
import streamlit as st
from pages.Home import render_home
from pages.분석기 import render_analysis
from pages.About import render_about
from pages.문의 import render_contact

st.set_page_config(page_title="AENOR DESIGN", layout="wide")
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Home"])[0]

with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div class="nav-container">
    <h3>AENOR DESIGN</h3>
    <div class="nav-items">
        <a href='/?page=Home'>Home</a>
        <a href='/?page=분석기'>Analysis</a>
        <a href='/?page=About'>About</a>
        <a href='/?page=문의'>Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

if page == "Home":
    render_home()
elif page == "분석기":
    render_analysis()
elif page == "About":
    render_about()
elif page == "문의":
    render_contact()
