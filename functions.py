import random
import requests
import json
from tkinter import *
import mysql.connector as ms

#------------------------------------------------------------------------------------TO CONNECT THE DATABASE 
# db = ms.connect(host='localhost', user='root',password="avinash2002",database="book_store")
# cur = db.cursor()



def abso_get_price(cursor, isbn):#-----------------------------------------------------TO GET THE PRICE 
    get_price(search_by_isbn(isbn, cursor))

def add_column(column_name, cursor_name, table_name, db_name, datatype):#--------------TO ADD NEW COLUMN IN A SQL DATABASE
    try:
        cursor_name.execute('USE %s;', (db_name, ))
        cursor_name.execute('ALTER TABLE %s ADD %s %s', (table_name, column_name, datatype))
    except:
        print('failed to connect to database')
    return None

def buy_book(sql_cursor_name, customer_name, phone, purchase_details, price):#!!!!!!!!---------TO CHANGE THE DB ON BUYING A BOOK
    purchase_details = str(nestedlist_to_json(purchase_details))
    sales_data_feed(sql_cursor_name, phone, customer_name, purchase_details, price)

def clear(entry):#---------------------------------------------------------------------TO CLEAR A PERTICULAR ENTRY BOX
    entry.delete(0, len(get_entry(entry)))
    return None

def clear_text(text):
    text.delete("1.0", END)
    return None

def create(dic,frame):#!!!!!!!!!!!!----------------------------------------------------------------TO CREATE THE TABLE OF SALE IN PURCHASE PANNEL
    for r in range(len(dic)):
        for i in range(len(dic[r])):
            if i ==0:
                Label(frame,text=dic[r][i],width=6).grid(row=r,column=i)
            elif i == 1:
                Label(frame,text=dic[r][i],width=36,height=1,justify=LEFT).grid(row=r,column=i)
            elif i==2 :
                Label(frame,text=dic[r][i],width=15).grid(row=r,column=i)
            elif i==3 :
                Label(frame,text=dic[r][i],width=8).grid(row=r,column=i)
            else:
                Label(frame,text=dic[r][i],width=8).grid(row=r,column=i)
    for widget in frame.winfo_children():
        widget.config(bg="white",bd=1,relief=SUNKEN)

def default_entry(entry, text):#-------------------------------------------------------TO SET A DEFAULT ENTRY IN A PERTICULAR ENTRYBOX
    return entry.insert(END, text)

def dict_diff(big, small):#------------------------------------------------------------TO GET DIFFERENCE OF TWO BOOK DATA JSON
    for i in small:
        if i in big:
            big[i] -= small[i]
    return big

def download(image_url):#!!!!!!!!--------------------------------------------------------------TO DOWNLOAD AND PLACE THE BANNER IMAGE OF SEARCHED BOOK
    data = requests.get(image_url)
    name = img_path("img")
    with open(name, 'wb') as file:
        file.write(data.content)
    return name

def fake_stock(sql_cursor):#-----------------------------------------------------------TO ADD RANDOM FAKE STOCK IN DATABASE(NOT USED)
    num = len(search_all_book(sql_cursor))
    for i in range(1, num):
        qty = random.randint(10, 20)
        sql_cursor.execute("UPDATE book_data SET stock=%s WHERE Id=%s", (qty, i))
    return None

def get_entry(entry):#!!!!!!!-----------------------------------------------------------------TO GET THE ENTRY OF A PERTICULAR ENTRY BOX
    return entry.get()

def get_entry_text(entry):
    return entry.get("1.0", END)

def get_sale_info(sql_cursor_name, phone):#!!!!!!!!!!--------------------------------------------TO GET THE DATA OF A PERTICULAR CUSTOMER FROM SALES DATA
    data = sql_cursor_name.execute("""SELECT * FROM sales_data WHERE Phone=%s;""", (phone, ))    
    data = sql_cursor_name.fetchall()[-1]
    return data

def get_sale_name(data):#--------------------------------------------------------------TO GET THE CUSTOMER'S NAME
    data = data[3]
    return data

def get_sale_date(data):#--------------------------------------------------------------TO GET THE SALE DATE(NOT USED YET)
    data = data[1]
    return data

def get_sale_details(data):#!!!!!!!!!!!!-----------------------------------------------------------TO GET THE DATA OF BOUGHT BOOKS AND THIER QUANTITY
    data = data[4]
    data = eval(data)
    print(data)
    return data

def get_sale_price(data):#-------------------------------------------------------------TO GET THE FINAL PAID PRICE BY THE CUSTOMER ON PURCHASE
    data = data[5]
    return data

def get_stock(book):#!!!!!!!------------------------------------------------------------------TO GET THE STOCK OF A PERTICULAR BOOK STORED IN BOOK DATA
    return book[0][7]

def get_stock_ofbooks(book,cur):#!!!!!!!------------------------------------------------------------------TO GET THE STOCK OF A PERTICULAR BOOK STORED IN BOOK DATA
    cur.execute("SELECT stock FROM book_data WHERE isbn=%s;",(book,))
    data=cur.fetchall()[0][0]
    # print(data)
    return data
    

def get_price(book):#!!!!!!!!------------------------------------------------------------------TO GET THE PRICE OF A PERTICULAR BOOK STORED IN BOOK DATA
    return book[0][6]

def get_author(book):#!!!!!!!-----------------------------------------------------------------TO GET THE NAME OF AUTHOR OF A PERTICULAR BOOK STORED IN BOOK DATA
    return book[0][5]

def get_summary(book):#!!!!!!----------------------------------------------------------------TO GET THE SUMMARY OF A PERTICULAR BOOK STORED IN BOOK STORE
    return book[0][4]

def get_image(book):#!!!!!!!------------------------------------------------------------------TO GET THE LINK OF IMAGE OF A PERTICULAR BOOK STORED IN THE BOOK DATA
    return book[0][3]

def get_title(book):#!!!!!------------------------------------------------------------------TO GET THE BOOK TITLE OF A PERTICULAR BOOK STORED IN BOOK DATA
    return book[0][2]

def get_isbn(book):#!!!!!!!-------------------------------------------------------------------TO GET THE ISBN OF A PERTICULAR BOOK 
    return book[0][1]

def get_id(book):#---------------------------------------------------------------------TO GET THE ID OF A PERTICULAR BOOK STORED IN BOOK DATA
    return book[0][0]

def img_path(x):#!!!!!!!----------------------------------------------------------------------TO GET THE ABSOLUTE PATH OF AN IMAGE WITH ITS NAME
    k = "images/"+x+".png" 
    return k

def json_to_nestedlist(x, sql_cursor_name):#!!!!!!!!!!-------------------------------------------TO CONVERT THE JSON BOOK DATA INTO NESTED LIST
    ric =  [["SNO","Book","ISBN","Price","Qty."]]
    temp = []
    index = 1
    for i in x:
        temp = [index, get_title(search_by_isbn(i, sql_cursor_name)), i, get_price(search_by_isbn(i, sql_cursor_name)), x[i]]
        ric.append(temp)
        temp = []
        index += 1
    return ric

def nestedlist_to_json(x):#------------------------------------------------------------TO CONVERT THE NESTED LIST INTO THE JSON BOOK DATA
    jsun = {}
    for i in x[1: len(x)]:
       jsun[i[2]] = i[4] 
    return jsun

def price_from_book_json(x, sql_cursor):#!!!!!!!!----------------------------------------------TO GET THE TOTAL PRICE OF THE SET OF BOOKS IN A PERTICULAR JSON 
    money = 0
    for i in x:
        money += x[i] * get_price(search_by_isbn(i, sql_cursor))
    print(money)
    return int(money)

def return_book(phone, customer_name, sql_cursor_name, returning_books,db):#!!!!!!--------------TO UPDATE RETURN DB AND SALES DB ON RETURNING THE BOOK  

    initial_price = get_sale_price(get_sale_info(sql_cursor_name, phone))
    book_data = get_sale_details(get_sale_info(sql_cursor_name, phone))
    return_price = 0
    dict_diff(book_data, returning_books)
    
    for i in book_data:                 # updating databases of return and sales
        return_price += get_price(search_by_isbn(i, sql_cursor_name)) * returning_books[i]
        stock_increase(sql_cursor_name, search_by_isbn(i, sql_cursor_name), returning_books[i])
    return_db(sql_cursor_name, phone, customer_name, str(book_data), return_price)
    sales_data_feed(sql_cursor_name, phone, customer_name, str(returning_books), initial_price-return_price)
    print("ho gya")
    db.commit()
    return return_price 

def return_db(sql_cursor_name, phone, name, return_details, net_balance):#-------------TO REMOVE THE OLDER SALES DATA OF PERTICULAR CUSTOMER AND ALSO CHANGE THE NEW RETURN DETAILS OF PURCHASE
    sql_cursor_name.execute("""INSERT INTO return_data(Return_Date, Phone, Customer_Name, Return_Details, Net_Balance)
                                VALUES((SELECT CURRENT_TIMESTAMP), %s, %s, %s, %s)""", ( phone, name, return_details, net_balance))
    sql_cursor_name.execute("""DELETE FROM sales_data WHERE Phone=%s""", (phone, ))

def sales_data_feed(sql_cursor_name, phone, customer_name, details, price):#-----------TO ADD THE DATA OF PURCHASE 
    sql_cursor_name.execute("""INSERT INTO sales_data( Purchase_Date, Phone, Customer_Name, Purchase_Details, Net_Balance)
                                VALUES((SELECT CURRENT_TIMESTAMP), %s, %s, %s, %s)""", (phone, customer_name, details, price))

def search_by_isbn(isbn, sql_cursor):#!!!!!!!!!!-------------------------------------------------TO SEARCH A BOOK DATA TUPLE BY ITS ISBN
    lis = sql_cursor.execute("SELECT * FROM book_store.book_data WHERE ISBN=%s", (isbn,))
    lis = sql_cursor.fetchall()
    return lis

def search_by_name(name, sql_cursor):#-------------------------------------------------TO SEARCH A BOOK DATA TUPLE BY ITS NAME
    lis = sql_cursor.execute("SELECT * FROM book_data WHERE Title=%s", (name,))
    lis = sql_cursor.fetchall()
    return lis

def search_by_less_price(price_limit, sql_cursor):#------------------------------------TO SEARCH A BOOK DATA LOWER THAN A PERTICULAR PRICE LIMIT
    lis = sql_cursor.execute("SELECT * FROM book_data WHERE Price<=%s", (price_limit,))
    lis = sql_cursor.fetchall()
    return lis

def search_by_more_price(price_limit, sql_cursor):#------------------------------------TO SEARCH A BOOK DATA HIGHER THAN A PERTICULAR PRICE LIMIT
    lis = sql_cursor.execute("SELECT * FROM book_data WHERE Price>=%s", (price_limit,))
    lis = sql_cursor.fetchall()
    return lis

def search_by_phone(phone, sql_cursor):#-----------------------------------------------TO SEARCH A SALES DATA TUPLE BY ITS PHONE NUMBER
    lis = sql_cursor.execute("SELECT * FROM sales_data WHERE phone=%s", (phone, ))
    lis = sql_cursor.fetchall()
    return lis

def search_all_book(sql_cursor):#------------------------------------------------------TO GET ALL BOOK DATA STORED IN DATABASE
    lis = sql_cursor.execute("SELECT * FROM book_data")
    lis = sql_cursor.fetchall()
    return lis

def stock_increase(sql_cursor, book, qty):#!!!!!!!!!!!--------------------------------------------TO INCREASE THE STOCK OF A PERTICULAR BOOK BY THE GIVEN QUANTITY 
    sql_cursor.execute("UPDATE book_data SET stock=%s WHERE Id=%s", (get_stock(book)+qty, get_id(book)))

def stock_decrease(sql_cursor, book, qty):#!!!!!!!!!!!--------------------------------------------TO DECREASE THE STOCK OF A PERTICULAR BOOK BY THE GIVEN QUANTITY
    sql_cursor.execute("UPDATE book_data SET stock=%s WHERE Id=%s", (get_stock(book)-qty, get_id(book)))

def strify(x):#------------------------------------------------------------------------TO CONVERT MULTIPLE DATATYPES INTO STRING 
    op = ''
    if type(x) == list:
        for k in x:
            op += str(k)
        return None
