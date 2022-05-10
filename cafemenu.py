# Cafe Menu, prompts login and stores existing logins, and presents the cafe menu for ordering.

# Libraries
import math
from tkinter import ttk
import tkinter

#GUI Setup
root = tkinter.Tk()
s = ttk.Style(root)
root.geometry("300x500+150+200")

mainFrameLeft = ttk.Frame(root)
mainFrameLeft.pack(side="left", expand=True, fill="both", ipadx=10, ipady=10)

mainFrameRight = ttk.Frame(root)
mainFrameRight.pack(side="right", expand=True, fill="both", ipadx=10, ipady=10)

#Global Functions
def fillConv(i):
    i = 1-(i%2)
    if i == 0: return mainFrameLeft
    else: return mainFrameRight

#Classes
s.configure("ItemFrame.TFrame", background="white")
s.configure("ItemFrame.TButton", background="#99032e")
s.configure("ItemFrame.TLabel", background="#b0ffe9")
s.configure("ItemFrameA.TLabel", background="#99032e", foreground="#FFFFFF")
class ItemFrame:
    def __init__(self,name,info,i) -> None:
        #Store Arguments
        self.Info = info
        self.Name = name

        #Frame Style
        #Create Base Frame
        f = fillConv(i)
        self.Frame = ttk.Frame(f, height=100, width=500, style="ItemFrame.TFrame")
        self.Frame.pack(side="top", fill="x", ipadx=10, ipady=10)
        
        #self.Frame.grid(column=1-(i%2),row=math.ceil(i/2))

        label = ttk.Label(self.Frame, text=name, anchor="center", style="ItemFrame.TLabel")
        label.pack(expand=True,fill="both")
        ttk.Label(self.Frame, style="ItemFrameA.TLabel", text="$" + str(float(info["Price"]))).pack(fill="both",expand=True,side="left")
        ttk.Button(self.Frame, style="ItemFrame.TButton", text="Add to order", command=self.f).pack(fill="both",expand=True,side="right")

        pass

    def f(self):
        self.obj.configure(text=self.info["ClickText"])

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
    }
}

i = 0
for Name,Info in Items.items():
    i += 1
    ItemFrame(Name,Info,i)

root.mainloop()