from tkinter import *
from py2neo import *
import csv
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename

#Object for GUI
root = Tk()

xaxis=StringVar()
yaxis=StringVar()

#Object for Neo4j Database
g=Graph(password="Heenu@96")

TT=("Request","Issue")
Sev=("0 - Unclassified","1 - Minor","2 - Normal","3 - Major","4 - Critical")
RS=("1 - Junior","2 - Regular","3 - Senior","4 - Management")
FA=("Systems","Software","Hardware","Access/Login")
Prio=("0 - Unassigned","1 - Low","2 - Medium","3 - High")
Sats=("0 - Unknown","1 - Unsatisfied","2 - Satisfied","3 - Highly satisfied")

#Radio button function
def sel():
    top = Tk()
    Label(top,
          text="""Choose the value""",
          justify=LEFT,
          padx=20).pack()
    vart = StringVar()
    vart.set("Issue")
    R1 = Radiobutton(top, text="Issue", variable=vart, value="Issue")
    R1.pack(anchor=W)
    R2 = Radiobutton(top, text="Request", variable=vart, value="Request")
    R2.pack(anchor=W)
    print(vart.get())
    if(vart.get()=="Issue"):
        x = Sev
        print(x)
        y=[]
        for i in (Sev):
            y.append(g.run("MATCH (a:Ticket) WHERE TicketType=Issue AND Severity="+i+" return count(a)").data())
        print(y)
        width = 1 / 1.5
        plt.bar(x, y, width, color="blue")
        plt.show()



def sel1():
    top = Tk()
    v=StringVar()
    L1 = Label(top, text=var.get())
    L1.pack(side=LEFT)
    E1 = Entry(top, bd=5)
    E1.pack(side=RIGHT)
    def show_entry_fields():
        v=E1.get()
    Button(top, text='Done', command=show_entry_fields, justify=RIGHT).pack()
    return v


#to browse CSV Data file and upload the data to Neo4j and make relationships among the nodes`
def browsefunc():
    root.filename = askopenfilename(initialdir='C', title="Choose your file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    print(root.filename)
    name=root.filename
    rqidarray=set()
    ITidarray = set()
    daysarray = set()
    with open(name) as csvfile:
        reader = csv.DictReader(csvfile)
        tx = g.begin()
        for line in reader:
            a = Node("Ticket", TicketID=line['Ticket'], TicketType=line['TicketType'], Severity=line['Severity'], RequesterID=int(line['RequesterID']), RequesterSeniority=line['RequesterSeniority'], FiledAgainst=line['FiledAgainst'],Priority=line['Priority'], ITOwnerID=int(line['ITOwnerID']), DaysOpen=int(line['DaysOpen']), Satisfaction=line['Satisfaction'])
            tx.merge(a)
            rqidarray.add(int(line['RequesterID']))
            ITidarray.add(int(line['ITOwnerID']))
            daysarray.add(int(line['DaysOpen']))
            b=Node("RequesterID", RequesterID=int(line['RequesterID']))
            tx.merge(b)
            c = Node("ITOwnerID", ITOwnerID=int(line['ITOwnerID']))
            tx.merge(c)
            d = Node("DaysOpen", DaysOpen=int(line['DaysOpen']))
            tx.merge(d)
        tx.commit()
    #print(array)
    #print(array.__len__())
    tx=g.begin()
    a=Node("TicketType", TicketType='Request')
    tx.merge(a)
    a = Node("TicketType", TicketType='Issue')
    tx.merge(a)
    a = Node("Severity", Severity='0 - Unclassified')
    tx.merge(a)
    a = Node("Severity", Severity='1 - Minor')
    tx.merge(a)
    a = Node("Severity", Severity='2 - Normal')
    tx.merge(a)
    a = Node("Severity", Severity='3 - Major')
    tx.merge(a)
    a = Node("Severity", Severity='4 - Critical')
    tx.merge(a)
    a = Node("RequesterSeniority", RequesterSeniority='1 - Junior')
    tx.merge(a)
    a = Node("RequesterSeniority", RequesterSeniority='2 - Regular')
    tx.merge(a)
    a = Node("RequesterSeniority", RequesterSeniority='3 - Senior')
    tx.merge(a)
    a = Node("RequesterSeniority", RequesterSeniority='4 - Manager')
    tx.merge(a)
    a = Node("FiledAgainst", FiledAgainst='Systems')
    tx.merge(a)
    a = Node("FiledAgainst", FiledAgainst='Software')
    tx.merge(a)
    a = Node("FiledAgainst", FiledAgainst='Access/Login')
    tx.merge(a)
    a = Node("Filed Against", FiledAgainst='Hardware')
    tx.merge(a)
    a = Node("Priority", Priority='0 - Unassigned')
    tx.merge(a)
    a = Node("Priority", Priority='1 - Low')
    tx.merge(a)
    a = Node("Priority", Priority='2 - Medium')
    tx.merge(a)
    a = Node("Priority", Priority='3 - High')
    tx.merge(a)
    a = Node("Satisfaction", Satisfaction='0 - Unknown')
    tx.merge(a)
    a = Node("Satisfaction", Satisfaction='1 - Unsatisfied')
    tx.merge(a)
    a = Node("Satisfaction", Satisfaction='2 - Satisfied')
    tx.merge(a)
    a = Node("Satisfaction", Satisfaction='3 - Highly satisfied')
    tx.merge(a)
    tx.commit()
    g.run("MATCH (a:Ticket),(b:Severity) WHERE a.Severity = '0 - Unclassified' AND b.Severity = '0 - Unclassified' MERGE (a)-[r:Severity]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Severity) WHERE a.Severity = '1 - Minor' AND b.Severity = '1 - Minor' MERGE (a)-[r:Severity]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Severity) WHERE a.Severity = '2 - Normal' AND b.Severity = '2 - Normal' MERGE (a)-[r:Severity]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Severity) WHERE a.Severity = '3 - Major' AND b.Severity = '3 - Major' MERGE (a)-[r:Severity]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Severity) WHERE a.Severity = '4 - Critical' AND b.Severity = '4 - Critical' MERGE (a)-[r:Severity]->(b)").data()
    g.run("MATCH (a:Ticket),(b:TicketType) WHERE a.TicketType = 'Issue' AND b.TicketType = 'Issue' MERGE (a)-[r:TicketType]->(b)").data()
    g.run("MATCH (a:Ticket),(b:TicketType) WHERE a.TicketType = 'Request' AND b.TicketType = 'Request' MERGE (a)-[r:TicketType]->(b)").data()
    g.run("MATCH (a:Ticket),(b:RequesterSeniority) WHERE a.RequesterSeniority = '1 - Junior' AND b.RequesterSeniority = '1 - Junior' MERGE (a)-[r:RequesterSeniority]->(b)").data()
    g.run("MATCH (a:Ticket),(b:RequesterSeniority) WHERE a.RequesterSeniority = '2 - Regular' AND b.RequesterSeniority = '2 - Regular' MERGE (a)-[r:RequesterSeniority]->(b)").data()
    g.run("MATCH (a:Ticket),(b:RequesterSeniority) WHERE a.RequesterSeniority = '3 - Senior' AND b.RequesterSeniority = '3 - Senior' MERGE (a)-[r:RequesterSeniority]->(b)").data()
    g.run("MATCH (a:Ticket),(b:RequesterSeniority) WHERE a.RequesterSeniority = '4 - Manager' AND b.RequesterSeniority = '4 - Manager' MERGE (a)-[r:RequesterSeniority]->(b)").data()
    g.run("MATCH (a:Ticket),(b:FiledAgainst) WHERE a.FiledAgainst = 'Systems' AND b.FiledAgainst = 'Systems' MERGE (a)-[r:FiledAgainst]->(b)").data()
    g.run("MATCH (a:Ticket),(b:FiledAgainst) WHERE a.FiledAgainst = 'Software' AND b.FiledAgainst = 'Software' MERGE (a)-[r:FiledAgainst]->(b)").data()
    g.run("MATCH (a:Ticket),(b:FiledAgainst) WHERE a.FiledAgainst = 'Hardware' AND b.FiledAgainst = 'Hardware' MERGE (a)-[r:FiledAgainst]->(b)").data()
    g.run("MATCH (a:Ticket),(b:FiledAgainst) WHERE a.FiledAgainst = 'Access/Login' AND b.FiledAgainst = 'Access/Login' MERGE (a)-[r:FiledAgainst]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Priority) WHERE a.Priority = '0 - Unassigned' AND b.Priority = '0 - Unassigned' MERGE (a)-[r:Priority]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Priority) WHERE a.Priority = '1 - Low' AND b.Priority = '1 - Low' MERGE (a)-[r:Priority]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Priority) WHERE a.Priority = '2 - Medium' AND b.Priority = '2 - Medium' MERGE (a)-[r:Priority]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Priority) WHERE a.Priority = '3 - High' AND b.Priority = '3 - High' MERGE (a)-[r:Priority]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Satisfaction) WHERE a.Satisfaction = '0 - Unknown' AND b.Satisfaction = '0 - Unknown' MERGE (a)-[r:Satisfaction]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Satisfaction) WHERE a.Satisfaction = '1 - Unsatisfied' AND b.Satisfaction = '1 - Unsatisfied' MERGE (a)-[r:Satisfaction]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Satisfaction) WHERE a.Satisfaction = '2 - Satisfied' AND b.Satisfaction = '2 - Satisfied' MERGE (a)-[r:Satisfaction]->(b)").data()
    g.run("MATCH (a:Ticket),(b:Satisfaction) WHERE a.Satisfaction = '3 - Highly satisfied' AND b.Satisfaction = '3 - Highly satisfied' MERGE (a)-[r:Satisfaction]->(b)").data()
    for value in rqidarray:
        g.run("MATCH (a:Ticket),(b:RequesterID) WHERE a.RequesterID = " +  str(value) + " AND b.RequesterID = " + str(value) + " MERGE (a)-[r:RequesterID]->(b)")
    for value in ITidarray:
        g.run("MATCH (a:Ticket),(b:ITOwnerID) WHERE a.ITOwnerID = " + str(value) + " AND b.ITOwnerID = " + str(value) + " MERGE (a)-[r:ITOwnerID]->(b)")
    for value in daysarray:
        g.run("MATCH (a:Ticket),(b:DaysOpen) WHERE a.DaysOpen = " + str(value) + " AND b.DaysOpen = " + str(value) + " MERGE (a)-[r:DaysOpen]->(b)")
    print("Database uploaded successfully to Neo4j")



def donothing():
    filewin = Toplevel(root)
    button = Button(filewin, text="Do nothing button")
    button.pack()

#GUI
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Browse", command=browsefunc)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

#Radio Button Selection for Y-axis
Label(root,
      text="""Choose the parameter for Y-Axis""",
      justify=LEFT,
      padx=20).pack()
var = StringVar()
var.set("abc")
R1 = Radiobutton(root, text="Total Number of Tickets", variable=var, value="Ticket")
R1.pack(anchor=W)
R2 = Radiobutton(root, text="Requester ID", variable=var, value="RequesterID", command=sel)
R2.pack( anchor = W )
R3 = Radiobutton(root, text="Ticket Type", variable=var, value="TicketType", command=sel)
R3.pack( anchor = W)
R4 = Radiobutton(root, text="Severity", variable=var, value="Severity", command=sel)
R4.pack( anchor = W)
R5 = Radiobutton(root, text="Requester Seniority", variable=var, value="RequesterSeniority", command=sel1)
R5.pack( anchor = W)
R6 = Radiobutton(root, text="Filed Against", variable=var, value="Filed Against", command=sel1)
R6.pack( anchor = W)
R7 = Radiobutton(root, text="Priority", variable=var, value="Priority", command=sel1)
R7.pack( anchor = W)
R8 = Radiobutton(root, text="IT Owner ID", variable=var, value="ITOwnerID", command=sel)
R8.pack( anchor = W)
R9 = Radiobutton(root, text="Days Open", variable=var, value="Days Open", command=sel)
R9.pack( anchor = W)
R10 = Radiobutton(root, text="Satisfaction", variable=var, value="Satisfaction", command=sel1)
R10.pack( anchor = W)
yaxis=var.get()
#yaxis=sel()

#Radio Button Selection for X-axis
Label(root,
      text="""Choose the parameter for X-Axis""",
      justify=LEFT,
      padx=20).pack()
var1 = StringVar()
var1.set("abc")
#R1 = Radiobutton(root, text="Total Number of Tickets", variable=var1, value="Ticket", command=sel)
#R1.pack(anchor=W)
R12 = Radiobutton(root, text="Requester ID", variable=var1, value="RequesterID")
R12.pack( anchor = W )
R13 = Radiobutton(root, text="Ticket Type", variable=var1, value="TicketType")
R13.pack( anchor = W)
R14 = Radiobutton(root, text="Severity", variable=var1, value="Severity")
R14.pack( anchor = W)
R15 = Radiobutton(root, text="Requester Seniority", variable=var1, value="RequesterSeniority")
R15.pack( anchor = W)
R16 = Radiobutton(root, text="Filed Against", variable=var1, value="Filed Against")
R16.pack( anchor = W)
R17 = Radiobutton(root, text="Priority", variable=var1, value="Priority")
R17.pack( anchor = W)
R18 = Radiobutton(root, text="IT Owner ID", variable=var1, value="ITOwnerID")
R18.pack( anchor = W)
R19 = Radiobutton(root, text="Days Open", variable=var1, value="Days Open")
R19.pack( anchor = W)
R20 = Radiobutton(root, text="Satisfaction", variable=var1, value="Satisfaction")
R20.pack( anchor = W)
xaxis=var.get()
#xaxis=sel1()


root.mainloop()


