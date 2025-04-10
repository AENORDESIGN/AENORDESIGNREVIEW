
import streamlit as st

def render_home():
    st.title("건축·경관 심의 자동 분석기")
    st.markdown("처음 심의를 준비하는 1인 건축가부터, 복잡한 프로젝트를 조율하는 실무자까지")
    st.markdown("누구나 참고할 수 있는 ‘작은 기준서’를 목표로 합니다.")
    if st.button("🔍 분석 시작하기"):
        st.session_state["navigate"] = "Analysis"
        st.experimental_rerun()
