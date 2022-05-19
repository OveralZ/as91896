# Cafe Menu, prompts login and stores existing logins, and presents the cafe menu for ordering.

# Libraries
import math
from operator import truediv
from re import A
from tkinter import Widget, ttk
import tkinter

#Menu
Items = {
    "Potato Puff": {
        "Price": 3.5,
        "Tier": "S",
    },
    "Hot Noodles": {
        "Price": 3.5,
        "Tier": "S+",
    },
    "Spaghetti Bun": {
        "Price": 2,
        "Tier": "B",
    },
    "Placeholder Bun": {
        "Price": 2,
        "Tier": "B",
    },
    "Placeholder Bun 2": {
        "Price": 2,
        "Tier": "B",
    },
    "Placeholder Bun 3": {
        "Price": 2,
        "Tier": "B",
    },
    "Placeholder Bun 4": {
        "Price": 2,
        "Tier": "B",
    },
    "Placeholder Bun 5": {
        "Price": 2,
        "Tier": "B",
    },
    "Placeholder Bun 6": {
        "Price": 2,
        "Tier": "B",
    },
    "Placeholder Bun 7": {
        "Price": 2,
        "Tier": "B",
    },
}

#GUI Setup
root = tkinter.Tk()
s = ttk.Style(root)
root.geometry("300x500+150+200")

#Styles
s.configure("ItemFrame.TFrame", background="white")
s.configure("ItemFrame.TButton", background="#99032e")
s.configure("ItemFrame.TLabel", background="#b0ffe9")
s.configure("ItemFrameA.TLabel", background="#99032e", foreground="#FFFFFF")



#Global Functions
def fillConv(i, mainFrameLeft, mainFrameRight):
    i = 1-(i%2)
    if i == 0: return mainFrameLeft
    else: return mainFrameRight

#Classes
class Menu:
    def __init__(self) -> None:
        
        self.menuCanvas = tkinter.Canvas(root)
        self.mainFrame = ttk.Frame(self.menuCanvas)
        self.scroll = ttk.Scrollbar(self.menuCanvas, orient='vertical', command=self.menuCanvas.yview)
            
        self.mainFrame.bind(
            "<Configure>",
            lambda e: self.menuCanvas.configure(
                scrollregion=self.menuCanvas.bbox("all")
            )
        )

        self.window = self.menuCanvas.create_window((0, 0), window=self.mainFrame, anchor="nw")
        self.menuCanvas.configure(yscrollcommand=self.scroll.set)

        self. menuCanvas.bind('<Configure>', self.FrameWidth)

        self.mainFrameLeft = ttk.Frame(self.mainFrame)
        self.mainFrameRight = ttk.Frame(self.mainFrame)

        pass

    def FrameWidth(self,event):
        canvas_width = event.width
        self.menuCanvas.itemconfig(self.window, width = canvas_width-19)

    def Setup(self):
        i = 0
        for _ in range(1,3):
            for Name,Info in Items.items():
                i += 1
                ItemFrame(Name,Info,i,self.mainFrameLeft,self.mainFrameRight)
        self.menuCanvas.pack(fill="both", expand=True)
        self.scroll.pack(side="right",fill="both")

        self.mainFrameLeft.pack(side="left", expand=True, fill="both")
        self.mainFrameRight.pack(side="right", expand=True, fill="both")

class ItemFrame:
    def __init__(self,name,info,i,mfl,mfr) -> None:
        #Store Arguments
        self.Info = info
        self.Name = name

        #Frame Style
        #Create Base Frame
        f = fillConv(i,mfl,mfr)
        self.Frame = ttk.Frame(f, height=100, width=500, style="ItemFrame.TFrame")
        self.Frame.pack(side="top", fill="x", ipadx=10, ipady=10)
        
        label = ttk.Label(self.Frame, text=name, anchor="center", style="ItemFrame.TLabel")
        label.pack(expand=True,fill="both")
        ttk.Label(self.Frame, style="ItemFrameA.TLabel", text="$" + str(float(info["Price"]))).pack(fill="both",expand=True,side="left")
        ttk.Button(self.Frame, style="ItemFrame.TButton", text="Add to order", command=self.f).pack(fill="both",expand=True,side="right")

        pass

    def f(self):
        self.obj.configure(text=self.info["ClickText"])

menu = Menu()
menu.Setup()

root.mainloop()