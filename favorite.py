from tkinter import *
from tkinter import font
from tkinter import ttk
import xml.etree.ElementTree as ET
import requests
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO
import main

class Favorite:
    def __init__(self):
        self.window = Tk()
        self.window.title('즐겨찾기')
        self.window.geometry("600x800")

        fontstyle = font.Font(self.window, size=30)

        Label(self.window, text="즐겨찾기", font=fontstyle).place(x=0, y=0)
        Button(self.window, text='뒤로가기', width=10, height=2,command=self.back).place(x=500, y=0)

        self.GetXML()
        self.InitListbox()  # 리스트 박스생성
        self.window.mainloop()

    def back(self):
        self.window.destroy()
        main.MainGUI()

    def test(self, none):
        print(none)

    def InitListbox(self):
        # 이 함수는 나중에 C/C++로 파일 입출력으로 다시 구현할 예정
        pass

    def GetXML(self):
        # 이 함수 또한 C/C++ 파일 입출력으로 바꿀 예정
        pass



if __name__ == "__main__":
    Favorite(0, 0)    # 인자는 keyword(검색), typeid(관광 시설 구분 코드)