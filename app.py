
import streamlit as st
from fpdf import FPDF
import requests
import time

st.set_page_config(page_title='AENOR DESIGN', layout='wide')

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
.nav-container {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 30px; background: #f9f9f9; border-bottom: 1px solid #eee;
}
.nav-items a {
    margin-left: 20px; font-weight: bold; text-decoration: none; color: #333;
}
.centered { text-align: center; margin-top: 60px; }
.card {
    background-color: #f8f8f8; padding: 20px; border-radius: 10px;
    border: 1px solid #ccc; margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nav-container">
    <h3>AENOR DESIGN</h3>
    <div class="nav-items">
        <a href="/?page=Home">Home</a>
        <a href="/?page=Analysis">Analysis</a>
        <a href="/?page=About">About</a>
        <a href="/?page=Contact">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.query_params.get("page", ["Home"])[0]

if page == "Home":
    st.markdown("""
    <div class="centered">
        <h1>건축·경관 심의대상<br>자동 분석기</h1>
        <p>국가법령정보센터 및 국토부 API를 통해<br>실시간 데이터를 제공합니다.</p>
        <a href="/?page=Analysis"><button style='padding:10px 30px;'>분석 시작하기</button></a>
    </div>
    """, unsafe_allow_html=True)

elif page == "Analysis":
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

            # 조례 링크 API
            st.markdown("### 관련 조례 정보")
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

elif page == "About":
    st.markdown("""
    <div class='centered'>
        <h2>About</h2>
        <p>
        AENOR DESIGN은<br>
        설계를 앞두고 행정 절차를 마주하는 건축가와 기획자들을 위해 만들어졌습니다.<br><br>

        우리는 설계자의 시선에서,<br>
        심의라는 복잡한 절차를 더 명확하고 간결하게 정리하고자 합니다.<br><br>

        전국 지자체의 조례와 법령을 바탕으로<br>
        대지와 건축물의 조건에 따라 어떤 심의가 필요한지를 판단하고,<br>
        그 근거를 정리해 보여주는 도구입니다.<br><br>

        설계를 더 잘하기 위한 준비가<br>
        조금 더 단순하고, 정확해지기를 바랍니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Contact":
    st.markdown("""
    <div class='centered'>
        <h2>Contact</h2>
        <p>문의: <strong>aenordesign@gmail.com</strong></p>
    </div>
    """, unsafe_allow_html=True)
