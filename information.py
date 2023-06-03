from tkinter import *
from tkinter import font
import xml.etree.ElementTree as ET
import main
import requests

class Information:
    def __init__(self, contentID):
        self.window = Toplevel()
        self.window.title('상세정보')
        self.window.geometry("600x600")
        self.markon = PhotoImage(file='star_on.png')
        self.markoff = PhotoImage(file='star_off.png')
        self.markon = self.markon.subsample(9)
        self.markoff = self.markoff.subsample(10)

        self.contentDic = contentID
        fontstyle = font.Font(self.window, size=30)
        fontstyle2 = font.Font(self.window, size=15)

        Label(self.window, text="관광지 상세 정보", font=fontstyle).place(x=0, y=0)
        self.bookmark = Button(self.window, text='off', image=self.markoff,bd=0,command=self.mark)
        self.bookmark.place(x=320,y=5)
        Button(self.window, text='뒤로가기', width=10, height=2, command=self.back).place(x=500,y=0)
        self.frame = Frame(self.window, width=550, height=500, bg="white")
        self.frame.place(x=10, y=50)

        self.GetXML()
        self.window.mainloop()

    def GetXML(self):
        self.keyword_params = {
            "serviceKey": main.api_key,
            "numOfRows": 20000,  # 최대 2000개의 관광 정보 데이터 요청
            "contentid": self.contentDic,
            "MobileOS": "ETC",  # 필수 입력 데이터(사용x)
            "MobileApp": "AppTest",  # 필수 입력 데이터(사용x)
        }
        response = requests.get(main.url + main.api_detail, params=self.keyword_params)
        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        self.contentDetails = []

        for item in items:
            self.tour = {
                "name": item.findtext("title"),  # 관광지 이름
                "address": item.findtext("addr1"),  # 주소
                "mapx": item.findtext("mapx"),  # 경도
                "mapy": item.findtext("mapy"),  # 위도
                "contentid": item.findtext("contentid"),  # 시설 고유 코드
                "imageUrl": item.findtext("firstimage"),  # 이미지 url
                "description": item.findtext("overview")    # 상세 설명
            }
            self.contentDetails = self.tour

    def PrintDetail(self):
        pass

    def back(self):
        self.window.destroy()

    def mark(self):
        if self.bookmark['text'] == 'off':
            self.bookmark['image'] = self.markon
            self.bookmark['text'] = 'on'
        else:
            self.bookmark['text'] = 'off'
            self.bookmark['image'] = self.markoff

if __name__ == '__main__':
    dic = {'name': '울산 컨트리클럽', 'address': '울산광역시 울주군 웅촌면 웅촌로 1', 'mapx': '129.1871810750', 'mapy': '35.4415154014', 'typeid': '28', 'contentid': '131382', 'imageUrl': ''}
    Information(dic, '')