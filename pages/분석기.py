
import streamlit as st
import time
from utils.pdf_utils import generate_pdf
from utils.api_law import get_law_titles_by_region

def render_analysis():
    st.markdown("<div class='centered'><h2>심의대상 분석기</h2></div>", unsafe_allow_html=True)

    with st.form("analysis_form"):
        address = st.text_input("대지 주소 또는 지자체명")
        use = st.selectbox("건축물 주 용도", ["공동주택", "업무시설", "판매시설", "기타"])

        category_options = {
            "주거지역": ["제1종 전용주거지역", "제2종 일반주거지역", "준주거지역"],
            "상업지역": ["일반상업지역", "중심상업지역"],
            "기타": ["자연녹지지역", "지구단위계획구역"]
        }
        col1, col2 = st.columns(2)
        with col1:
            region_category = st.selectbox("1단계 지역 분류", list(category_options.keys()))
        with col2:
            district = st.selectbox("2단계 세부 지구", category_options[region_category])

        area = st.number_input("연면적 (㎡)", 0.0)
        land = st.number_input("대지면적 (㎡)", 0.0)
        floors = st.number_input("지상 층수", 1)
        households = st.number_input("세대 수", 0)

        submitted = st.form_submit_button("분석 시작")

    if submitted:
        with st.spinner("심의 조건을 분석 중입니다..."):
            time.sleep(1.5)
            targets = []
            if area >= 10000 or floors >= 10:
                targets.append("건축심의 대상")
            if households >= 500:
                targets.append("공동위원회 심의")
            if use == "공동주택" and "주거" in district:
                targets.append("도시계획 자문위원회")
            if "지구단위" in district:
                targets.append("지구단위계획 심의")

            result = "\n".join(f"- {t}" for t in targets) if targets else "심의 대상 항목이 없습니다."

            st.markdown(f"<div class='card'><h4>분석 결과</h4><pre>{result}</pre></div>", unsafe_allow_html=True)
            pdf_file = generate_pdf(result)
            with open(pdf_file, "rb") as f:
                st.download_button("PDF 다운로드", f, file_name=pdf_file)

            titles = get_law_titles_by_region(address)
            st.markdown("### 관련 조례")
            for t in titles:
                st.markdown(f"- {t}")
