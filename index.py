import mysql.connector
import sys
from tabulate import tabulate

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "shalini.s.13",
    database = "roots"
)
c = mydb.cursor()

def sub():
    print("Submitting a book\n")
    bcode = int(input("Enter the book code : "))
    c.execute("select name from books where bcode = %s;",[bcode])
    r = c.fetchall()
    if len(r) == 0:
        print("Invalid book code")
        libop()
    else:
        c.execute("select availability,holdBy from books where bcode = %s;",[bcode])
        r = c.fetchall()
        if r[0][0] == "no":
            sql = "update books set availability = %s,holdBy = %s where bcode = %s;"
            c.execute(sql,["yes","None",bcode])
            print("Book submitted successfully")
            mydb.commit()
            libop()
        else:
            print("Book is not registered")
            libop()

def regis():
    print("Registering a book for the member\n")
    bcode = int(input("Enter the book code : "))
    idno = int(input("Enter the member's id no : "))
    c.execute("select name from libmem where idno = %s;",[idno])
    r = c.fetchall()
    name = r[0][0]
    if len(r) == 0:
        print("Invalid id no")
        libop()
    else:
        c.execute("select name from books where bcode = %s;",[bcode])
        r = c.fetchall()
        if len(r) == 0:
            print("Invalid book code")
            libop()
        else:
            c.execute("select availability,holdBy from books where bcode = %s;",[bcode])
            r = c.fetchall()
            if r[0][0] == "yes":
                sql = "update books set availability = %s,holdBy = %s where bcode = %s;"
                c.execute(sql,["no",name,bcode])
                print("Book registered successfully")
                mydb.commit()
                libop()
            else:
                print("Book is not available")
                libop()

def newbook():
    name = input("Enter name : ")
    sub = input("Enter the subject : ")
    avail = "yes"
    author = input("Enter the author name : ")
    holdBy = "None"
    c.execute("select bcode from books;")
    res = c.fetchall()
    bcode = len(res) + 1
    sql = "insert into books (bcode,name,subjects,availability,aurthor,holdBy) values(%s,%s,%s,%s,%s,%s)"
    c.execute(sql,[bcode,name,sub,avail,author,holdBy])
    print("Added the new member successfully")
    mydb.commit()
    libop()

def newlib():
    name = input("Enter name :")
    add = input("Enter address :")
    phno = input("Enter ph no :") 
    c.execute("select idno from libmem;")
    res = c.fetchall()
    idno = len(res) + 1
    sql = "insert into libmem (idno,name,address,ph) values(%s,%s,%s,%s)"
    c.execute(sql,[idno,name,add,phno])
    print("Added the new member successfully")
    mydb.commit()
    libop()


#giving options to librarian
def libop():
    print("\nOperations available....")
    print("\n1. View books status")
    print("2. Library members info")
    print("3. Add new library member")
    print("4. Add new book")
    print("5. Registering a book for a member")
    print("6. Submitting a book")
    print("7. Exit\n")
    res = int(input("\nEnter your option : "))

    if res == 1 :
        c.execute("select * from books;")
        r = c.fetchall()
        print("\nShowing books status.....\n")
        print(tabulate(r,headers=["Code","Name","Subject","Availability","Author","Hold by"]),"\n")
        libop()

    elif res == 2 :
        c.execute("select name,address,ph from libmem;")
        r = c.fetchall()
        print("\nShowing library members info.....\n")
        print(tabulate(r,headers=["Name","address","mobile no"]),"\n")
        libop()

    elif res == 3:
        newlib()
    elif res == 4:
        newbook()
    elif res == 5:
        regis()
    elif res == 6:
        sub()
    elif res == 7:
        sys.exit()
    else :
        print("Invalid option \n")
        libop()

def lib():
    flag = True
    idno = int(input("Enter you id : "))
    pwd = input("Enter you password : ")
    c.execute("select idno,pass,name from libname;")
    r = c.fetchall()
#verifing the librarian
    for i in r:
        if idno == i[0] and pwd == i[1]:
            print("\nwelcome %s"%(i[2]))
            libop()
            flag = False
            break
    if flag:
        print("your password or username is incorrect")
        print("\n")
        main()

def main():
    print("\n~~~~~~~~~ library managment system ~~~~~~~~~\n")
    print("1. Librarian")
    print("2. Exit\n")
    res = int(input("Enter the option : "))

    if res ==1 :
        lib()
    else :
        sys.exit()
main()