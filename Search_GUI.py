from tkinter import *
from tkinter import font
import xml.etree.ElementTree as ET
import requests

class Search:
    def __init__(self):
        self.window = Tk()
        self.window.title('검색 결과')
        # self.window.configure(bg='light gray')
        fontstyle = font.Font(self.window, size=30)
        self.frame = Frame(self.window)
        self.frame.pack()
        Label(self.frame, text="관광지 검색 결과", font=fontstyle).pack(side=LEFT)
        Button(self.frame, text='뒤로가기', width=10, height=2,command=self.back).pack(side=RIGHT)
        self.InitListbox()
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
        for i in range(40):
            self.Listbox.insert(END,str(i))
        scrollbar.config(command=self.Listbox.yview)


Search()