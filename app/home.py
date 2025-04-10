
import streamlit as st
import os

def render_home():
    # 스타일 적용
    st.markdown("""
        <style>
            .main-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 85vh;
                text-align: center;
            }
            .title-text {
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .description {
                font-size: 1.2rem;
                color: #666;
                margin-bottom: 30px;
            }
            .start-button {
                font-size: 1.1rem;
                padding: 0.6rem 1.5rem;
                background-color: black;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }
            .start-button:hover {
                background-color: #333;
            }
            .logo {
                position: fixed;
                top: 20px;
                left: 20px;
                height: 40px;
            }
        </style>
    """, unsafe_allow_html=True)

    # 로고 이미지 삽입
    if os.path.exists("static/images/aenor_logo.png"):
        st.image("static/images/aenor_logo.png", width=120)

    # 메인 내용
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="title-text">건축·경관 심의 자동 분석기</div>', unsafe_allow_html=True)
    st.markdown('<div class="description">처음 심의를 준비하는 1인 건축가부터,<br>복잡한 프로젝트를 조율하는 실무자까지<br>누구나 참고할 수 있는 ‘작은 기준서’를 목표로 합니다.</div>', unsafe_allow_html=True)

    if st.button("🔍 분석 시작하기"):
        st.session_state["navigate"] = "Analysis"
        st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # 배경 일러스트 하단 출력
    if os.path.exists("static/images/city_bg.png"):
        st.image("static/images/city_bg.png", use_column_width=True)
