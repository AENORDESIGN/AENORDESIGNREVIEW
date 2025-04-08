import streamlit as st
from PIL import Image
from fpdf import FPDF
from datetime import datetime
import requests

# 왼쪽 바 비활성화
st.set_page_config(page_title="AENOR 심의대상 분석기", layout="wide")

# 헤더 구성
logo = Image.open("aenor_logo.png")
st.sidebar.image(logo, use_container_width=True)
st.sidebar.markdown("# AENOR")

# 상단 네비게이션 바
nav_items = ["Home", "Analysis", "About", "Contact"]
nav_selection = st.sidebar.radio("Navigation", nav_items)

# 로고 추가
st.markdown(
    """
    <style>
    .stSidebar { display: none; }
    .mainHeader {
        position: fixed;
        width: 100%;
        top: 0;
        background-color: white;
        border-bottom: 1px solid #ddd;
        z-index: 1000;
        padding: 10px 20px;
    }
    .mainHeader img { height: 40px; }
    .mainHeader .nav-items { float: right; }
    .mainHeader .nav-items a {
        margin-left: 20px;
        color: black;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
    <div class="mainHeader">
        <img src="aenor_logo.png" alt="AENOR Logo">
        <div class="nav-items">
            <a href="?page=Home">Home</a>
            <a href="?page=Analysis">Analysis</a>
            <a href="?page=About">About</a>
            <a href="?page=Contact">Contact</a>
        </div>
    </div>
    """,
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

# 국가법령정보 API 함수
def get_local_ordinance_url(local_gov_name):
    try:
        url = "https://www.law.go.kr/DRF/lawSearch.do"
        params = {
            "OC": "aenordesign@gmail.com",
            "target": "precendent",
            "query": f"{local_gov_name} 건축 조례"
        }
        res = requests.get(url, params=params)
        if res.status_code == 200 and 'lawSearch' in res.text:
            return f"https://www.law.go.kr/search/lawSearch.do?query={local_gov_name}+건축+조례"
        else:
            return None
    except:
        return None

# 페이지 내용
if nav_selection == "Home":
    st.title("Home")
    st.write("건축·경관 심의 대상 자동 분석기입니다. Analysis 탭에서 심의 항목을 분석하세요.")

elif nav_selection == "Analysis":
    st.title("심의대상 분석기")

    st.markdown("""
<style>
.result-box {
    background-color: #f9f9f9;
    border: 1px solid #ccc;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

    st.subheader("설계개요")
    st.markdown("""
**[기본 정보]**
- 사업명, 위치, 용도, 지역지구, 건설규모 등 정보를 아래 항목에 입력하세요.
""")

    total_area = st.number_input("대지면적 (㎡)", min_value=0.0, step=1.0)
    building_area = st.number_input("건축면적 (㎡)", min_value=0.0, step=1.0)
    gfa = st.number_input("용적률 산정 연면적 (㎡)", min_value=0.0, step=1.0)
    num_households = st.number_input("세대 수", min_value=0, step=1)
    address = st.text_input("건축물 주소")
    building_use = st.selectbox("건축물 주용도", ["공동주택", "근린생활시설", "업무시설", "판매시설", "교육연구시설", "운동시설", "의료시설", "기타"])
    land_zone = st.text_input("지구단위 여부 (예: 지구단위계획구역, 해당없음 등)")
    district = st.text_input("도시지역 구분 (예: 제2종 일반주거지역 등 다양한 입력 허용)")
    local_gov = st.selectbox("해당 지자체", ["서울특별시", "경기도", "부산광역시", "대구광역시", "기타"])
    redevelopment_type = st.selectbox("사업 유형", ["신축", "재건축", "재개발", "정비사업", "도시개발사업", "기타"])
    is_special_zone = st.checkbox("정비구역/특정지구 지정 여부")
    above_ground_floors = st.number_input("지상 층수", min_value=1, step=1)
    underground_floors = st.number_input("지하 층수", min_value=0, step=1)

    if st.button("분석 시작하기"):
        result = ""
        result += f"주소: {address}\n"
        result += f"건축물 주용도: {building_use}\n지구단위계획 여부: {land_zone}\n도시지역 구분: {district}\n"
        result += f"지상 {above_ground_floors}층, 지하 {underground_floors}층\n"
        result += f"건물 높이: 자동 미입력\n연면적: {gfa}㎡\n"
        result += f"대지면적: {total_area}㎡\n건축면적: {building_area}㎡\n세대 수: {num_households}세대\n"
        result += f"용적률: {round(gfa/total_area*100, 2) if total_area else 0}%\n건폐율: {round(building_area/total_area*100, 2) if total_area else 0}%\n"
        result += f"지자체: {local_gov}\n사업유형: {redevelopment_type}\n정비구역/특정지구 지정 여부: {'예' if is_special_zone else '아니오'}\n\n"

        심의항목 = []
        if gfa >= 10000 or above_ground_floors >= 10:
            심의항목.append("건축심의 대상")
        if "지구단위" in land_zone:
            심의항목.append("지구단위계획 심의")
        if num_households >= 500:
            심의항목.append("공동위원회 심의")
        if "주거" in district and building_use == "공동주택":
            심의항목.append("도시계획 자문위원회")
        if is_special_zone:
            심의항목.append("통합심의 대상 가능성")

        if 심의항목:
            result += "[해당되는 심의 항목]\n"
            for item in 심의항목:
                result += f"- {item}\n"
        else:
            result += "심의 대상 항목이 없습니다.\n"

        st.markdown("""---\n### 분석 결과 요약""")
        ordinance_link = get_local_ordinance_url(local_gov)
        if ordinance_link:
            st.markdown(f"[{local_gov} 조례 바로가기]({ordinance_link})")
            result += f"\n📘 조례 확인 링크: {ordinance_link}"

        st.markdown("""
        ---
        ℹ️ 본 결과는 국가법령정보센터의 데이터를 활용한 자동분석이며,
        보다 정확한 내용은 각 지자체에 문의해주세요.

        출처: 국가법령정보센터 / © AENOR DESIGN  
        문의: aenordesign@gmail.com
        """)

        st.markdown(f"""<div class='result-box'><pre>{result}</pre></div>""", unsafe_allow_html=True)

        pdf_file = generate_pdf(result)
        with open(pdf_file, "rb") as f:
            st.download_button(label="결과 PDF 다운로드", data=f, file_name=pdf_file, mime="application/pdf")

elif nav_selection == "About":
    st.title("About")
    st.markdown("""
    **AENOR DESIGN**은 전국 건축·경관 심의 기준에 따라 자동 분석 시스템을 제공합니다.  
    이 앱은 건축물의 높이, 면적, 용도, 지역, 세대수, 층수, 용적률 등을 기반으로 심의 대상 여부를 판단하고,  
    PDF 형식으로 결과를 제공합니다.
    """)

elif nav_selection == "Contact":
    st.title("Contact")
    st.markdown("문의: **aenordesign@gmail.com**")
    st.markdown("© 2025 AENOR DESIGN")
