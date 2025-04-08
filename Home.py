import streamlit as st
import requests
import xmltodict
from fpdf import FPDF
import re
import sqlite3
from datetime import datetime

# --- 기본 설정 ---
OC = "aenordesign"  # 이메일 아이디
API_BASE = "https://open.law.go.kr/LSO/openApi"

# --- API 함수 (이전 코드 그대로) ---
def fetch_local_ordinance_list(city):
    url = f"{API_BASE}/localLawList?OC={OC}&target=local&city={city}&type=XML"
    res = requests.get(url)
    if res.status_code == 200:
        data = xmltodict.parse(res.text)
        ordinances = data.get("OrdinanceList", {}).get("ordinance", [])
        if isinstance(ordinances, dict):
            return [ordinances]
        return ordinances
    return []

def build_law_link(ordin_seq):
    return f"https://www.law.go.kr/LSW/ordinanceInfoP.do?ordinSeq={ordin_seq}"

def fetch_ordinance_contents(ordin_seq):
    url = f"{API_BASE}/lawContents?OC={OC}&target=local&ordinSeq={ordin_seq}&type=XML"
    res = requests.get(url)
    if res.status_code == 200:
        data = xmltodict.parse(res.text)
        return data.get("OrdinanceContents", {}).get("ordinContent", "")
    return ""

def extract_criteria(ordinance_text):
    lines = ordinance_text.split("\n")
    keywords = ["심의", "경관", "건축", "대상", "높이", "면적", "제", "조"]
    return [line.strip() for line in lines if any(k in line for k in keywords) and line.strip() != ""]

# --- PDF 생성 함수 ---
def generate_pdf(result_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in result_text.split("\n"):
        pdf.multi_cell(0, 10, txt=line)
    pdf_path = "심의분석결과.pdf"
    pdf.output(pdf_path)
    return pdf_path

# --- DB 저장 함수 (기본 SQLite 사용) ---
def save_record(address, city, district, height, floor_area, result):
    conn = sqlite3.connect("review_history.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        address TEXT,
        city TEXT,
        district TEXT,
        height REAL,
        floor_area REAL,
        result TEXT
    )""")
    conn.commit()
    c.execute("INSERT INTO records (created_at, address, city, district, height, floor_area, result) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (datetime.now().isoformat(), address, city, district, height, floor_area, result))
    conn.commit()
    conn.close()

# --- DB 검색 함수 ---
def search_records(keyword):
    conn = sqlite3.connect("review_history.db")
    c = conn.cursor()
    c.execute("SELECT created_at, address, result FROM records WHERE address LIKE ? OR result LIKE ? ORDER BY created_at DESC",
              (f"%{keyword}%", f"%{keyword}%"))
    results = c.fetchall()
    conn.close()
    return results

# --- CSS 스타일 (도면 느낌, 세련된 디자인) ---
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(145deg, #f2f2f2, #ffffff);
        font-family: 'Noto Sans KR', sans-serif;
    }
    .stButton button {
        border-radius: 0;
        border: 1px solid #888;
        background-color: #ffffff;
        color: #333;
        padding: 0.5em 1.2em;
        transition: all 0.2s ease-in-out;
    }
    .stButton button:hover {
        border: 1px solid #555;
        background-color: #f0f0f0;
    }
    .stTextInput>div>div>input {
        border: 1px solid #ddd;
        border-radius: 0;
        padding: 0.6em;
    }
    .result-card {
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        padding: 1em;
        margin-bottom: 1.5em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 상단 탭 메뉴로 멀티 페이지 구성 ---
tabs = st.tabs(["홈", "분석기", "어바웃", "문의"])

# ------- 홈 탭 -------
with tabs[0]:
    st.title("AENOR 심의대상 분석기")
    st.markdown("""
이 서비스는 주소 및 건축 정보를 바탕으로  
건축, 경관, 지구단위계획 등 다양한 심의 대상 여부를 자동으로 분석합니다.

버튼을 누르면 심의 분석 페이지로 이동합니다.
    """)
    if st.button("심의대상 분석하기"):
        st.experimental_set_query_params(page="분석기")
        st.experimental_rerun()

# ------- 분석기 탭 -------
with tabs[1]:
    st.title("건축·경관 심의 분석기")
    st.markdown("아래 정보를 입력하세요.")
    address = st.text_input("주소 (예: 서울특별시 강남구 삼성동 123-4)")
    city = st.text_input("시/도", value="서울특별시")
    district = st.text_input("시/군/구", value="강남구")
    height = st.number_input("건물 높이 (m)", min_value=0.0, step=1.0)
    floor_area = st.number_input("연면적 (㎡)", min_value=0.0, step=1.0)
    
    if st.button("분석 시작하기"):
        result_text = ""
        # 간단 심의 대상 판단 (예시 로직)
        if height >= 30 or floor_area >= 10000:
            result_text += "심의 대상일 가능성이 높음\n"
        else:
            result_text += "심의 대상이 아닐 가능성이 높음\n"
        
        # 조례 조회 (city 기준 API 호출)
        ordinances = fetch_local_ordinance_list(city)
        found = None
        for ordinance in ordinances:
            title = ordinance.get("ordinNm", "")
            org = ordinance.get("organNm", "")
            if district in title or city in title:
                found = ordinance
                break
        if found:
            ordin_seq = found.get("ordinSeq")
            link = build_law_link(ordin_seq)
            ordinance_text = fetch_ordinance_contents(ordin_seq)
            criteria_lines = extract_criteria(ordinance_text)
            
            result_text += f"\n적용 조례: {found.get('ordinNm')} ({found.get('organNm')})\n"
            result_text += f"조례 원문 링크: {link}\n"
            result_text += "\n주요 심의 기준 요약:\n"
            for line in criteria_lines:
                result_text += f"- {line}\n"
        else:
            result_text += f"\n{district}에 해당하는 조례 정보를 찾을 수 없습니다. {city} 광역 조례로 판단합니다.\n"
        result_text += "\n담당 부서 예시: 도시계획과 경관심의팀 / 건축과 건축허가팀 (지자체 별 상이)"
        
        # DB에 저장
        save_record(address, city, district, height, floor_area, result_text)
        
        # 상단 요약 시각화
        st.markdown("### 분석 요약")
        st.metric("건물 높이 (m)", f"{height:.1f}", delta="기준 초과" if height >= 30 else "")
        st.metric("연면적 (㎡)", f"{floor_area:.1f}", delta="기준 초과" if floor_area >= 10000 else "")
        
        # 분석 결과 카드
        st.markdown("---")
        st.subheader("분석 결과")
        st.text_area("분석 결과 요약", result_text, height=300)
        
        # PDF 다운로드 버튼
        if st.button("PDF 다운로드"):
            pdf_file = generate_pdf(result_text)
            with open(pdf_file, "rb") as f:
                st.download_button("PDF 저장하기", f, file_name=pdf_file)
        
        # 자동 스크롤/페이지 전환 없이 결과 하단에 표시됨.
        
        if st.button("다시 분석하기"):
            st.experimental_set_query_params(page="홈")
            st.experimental_rerun()

# ------- 어바웃 탭 -------
with tabs[2]:
    st.title("어바웃")
    st.markdown("""
**AENOR DESIGN**은 건축, 도시, 경관 분야의 최신 심의 및 법령 정보를  
실시간으로 분석하여, 설계 및 인허가 과정에서 신뢰도 높은 정보를 제공하는  
자동 분석 도구를 개발합니다.

이 도구는 국가법령정보센터와 국토부 토지이용규제정보 API 등 공공 데이터를  
활용하며, 지속적인 데이터 업데이트와 정밀한 분석을 통해 건축물 심의 대상 여부를  
정확하게 판단하는 것을 목표로 합니다.
    """)
    st.markdown("---")
    st.markdown("© 2025 AENOR DESIGN | aenordesign@gmail.com")

# ------- 문의 탭 -------
with tabs[3]:
    st.title("문의")
    st.markdown("""
문의 사항이나 건의사항이 있으시면 아래 이메일로 연락주시기 바랍니다.

**aenordesign@gmail.com**
    """)
    st.markdown("---")
    st.markdown("© 2025 AENOR DESIGN")
