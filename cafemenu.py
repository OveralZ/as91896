# Cafe Menu, prompts login and stores existing logins, and presents the cafe menu for ordering.

# Libraries
from tkinter import CENTER, END, PhotoImage, Widget, ttk
from PIL import Image, ImageTk
import tkinter
import json

#Constants
SEP = "----------------------"
MAROON = "#5f0137"
LBLUE = "#89c9ec"
LGREY = "#F0F0F0"

#Logins
loginsjson = None
logins = None
try:
    loginsjson = open("logins.json","r+") #Attempt to open the data in read & write form.
except FileNotFoundError:
    loginsjson = open("logins.json","a+") #If it doesn't exist, use a+ to create it.
    json.dump({},loginsjson)

logins = json.load(loginsjson)
loginsjson.close()

#Menu
from menu import Items

#GUI Setup
root = tkinter.Tk()
root.title("BDSC Cafe Order")
root.iconbitmap("./assets/icon.ico")
s = ttk.Style(root)
root.geometry("300x500+150+200")

#Styles
s.configure("ItemFrame.TFrame", background=LGREY)
s.configure("ItemFrame.TButton", background=MAROON)
s.configure("ItemFrame.TLabel", background=LGREY)
s.configure("ItemFrameA.TLabel", background=MAROON, foreground="#FFFFFF")

s.configure("Menu.TLabel", background=LGREY, font=("Helvetica",20), anchor=CENTER)
s.configure("Error.TLabel",foreground="red", anchor=CENTER)

#Global Functions
def fillConv(i, mainFrameLeft, mainFrameRight): #Gives the appropriate frame for the item frame to be in depending on the order.
    i = 1-(i%2)
    if i == 0: return mainFrameLeft
    else: return mainFrameRight

def priceConversion(price): #Makes sure that the price tag is rounded to 2 decimal points in string form.
    price = str(float(price))
    places = price.split(".")[1]
    if len(places) == 1:
        price = price + "0"
    return price

#Classes
class ScrollingCanvas: #Makes a scrolling canvas.
    def __init__(self):
        #Create the base widgets
        self.canvas = tkinter.Canvas(root)
        self.frame = ttk.Frame(self.canvas)
        self.scroll = ttk.Scrollbar(self.canvas, orient='vertical', command=self.canvas.yview)

        #Make the scrolling region of the canvas change whenever the frame updates. 
        self.frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        #Create the window and set up the scrollbar.
        self.window = self.canvas.create_window((0, 0), window=self.frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scroll.set)

        #Adjust the size of the window when the size of the canvas changes. Used to be for when the window is resized, but now it is here as future-proofing.
        self.canvas.bind('<Configure>', self.frameWidth)

        pass

    def frameWidth(self,event):
        canvas_width = event.width
        self.canvas.itemconfig(self.window, width = canvas_width-19)

class Menu: #Main menu class.
    def __init__(self,user):
        #Set up values
        self.Orders = {}
        self.totalCost = 0
        self.user = user
        self.currentMenu = "Menu"
        
        #Create widgets for the top nd the bottom.
        self.topLabel = ttk.Label(root,style="Menu.TLabel",text="Café Menu", foreground=MAROON)
        self.topBar = tkinter.Label(root,bg=MAROON)
        self.topBar.place(relwidth=0.8,relheight=0.005,relx=0.5,rely=0.1,anchor="s")
        self.botFrame = ttk.Frame(root,borderwidth=5,relief="sunken")

        self.costLabel = ttk.Label(self.botFrame, text="Current Order Cost: $0.00", anchor="center")
        self.costLabel.pack(expand=True,fill="both")
        self.displayButton = ttk.Button(self.botFrame, text="Display Order", command=self.displayOrder)
        self.displayButton.pack(fill="both",expand=True)
        self.exportButton = ttk.Button(self.botFrame, text="Export Order", command=self.exportOrder)
        self.exportButton.pack(fill="both",expand=True, side="right")
        self.clearButton = ttk.Button(self.botFrame, text="Clear Order", command=self.clearOrder)
        self.clearButton.pack(fill="both",expand=True, side="left")

        #Create the cafe menu which will go in between.
        self.menuCreate()

        pass

    def menuCreate(self): #Creates the cafe menu.
        self.currentMenu = "Menu"
        self.topLabel.configure(foreground=MAROON,text="Café Menu")
        self.topBar.configure(bg=MAROON)

        self.menuCanvas = ScrollingCanvas() #Create the scrolling canvas
        self.mainFrame = self.menuCanvas.frame

        #Create the frames on the left and right for organization.
        self.mainFrameLeft = ttk.Frame(self.mainFrame)
        self.mainFrameRight = ttk.Frame(self.mainFrame)

        #Make sure that the display order button shows display order instead of display menu.
        self.displayButton.configure(text="Display Order", command=self.displayOrder)

        #Set up the item frames.
        self.setup()

    def exportOrder(self): #Exports orders into a TXT file.
        if len(self.Orders) > 0:
            res = ""
            orders = ""
            for i,v in self.Orders.items(): #For every single item inside of the order, add them to the final string.
                orders += str(v)+" x "+i+" - $"+priceConversion(round(v*Items[i]["Price"],2))+"\n"
            res = "{s}\nOrder for {name}\n{s}\nItems\n{s}\n{orders}{s}\nTotal: ${total}".format(s=SEP,name=self.user,orders=orders,total=priceConversion(self.totalCost))
            txt = open("Order.txt","w") #Open the order, creates it if it doesn't exist.
            txt.write(res) #Write into it.
            self.exportButton.configure(text = "Order exported!")
        else:
            self.exportButton.configure(text = "Please order a product first!")
    
    def clearOrder(self): #Clears the order and updates data.
        self.totalCost = 0
        self.costLabel.configure(text="Current Order Cost: $0.00")
        if self.currentMenu == "Order":
            self.menuCreate()
        self.Orders.clear()

    def displayOrder(self): #Changes the cafe menu into the order menu.
        if len(self.Orders) > 0:
            #Change values
            self.currentMenu = "Order"
            self.menuCanvas.canvas.destroy()
            self.topLabel.configure(text="Your Order")
            self.displayButton.configure(text="Display Menu", command=self.menuCreate)

            #Create a new scrolling canvas and store item labels inside of them.
            self.orderCanvas = ScrollingCanvas()
            for Name, Amt in self.Orders.items():
                ItemLabel({"Name": Name, "Amount": Amt},self)
            self.orderCanvas.canvas.place(relwidth=1,relheight=0.7,rely=0.1)
            self.orderCanvas.scroll.pack(side="right",fill="both")
            root.update_idletasks()
        else:
            self.displayButton.configure(text = "Please order a product first!")
        

    def setup(self): #Places everything in the GUI down.
        i = 0
        for Name,Info in Items.items(): #Put all the items inside of the main frame.
            i += 1
            ItemFrame(Name,Info,i,self)

        #Place everything down.
        self.topLabel.place(relwidth=1,relheight=0.1)

        self.menuCanvas.canvas.place(relwidth=1,relheight=0.7,rely=0.1)
        self.menuCanvas.scroll.pack(side="right",fill="both")

        self.mainFrameLeft.pack(side="left", expand=True, fill="both")
        self.mainFrameRight.pack(side="right", expand=True, fill="both")

        self.botFrame.place(anchor="sw",rely=1,relwidth=1,relheight=0.2)

class ItemLabel: #Item label class for order display.
    def __init__(self,info,menu):
        #Store Arguments
        self.Menu = menu
        self.Name = info["Name"]
        self.Info = Items[self.Name]
        self.Amount = info["Amount"]

        #Frame Style
        #Create Base Frame
        self.Frame = ttk.Frame(menu.orderCanvas.frame)
        self.Frame.pack(side="top", fill="x", ipadx=10, ipady=30)
        self.Label = ttk.Label(self.Frame, text=self.Name + ": " + str(self.Amount) + " - $" + priceConversion(round(self.Amount*Items[self.Name]["Price"],2)), anchor="center", style="ItemFrame.TLabel")
        self.Label.place(anchor="nw",relwidth=1,relheight=0.6,relx=0)
        ttk.Button(self.Frame, style="ItemFrame.TButton", text="Remove from order", command=self.update).place(anchor="sw",relwidth=1,relheight=0.4,rely=1,relx=0)
        tkinter.Label(self.Frame,bg=LBLUE).place(relwidth=0.8,relheight=0.05,relx=0.5,rely=0.5,anchor=CENTER)

        pass

    def update(self): #Update everything when a button is pressed.
        self.Menu.Orders[self.Name] -= 1
        self.Amount -= 1
        self.Menu.totalCost = round(self.Menu.totalCost - float(self.Info["Price"]),2)
        self.Menu.costLabel.configure(text="Current Order Cost: ${}".format(priceConversion(round(self.Menu.totalCost,2))))
        if self.Menu.Orders[self.Name] <= 0:
            self.Menu.Orders.pop(self.Name)
            self.Frame.destroy()
        else:
            self.Label.configure(text=self.Name + ": " + str(self.Amount) + " - $" + priceConversion(round(self.Amount*Items[self.Name]["Price"],2)))

class ItemFrame: #Item frame class for adding items to the order.
    def __init__(self,name,info,i,menu):
        #Store Arguments
        self.Info = info
        self.Name = name
        self.Menu = menu

        #Frame Style
        #Create Base Frame
        f = fillConv(i,menu.mainFrameLeft,menu.mainFrameRight)
        self.Frame = ttk.Frame(f, style="ItemFrame.TFrame")
        self.Frame.pack(side="top", fill="x", ipadx=5, ipady=35)
        
        price = priceConversion(info["Price"])
        ttk.Label(self.Frame, text=name, anchor="center", style="ItemFrame.TLabel",wraplength=150).place(anchor="nw",relwidth=1,relheight=0.6)
        ttk.Label(self.Frame, style="ItemFrameA.TLabel", text="$" + price).place(anchor="sw",relwidth=0.3,relheight=0.4,relx=0,rely=1)
        ttk.Button(self.Frame, style="ItemFrame.TButton", text="Add to order", command=self.update).place(anchor="se",relwidth=0.7,relheight=0.4,relx=1,rely=1)
        tkinter.Label(self.Frame,bg=MAROON).place(relwidth=0.8,relheight=0.03,relx=0.5,rely=0.55,anchor=CENTER)

        pass

    def update(self): #Update everything when a button is pressed.
        try:
            self.Menu.Orders[self.Name] += 1
        except KeyError:
            self.Menu.Orders[self.Name] = 1
        self.Menu.totalCost = round(self.Menu.totalCost + float(self.Info["Price"]),2)
        self.Menu.exportButton.configure(text = "Export Order")
        self.Menu.displayButton.configure(text = "Display Order")
        self.Menu.costLabel.configure(text="Current Order Cost: ${}".format(priceConversion(round(self.Menu.totalCost,2))))
        return

class Entry: #Entries for the login and password.
    def __init__(self,frame,initialText,show):
        self.cleared = False
        self.show = show
        self.text = tkinter.Entry(frame, fg="#666666")
        self.text.bind("<FocusIn>",lambda e:self.clear()) #When the entry is focused for the first time, clear the entry.
        self.text.insert("end",initialText)
        pass
    
    def clear(self): #The function used for clearing the entry.
        if self.cleared == False:
            self.text.delete(0, END)
            self.text.configure(fg="#000000")
            self.cleared = True
            if self.show:
                self.text.configure(show=self.show)

    def criteria(self): #Returns if the entry is considered empty for login checks.
        if self.cleared == True and len(self.text.get()) > 0:
            return True
        else: return False
    

class LoginMenu: #The menu used to log in the program.
    def __init__(self):
        #Create widgets
        self.frame = ttk.Frame(root)
        self.frame.pack(fill="both",expand=True)

        #Entries
        self.usernameText = Entry(self.frame,"Username",None)
        self.usernameText.text.place(relwidth=0.7,relheight=0.04,relx=0.5,rely=0.4,anchor=CENTER)
        self.passwordText = Entry(self.frame,"Password","*")
        self.passwordText.text.place(relwidth=0.7,relheight=0.04,relx=0.5,rely=0.45,anchor=CENTER)

        #Buttons
        self.loginButton = ttk.Button(self.frame, text="Login", command=self.login)
        self.loginButton.place(relwidth=0.35,relheight=0.05,relx=0.5,rely=0.5,anchor="e")
        self.registerButton = ttk.Button(self.frame, text="Register", command=self.register)
        self.registerButton.place(relwidth=0.35,relheight=0.05,relx=0.5,rely=0.5,anchor="w")

        #Decorations
        relw,relh = 0.75,0.3
        imagelabel = ttk.Label(self.frame)
        imagelabel.place(relwidth=relw,relheight=relh,relx=0.5,rely=0.2,anchor=CENTER)
        #Since images cannot be resized relatively, I have to use a workaround.
        root.update_idletasks()
        rw, rh = root.winfo_width(), root.winfo_height()
        self.img = Image.open('./assets/Logo.png').resize((int(rw*relw),int(rh*relh)))
        self.render = ImageTk.PhotoImage(self.img)
        imagelabel.configure(image=self.render)

        tkinter.Label(self.frame,bg=MAROON).place(relwidth=0.8,relheight=0.01,relx=0.5,rely=0.55,anchor=CENTER)
        
        pass

    def getInfo(self): #Gets the info of the entries, returns False if the information is not valid.
        if self.usernameText.criteria() == True and self.passwordText.criteria() == True:
            return self.usernameText.text.get(), self.passwordText.text.get()
        else: return False, False

    def errorMessage(self,msg): #Creates an error message.
        try:
            self.errormsg.configure(text=msg)
        except AttributeError:
            self.errormsg = ttk.Label(self.frame,style="Error.TLabel",text=msg)
            self.errormsg.place(relwidth=0.7,relheight=0.1,relx=0.5,rely=0.65,anchor=CENTER)
            root.update_idletasks()
    
    def login(self): #Logs in the user if they have the right login, creates error messages if not.
        user, passw = self.getInfo()
        if user == False:
            self.errorMessage("One or more fields are blank!")
            return
        try:
            if logins[user]["Password"] == passw:
                self.frame.destroy()
                menu = Menu(user)
            else: self.errorMessage("Invalid Password!")
        except KeyError:
            self.errorMessage("Invalid Username, try registering.")

    def register(self): #Registers the user and puts their login into the dictionary.
         user, passw = self.getInfo()
         if user == False:
            self.errorMessage("One or more fields are blank!")
            return
         if user in logins:
            self.errorMessage("Username already in use.")
         else:
            logins[user] = {"Password": passw}

login = LoginMenu() #Creates the main menu upon initilization.

#Root configurations, mainloop.
root.resizable(False,False)
root.mainloop()

#After the program is closed, update the login JSON.
loginsjson = open("logins.json","w")
json.dump(logins,loginsjson)
loginsjson.close()