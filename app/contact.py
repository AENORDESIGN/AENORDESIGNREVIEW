
import streamlit as st

def render_contact():
    # 스타일 정의
    st.markdown("""
        <style>
            .contact-container {
                text-align: center;
                padding: 80px 20px;
            }
            .contact-title {
                font-size: 2.5rem;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .contact-subtext {
                font-size: 1.1rem;
                color: #555;
                margin-bottom: 30px;
            }
            .contact-email {
                font-size: 1.2rem;
                font-weight: bold;
                color: #111;
                background: #f0f0f0;
                padding: 12px 20px;
                display: inline-block;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

    # 콘텐츠 출력
    st.markdown("""
        <div class="contact-container">
            <div class="contact-title">문의하기</div>
            <div class="contact-subtext">서비스 개선 제안이나 문의가 있다면 아래 이메일로 연락주세요.</div>
            <div class="contact-email">aenordesign@gmail.com</div>
        </div>
    """, unsafe_allow_html=True)
