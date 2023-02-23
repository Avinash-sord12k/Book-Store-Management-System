from tkinter import *
from tkinter import messagebox
import json
from functions import *
import mysql.connector as ms
from PIL import Image , ImageTk
import requests



#--------------------------------MAIN_WINDOW_GEOMETRY-------------------------#
root =  Tk()
root.geometry("800x500")
root.title("BOOK STORE MANAGEMENT SYSTEM")
root.resizable(0, 0)


#--------------------------------------------------------------------CONNECTING DATABASE------------------------------#

def dbsetup():
    global cur,db
    cur = db.cursor()
    try:
        cur.execute("use book_store")
        cur.execute("select * from book_data")
        cur.fetchall()
        specialvar=True
        print("done")
    except:
        specialvar=False
        print("note done") 

    if specialvar==False:
        cur.execute('CREATE DATABASE IF NOT EXISTS BOOK_STORE;')
        cur.execute('USE BOOK_STORE;')
        cur.execute("""CREATE TABLE IF NOT EXISTS BOOK_DATA(
        Id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        ISBN BIGINT not null ,
        Title char(100) not null,
        Image varchar(500) ,
        Summary TEXT,
        Author char(100) not null, price float, stock int)""")

        # cur.execute('USE BOOK_STORE;')
        # cur.execute("""CREATE TABLE IF NOT EXISTS STAFF_DATA(
        # Id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        # Staff_Name varchar(50) not null ,
        # password char(100) not null);""")

        # cur.execute('CREATE DATABASE IF NOT EXISTS BOOK_STORE;')
        # cur.execute('USE BOOK_STORE;')
        cur.execute("""CREATE TABLE IF NOT EXISTS SALES_DATA(
        Id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        Purchase_Date time not null,
        Phone BIGINT not null ,
        Customer_Name char(100) not null,
        Purchase_Details varchar(200) ,
        Net_Balance int)""")

        # cur.execute('CREATE DATABASE IF NOT EXISTS BOOK_STORE;')
        # cur.execute('USE BOOK_STORE;')
        cur.execute("""CREATE TABLE IF NOT EXISTS RETURN_DATA(
        Id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        Return_Date time not null,
        Phone BIGINT not null ,
        Customer_Name char(100) not null,
        Return_Details varchar(200) ,
        Net_Balance int)""")

        with open('books.json', encoding='utf8') as b:
            data = json.load(b)

        # lis = []
        for i in data['books']:
            print()
            isbn = int(i['ISBN'])
            title = i['title']
            image = i['image']
            summary = i['summary']
            author = i['author']
            price = float(i['price']['value'])
            stock = int(i['stock'])
            cur.execute(" INSERT INTO book_data(ISBN, Title, Image, Summary, Author, Price, stock) VALUES(%s, %s, %s, %s, %s, %s, %s)", (isbn, title, image, summary, author, price, stock))
        db.commit()
        db = ms.connect(host='localhost', user=username,password=PWD,database="book_store")
        cur = db.cursor()#buffered=True


#------------------------------------------------LOGIN PAGE-----------------------------------------
login = Toplevel(root)
# print(font.families())
login.geometry("300x280")
login.resizable(0,0)
login.protocol ('WM_DELETE_WINDOW', (lambda: root.destroy) ())


loginimg = PhotoImage(file = img_path("LOGIN"))
l1 = Label(login,image=loginimg,bd=0)
l1.pack(pady=(10,0))

usernameimg = PhotoImage(file = img_path("USERNAME"))
l2 = Label(login,image=usernameimg,bd=0)
l2.pack(anchor=W,padx=(22,0),pady=(10,0))
e1 = Entry(login,font=20)
e1.pack(anchor=W,padx=(22,0))

passwordimg = PhotoImage(file = img_path("PASSWORD"))
l3 = Label(login,image=passwordimg,bd=0)
l3.pack(anchor=W,padx=(22,0))
e2 = Entry(login,font="Tahoma",show="*")
e2.pack(anchor=W,padx=(22,0))

def user_login():
    global username,PWD
    global db
    username = get_entry(e1).lower()
    PWD = get_entry(e2)
    try:
        # cur.execute("""SELECT * FROM staff_data WHERE staff_name=%s;""", (user,))
        db = ms.connect(host='localhost', user=username,password=PWD)
        permission=True
    except:
        permission=False
    
    if permission==True:
        root.deiconify()
        login.withdraw()
        dbsetup()
    else:
        messagebox.showerror("details error", "You have entered wrong details OR You don't have MYSQL installed on your system")

continueimg = PhotoImage(file = img_path("CONTINUE"))
b1=Button(login,image=continueimg,bd=0,highlightthickness=0,command=user_login)
b1.pack(pady=(15,0))



# db = ms.connect(host='localhost', user="root",password="ajay0000",database="book_store")
# cur = db.cursor()


#------------------------------MENU_FUNCTIONS--------------------------------------#
def gotoreturn():
    r.deiconify()
    root.withdraw()

def gotostock():
    stock.deiconify()
    root.withdraw()

# --------------------------------MENU-------------------------------#
menu = Menu(root)
menu.add_command(label="Purchase")
menu.add_command(label="Return",command=gotoreturn)
menu.add_command(label="Stock",command=gotostock)
menu.add_command(label="Exit",command= root.destroy)
root.config(menu=menu)

# -----------------------------------------------------------------FRAME111111111111111------------------------------#
frame1 = Frame(root,bg="#FFF748")
frame1.place(x=0,y=0,height=50,width=800)
frame1.pack_propagate(0)
purchaseimg=PhotoImage(file=img_path("PURCHASE"))
f1l1= Label(frame1,image=purchaseimg,bd=0)
f1l1.pack()


# ------------------------------------------------------------------FRAME2222222------------------------------#
frame2 = Frame(root)#borderwidth=1,relief=GROOVE
frame2.place(y=50,x=0,height=250,width=300)

getdetailsimg=PhotoImage(file=img_path("GETDETAILS"))#-----------MEIN LABEL "GET DETAILS"---------
f2l1= Label(frame2,image=getdetailsimg,bd=0)
f2l1.pack(pady=(24,0))

f2e1 = Entry(frame2, width=13,font = "Montserrat 15 bold")#--------ENTRY TO GET ISBN-----------
f2e1.pack(pady=(17,0),padx=38)
f2e1.focus_set()

def search():                          #FUNCTION FOR SEARCH BUTTON OF FRAME 2
    # cur.execute("use book_store")
    isbn=get_entry(f2e1)               
    # isbn=9789460681387
    if isbn=="":
        return None
    global c,photo,x
    # print(cur)
    x = search_by_isbn(isbn, cur)
    f3l1.config(text=get_title(x))#----------------------DISPLAYIN TITLE
    f3l2.config(text=get_author(x))#---------------------DISPLAYING AUTHER
    text.config(state=NORMAL)#--------------------------DISPLAYING DISCRIPTION
    text.delete("1.0" ,END)
    text.insert(INSERT,get_summary(x) )
    text.config(state=DISABLED)
    url = get_image(x)#--------------------------------FETCHING TH COVER PHOTO
    download(url)
    c = Image.open(img_path("IMG"))
    new_image = c.resize((150, 200))
    photo = ImageTk.PhotoImage(new_image)
    f3c1.config(image=photo)
    t = "Price:"+str(get_price(x))#----------------------DISPLAYING PRICE
    f3l4.config(text=t)

    if get_stock(x) < 1:#--------------------------------IF STOCK == 0 THEN ADD BUTTON DIABLE
        f3b1.config(state=DISABLED)           
    else:
        f3b1.config(state=NORMAL)#-----------------------ELSE DONT DISABLE

searchimg=PhotoImage(file=img_path("SEARCH"))#-----------SEARCH BUTTON
f2b1 = Button(frame2,image=searchimg,command=search,bd=0,highlightthickness=0)
f2b1.pack(pady=(20,0),ipady=0)



# --------------------------------------------FRAME333333------------------------------#
frame3 = Frame(root)#,borderwidth=1,relief=GROOVE
frame3.place(y=50,x=300,height=250,width=500)
# --------------------------------------------COVER IMAGE OF THE BOOK----------------------------#
frame31=Frame(frame3,height=250,width=200)
frame31.grid(row=0,column=0)
frame31.pack_propagate(0)
pilcoverimg = Image.open(img_path("COVER"))
coverimg = ImageTk.PhotoImage(pilcoverimg)
f3c1 = Label(frame31, width = 150, height = 200,image=coverimg)      
f3c1.pack(pady=25,padx=25)
# --------------------------------------------DEATAILS OF BOOKS---------------------#
frame32=Frame(frame3,height=250,width=300)
frame32.grid(row=0,column=1)
frame32.pack_propagate(0)

f3l1= Label(frame32,text="Title",font =("Tahoma", 21,"bold"),bg="#3c1a58",fg="#fff748")#---------Title
f3l1.pack(pady=(18,0),anchor=W)
f3l2= Label(frame32,text="Author",font =("Segoe Script", 12,"bold"),bg="#3c1a58",fg="#fff748")#--------AUTHER
f3l2.pack(pady=(0,0),anchor=NW)

frame321= Frame(frame32,width=230,height=90)#------------------SCROLLABEL TEXT FOR DISCRIPTION
frame321.pack(anchor=W,fill=X,padx=(0,25))#-----------------THIS IS DISCRIPTION
frame321.pack_propagate(0)
scrollbar = Scrollbar(frame321)
scrollbar.pack( side = RIGHT, fill = Y )
text = Text(frame321,yscrollcommand = scrollbar.set,wrap=WORD,bg="#3c1a58",fg="#fff748",relief=FLAT,font =("Sitka Small", 10,"bold"),bd=1)
text.insert(INSERT,"Discription" )
text.pack(fill=X)
text.config(state=DISABLED)
scrollbar.config(command = text.yview)

#----------------------------------------------------------FRAME FOR PRICE AND ADD-------------
frame322 = Frame(frame32,bg="#3c1a58")#,bd=1,relief=SUNKEN
frame322.pack(anchor=W,fill=X,pady=15,padx=(0,25) )  
frame322.pack_propagate(1)
f3l4= Label(frame322,text="Price:",bg="#3c1a58",fg="#fff748",font=("Gabriola", "24", "bold"))
f3l4.pack(side=LEFT)
                                    


def add():#-------------------------------------FUNCTION TO ADD BOOKS TO THE CART----------------
    n=0
    if get_stock_ofbooks(get_isbn(x),cur) == 1:
        f3b1.config(state=DISABLED)
        return None

    for i in range(1, len(dic)):#---------------------TO CHECK IS BOOK PRESENT IN TABLE OR NOT
        if get_isbn(x) not in dic[i]:            
            n += 1          
    if n == len(dic) - 1:#----------------------------IF NOT IN TABLE THEN ADD IT
        dic.append([len(dic), get_title(x), get_isbn(x), get_price(x), 1])     
    else:#--------------------------------------------IF IT IS IN TABLE THEN INCREASE QTY
        for k in range(len(dic)):
            if get_isbn(x) in dic[k]:
                dic[k][4] += 1
                break
    stock_decrease(cur, search_by_isbn(get_isbn(x), cur), 1)
    for widget in frame41.winfo_children():
        widget.destroy()
    create(dic, frame41)
    total_cart()
    f4b1.config(state=NORMAL)
    f5b1.config(state=NORMAL)


def total_cart():#---------------------------TO DISPLAY THE TOTAL AMMOUNT---------------------
    total = 0
    for i in range(1, len(dic)):
        total +=  dic[i][4] * dic[i][3]
    f4total.config(text='Total: ' + str(round(total, 2)))


addimg=PhotoImage(file=img_path("MADD"))#---------------ADD BUUTON-------------------
f3b1 = Button(frame322, image=addimg,command=add,state=DISABLED,bd=0,highlightthickness=0)
f3b1.pack(side=RIGHT,anchor=NE)


for widget in frame3.winfo_children():#------------------CHANGING THE BACKGROUND OF FRAME-3-----------
    widget.config(bg="#3c1a58")


# -----------------------------------------FRAME444444---------------------#
frame4 = Frame(root)#,borderwidth=1,relief=GROOVE
frame4.place(y=300,x=250,height=200,width=550)

frame41= Frame(frame4,borderwidth=1,relief=GROOVE)#--------------FRAME FOR TABLE-----------
frame41.pack(fill="x",padx=10,pady=10)

dic = [["SNO","Book","ISBN","Price","Qty."]]#-------------------INIT LIST FOR THE TABEL-----------
create(dic,frame41)

frame42= Frame(frame4,borderwidth=1,bg="#3c1a58")#------------------FRAME FOR SNO ENTRY
frame42.pack(fill="x",padx=20,pady=12,side=BOTTOM)#---------------AND FOR REMOVE BUTTON AND TOTAL
f4e1=Entry(frame42,font =("Tahoma", 17),width=3,bd=2,relief=SUNKEN)             
f4e1.pack(side=LEFT)


def remove():#----------------------------------------------FUCTION FOR REMOVE BUTTON
    if get_entry(f4e1) == "":
        # f4b1.config(state=DISABLED)
        return None
    sno = int(get_entry(f4e1))#-----------------------------GETTING ENTRY FROM SNO ENTRY
    if sno>len(dic)-1 or len(dic)==1:#-------------------------------------
        pass
    elif dic[sno][4] == 1:
        stock_increase(cur, search_by_isbn(int(dic[sno][2]), cur), 1)
        del dic[sno]
        clear(f4e1)
        f5b1.config(state=DISABLED)
    else:
        dic[sno][4] -= 1
        stock_increase(cur, search_by_isbn(int(dic[sno][2]), cur), 1)
    if len(dic)==1:#---------------------------------------IF ALL DATA IS REVOED THEN REMOVE BUTTON WLL DISABLE
        f4b1.config(state=DISABLED)
    if get_stock_ofbooks(get_isbn(x),cur) >= 1:
        f3b1.config(state=NORMAL)
    for widget in frame41.winfo_children():#----------------DELETING ALL TABLE
            widget.destroy()
    create(dic, frame41)#----------------------------------RECREATING TABLE AFTER DELETING IT
    total_cart()
    # db.commit()


removeimg = Image.open(img_path("REMOVE"))#-----------------REMOVE BUTTON--------------
resizeremoveimg= removeimg.resize((50,30))
finelremoveimg=ImageTk.PhotoImage(resizeremoveimg)
f4b1 = Button(frame42,image=finelremoveimg,command=remove,state=DISABLED,bd=0)
f4b1.pack(side=LEFT,padx=10)

f4total = Label(frame42,text="Total:   ",bg="#3c1a58",fg="#fff748",font =("Tahoma", 21,"bold"))#--------TOTAL LABLE
f4total.pack(side=RIGHT,padx=10)


#-------------------------------------------FRAME55555555-----------------#
frame5 = Frame(root)#,borderwidth=1,relief=GROOVE
frame5.place(y=300,x=0,height=200,width=250)

customerdetailsimg = PhotoImage(file=img_path("CUSTOMERDETAILS"))#-----------CUTOMER DETAIL LABLE
f5l1= Label(frame5,image=customerdetailsimg,bd=0)
f5l1.pack(pady=(4,0))

f5e1 = Entry(frame5, bd =2,width=50,font = "Montserrat 16 bold",fg="#3c1a58")#------------NAME NO 
f5e1.pack(pady=(14,0),padx=38)
f5e1.insert(END, 'Name')

f5e2 = Entry(frame5, bd =2,width=50,font = "Montserrat 16 bold",fg="#3c1a58")#------------PHONE NO ENTRY
f5e2.pack(pady=(14,0),padx=38)
f5e2.insert(END, 'Phone')

frame51 = Frame(frame5,bg="#3c1a58")#------------------FRAME FOR SUBMIT AND RESET FUNTION
frame51.pack(pady=(18,0),padx=18)

def submit():#----------------------------------SUBMIT BUTTON FUNCTION
    if get_entry(f5e2) == "" or len(get_entry(f5e2))!=10:
        return None
    price = float(f4total.cget('text').split()[1])
    # print(price)
    buy_book(cur, get_entry(f5e1), get_entry(f5e2), dic, price)
    db.commit()
    reset()
    
msubmitimg = Image.open(img_path("MSUBMIT"))#-------------SUBMIT BUTTON
resizesubmitimg= msubmitimg.resize((50,30))
finelsubmitimg=ImageTk.PhotoImage(resizesubmitimg)
f5b1 = Button(frame51, image=finelsubmitimg, command = submit,state=DISABLED,bd=0)
f5b1.pack(side=RIGHT,padx=(80,0))

def reset():#----------------------------------------------------------------RESET ALL THE THING ON THE PAGE
    f2e1.config(text="")
    global c
    c = PhotoImage(file = img_path("COVERPHOTO"))
    # photo = ImageTk.PhotoImage(c)
    f3c1.config(image=c)
    f3l1.config(text="Title")
    f3l2.config(text="Author")
    text.config(state=NORMAL)
    text.delete("1.0", END)
    text.insert(INSERT, "Discription")
    text.config(state=DISABLED)
    f3l4.config(text="Price")
    f5e1.config(text="Name")
    f5e1.config(text="Phone")
    f4total.config(text="Total:")
    f3b1.config(state=DISABLED)
    f5b1.config(state=DISABLED)
    f4b1.config(state=DISABLED)
    clear(f5e1)
    f5e1.insert(END, 'Name')
    clear(f5e2)
    f5e2.insert(END, 'Phone')
    clear(f2e1)
    f2e1.focus_set()
    global dic
    dic = [["SNO","Book","ISBN","Price","Qty."]]
    for widget in frame41.winfo_children():
            widget.destroy()
    create(dic, frame41)

resetimg = Image.open(img_path("RESET"))#------------------RESET BUTTON
resizeresetimg= resetimg.resize((50,30))
finelresetimg=ImageTk.PhotoImage(resizeresetimg)
f5b2 = Button(frame51, image=finelresetimg, command = reset,bd=0)
f5b2.pack(side=LEFT)

for widget in root.winfo_children():#----------------------CHANGING THE BACKGROUND OF ALL FRAMES
    widget.config(bg="#3c1a58")

root.withdraw()

#----------------------------------------------------------------------------------------------------------------RETURN PAGE-----------------------------------------------------------------#
r = Toplevel(root)
r.geometry("800x500")
r.resizable(0, 0)
r.withdraw()
#------------------------------------------------------------------------FUNCTIONS FOR MENUES------------------
def rgotomain():
    root.deiconify()
    r.withdraw()

def rgotostock():
    stock.deiconify()
    r.withdraw()


#------------------------------------------------------------------------RETURN MENUES------------------------
menu = Menu(r)
menu.add_command(label="Purchase",command=rgotomain)
menu.add_command(label="Return")
menu.add_command(label="Stock",command=rgotostock)
menu.add_command(label="Exit",command=root.destroy)
r.config(menu=menu)

r.protocol ('WM_DELETE_WINDOW', (lambda: root.destroy) ())#--------------------DISABLING THE CLOSE BUTTON OF THE RETURN MENU 

#-----------------------------------------FRAME1-----------------------#
rframe1 = Frame(r, height=60,width=800,bg="#14213D")
rframe1.pack()
rframe1.pack_propagate(0)

returnimg = PhotoImage(file = img_path("RETURN"))#-----------------------MAIN HEADING RETURN
rf1l1 = Label(rframe1,image=returnimg,bd=0)
rf1l1.pack(side=BOTTOM)



#-----------------------------------------FRAME2-----------------------#
rframe2 = Frame(r, height=50, width=800,bg="#61A5C2")
rframe2.pack()
rframe2.pack_propagate(0)

phonenobg = PhotoImage(file = img_path("RPHONENO"))#---------------------PHONE NO LABLE
rf2l1=Label(rframe2,image=phonenobg,bd=0)
rf2l1.pack(side="left",padx=(20,10))

rf2e1=Entry(rframe2,font=("Vardana",18,"bold"),width=15)#----------------ENTRY FOR PHONE NO
rf2e1.pack(side="left")


def rsubmit():#----------------------------------------------------------FUNCTION FOR DONE BUTTON
    global ric, r_phone
    r_phone = get_entry(rf2e1)
    # print(cur)

    if r_phone == "" or len(r_phone)!=10:#---------------------------------------------------AVOIDING BAD CASES
        return None
    else:
        try:
            cur.execute("""SELECT * FROM sales_data WHERE Phone=%s;""", (r_phone, ))
            cur.fetchall()[0]
        except:
            messagebox.showinfo("not found","you dont have buyed anybook")
            clear(rf2e1)
            return None
 
    ric =  json_to_nestedlist(get_sale_details(get_sale_info(cur, r_phone)), cur)#---1st json to list 2nd getting json 3rd getting sale data
    rcreate(ric)
    rf4e1.config(state=NORMAL)
    rf4b1.config(state=NORMAL)

submitimg = PhotoImage(file = img_path("RSUBMIT"))#----------------------SUBMIT BUTTON
rf2b1 = Button(rframe2,image=submitimg,bd=0,relief=FLAT,highlightthickness=0,command=rsubmit)
rf2b1.pack(side=RIGHT,padx=20)


#-----------------------------------------FRAME3---------------------------#
rframe3 = Frame(r, height=330, width=800,bg="#61A5C2")
rframe3.pack()
rframe3.pack_propagate(0)

rframe31=Frame(rframe3)#-------------------------------------------------FRAME FOR TABLE
rframe31.pack(pady=(20,0))
ric = [["SNO","Book","ISBN","Price","Qty."]]
def rcreate(ric):
    for r in range(len(ric)):
        for i in range(len(ric[r])):
            if i ==0:
                Label(rframe31,text=ric[r][i],width=6).grid(row=r,column=i)
            elif i == 1:
                Label(rframe31,text=ric[r][i],width=50,height=1,justify=LEFT).grid(row=r,column=i)
            elif i==2 :
                Label(rframe31,text=ric[r][i],width=20).grid(row=r,column=i)
            elif i==3 :
                Label(rframe31,text=ric[r][i],width=10).grid(row=r,column=i)
            else:
                Label(rframe31,text=ric[r][i],width=10).grid(row=r,column=i)
    for widget in rframe31.winfo_children():
        widget.config(bg="white",bd=1,relief=SUNKEN)
rcreate(ric)



rframe32=Frame(rframe3,bg="#61A5C2")#------------------------------------FRAME FOR REMOVE AND SNO
rframe32.pack(side=BOTTOM,anchor=W,padx=(20,0))

rsnoimg = PhotoImage(file = img_path("RSNO"))#---------------------------LABLE FOR SNO 
rf4l1=Label(rframe32,image=rsnoimg,bd=0)
rf4l1.pack(side=LEFT)

rf4e1=Entry(rframe32,font=("TrebuchetMS",15,"bold"),width=4,state=DISABLED)#---ENTRY FOR SNO
rf4e1.pack(side=LEFT,pady=(2,0))


def remove_book():
    if get_entry(rf4e1) == "":
        return None
    for widget in rframe31.winfo_children():                             # removing table
        widget.destroy()
    sno = int(get_entry(rf4e1))
    index = 1                                                           
    for data in ric[1:]:
        if sno == int(data[0]):                                    # agar sno match kia
            # money -= get_price(search_by_isbn(data[2], cur))
            if data[4] > 0:                                     # data[4] qunatity hai
                data[4] -= 1
                break
            # else:                                              
            #     ric.pop(index)
            #     break
        index += 1
    rcreate(ric)                                                 # getting table back
    rf2b1.config(state=NORMAL)
    rf4l2.config(text= "-" + str(price_from_book_json(get_sale_details(get_sale_info(cur, r_phone)), cur) - price_from_book_json(nestedlist_to_json(ric), cur)) + "$")


rremoveimg = PhotoImage(file = img_path("RREMOVE"))#----------------------REMOVE BUTTON
rf4b1=Button(rframe32,image=rremoveimg,bd=0,highlightthickness=0,command=remove_book,state=DISABLED)
rf4b1.pack(side=LEFT,padx=(10,0))


#-----------------------------------------FRAME4----------------------------------#
rframe4 = Frame(r, bg="#14213D",height=60)
rframe4.pack(fill=X)
rframe4.pack_propagate(0)

rf4l2=Label(rframe4,text="0$",font=("Trebuchet MS",30,"bold"),fg="#FCA311",bd=0,bg="#14213D")#---BACK RUPESS
rf4l2.pack(side=LEFT,padx=(20,0))

def return_done():
    final_details = (nestedlist_to_json(ric))
    return_book(r_phone, get_sale_name(get_sale_info(cur, r_phone)), cur, final_details,db)
    clear(rf2e1)
    clear(rf4e1)
    rf4e1.config(state=DISABLED)
    rf2b1.config(state=DISABLED)
    rf4b1.config(state=DISABLED)
    rf4l2.config(text="0$")
    for widget in rframe31.winfo_children():                             # removing table
        widget.destroy()
    for r in range(len(ric)):
        if r!=0:
            del ric[r]
    rcreate(ric)
    return None

rdoneimg = PhotoImage(file = img_path("RDONE"))#-------------------------DONE BUTTON
rf2b1 = Button(rframe4,image=rdoneimg,highlightthickness=0,bd=0,command=return_done,state=DISABLED)
rf2b1.pack(side=RIGHT,padx=(0,10))    
# print(font.families())


#----------------------------------------------------------------------------------------------------------------STOCK PAGE------------------------------------------------------------#
stock = Toplevel(root)
stock.geometry("800x500")
stock.resizable(0, 0)
stock.config(bg="#14213D")
stock.withdraw()

def sgotoreturn():
    r.deiconify()
    stock.withdraw()

def sgotomain():
    root.deiconify()
    stock.withdraw()


menu = Menu(stock)
menu.add_command(label="Purchase",command=sgotomain)
menu.add_command(label="Return",command=sgotoreturn)
menu.add_command(label="Stock")
menu.add_command(label="Exit",command=root.destroy)
stock.config(menu=menu)

stock.protocol ('WM_DELETE_WINDOW', (lambda: root.destroy) ())

#-----------------------------------------------------------FRAME1-------------------------------------------------#
sframe1 = Frame(stock, height=60,width=800)
sframe1.pack(anchor=W)
stockheadimg = PhotoImage(file = img_path("STOCKHEAD"))#-----------------------------MEIN HEAIDNG "STOCKMANGEMENT"
sf1l1 = Label(sframe1,image=stockheadimg,bd=0)
sf1l1.pack(side=BOTTOM)

#-----------------------------------------------------------FRAME2-------------------------------------------------#
sframe2 = Frame(stock,height=50,width=800,)
sframe2.pack(anchor=W)

risbnnoimg = PhotoImage(file = img_path("ISBNNO"))#----------------------------------ISBN LABLE
sf2l1 = Label(sframe2,image=risbnnoimg,bd=0)
sf2l1.pack(side=LEFT,padx=(20,0))

sf2e1 = Entry(sframe2,font=("Vardana",17),width=13)#---------------------------------ENTRY FOR ISBN
sf2e1.pack(side=LEFT,padx=(10,0))


#---------------------------------------------------------------FRAME3-----------------------------------------------
sframe3 = Frame(stock,height=50,width=800,)
sframe3.pack(anchor=W)

def init_stock_add():#---------------------------------------------------------------FUNTION FOR ADD BUTTON
    stock_config("clear")
    try:
        cur.execute("SELECT isbn FROM book_data WHERE isbn=%s;",(get_entry(sf2e1),))
        cur.fetchall()[0]
        founded = True
    except:
        founded=False
    
    # print(founded)
    if (get_entry(sf2e1)) == "" or founded==True: 
        stock_config("disable")
        return None                   
    global s_isbn, todo
    todo = "add"
    s_isbn = int(get_entry(sf2e1))
    stock_config("normal")

saddimg = PhotoImage(file = img_path("ADD"))#-----------------------------------------ADD BUTTON
sf3b1 = Button(sframe3,image=saddimg,bd=0,relief=FLAT,highlightthickness=0,command=init_stock_add)
sf3b1.pack(side=LEFT,padx=15)


def init_stock_change():
    try:
        cur.execute("SELECT isbn FROM book_data WHERE isbn=%s;",(get_entry(sf2e1),))
        cur.fetchall()[0]
        founded = True
    except:
        founded=False

    if (get_entry(sf2e1)) == "" or founded==False:
        stock_config("disable")
        return None
    stock_config("clear")
    global s_isbn, todo
    todo = "change"
    s_isbn = int(get_entry(sf2e1))
    stock_config("normal")
    default_entry(sf4e1, get_title(search_by_isbn(s_isbn, cur)))
    default_entry(sf6e3, get_image(search_by_isbn(s_isbn, cur)))
    default_entry(sf5t1, get_summary(search_by_isbn(s_isbn, cur)))
    default_entry(sf4e2, get_author(search_by_isbn(s_isbn, cur)))
    default_entry(sf6e2, get_price(search_by_isbn(s_isbn, cur)))
    default_entry(sf6e1, get_stock(search_by_isbn(s_isbn, cur)))

def stock_config(stat):
    lis = [sf4e1,sf4e2,sf6e1,sf6e2,sf6e3]
    if stat == "disable":
        for z in lis:
            z.config(state=DISABLED)
        sdone.config(state=DISABLED)
        sf5t1.config(state=DISABLED)
    elif stat=="normal":
        for z in lis:
            z.config(state=NORMAL)
        sdone.config(state=NORMAL)
        sf5t1.config(state=NORMAL)
    elif stat=="clear":
        for z in lis:
            clear(z)
        sf5t1.delete("1.0" ,END)

def done_stock(): 
    title = get_entry(sf4e1)
    image = get_entry(sf6e3)
    summary = get_entry_text(sf5t1)
    author = get_entry(sf4e2)
    price = get_entry(sf6e2)
    stock = get_entry(sf6e1)
    if todo == "add":
        cur.execute("""INSERT INTO book_data(isbn, title, image, summary, author, price, stock)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s)""", ( s_isbn, title, image, summary, author, price, stock))
    elif todo == "change":
        cur.execute("""UPDATE book_data SET Title=%s, Image=%s
        , Summary=%s, Author=%s, Price=%s, Stock=%s WHERE ISBN=%s;""", (title, image, summary, author, price, stock, s_isbn))
    
    stock_config("clear")
    stock_config("disable")
    db.commit()
    return None



changeimg = PhotoImage(file = img_path("CHANGE"))#---------------------------CHANGE BUTTON
sf3b2 = Button(sframe3,image=changeimg,bd=0,relief=FLAT,highlightthickness=0,command=init_stock_change)
sf3b2.pack(side=LEFT)

#------------------------------------------------------FRAME4---------------------------------------------------
sframe4 = Frame(stock,height=50,width=800,)
sframe4.pack(anchor=W)

stitleimg = PhotoImage(file = img_path("TITLE"))#----------------------------TITLE LABEL
sf4l1 = Label(sframe4,image=stitleimg,bd=0)
sf4l1.pack(side=LEFT,padx=(20,0))

sf4e1 = Entry(sframe4,font=("Vardana",17),width=15)#-------------------------ENTRY FOR BOOK TITLE
sf4e1.pack(side=LEFT,padx=(10,0))

authorimg = PhotoImage(file = img_path("AUTHOR"))#---------------------------AUTHER NAME LABEL
sf4l2 = Label(sframe4,image=authorimg,bd=0)
sf4l2.pack(side=LEFT,padx=(20,0))

sf4e2 = Entry(sframe4,font=("Vardana",17),width=15)#-------------------------ENTRY FOR AUTHER NAME
sf4e2.pack(side=LEFT,padx=(10,0))

#-----------------------------------------------------FRAME5----------------------------------------
sframe5 = Frame(stock,height=200,width=800)
sframe5.pack(anchor=W)

summaryimg = PhotoImage(file = img_path("SUMMARY"))#-------------------------SUMMARY LABEL
sf5l1 = Label(sframe5,image=summaryimg,bd=0)
sf5l1.pack(anchor=SW,padx=(20,0),pady=(0,3))

sf5t1 = Text(sframe5,width=50,height=10)#------------------------------------TEXT ENTRY FOR SUMMARY
sf5t1.pack(anchor=W,padx=(20,0))

#----------------------------------------------------FRAME6-------------------------------------------
sframe6 = Frame(stock,height=50,width=800)
sframe6.pack(anchor=W)

stockimg = PhotoImage(file = img_path("STOCK"))#-----------------------------STOCK LABLE
sf6l1 = Label(sframe6,image=stockimg,bd=0)
sf6l1.pack(side=LEFT,padx=(13,0))

sf6e1 = Entry(sframe6,width=4,font=("Vardana",17))#--------------------------ENTRY FOR STOCK
sf6e1.pack(side=LEFT,padx=(5,10))

priceimg = PhotoImage(file = img_path("PRICE"))#-----------------------------PRICE LABLE
sf6l2 = Label(sframe6,image=priceimg,bd=0)
sf6l2.pack(side=LEFT)

sf6e2 = Entry(sframe6,width=4,font=("Vardana",17))#--------------------------ENTRY FOR PRICE
sf6e2.pack(side=LEFT,padx=(5,10))

imglinkimg = PhotoImage(file = img_path("IMGLINK"))#-------------------------IMAGELINK LABLE
sf6l3 = Label(sframe6,image=imglinkimg,bd=0)
sf6l3.pack(side=LEFT)

sf6e3 = Entry(sframe6,width=15,font=("Vardana",17))#-------------------------ENTRY FOR IMAGELINK
sf6e3.pack(side=LEFT,padx=(5,10))

doneimg = PhotoImage(file = img_path("RDONE"))#------------------------------DONE BUTTON
sdone = Button(stock,image=doneimg,bd=0,highlightthickness=0,command=done_stock)
sdone.pack(side=RIGHT)

for widget in stock.winfo_children():#---------------------------------------TO SET HEIGHT AND WIDTH FIX
    widget.pack_propagate(0)         #---------------------------------------AND TO CHANGE BG COLOR
    # widget.config(relief=SUNKEN)
    # widget.config(bd=1)
    widget.config(bg="#61a5c2")
    # widget.config(bg="#e85d04")
    # widget.config(bg="#FCA311")

sframe1.config(bg="#14213D")
stock_config("disable")

login.config(bg="#fca311")
login.mainloop()
stock.mainloop()

r.mainloop()

root.mainloop()
