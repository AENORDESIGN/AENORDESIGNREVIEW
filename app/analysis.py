
import streamlit as st
from utils.api_law import get_law_titles_by_region
from utils.pdf_utils import generate_pdf
import time

def render_analysis():
    st.markdown("<h1 style='text-align: center;'>📋 심의 조건 분석기</h1>", unsafe_allow_html=True)

    # 사용자 입력 폼
    with st.form("analysis_form"):
        st.markdown("#### 🔎 기본 정보를 입력하세요")
        region = st.text_input("지역 (예: 서울특별시)")
        use = st.selectbox("건축물 주 용도", ["공동주택", "업무시설", "판매시설", "기타"])
        area = st.number_input("연면적 (㎡)", min_value=0.0, step=1.0)
        floors = st.number_input("지상 층수", min_value=1)
        households = st.number_input("세대 수", min_value=0)
        submitted = st.form_submit_button("분석하기")

    if submitted:
        with st.spinner("심의 조건을 분석 중입니다... ⏳"):
            time.sleep(1.5)

            results = []
            if area >= 10000 or floors >= 10:
                results.append("🏢 건축심의 대상")
            if households >= 500:
                results.append("👥 공동위원회 심의 대상")
            if use == "공동주택":
                results.append("🏘️ 도시계획 자문위원회")

            st.markdown("---")
            st.subheader("✅ 분석 결과")
            if results:
                for item in results:
                    st.success(f"{item}")
            else:
                st.info("심의 대상에 해당하지 않을 수 있습니다.")

            # 조례 정보 출력
            st.markdown("---")
            st.subheader("📚 관련 조례 정보")

            for title, url, summary in get_law_titles_by_region(region):
                st.markdown(f"**[{title}]({url})**")
                st.caption(summary)

            # PDF 생성 및 다운로드
            pdf_text = "\n".join(results)
            pdf_file = generate_pdf(pdf_text)
            with open(pdf_file, "rb") as f:
                st.download_button("📄 분석 결과 PDF 저장", f, file_name=pdf_file)
