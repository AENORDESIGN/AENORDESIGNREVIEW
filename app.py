
import streamlit as st
from pages.home import render_home
from pages.analysis import render_analysis
from pages.about import render_about
from pages.contact import render_contact

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
        <a href='/?page=Analysis'>Analysis</a>
        <a href='/?page=About'>About</a>
        <a href='/?page=Contact'>Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

if page == "Home":
    render_home()
elif page == "Analysis":
    render_analysis()
elif page == "About":
    render_about()
elif page == "Contact":
    render_contact()
