from tkinter import *
import pyodbc
import datetime
import socket
import random

driver = 'SQL Server'
server = 'E72N7-001208\SQLEXPRESS'
db = 'AdminIT'
tcon = 'yes'
uname = 'sansa00c'
pword = 'Siemens1!'

cnxn = pyodbc.connect('driver={%s};server=%s;database=%s;trusted_connection=%s' % ( driver, server, db, tcon ) )

cursor = cnxn.cursor()

cursor.tables()
rows = cursor.fetchall()
for row in rows:
    print(row)

COLOR = "white"

root = Tk()
root.title("AdminIT")
root.config(bg=COLOR)

locationVar = StringVar()
issueVar = StringVar()
userVar = StringVar()
adminVar = StringVar()

def amazon():
    cursor.execute("SELECT MAX(AdminIT.Counter) FROM dbo.AdminIT")
    largeCounter = cursor.fetchone()
    cnxn.commit()

    mainCounterVariable = largeCounter[0] + 1

    techList = ['Alyson', 'Chris', 'Denzel', 'Ed', 'Felicia', 'Gary', 'Josh', 'Kyle', 'Lance', 'Kamel']
    techVar = random.sample(techList, 1)
    technician = ''.join(techVar)

    cursor.execute("insert into dbo.AdminIT(Admin, UserCol, Tech, Location, Issue, Amazon, datetime, IP, Active, Counter, RowAdded) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", adminVar.get(),
                   userVar.get(), technician, locationVar.get(), issueVar.get(), '0', datetime.datetime.now(), socket.gethostbyname(socket.gethostname()), '1', mainCounterVariable, '1')
    cnxn.commit()

locationImage = PhotoImage(file='Location.gif')
Location = Label(root, image=locationImage, background = COLOR)
Location.image = locationImage
Location.grid(row=0, column=0)
locationEntry = Entry(root, textvariable=locationVar)
locationEntry.grid(row=0, column=1)

issueImage = PhotoImage(file='Issue.gif')
Issue = Label(root, image=issueImage, background = COLOR)
Issue.image = issueImage
Issue.grid(row=1, column=0)
issueEntry = Entry(root, textvariable=issueVar)
issueEntry.grid(row=1, column=1)

userImage = PhotoImage(file='User.gif')
User = Label(root, image=userImage, background = COLOR)
User.image = userImage
User.grid(row=2, column = 0)
userEntry = Entry(root, textvariable=userVar)
userEntry.grid(row=2, column=1)

adminImage = PhotoImage(file='Admin.gif')
Admin = Label(root, image=adminImage, background = COLOR)
Admin.image = adminImage
Admin.grid(row=3, column = 0)
adminEntry=Entry(root, textvariable=adminVar)
adminEntry.grid(row=3, column=1)

locationAmazonButton = Button(root, text="Submit", bg=COLOR, command=amazon)
locationAmazonButton.grid(row=4, column=0)

root.mainloop()