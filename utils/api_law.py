
import requests
from xml.etree import ElementTree as ET

def get_law_titles_by_region(region_name):
    url = "https://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": "aenordesign@gmail.com",
        "target": "law",
        "query": f"{region_name} 건축 조례",
        "display": "3",
        "type": "XML"
    }
    try:
        res = requests.get(url, params=params, timeout=5)
        tree = ET.fromstring(res.content)
        titles = tree.findall(".//lawName")
        return [title.text for title in titles]
    except:
        return ["(조례 검색 실패) 직접 국가법령정보센터에서 확인해주세요."]
