import io
from tkinter import *
from tkinter import font
from tkinter import scrolledtext
import xml.etree.ElementTree as ET
import requests
import main
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import spam

bookmarks = spam.fileIn()
print(bookmarks)
class Information:
    def __init__(self, contentID):
        self.window = Toplevel()
        self.window.title('상세정보')
        self.window.geometry("610x600")
        self.markon = PhotoImage(file='star_on.png')
        self.markoff = PhotoImage(file='star_off.png')
        self.markon = self.markon.subsample(9)
        self.markoff = self.markoff.subsample(10)
        # API키 깃허브 안올라가게 조심
        self.Google_API_Key = ''
        self.zoom = 13

        self.contentDic = contentID
        fontstyle = font.Font(self.window, size=30)
        fontstyle2 = font.Font(self.window, size=15)

        self.label = Label(self.window, text=" 상세 정보", font=fontstyle)
        self.label.place(x=0, y=0)
        self.bookmark = Button(self.window, text='off', image=self.markoff,bd=0,command=self.mark)
        self.bookmark.place(x=320,y=5)
        Button(self.window, text='뒤로가기', width=10, height=2, command=self.back).place(x=500,y=0)

        self.GetXML()
        if self.detail['imageUrl'] == '':
            im = Image.open('존재하지 않는 이미지.png')
            photo = ImageTk.PhotoImage(im)
        else:
            with urllib.request.urlopen(self.detail['imageUrl']) as u:
                raw_data = u.read()
            im = Image.open(BytesIO(raw_data))
            im = im.resize((300,300))
            photo = ImageTk.PhotoImage(im)
        Label(self.window, image=photo, height=300, width=300, bg='white').place(x=0, y=97)

        self.frame = Frame(self.window, width=300, height=300)
        self.frame.place(x=300, y=97)

        # API키 깃허브 안올라가게 조심
        # 맵 URL만드는 함수
        self.googlemap()
        # url받아서 이미지화
        response = requests.get(self.map_url + '&key=' + self.Google_API_Key)
        map_image = Image.open(io.BytesIO(response.content))
        map_photo = ImageTk.PhotoImage(map_image)
        # 이미지 라벨에 올리기
        Label(self.window, bg='white', height=300, width=300, image=map_photo).place(x=300, y=97)

        modifieddate = self.detail['modifiedtime']
        modidate = modifieddate[:4] + '/' + modifieddate[4:6] + '/' + modifieddate[6:8]
        self.texts = scrolledtext.ScrolledText(self.window, width=53, height=9, font=fontstyle2, bg='white')
        self.texts.insert(END, '\t\t\t     최근 수정된 날짜 : ' + modidate +'\n이름 : ' +self.detail['name']+'\n\n주소: '+self.detail['address']
                          + '\n\n상세설명 : ' + self.detail['description'])
        self.texts.configure(state='disabled')
        self.texts.place(x=0, y=400)

        self.window.mainloop()

    def GetXML(self):
        self.keyword_params = {
            "serviceKey": main.api_key,
            "numOfRows": 20000,  # 최대 2000개의 관광 정보 데이터 요청
            "contentId": self.contentDic,
            "MobileOS": "ETC",  # 필수 입력 데이터(사용x)
            "MobileApp": "AppTest",  # 필수 입력 데이터(사용x)
            "defaultYN": "Y",
            "firstImageYN": "Y",
            "mapinfoYN": "Y",
            "overviewYN": "Y",
            "addrinfoYN": "Y"
        }
        response = requests.get(main.url + main.api_detail, params=self.keyword_params)
        root = ET.fromstring(response.content)
        items = root.findall(".//item")

        for item in items:
            self.detail = {
                "name": item.findtext("title"),  # 관광지 이름
                "address": item.findtext("addr1"),  # 주소
                "mapx": item.findtext("mapx"),  # 경도
                "mapy": item.findtext("mapy"),  # 위도
                "contentid": item.findtext("contentid"),  # 시설 고유 코드
                "imageUrl": item.findtext("firstimage"),  # 이미지 url
                "description": item.findtext("overview"),    # 상세 설명
                "modifiedtime": item.findtext("modifiedtime")
            }

    def back(self):
        self.window.destroy()

    def mark(self):
        if self.bookmark['text'] == 'off':
            self.bookmark['image'] = self.markon
            self.bookmark['text'] = 'on'
            for bookmark in bookmarks:
                if self.detail['contentid'] in bookmark:
                    return
            bookmarks.append([self.detail["contentid"], self.detail['name']])

        else:
            self.bookmark['text'] = 'off'
            self.bookmark['image'] = self.markoff
    def googlemap(self):    # API키 깃허브 안올라가게 조심
        self.map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={self.detail['mapy']},{self.detail['mapx']}&zoom={self.zoom}&size=400x400&maptype=roadmap"
        mapy, mapx = self.detail['mapy'], self.detail['mapx']
        marker_url = f"&markers=color:red%7C{mapy},{mapx}"
        self.map_url += marker_url

if __name__ == '__main__':
    Information(131382)
