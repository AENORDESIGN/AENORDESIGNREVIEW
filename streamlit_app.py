import streamlit as st
import requests
import pandas as pd

# 페이지 설정
st.set_page_config(page_title='건축·경관 심의대상 분석기', layout="wide")

# 사이드바 로고 및 메뉴 구성
with st.sidebar:
    st.markdown('<div style="text-align:center;"><img src="https://raw.githubusercontent.com/AENORDESIGN/AENORDESIGNREVIEW/main/aenor_logo.png" width="180"></div>', unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("메뉴", ["AENOR DESIGN", "심의대상 분석기", "지자체 법령", "기본계획", "기타"])

# AENOR DESIGN 소개 페이지
if menu == "AENOR DESIGN":
    st.header('AENOR DESIGN')
    st.markdown('''
    ## 스마트한 건축·경관 분석의 시작, AENOR DESIGN

    AENOR DESIGN은 건축과 경관 분야에서 정확하고 스마트한 분석을 제공하는 혁신 기업입니다.  
    도시환경의 지속가능성과 미적 가치를 극대화하기 위한 기술적 분석 도구를 개발합니다.

    ### 우리의 비전
    건축과 경관이 조화를 이루는 더 나은 도시공간을 만드는 것. 데이터 기반의 명확하고 신속한 분석을 통해 사용자와 도시 모두에게 가치를 제공합니다.

    ### 주요 업무 분야
    - 건축·경관 심의 대상 분석
    - 실시간 법령 연계 서비스
    - 데이터 기반 스마트 도시설계

    ### 문의
    📧 aenordesign@gmail.com

# 심의대상 분석기 페이지
elif menu == "심의대상 분석기":
    st.title('건축·경관 심의대상 분석기')

    with st.form('사업 개요 입력'):
        st.subheader('사업 개요 입력')
        project_name = st.text_input('사업명', 'AENOR 타워 신축공사')
        location = st.text_input('사업 위치', '서울특별시 강남구 역삼동')

        col1, col2, col3 = st.columns(3)
        with col1:
            land_area = st.number_input('대지면적(㎡)', value=5500)
        with col2:
            total_area = st.number_input('연면적(㎡)', value=12000)
        with col3:
            building_height = st.number_input('건축물 높이(m)', value=60)

        usage = st.selectbox('건축물 용도', ['업무시설', '주거시설', '문화집회시설', '숙박시설'])
        lighting_type = st.selectbox('조명 종류', ['LED', '일반조명', '기타'])

        submitted = st.form_submit_button('분석 및 보고서 생성')

    if submitted:
        st.markdown("결과는 국가법령정보 API 연동 후 표시됩니다.")

# Google Sheets 연동해서 지자체 법령 및 기본계획 콘텐츠 표시
elif menu in ["지자체 법령", "기본계획"]:
    st.header(menu)

    sheet_url = st.secrets["local_law"] if menu == "지자체 법령" else st.secrets["basic_plan"]
    csv_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
    
    df = pd.read_csv(csv_url)

    for index, row in df.iterrows():
        st.subheader(f"{row['제목']}")
        st.caption(row['날짜'])
        st.write(row['내용'])
        st.markdown('---')

# 하단 정보 (푸터)
st.markdown("""
<div style="text-align:center; margin-top:50px; font-size:14px; color:gray;">
    <strong>AENOR DESIGN</strong><br>
    aenordesign@gmail.com
</div>
""", unsafe_allow_html=True)
