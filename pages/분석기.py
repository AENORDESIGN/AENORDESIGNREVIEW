
import streamlit as st
from datetime import datetime
from fpdf import FPDF

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)
    filename = f"심의분석결과_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

st.set_page_config(page_title="Analysis", layout="wide")
st.markdown("<h1>심의대상 분석기</h1>", unsafe_allow_html=True)

st.subheader("설계개요 입력")

address = st.text_input("대지 위치")
district = st.text_input("도시지역 구분")
building_use = st.selectbox("건축물 용도", ["공동주택", "업무시설", "판매시설", "기타"])
gfa = st.number_input("연면적 (㎡)", 0.0)
floor = st.number_input("층수", 1)
households = st.number_input("세대 수", 0)

if st.button("분석 시작하기"):
    result = f"대지위치: {address}\n도시지역: {district}\n용도: {building_use}\n연면적: {gfa}㎡\n층수: {floor}\n세대수: {households}세대\n"

    심의항목 = []
    if gfa >= 10000: 심의항목.append("건축심의 대상")
    if households >= 500: 심의항목.append("공동위원회 심의")

    result += "\n[해당 심의항목]\n" + "\n".join(f"- {x}" for x in 심의항목) if 심의항목 else "심의대상 아님"

    st.text_area("분석 결과", result, height=250)
    pdf_file = generate_pdf(result)
    with open(pdf_file, "rb") as f:
        st.download_button("PDF 다운로드", f, file_name=pdf_file)
