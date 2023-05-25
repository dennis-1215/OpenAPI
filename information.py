from tkinter import *
from tkinter import font
import xml.etree.ElementTree as ET
import requests

class Information:
    def __init__(self):
        self.window = Tk()
        self.window.title('상세정보')
        self.window.geometry("500x800")
        self.markon = PhotoImage(file='star_on.png')
        self.markoff = PhotoImage(file='star_off.png')
        self.markon = self.markon.subsample(9)
        self.markoff = self.markoff.subsample(10)

        fontstyle = font.Font(self.window, size=30)

        Label(self.window, text="관광지 검색 결과", font=fontstyle).place(x=0, y=0)
        self.bookmark = Button(self.window, text='off', image=self.markoff,bd=0,command=self.mark)
        self.bookmark.place(x=320,y=5)
        Button(self.window, text='뒤로가기', width=10, height=2, command=self.back).place(x=410,y=0)

        self.window.mainloop()

    def back(self):
        pass
    def mark(self):
        if self.bookmark['text'] == 'off':
            self.bookmark['image'] = self.markon
            self.bookmark['text'] = 'on'
        else:
            self.bookmark['text'] = 'off'
            self.bookmark['image'] = self.markoff
Information()