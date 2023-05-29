from tkinter import *
from tkinter import font
from tkinter import ttk
import xml.etree.ElementTree as ET
import requests
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import main
import information

class Search:
    def __init__(self, keyword, typeid, content = '관광'):
        self.window = Tk()
        self.window.title('검색 결과')
        self.window.geometry("600x800")

        self.keyword = keyword
        self.typeid = typeid
        self.content = content

        fontstyle = font.Font(self.window, size=30)

        Label(self.window, text=self.content + " 검색 결과", font=fontstyle).place(x=0, y=0)
        Button(self.window, text='뒤로가기', width=10, height=2,command=self.back).place(x=500, y=0)

        self.GetXML()
        self.InitListbox()  # 리스트 박스생성
        self.window.mainloop()

    def back(self):
        self.window.destroy()
        main.MainGUI()
    def Information(self, event):
        selectedItem = self.treeview.selection()
        print(type(selectedItem[0]))
        index = int(selectedItem[0])
        # photo = self.Inform_Image(index)
        information.Information(self.contentList[index], self.photo_inform[index])

    def Inform_Image(self, index):
        if self.contentList[index]['imageUrl'] != '':  # 만약 이미지가 있다면
            with urllib.request.urlopen(self.contentList[index]['imageUrl']) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((400, 400))
            photo = ImageTk.PhotoImage(im)
            return photo
        return ''

    def click_item(self, event):
        selectedItem = self.treeview.selection()
        print(selectedItem)

    def InitListbox(self):
        self.photo_list = []  # 사진 들어갈것
        self.photo_inform = []
        self.frame_list = Frame(self.window)
        self.frame_list.place(x=10, y=100)

        scrollbar = Scrollbar(self.frame_list)  # 스크롤 바 만듬
        scrollbar.pack(side=RIGHT, fill='y')    # 스크롤 바 팩

        self.treeview = ttk.Treeview(self.frame_list, columns=('A'),yscrollcommand=scrollbar.set) # Treeview위젯 생성
        self.treeview.pack()

        self.treeview.column('#0', width=200)   # 첫번째 열(이게 아마 디폴트 열인듯?) 너비를 550으로 설정
        self.treeview.column('A', anchor='center', width=350)
        # type(self.contentList[0]['name'])

        img = Image.open('존재하지 않는 이미지.png')
        none_image_s = ImageTk.PhotoImage(img.resize((150,150)))
        none_image_i = ImageTk.PhotoImage(img)


        for i in range(len(self.contentList)):
            if self.contentList[i]['imageUrl'] != '':   # 만약 이미지가 있다면
                with urllib.request.urlopen(self.contentList[i]['imageUrl']) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data))
                im = im.resize((150, 150))
                photo = ImageTk.PhotoImage(im)      # url 받아서 이미지화 하는 과정들 (교수님 예시보고 따라함)
                self.photo_list.append(photo)       # photo_list로 저장해놔야 사진들이 다 나옴
                im = im.resize((300, 300))
                photo = ImageTk.PhotoImage(im)
                self.photo_inform.append(photo)
                self.treeview.insert('', 'end', image=self.photo_list[-1], values=(self.contentList[i]['name'].replace(' ', '\ ')), iid=i)    # 만들어둔 treeview 객체에 인서트
            else:
                self.photo_inform.append(none_image_i)
                self.photo_list.append(none_image_s)
                self.treeview.insert('', 'end', image=self.photo_list[-1], values=(self.contentList[i]['name'].replace(' ', '\ ')), iid=i) # 사진이 없으면 그냥 공백넣기
            print(self.contentList[i]['name'])          # 이건 이름이 잘 안나오길래 이름 잘 불러왔나 테스트한거
        style = ttk.Style()                             # Treeview 내부의 행들 높이 설정해 줄려고 만듬
        style.configure('Treeview', rowheight=200)      # 행의 높이 크기 늘려줌 (원래 글자만 들어갈 정도로 작았음)
        self.treeview.configure(height=3)               # 그랬더니 Treeview 위젯의 높이가 행높이에 곱해져서 위젯 자체의 높이를 줄임

        scrollbar.config(command=self.treeview.yview)   # 이건 스크롤 관련
        self.treeview.bind('<ButtonRelease-1>', self.Information)


    def GetXML(self):
        self.keyword_params = {
            "serviceKey": main.api_key,
            "numOfRows": 20000,  # 최대 2000개의 관광 정보 데이터 요청
            "contentTypeId": self.typeid,
            "MobileOS": "ETC",  # 필수 입력 데이터(사용x)
            "MobileApp": "AppTest",  # 필수 입력 데이터(사용x)
            "Keyword": self.keyword,  # 필수 입력 데이터(input 값을 넣음)
        }

        response = requests.get(main.url + main.api_keyword, params=self.keyword_params)
        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        self.contentList = []

        for item in items:
            self.tour = {
                "name": item.findtext("title"),  # 관광지 이름
                "address": item.findtext("addr1"),  # 주소
                "mapx": item.findtext("mapx"),  # 경도
                "mapy": item.findtext("mapy"),  # 위도
                "typeid": item.findtext("contenttypeid"),
                "contentid": item.findtext("contentid"),  # 시설 고유 코드
                "imageUrl": item.findtext("firstimage")  # 이미지 url
            }
            self.contentList.append(self.tour)



if __name__ == "__main__":
    Search(0, 0)    # 인자는 keyword(검색), typeid(관광 시설 구분 코드)