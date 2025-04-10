
import requests
from xml.etree import ElementTree as ET

def get_law_titles_by_region(region_name):
    try:
        url = "https://www.law.go.kr/DRF/lawSearch.do"
        params = {
            "OC": "aenordesign@gmail.com",
            "target": "law",
            "query": f"{region_name} 건축 조례",
            "display": "3",
            "type": "XML"
        }
        res = requests.get(url, params=params)
        root = ET.fromstring(res.content)
        results = []
        for law in root.findall(".//law"):
            title = law.findtext("lawName")
            law_id = law.findtext("lawId")
            summary = law.findtext("enforcementNo") or "요약 정보 없음"
            law_url = f"https://www.law.go.kr/법령/{law_id}"
            results.append((title, law_url, summary))
        return results
    except:
        return [("조례 정보를 불러올 수 없습니다", "#", "국가법령정보센터를 직접 참조해 주세요.")]
