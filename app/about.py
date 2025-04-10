
import streamlit as st
import os

def render_about():
    # 스타일 정의
    st.markdown("""
        <style>
            .about-container {
                text-align: center;
                padding-top: 60px;
                padding-bottom: 40px;
            }
            .about-title {
                font-size: 3rem;
                font-weight: bold;
                margin-bottom: 20px;
                color: #222;
            }
            .about-subtext {
                font-size: 1.1rem;
                color: #555;
                line-height: 1.7;
                max-width: 700px;
                margin: 0 auto;
            }
        </style>
    """, unsafe_allow_html=True)

    # 타이틀 및 설명
    st.markdown("""
        <div class="about-container">
            <div class="about-title">AENOR DESIGN</div>
            <div class="about-subtext">
                AENOR DESIGN은 전국 건축·경관 심의 기준에 따라 실시간으로 대상 여부를 판단하고,<br>
                누구나 이해할 수 있는 기준과 해석을 제공합니다.<br><br>
                도면과 규정 사이에서 혼란을 겪는 모든 건축가, 기획자를 위한 작은 기준서가 되고자 합니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 일러스트 배경 (선형 빌딩 이미지)
    if os.path.exists("static/images/city_bg.png"):
        st.image("static/images/city_bg.png", use_column_width=True)
