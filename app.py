
import streamlit as st
from PIL import Image
from fpdf import FPDF
from datetime import datetime

# 상단 네비게이션 설정
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["Home"])[0]

# 공통 로고 및 헤더 삽입
logo_path = "aenor_logo.png"
logo = Image.open(logo_path)
st.markdown(
    f'''
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ddd; padding-bottom: 10px;">
        <div><img src="data:image/png;base64,{logo_path}" style="height: 40px;"></div>
        <div style="margin-left: auto;">
            <a href="?page=Home" style="margin: 0 15px;">Home</a>
            <a href="?page=Analysis" style="margin: 0 15px;">Analysis</a>
            <a href="?page=About" style="margin: 0 15px;">About</a>
            <a href="?page=Contact" style="margin: 0 15px;">Contact</a>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# PDF 생성 함수
def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)
    filename = f"심의분석결과_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# 분석 페이지
if page == "Home":
    st.title("Home")
    st.write("건축·경관 심의 대상 자동 분석기입니다. Analysis 탭에서 심의 항목을 분석하세요.")

elif page == "Analysis":
    st.title("심의대상 분석기")
    total_area = st.number_input("대지면적 (㎡)", min_value=0.0, step=1.0)
    building_area = st.number_input("건축면적 (㎡)", min_value=0.0, step=1.0)
    gfa = st.number_input("용적률 산정 연면적 (㎡)", min_value=0.0, step=1.0)
    num_households = st.number_input("세대 수", min_value=0, step=1)
    address = st.text_input("건축물 주소")
    if st.button("분석 시작하기"):
        result = f"주소: {address}\n연면적: {gfa}㎡\n대지면적: {total_area}㎡\n건축면적: {building_area}㎡\n세대 수: {num_households}세대"
        st.markdown(f"**분석 결과**\n\n{result}")
        pdf_file = generate_pdf(result)
        with open(pdf_file, "rb") as f:
            st.download_button("PDF 다운로드", f, file_name=pdf_file, mime="application/pdf")

elif page == "About":
    st.title("About")
    st.write("AENOR DESIGN은 전국 건축·경관 심의 기준에 따라 자동 분석 시스템을 제공합니다.")

elif page == "Contact":
    st.title("Contact")
    st.markdown("문의: aenordesign@gmail.com")
