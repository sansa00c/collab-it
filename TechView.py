from tkinter import *
import pyodbc
import datetime
import socket
import threading

driver = 'SQL Server'
server = 'Placeholder'
db = 'AdminIT'
tcon = 'yes'
uname = 'sansa00c'
pword = 'Test'

cnxn = pyodbc.connect('driver={%s};server=%s;database=%s;trusted_connection=%s' % ( driver, server, db, tcon ) )

cursor = cnxn.cursor()

cursor.tables()
rows = cursor.fetchall()
for row in rows:
    print(row)

'''
Table: dbo.AdminIT
Columns:Admin, User, Location, Issue, Amazon, IP, Active, datetime
'''

COLOR = "white"

root = Tk()
root.title("LiveIT")
Tk.iconbitmap(root, default="AdminIcon.ico")
root.config(bg=COLOR)

testList = []
m=0
n=0
labelList = []

databaseLength = 6
cursor.execute("SELECT AdminIT.Tech, AdminIT.UserCol, AdminIT.Location, AdminIT.Issue, AdminIT.Amazon, AdminIT.Counter FROM dbo.AdminIT WHERE AdminIT.Active = ?", "1")

row = cursor.fetchall()
for element in row:
    for item in element:
        item = str(item)
        item = item.strip()
        testList.append(item)

compositeList = [testList[x:x+databaseLength] for x in range(0, len(testList), databaseLength)]

for element in compositeList:
    for item in element:
        dynamicLabel = Label(root, text=item, bg=COLOR)
        dynamicLabel.grid(row=m+1, column=n)
        labelList.append(dynamicLabel)
        n = n + 1
        if n is databaseLength:
            m = m + 1
            n = 0

cnxn.commit()

def onExit():
    quit()

def queryfunction():
    global adminEnt
    global userEnt
    global locationEnt
    global techEnt
    global issueEnt
    global activeEnt

    cursor.execute("SELECT Admin, UserCol, Location, Tech, Issue, Active FROM dbo.AdminIT WHERE Admin = ? AND UserCol = ? AND Location = ? AND Tech = ? AND Issue = ? AND Active = ?", adminEnt.get(), userEnt.get(),
                   locationEnt.get(), techEnt.get(), issueEnt.get(), activeEnt.get())
    for row in rows:
        print(row)

def onQuery():
    toplevel = Toplevel()

    adminEnt = StringVar()
    userEnt = StringVar()
    locationEnt = StringVar()
    techEnt = StringVar()
    issueEnt = StringVar()
    activeEnt = StringVar()

    i = 0

    labelList = ['Admin', 'User', 'Location', 'Tech', 'Issue', 'Active']
    varList = [adminEnt, userEnt, locationEnt, techEnt, issueEnt, activeEnt]

    for element in labelList:
        labelLabel = Label(toplevel, text=element)
        labelLabel.grid(row=0, column=i)
        i = i + 1
    i = 0

    for element in varList:
        entryEntry = Entry(toplevel, textvariable=element)
        entryEntry.grid(row=1, column=i)
        i = i + 1
    i = 0

    QueryButton = Button(toplevel, text="Query", bg=COLOR, command=queryfunction)
    QueryButton.grid(row=2, column=5)


def timer():
    appendList = []
    global labelList
    global m
    global n
    databaseLength = 6
    threading.Timer(3.0, timer).start()

    cursor.execute("SELECT AdminIT.Tech, AdminIT.UserCol, AdminIT.Location, AdminIT.Issue, AdminIT.Amazon, "
                   "AdminIT.Counter FROM dbo.AdminIT WHERE AdminIT.RowAdded = ?", '1')
    rows = cursor.fetchall()
    for row in rows:
        for item in row:
            item = str(item)
            item = item.strip()
            appendList.append(item)

    timerList = [appendList[x:x+databaseLength] for x in range(0, len(appendList), databaseLength)]

    for element in timerList:
        for item in element:
            dynamicLabel = Label(root, text=item, bg=COLOR)
            dynamicLabel.grid(row=m+1, column=n)
            labelList.append(dynamicLabel)
            n = n + 1
            if n is databaseLength:
                 m = m + 1
                 n = 0

    cursor.execute("UPDATE dbo.AdminIT SET AdminIT.RowAdded = ? WHERE AdminIT.RowAdded = ?", '0', '1')
    cnxn.commit()

def amazon():
    cursor.execute("UPDATE dbo.AdminIT SET Amazon = ? WHERE UserCol = ? AND Active = ?", '0', userVar.get(), '1')
    cnxn.commit()

def finish():
    global labelList
    finishList = []

    cursor.execute("SELECT AdminIT.Tech, AdminIT.UserCol, AdminIT.Location, AdminIT.Issue, AdminIT.Amazon, AdminIT.Counter FROM dbo.AdminIT WHERE AdminIT.Active = ?", "1")

    row = cursor.fetchall()
    for element in row:
        for item in element:
            item = str(item)
            item = item.strip()
            finishList.append(item)

    indexDestroy = finishList.index(countEntryVar.get())

    for i in range(5,-1,-1):
        labelList[int(indexDestroy)-i].destroy()

    cursor.execute("UPDATE dbo.AdminIT SET AdminIT.Active = ? WHERE AdminIT.Counter = ?", '0', countEntryVar.get())
    cnxn.commit()

def inputInfo():
    i = 0

    cursor.execute("SELECT MAX(AdminIT.Counter) FROM dbo.AdminIT")
    largeCounter = cursor.fetchone()
    cnxn.commit()

    cursor.execute("SELECT COUNT(AdminIT.Active) FROM dbo.AdminIT WHERE AdminIT.Active = ?", '1')
    countActive = cursor.fetchone()
    cnxn.commit()

    mainCounterVariable = largeCounter[0] + 1

    inputList = [techVar.get(), userVar.get(), locationVar.get(), issueVar.get(), amazonVar.get(), mainCounterVariable]

    integerActive = countActive[0]

    for item in inputList:
            dynamicLabel = Label(root, text=item, bg=COLOR)
            dynamicLabel.grid(row=integerActive+1, column=i)
            i = i + 1

    cursor.execute("insert into dbo.AdminIT(UserCol, Tech, Location, Issue, Amazon, datetime, IP, Active,  Counter, RowAdded) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   userVar.get(), techVar.get(), locationVar.get(), issueVar.get(), '0', datetime.datetime.now(), socket.gethostbyname(socket.gethostname()), '1', mainCounterVariable, '1')

    cnxn.commit()

techImage = PhotoImage(file='Tech.gif')
Tech = Label(root, image=techImage, background = COLOR)
Tech.image = techImage
Tech.grid(row=0, column=0)

userImage = PhotoImage(file='User.gif')
User = Label(root, image=userImage, background = COLOR)
User.image = userImage
User.grid(row=0, column = 1)

locationImage = PhotoImage(file='Location.gif')
Location = Label(root, image=locationImage, background = COLOR)
Location.image = locationImage
Location.grid(row=0, column=2)

issueImage = PhotoImage(file='Issue.gif')
Issue = Label(root, image=issueImage, background = COLOR)
Issue.image = issueImage
Issue.grid(row=0, column=3)

buttonImage = PhotoImage(file='Button.gif')
redButton = Label(root, image=buttonImage, background = COLOR)
redButton.image = buttonImage
redButton.grid(row=0, column=4)

counterImage = PhotoImage(file='Counter.gif')
counter = Label(root, image=counterImage, background = COLOR)
counter.image = counterImage
counter.grid(row=0, column=5)

techVar = StringVar()
locationVar = StringVar()
issueVar = StringVar()
amazonVar = IntVar()
countEntryVar = StringVar()
userVar = StringVar()

techEntryLabel = Label(root, text="INSERT Tech Name", bg=COLOR)
techEntryLabel.grid(row=1000, column=1)
techEntry = Entry(root, textvariable=techVar)
techEntry.grid(row=1001, column=1)

locationEntryLabel = Label(root, text="INSERT Location", bg=COLOR)
locationEntryLabel.grid(row=1000, column=2)
locationEntry = Entry(root, textvariable=locationVar)
locationEntry.grid(row=1001, column=2)

issueEntryLabel = Label(root, text="INSERT Issue", bg=COLOR)
issueEntryLabel.grid(row=1000, column=3)
issueEntry = Entry(root, textvariable=issueVar)
issueEntry.grid(row=1001, column=3)

userEntryLabel = Label(root, text="INSERT User", bg=COLOR)
userEntryLabel.grid(row=1000, column=4)
userEntry = Entry(root, textvariable=userVar)
userEntry.grid(row=1001, column=4)

amazonEntryLabel = Label(root, bg=COLOR)
amazonEntry = Entry(root, textvariable=countEntryVar)

submitButton = Button(root, text="Submit", bg=COLOR, command=inputInfo)
submitButton.grid(row=1001, column=5)

locationAmazonButton = Button(root, text="User", bg=COLOR, command=amazon)
locationAmazonButton.grid(row=1001, column=6)
buttonEntry = Entry(root,textvariable=countEntryVar)
buttonEntry.grid(row=1002, column=6)

finishButton = Button(root, text="Finish", bg=COLOR, command=finish)
finishButton.grid(row=1003, column=6)
finishEntry = Entry(root, textvariable=countEntryVar)
finishEntry.grid(row=1004, column=6)

timer()

menubar = Menu(root)
root.config(menu=menubar)
fileMenu = Menu(menubar)
fileMenu.add_command(label="Exit", command=onExit)
fileMenu.add_command(label="Query", command=onQuery)
menubar.add_cascade(label="File", menu=fileMenu)

root.mainloop()