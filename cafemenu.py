# Cafe Menu, prompts login and stores existing logins, and presents the cafe menu for ordering.

# Libraries
from re import A
from tkinter import CENTER, END, Widget, ttk
import tkinter
import json

#Logins
loginsjson = None
logins = None
try:
    loginsjson = open("logins.json","r+")
except FileNotFoundError:
    loginsjson = open("logins.json","a+")
    json.dump({},loginsjson)

logins = json.load(loginsjson)
loginsjson.close()

#Menu
from menu import Items

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
class ScrollingCanvas:
    def __init__(self):
        self.canvas = tkinter.Canvas(root)
        self.frame = ttk.Frame(self.canvas)
        self.scroll = ttk.Scrollbar(self.canvas, orient='vertical', command=self.canvas.yview)
            
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.window = self.canvas.create_window((0, 0), window=self.frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        self.canvas.bind('<Configure>', self.frameWidth)

        pass

    def frameWidth(self,event):
        canvas_width = event.width
        self.canvas.itemconfig(self.window, width = canvas_width-19)

class Menu:
    def __init__(self):
        
        self.botFrame = ttk.Frame(root,borderwidth=5,relief="sunken")
        self.costLabel = ttk.Label(self.botFrame, text="Current Order Cost: $0", anchor="center")
        self.costLabel.pack(expand=True,fill="both")
        self.displayButton = ttk.Button(self.botFrame, text="Display Order", command=self.displayOrder)
        self.displayButton.pack(fill="both",expand=True)
        self.exportButton = ttk.Button(self.botFrame, text="Export Order", command=self.exportOrder)
        self.exportButton.pack(fill="both",expand=True, side="right")
        self.clearButton = ttk.Button(self.botFrame, text="Clear Order", command=self.clearOrder)
        self.clearButton.pack(fill="both",expand=True, side="left")

        self.menuCreate()

        pass

    def menuCreate(self):
        self.menuCanvas = ScrollingCanvas()
        self.mainFrame = self.menuCanvas.frame

        self.mainFrameLeft = ttk.Frame(self.mainFrame)
        self.mainFrameRight = ttk.Frame(self.mainFrame)

        self.displayButton.configure(text="Display Order", command=self.displayOrder)

        self.setup(True)

    def exportOrder(self):
        if len(self.Orders) > 0:
            print(self.Orders)
        else:
            self.exportButton.configure(text = "Please order a product first!")
    
    def clearOrder(self):
        self.totalCost = 0
        self.costLabel.configure(text="Current Order Cost: $0")
        self.Orders.clear()

    def displayOrder(self):
        if len(self.Orders) > 0:
            self.menuCanvas.canvas.destroy()
            self.displayButton.configure(text="Display Menu", command=self.menuCreate)

            self.orderCanvas = ScrollingCanvas()
            for Name, Amt in self.Orders.items():
                ItemLabel({"Name": Name, "Amount": Amt},self)
            self.orderCanvas.canvas.place(relwidth=1,relheight=0.8)
            self.orderCanvas.scroll.pack(side="right",fill="both")
        else:
            self.displayButton.configure(text = "Please order a product first!")
        

    def setup(self,bool):
        if bool == True:
            i = 0
            for _ in range(1,3):
                for Name,Info in Items.items():
                    i += 1
                    ItemFrame(Name,Info,i,self)
            self.menuCanvas.canvas.place(relwidth=1,relheight=0.8)
            self.menuCanvas.scroll.pack(side="right",fill="both")

            self.mainFrameLeft.pack(side="left", expand=True, fill="both")
            self.mainFrameRight.pack(side="right", expand=True, fill="both")
            self.botFrame.place(anchor="sw",rely=1,relwidth=1,relheight=0.2)
        else:
            self.Orders = {}
            self.totalCost = 0

class ItemLabel:
    def __init__(self,info,menu):
        #Store Arguments
        self.Menu = menu
        self.Name = info["Name"]
        self.Info = Items[self.Name]
        self.Amount = info["Amount"]

        #Frame Style
        #Create Base Frame
        self.Frame = ttk.Frame(menu.orderCanvas.frame, height=100, width=500)
        self.Frame.pack(side="top", fill="x", ipadx=10, ipady=10)
        self.Label = ttk.Label(self.Frame, text=self.Name + ": " + str(self.Amount), anchor="center", style="ItemFrame.TLabel")
        self.Label.pack(expand=True,fill="both")
        ttk.Button(self.Frame, style="ItemFrame.TButton", text="Remove from order", command=self.update).pack(fill="both",expand=True,side="right")

        pass

    def update(self):
        self.Menu.Orders[self.Name] -= 1
        self.Amount -= 1
        self.Menu.totalCost = round(self.Menu.totalCost - float(self.Info["Price"]),2)
        self.Menu.costLabel.configure(text="Current Order Cost: ${}".format(self.Menu.totalCost))
        if self.Menu.Orders[self.Name] <= 0:
            self.Menu.Orders.pop(self.Name)
            self.Frame.destroy()
        else:
            self.Label.configure(text=self.Name + ": " + str(self.Amount))

class ItemFrame:
    def __init__(self,name,info,i,menu):
        #Store Arguments
        self.Info = info
        self.Name = name
        self.Menu = menu

        #Frame Style
        #Create Base Frame
        f = fillConv(i,menu.mainFrameLeft,menu.mainFrameRight)
        self.Frame = ttk.Frame(f, height=100, width=500, style="ItemFrame.TFrame")
        self.Frame.pack(side="top", fill="x", ipadx=10, ipady=10)
        
        price = str(float(info["Price"]))
        places = price.split(".")[1]
        if len(places) == 1:
            price = price + "0"
        ttk.Label(self.Frame, text=name, anchor="center", style="ItemFrame.TLabel").pack(expand=True,fill="both")
        ttk.Label(self.Frame, style="ItemFrameA.TLabel", text="$" + price).pack(fill="both",expand=True,side="left")
        ttk.Button(self.Frame, style="ItemFrame.TButton", text="Add to order", command=self.update).pack(fill="both",expand=True,side="right")

        pass

    def update(self):
        try:
            self.Menu.Orders[self.Name] += 1
        except KeyError:
            self.Menu.Orders[self.Name] = 1
        self.Menu.totalCost = round(self.Menu.totalCost + float(self.Info["Price"]),2)
        self.Menu.exportButton.configure(text = "Export Order")
        self.Menu.displayButton.configure(text = "Display Order")
        self.Menu.costLabel.configure(text="Current Order Cost: ${}".format(self.Menu.totalCost))
        return

class Entry:
    def __init__(self,frame,initialText,show):
        self.cleared = False
        self.show = show
        self.text = tkinter.Entry(frame, fg="#666666")
        self.text.bind("<FocusIn>",lambda e:self.clear())
        self.text.insert("end",initialText)
        pass
    
    def clear(self):
        self.text.delete(0, END)
        self.text.configure(fg="#000000")
        self.cleared = True
        if self.show:
            self.text.configure(show=self.show)

    def criteria(self):
        if self.cleared == True and len(self.text.get()) > 0:
            return True
        else: return False
    

class LoginMenu:
    def __init__(self):
        self.frame = ttk.Frame(root)

        self.usernameText = Entry(self.frame,"Username",None)
        self.usernameText.text.place(relwidth=0.7,relheight=0.04,relx=0.5,rely=0.4,anchor=CENTER)
        self.passwordText = Entry(self.frame,"Password","*")
        self.passwordText.text.place(relwidth=0.7,relheight=0.04,relx=0.5,rely=0.45,anchor=CENTER)

        self.loginButton = ttk.Button(self.frame, text="Login", command=self.login)
        self.loginButton.place(relwidth=0.35,relheight=0.05,relx=0.5,rely=0.5,anchor="e")
        self.registerButton = ttk.Button(self.frame, text="Register", command=self.register)
        self.registerButton.place(relwidth=0.35,relheight=0.05,relx=0.5,rely=0.5,anchor="w")

        self.frame.pack(fill="both",expand=True)
        pass

    def getInfo(self):
        if self.usernameText.criteria() == True and self.passwordText.criteria() == True:
            return self.usernameText.text.get(), self.passwordText.text.get()
        else: return False, False
    
    def login(self):
        user, passw = self.getInfo()
        try:
            if logins[user]["Password"] == passw:
                self.frame.destroy()
                menu = Menu()
                menu.setup(False)
            else: print("Invalid")
        except KeyError:
            print("Invalid")

    def register(self):
         user, passw = self.getInfo()
         if user == False: return
         logins[user] = {"Password": passw}

login = LoginMenu()

root.resizable(False,False)
root.mainloop()

loginsjson = open("logins.json","w")
json.dump(logins,loginsjson)
loginsjson.close()