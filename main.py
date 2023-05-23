from tkinter import *
import xml.etree.ElementTree as ET
import requests

# 공공데이터 API 키
api_key = ""

url = "http://apis.data.go.kr/B551011/KorService1/"
api_keyword = "searchKeyword1"
api_location = "locationBasedList1"
api_detail = "detailCommon1"
api_image = "detailImage1"

keyword = "강원"

keyword_params = {
    "serviceKey": api_key,
    "numOfRows": 2000,  # 최대 2000개의 관광 정보 데이터 요청
    "MobileOS": "ETC",  # 필수 입력 데이터(사용x)
    "MobileApp": "AppTest",  # 필수 입력 데이터(사용x)
    "Keyword": keyword,  # 필수 입력 데이터(input 값을 넣음)
}

response = requests.get(url + api_keyword, params=keyword_params)
root = ET.fromstring(response.content)
items = root.findall(".//item")

tourLists = []
for item in items:
    tour = {
        "name": item.findtext("title"),  # 관광지 이름
        "address": item.findtext("addr1"),  # 주소
        "mapx": item.findtext("mapx"),  # 경도
        "mapy": item.findtext("mapy"),  # 위도
        "typeid": item.findtext("contenttypeid"),  # 관광 시설 구분 코드
        # 12:관광지, 14:문화시설, 15:축제공연행사, 25:여행코스
        # 28:레포츠, 32:숙박, 38:쇼핑, 39:음식점
        "contentid": item.findtext("contentid"),  # 시설 고유 코드
        "imageUrl": item.findtext("firstimage")  # 이미지 url
    }
    tourLists.append(tour)

content_count = {
    "관광지": 0,
    "문화시설": 0,
    "레포츠": 0,
    "숙박": 0,
    "쇼핑": 0,
    "음식점": 0
}

content_colors = ["pink", "cyan", "antique white", "cornflower blue", "medium spring green", "purple"]

print("<<<<관광지 목록>>>>")
for tour in tourLists:
    if tour["typeid"] == '12':
        content_count["관광지"] += 1
        print(tour)

print()
print()

print("<<<<문화시설 목록>>>>")
for tour in tourLists:
    if tour["typeid"] == '14':
        content_count["문화시설"] += 1
        print(tour)

print()
print()

print("<<<<레포츠 목록>>>>")
for tour in tourLists:
    if tour["typeid"] == '28':
        content_count["레포츠"] += 1
        print(tour)

print()
print()

print("<<<<숙박 목록>>>>")
for tour in tourLists:
    if tour["typeid"] == '32':
        content_count["숙박"] += 1
        print(tour)

print()
print()

print("<<<<쇼핑 목록>>>>")
for tour in tourLists:
    if tour["typeid"] == '38':
        content_count["쇼핑"] += 1
        print(tour)

print()
print()

print("<<<<음식점 목록>>>>")
for tour in tourLists:
    if tour["typeid"] == '39':
        content_count["음식점"] += 1
        print(tour)

root = Tk()
root.title("서울시 구별 병원 정보")

# 캔버스 생성
canvas = Canvas(root, width=800, height=400)
canvas.pack()

max_content_count = max(content_count.values())
bar_width = 20
x_gap = 30
y_gap = 30
# x0 = 60
# y0 = 250
x0 = 60
y0 = 30
content_names = list(content_count.keys())
content_values = list(content_count.values())


for i in range(6):
    x1 = x0 + 200 * content_values[i] / max_content_count
    y1 = y0 + i * (bar_width + y_gap)
    # x1 = x0 + i * (bar_width + x_gap)
    # y1 = y0 - 200 * content_values[i] / max_content_count
    canvas.create_rectangle(x0, y1, x1, y1 + bar_width, fill=content_colors[i])
    canvas.create_text(x0 - 30, y1 + bar_width / 2, text=content_names[i], anchor='s')
    canvas.create_text(x1 + 10, y1 + bar_width / 2, text=content_values[i], anchor='s')
    # canvas.create_text(x1 + bar_width / 2, y0 + 100, text=content_names[i], anchor='s')
    # canvas.create_text(x1 + bar_width / 2, y1 - 10, text=content_values[i], anchor='s')

root.mainloop()
