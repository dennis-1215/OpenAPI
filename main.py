from tkinter import *
from tkinter import font
from tkinter import ttk
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import requests

import information
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
        self.typeids = [12, 14, 28, 32, 38, 39]
        self.content_colors = ["pink", "cyan", "antique white", "cornflower blue", "medium spring green", "purple"]
        self.fileName = ["graph.png", "tour.png", "culture.png", "leports.png", "hotel.png", "shopping.png", "restaurant.png", "star.png"]
        self.buttonIamges = []
        self.InitMain()
        self.keyword = keyword

    def InitMain(self):
        self.root = Tk()
        self.root.geometry("600x800")
        self.root.title("관광지 정보")

        # 폰트
        self.main_font = font.Font(size=16, family='Consolas')
        self.main_fontB = font.Font(size=12, weight='bold', family='Consolas')
        self.font_16_B = font.Font(size=16, weight='bold', family='Consolas')

        # frame1 : 검색 entry
        self.frame1 = Frame(self.root, width=100, height=20)
        self.frame1.place(x=100, y=0)

        self.label_search = Label(self.frame1, text="검색", font=self.main_fontB)
        self.entry_search = Entry(self.frame1, width=30, font=self.main_fontB)
        self.label_search.pack(side=LEFT)
        self.entry_search.pack()

        # frame3 : 버튼 5개
        # self.frame3 = Frame(self.root, width=600, height=200)
        # self.frame3.place(x=20, y=580)

        self.frame3 = ttk.Notebook(self.root, width=500, height=600)
        self.frame3.place(x=20, y=80)

        # 버튼
        self.buttons = []

        for i in range(8):
            self.buttonIamges.append(PhotoImage(file="icon/" + self.fileName[i]))

        self.tapList = []

        for i in range(0, 8):
            self.tapList.append(Label(self.root))
            self.frame3.add(self.tapList[i], image=self.buttonIamges[i])

        self.GetXML("")

        self.entry_search.bind("<Return>", self.GetXML)
        self.root.mainloop()

    def GetXML(self, str):
        self.frame3.select(0)
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
            #print(self.tour)
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
        Label(self.tapList[0], text=self.keyword + " 검색 결과", font=self.font_16_B).place(x=200, y=0)
        self.canvas = Canvas(self.tapList[0], width=500, height=500, bg='white')
        self.canvas.place(x=20, y=50)
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


        self.InitListbox()
        self.makeList()

    def InitListbox(self):
        self.treeviews = []
        for i in range(1, 8):
            if not i == 7:
                Label(self.tapList[i], text=self.content_List[i-1]+" 검색 결과", font=self.font_16_B).place(x=0, y=0)
            else:
                Label(self.tapList[i], text="즐겨찾기 목록", font=self.font_16_B).place(x=0, y=0)


            self.frame_list = Frame(self.tapList[i])
            self.frame_list.place(x=10, y=50)

            scrollbar = Scrollbar(self.frame_list)  # 스크롤 바 만듬
            scrollbar.pack(side=RIGHT, fill='y')    # 스크롤 바 팩


            self.treeview = ttk.Treeview(self.frame_list, height=25 ,columns=('A'),yscrollcommand=scrollbar.set) # Treeview위젯 생성
            self.treeview.pack()

            self.treeview.column('#0', width=40)   # 첫번째 열(이게 아마 디폴트 열인듯?) 너비를 550으로 설정
            self.treeview.heading('#0', text='번호')

            self.treeview.column('A', anchor='center', width=470)
            self.treeview.heading('A', text='이름', anchor='center')

            self.treeviews.append(self.treeview)
            scrollbar.config(command=self.treeview.yview)  # 이건 스크롤 관련
            self.treeview.bind('<Double-Button-1>', self.Information)

        # type(self.tourLists[0]['name'])

    def Information(self, event):
        tab_index = self.frame3.index("current")
        selectedItem = self.treeviews[tab_index - 1].selection()
        index = int(selectedItem[0])
        information.Information(self.tourLists[index]['contentid'])

    def makeList(self):
        content_count = {
            "12": 0,
            "14": 0,
            "28": 0,
            "32": 0,
            "38": 0,
            "39": 0
        }
        tapList = [12, 14, 28, 32, 38, 39]
        for i in range(len(self.tourLists)):
            if int(self.tourLists[i]['typeid']) in self.typeids:
                content_count[self.tourLists[i]['typeid']] += 1
                self.treeviews[tapList.index(int(self.tourLists[i]['typeid']))].insert('', 'end', text=content_count[self.tourLists[i]['typeid']], values=(self.tourLists[i]['name'].replace(' ', '\ ')), iid=i)
            style = ttk.Style()                             # Treeview 내부의 행들 높이 설정해 줄려고 만듬
            style.configure('Treeview', rowheight=20)      # 행의 높이 크기 늘려줌 (원래 글자만 들어갈 정도로 작았음)

            #self.treeview.bind('<ButtonRelease-1>', self.Information)

if __name__ == "__main__":
    MainGUI()
