import streamlit as st
import requests
from datetime import date

# 페이지 설정 (레이아웃 및 색상)
st.set_page_config(page_title='건축·경관 심의대상 분석기', layout="wide")

# 사이드바에 로고 및 카테고리
with st.sidebar:
    st.image('https://raw.githubusercontent.com/AENORDESIGN/AENORDESIGNREVIEW/main/aenor_logo.jpg', width=200)
    st.markdown("---")
    menu = st.radio("", ["AENOR DESIGN", "심의대상 분석기", "지자체 법령", "기본계획", "기타"])

# 카테고리별 페이지 구성
if menu == "AENOR DESIGN":
    st.header('AENOR DESIGN 소개')
    st.markdown('''
    AENOR DESIGN은 건축 및 경관 분야에서 혁신적이고 스마트한 분석 도구를 개발합니다.
    정확한 데이터와 실시간 법령 분석을 통해 건축물과 도시환경의 조화를 추구합니다.
    지속가능한 도시개발과 사용자 친화적인 기술 개발이 저희의 핵심 목표입니다.
    ''')

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

    API_KEY = st.secrets.get("api_key", None)

    def analyze_review(total_area, height, usage, location, land_area):
        building_review = total_area >= 10000 or height >= 50
        landscape_review = total_area >= 5000 or height >= 30 or land_area >= 3000

        if building_review and landscape_review:
            review_type = '공동위원회(건축+경관)'
        elif building_review:
            review_type = '건축 단독심의'
        elif landscape_review:
            review_type = '경관 단독심의'
        elif usage in ['숙박시설', '문화집회시설']:
            review_type = '통합심의'
        else:
            review_type = '심의대상 아님'

        good_light_review = '적용' if '서울특별시' in location else '미적용'
        return review_type, good_light_review

    def fetch_law_info(api_key, law_name):
        url = 'https://www.law.go.kr/DRF/lawSearch.do'
        params = {'OC': api_key, 'target': 'law', 'type': 'json', 'query': law_name, 'display': 3}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def generate_law_link(law_name):
        return f"https://www.law.go.kr/법령/{law_name}"

    if submitted:
        review_type, good_light_review = analyze_review(total_area, building_height, usage, location, land_area)

        api_key = st.secrets["api_key"] if "api_key" in st.secrets else None

        if api_key:
            laws = []
            for law in ['건축법', '경관법', f'{location.split()[0]} 경관조례']:
                law_data = fetch_law_info(api_key, law)
                if law_data and 'law' in law_data:
                    laws.append({
                        '법령명': law,
                        '내용': law_data['law'][0]['lawName']
                    })
        else:
            laws = [{'법령명':'API Key 필요','내용':'관리자에게 문의하세요.'}]

        st.markdown(f"""
        ### 심의대상 검토 결과 보고서

        **사업명**: {project_name}  
        **위치**: {location}  
        **대지면적**: {land_area}㎡  
        **연면적**: {total_area}㎡  
        **건축물 높이**: {building_height}m  
        **용도**: {usage}

        ---

        **심의 대상 여부**: {"심의대상" if review_type != '심의대상 아님' else "심의대상 아님"}  
        **심의 유형**: {review_type}  
        **좋은빛 디자인 심의(서울)**: {good_light_review}

        ---

        ### 적용 법령 및 근거:
        """)

        for law in laws:
            law_link = generate_law_link(law['법령명'])
            st.markdown(f"- [{law['법령명']}]({law_link}): {law['내용']}")

        st.info("※ 국가법령정보 API로 실시간 법령정보를 받아옵니다.")

# 하단 정보 (푸터)
st.markdown("""
<div style="text-align:center; margin-top:50px; font-size:14px; color:gray;">
    <strong>AENOR DESIGN</strong><br>
    aenordesign@gmail.com
</div>
""", unsafe_allow_html=True)
