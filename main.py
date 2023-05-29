from tkinter import *
from tkinter import font
import xml.etree.ElementTree as ET
import requests
import search
import favorite

# 공공데이터 API 키
api_key = 'FY7EEMN2XjyyDAaIDkLDvSUP1oMLoUsDPDd+EmzrNf/fB6r2A4hrTNwXRG4XgVEKcyFa7KrwJHHG83ohTl/81g=='
url = "http://apis.data.go.kr/B551011/KorService1/"
api_keyword = "searchKeyword1"
api_location = "locationBasedList1"
api_detail = "detailCommon1"
api_image = "detailImage1"

class MainGUI:
    def __init__(self, keyword=""):
        self.content_List = ["관광지", "문화시설", "레포츠", "숙박", "쇼핑", "음식점"]
        self.content_colors = ["pink", "cyan", "antique white", "cornflower blue", "medium spring green", "purple"]
        self.fileName = ["tour.png", "culture.png", "leports.png", "hotel.png", "shopping.png", "restaurant.png"]
        self.buttonIamges = []
        self.InitMain()
        self.keyword = keyword
    def SearchPage(self, case):
        typeids = [12, 14, 28, 32, 38, 39]
        if self.keyword == "":
            return None
        self.root.destroy()
        search.Search(self.keyword, typeids[case], self.content_List[case])

    def FavoritePage(self):
        self.root.destroy()
        favorite.Favorite()

    def InitMain(self):
        self.root = Tk()
        self.root.geometry("600x800")
        self.root.title("관광지 정보")

        # 폰트
        self.main_font = font.Font(size=16, family='Consolas')
        self.main_fontB = font.Font(size=12, weight='bold', family='Consolas')

        # frame1 : 검색 entry
        self.frame1 = Frame(self.root, width=100, height=20)
        self.frame1.place(x=100, y=0)

        self.label_search = Label(self.frame1, text="검색", font=self.main_fontB)
        self.entry_search = Entry(self.frame1, width=30, font=self.main_fontB)
        self.label_search.pack(side=LEFT)
        self.entry_search.pack()

        # frame2 : 그래프 그리는 캔버스
        self.frame2 = Frame(self.root, width=500, height=500)
        self.frame2.place(x=50, y=50)

        self.canvas = Canvas(self.frame2, width=500, height=500, bg='white')
        self.canvas.pack()

        # frame3 : 버튼 5개
        self.frame3 = Frame(self.root, width=600, height=200)
        self.frame3.place(x=20, y=580)

        # 버튼
        self.buttons = []

        for i in range(6):
            self.buttonIamges.append(PhotoImage(file="icon/"+self.fileName[i]))
            self.buttonIamges[i] = self.buttonIamges[i]

        for i in range(6):
            self.buttons.append(
                Button(self.frame3, image=self.buttonIamges[i], width=80, height=80, bg=self.content_colors[i],
                       command=lambda case=i: self.SearchPage(case)).place(x=i * 95, y=10))

        self.buttons.append(Button(self.frame3, text="즐겨찾기", bg="yellow", width=45, height=2, font=self.main_font,
                       command=self.FavoritePage).place(x=3, y=120))

        self.GetXML("")

        self.entry_search.bind("<Return>", self.GetXML)

        self.root.mainloop()

    def GetXML(self, str):
        self.keyword = self.entry_search.get()

        self.keyword_params = {
            "serviceKey": api_key,
            "numOfRows": 20000,  # 최대 2000개의 관광 정보 데이터 요청
            "MobileOS": "ETC",  # 필수 입력 데이터(사용x)
            "MobileApp": "AppTest",  # 필수 입력 데이터(사용x)
            "Keyword": self.keyword,  # 필수 입력 데이터(input 값을 넣음)
        }

        response = requests.get(url + api_keyword, params=self.keyword_params)
        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        self.tourLists = []

        for item in items:
            self.tour = {
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
            self.tourLists.append(self.tour)

        self.content_count = {
            "관광지": 0,
            "문화시설": 0,
            "레포츠": 0,
            "숙박": 0,
            "쇼핑": 0,
            "음식점": 0
        }

        for self.tour in self.tourLists:
            if self.tour["typeid"] == '12':
                self.content_count["관광지"] += 1
            elif self.tour["typeid"] == '14':
                self.content_count["문화시설"] += 1
            elif self.tour["typeid"] == '28':
                self.content_count["레포츠"] += 1
            elif self.tour["typeid"] == '32':
                self.content_count["숙박"] += 1
            elif self.tour["typeid"] == '38':
                self.content_count["쇼핑"] += 1
            elif self.tour["typeid"] == '39':
                self.content_count["음식점"] += 1

        self.DrawGraph()


    def DrawGraph(self):
        self.canvas.destroy()
        self.canvas = Canvas(self.frame2, width=500, height=500, bg='white')
        self.canvas.pack()
        # 그래프 막대 그리기
        max_content_count = max(self.content_count.values())
        bar_width = 30
        y_gap = 50
        x0 = 80
        y0 = 30
        content_names = list(self.content_count.keys())
        content_values = list(self.content_count.values())

        for i in range(6):
            x1 = x0 + 400 * content_values[i] / max(max_content_count, 1)
            y1 = y0 + i * (bar_width + y_gap)
            self.canvas.create_rectangle(x0, y1, x1, y1 + bar_width, fill=self.content_colors[i])
            self.canvas.create_text(x0 - 40, y1 + bar_width / 2, text=content_names[i], anchor='s')
            self.canvas.create_text(x1 + 10, y1 + bar_width / 2, text=content_values[i], anchor='s')

if __name__ == "__main__":
    MainGUI()




