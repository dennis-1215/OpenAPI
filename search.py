from tkinter import *
from tkinter import font
import xml.etree.ElementTree as ET
import requests
import main

class Search:
    def __init__(self, keyword, typeid, content):
        self.window = Tk()
        self.window.title('검색 결과')
        self.window.geometry("600x800")

        self.keyword = keyword
        self.typeid = typeid
        self.content = content

        # self.window.configure(bg='light gray')
        fontstyle = font.Font(self.window, size=30)
        self.frame = Frame(self.window)
        self.frame.pack()

        Label(self.frame, text=self.content + " 검색 결과", font=fontstyle).pack(side=LEFT)
        Button(self.frame, text='뒤로가기', width=10, height=2,command=self.back).pack(side=RIGHT)

        self.GetXML()
        self.InitListbox()  # 리스트 박스생성
        self.window.mainloop()
    def back(self):
        pass
    def InitListbox(self):
        self.frame_list = Frame(self.window)
        self.frame_list.pack()
        scrollbar = Scrollbar(self.frame_list)
        scrollbar.pack(side=RIGHT,fill='y')
        self.Listbox = Listbox(self.frame_list, width=50,height=20, yscrollcommand=scrollbar.set)
        self.Listbox.pack()
        for i in range(len(self.contentList)):
            self.Listbox.insert(END,str(i))
        scrollbar.config(command=self.Listbox.yview)

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
    Search(0, 0, 0)    # 인자는 keyword(검색), typeid(관광 시설 구분 코드)