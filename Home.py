import streamlit as st
from PIL import Image

# 왼쪽 바 비활성화
st.set_page_config(page_title="AENOR 심의대상 분석기", layout="wide")

# 헤더 구성
logo = Image.open("aenor_logo.png")
st.sidebar.image(logo, use_container_width=True)
st.sidebar.markdown("# AENOR")

# 상단 네비게이션 바
nav_items = ["Home", "Analysis", "About", "Contact"]
nav_selection = st.sidebar.radio("Navigation", nav_items)

# 로고 추가
st.markdown(
    """
    <style>
    .stSidebar {
        display: none;
    }
    .mainHeader {
        position: fixed;
        width: 100%;
        top: 0;
        background-color: white;
        border-bottom: 1px solid #ddd;
        z-index: 1000;
        padding: 10px 20px;
    }
    .mainHeader img {
        height: 40px;
    }
    .mainHeader .nav-items {
        float: right;
    }
    .mainHeader .nav-items a {
        margin-left: 20px;
        color: black;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
    <div class="mainHeader">
        <img src="aenor_logo.png" alt="AENOR Logo">
        <div class="nav-items">
            <a href="?page=Home">Home</a>
            <a href="?page=Analysis">Analysis</a>
            <a href="?page=About">About</a>
            <a href="?page=Contact">Contact</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 페이지 내용
if nav_selection == "Home":
    st.title("Home")
    st.write("Welcome to the Home page.")
elif nav_selection == "Analysis":
    st.title("Analysis")
    st.write("This is the Analysis page.")
elif nav_selection == "About":
    st.title("About")
    st.write("This is the About page.")
elif nav_selection == "Contact":
    st.title("Contact")
    st.write("This is the Contact page.")
