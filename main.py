from tkinter import *
from tkinter import font
from tkinter import ttk
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
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
        self.typeids = [12, 14, 28, 32, 38, 39]
        self.content_colors = ["pink", "cyan", "antique white", "cornflower blue", "medium spring green", "purple"]
        self.fileName = ["tour.png", "culture.png", "leports.png", "hotel.png", "shopping.png", "restaurant.png"]
        self.buttonIamges = []
        self.InitMain()
        self.keyword = keyword

    def SearchPage(self, case):
        if self.keyword == "":
            return None
        self.root.destroy()
        search.Search(self.keyword, self.typeids[case], self.content_List[case])

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
        self.font_16_B = font.Font(size=16, weight='bold', family='Consolas')

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
        # self.frame3 = Frame(self.root, width=600, height=200)
        # self.frame3.place(x=20, y=580)

        self.frame3 = ttk.Notebook(self.root, width=500, height=600)
        self.frame3.place(x=20, y=80)

        # 버튼
        self.buttons = []

        for i in range(6):
            self.buttonIamges.append(PhotoImage(file="icon/" + self.fileName[i]))

        self.tapList = []
        for i in range(6):
            self.tapList.append(Label(self.root, bg=self.content_colors[i]))
            self.frame3.add(self.tapList[i], image=self.buttonIamges[i])
        self.canvasFrame = Label(self.root)
        self.frame3.insert(0, self.canvasFrame, image=self.buttonIamges[0])

        # for i in range(6):
        #     self.buttons.append(
        #         Button(self.frame3, image=self.buttonIamges[i], width=80, height=80, bg=self.content_colors[i],
        #                command=lambda case=i: self.SearchPage(case)).place(x=i * 95, y=10))

        # self.buttons.append(Button(self.frame3, text="즐겨찾기", bg="yellow", width=45, height=2, font=self.main_font,
        #                command=self.FavoritePage).place(x=3, y=120))

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
        Label(self.canvasFrame, text=self.keyword + " 검색 결과", font=self.font_16_B).place(x=200, y=0)
        self.canvas = Canvas(self.canvasFrame, width=500, height=500, bg='white')
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

        for i in range(6):
            self.InitListbox(self.tapList[i], i)
    def InitListbox(self, frame, num):
        self.photo_list = []  # 사진 들어갈것
        self.photo_inform = []
        self.frame_list = Frame(frame)
        self.frame_list.place(x=10, y=100)

        scrollbar = Scrollbar(self.frame_list)  # 스크롤 바 만듬
        scrollbar.pack(side=RIGHT, fill='y')    # 스크롤 바 팩

        self.treeview = ttk.Treeview(self.frame_list, columns=('A'),yscrollcommand=scrollbar.set) # Treeview위젯 생성
        self.treeview.pack()

        self.treeview.column('#0', width=200)   # 첫번째 열(이게 아마 디폴트 열인듯?) 너비를 550으로 설정
        self.treeview.column('A', anchor='center', width=350)
        # type(self.tourLists[0]['name'])

        img = Image.open('존재하지 않는 이미지.png')
        none_image_s = ImageTk.PhotoImage(img.resize((150,150)))
        none_image_i = ImageTk.PhotoImage(img)


        for i in range(len(self.tourLists)):
            print("nowid :", self.tourLists[i]['typeid'])
            print("typeids : ", self.typeids[num])
            if self.tourLists[i]['typeid'] == str(self.typeids[num]):
                print("         correct!")
                if self.tourLists[i]['imageUrl'] != '':   # 만약 이미지가 있다면
                    with urllib.request.urlopen(self.tourLists[i]['imageUrl']) as u:
                        raw_data = u.read()
                    im = Image.open(BytesIO(raw_data))
                    im = im.resize((150, 150))
                    photo = ImageTk.PhotoImage(im)      # url 받아서 이미지화 하는 과정들 (교수님 예시보고 따라함)
                    self.photo_list.append(photo)       # photo_list로 저장해놔야 사진들이 다 나옴
                    im = im.resize((300, 300))
                    photo = ImageTk.PhotoImage(im)
                    self.photo_inform.append(photo)
                    self.treeview.insert('', 'end', image=self.photo_list[-1], values=(self.tourLists[i]['name'].replace(' ', '\ ')), iid=i)    # 만들어둔 treeview 객체에 인서트
                else:
                    self.photo_inform.append(none_image_i)
                    self.photo_list.append(none_image_s)
                    self.treeview.insert('', 'end', image=self.photo_list[-1], values=(self.tourLists[i]['name'].replace(' ', '\ ')), iid=i) # 사진이 없으면 그냥 공백넣기
                print(self.tourLists[i]['name'])          # 이건 이름이 잘 안나오길래 이름 잘 불러왔나 테스트한거
            style = ttk.Style()                             # Treeview 내부의 행들 높이 설정해 줄려고 만듬
            style.configure('Treeview', rowheight=200)      # 행의 높이 크기 늘려줌 (원래 글자만 들어갈 정도로 작았음)
            self.treeview.configure(height=3)               # 그랬더니 Treeview 위젯의 높이가 행높이에 곱해져서 위젯 자체의 높이를 줄임

            scrollbar.config(command=self.treeview.yview)   # 이건 스크롤 관련
            #self.treeview.bind('<ButtonRelease-1>', self.Information)

if __name__ == "__main__":
    MainGUI()
