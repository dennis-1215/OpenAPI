import main
import requests
import xml.etree.ElementTree as ET

def GetData(title, key):

    keyword_params = {
        "serviceKey": main.api_key,
        "numOfRows": 20000,  # 최대 2000개의 관광 정보 데이터 요청
        "MobileOS": "ETC",  # 필수 입력 데이터(사용x)
        "MobileApp": "AppTest",  # 필수 입력 데이터(사용x)
        "Keyword": title,  # 필수 입력 데이터(input 값을 넣음)
    }

    response = requests.get(main.url + main.api_keyword, params=keyword_params)
    root = ET.fromstring(response.content)
    items = root.findall(".//item")
    tourLists = []
    type = {
        '관광지' : '12',
        '문화시설' : '14',
        '축제공연행사' : '15',
        '여행코스' : '25',
        '레포츠' : '28',
        '숙박' : '32',
        '쇼핑' : '38',
        '음식점' : '39'
    }

    for item in items:
        if item.findtext('contenttypeid') == type[key]:
            tour = [
                item.findtext("title"),  # 관광지 이름
                item.findtext("addr1")  # 주소
            ]
            tourLists.append('관광지 이름 : '+tour[0]+', 주소 : '+tour[1])

    return tourLists
