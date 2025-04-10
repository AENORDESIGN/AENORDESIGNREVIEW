
import streamlit as st
from fpdf import FPDF
import requests
import time

def render_analysis():
    st.markdown("<div class='centered'><h2>심의대상 분석기</h2></div>", unsafe_allow_html=True)

    with st.form("input_form"):
        address = st.text_input("대지 주소 또는 지자체명")
        use = st.selectbox("건축물 용도", ["공동주택", "업무시설", "판매시설", "기타"])
        area = st.number_input("연면적 (㎡)", 0.0)
        land = st.number_input("대지면적 (㎡)", 0.0)
        floors = st.number_input("지상 층수", 1)
        households = st.number_input("세대 수", 0)
        district = st.text_input("지역/지구 구분")
        submit = st.form_submit_button("분석 시작")

    if submit:
        with st.spinner("심의 조건을 분석 중입니다..."):
            time.sleep(1.5)
            result = ""
            targets = []
            if area >= 10000 or floors >= 10:
                targets.append("건축심의 대상")
            if households >= 500:
                targets.append("공동위원회 심의")
            if use == "공동주택" and "주거" in district:
                targets.append("도시계획 자문위원회")
            if "지구단위" in district:
                targets.append("지구단위계획 심의")
            if not targets:
                result = "심의 대상 항목이 없습니다."
            else:
                result = "\n".join(f"- {t}" for t in targets)

            st.markdown(f"<div class='card'><h4>분석 결과</h4><pre>{result}</pre></div>", unsafe_allow_html=True)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(200, 10, txt=f"AENOR DESIGN 심의대상 분석 결과\n\n{result}")
            filename = "심의결과.pdf"
            pdf.output(f"/mnt/data/{filename}")
            with open(f"/mnt/data/{filename}", "rb") as f:
                st.download_button("결과 PDF 다운로드", f, file_name=filename)

            try:
                query = address + " 건축 조례"
                url = "https://www.law.go.kr/DRF/lawSearch.do"
                params = {
                    "OC": "aenordesign@gmail.com",
                    "target": "law",
                    "query": query
                }
                res = requests.get(url, params=params)
                if res.status_code == 200:
                    law_url = f"https://www.law.go.kr/search/lawSearch.do?query={query}"
                    st.markdown(f"[국가법령정보센터 조례 검색 바로가기]({law_url})")
                else:
                    st.warning("조례 API 응답 오류. 직접 검색을 이용해주세요.")
            except Exception as e:
                st.error("조례 검색 중 오류 발생: " + str(e))
