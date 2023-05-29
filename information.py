from tkinter import *
from tkinter import font
import xml.etree.ElementTree as ET
import requests
import search

class Information:
    def __init__(self, contentDic, image):
        self.window = Toplevel()
        self.window.title('상세정보')
        self.window.geometry("600x600")
        self.markon = PhotoImage(file='star_on.png')
        self.markoff = PhotoImage(file='star_off.png')
        self.markon = self.markon.subsample(9)
        self.markoff = self.markoff.subsample(10)
        none_image = PhotoImage(file='존재하지 않는 이미지.png')

        self.contentDic = contentDic
        print(self.contentDic)
        self.image = image
        fontstyle = font.Font(self.window, size=30)
        fontstyle2 = font.Font(self.window, size=15)

        Label(self.window, text="관광지 상세 정보", font=fontstyle).place(x=0, y=0)
        self.bookmark = Button(self.window, text='off', image=self.markoff,bd=0,command=self.mark)
        self.bookmark.place(x=320,y=5)
        Button(self.window, text='뒤로가기', width=10, height=2, command=self.back).place(x=500,y=0)
        if self.image:
            self.image.width()
            Label(self.window, image=self.image, height=300, width=300, bg='white').place(x=0, y=100)
        Label(self.window, width=54, height=10,font=fontstyle2,bg='white',
              text=self.contentDic['name']+'\n주소: '+self.contentDic['address']+'\n위도 : '+self.contentDic['mapx']+'\n경도 : '+self.contentDic['mapy']).place(x=0, y=400)

        self.window.mainloop()

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