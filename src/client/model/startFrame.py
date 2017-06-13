from tkinter import *
from _pickle import loads, dumps
from model.message import message

class startFrame():

    def __init__(self, client, master, list_team):
        self.client = client
        self.master = master
        self.list_team = list_team
        self.master.title("Small-Game")
        self.master.geometry("430x170")

        self.table_team = Frame(self.master)
        self.lable1 = Label(self.master, text = "Team Id:", relief= RIDGE, width = 10)
        self.teamId = Entry(self.master, width = 15)
        self.btjoin = Button(self.master, text = "Play", command = lambda: self.playGame(self.teamId.get()), width = 5)
        self.btexit = Button(self.master, text = "Exit", command = lambda: self.Exit(), width = 5)

        #Layout
        self.table_team.place(x= 0, y = 0)
        self.lable1.place(x = 5, y = 100)
        self.teamId.place(x = 80,y = 100)
        self.btjoin.place(x = 350, y = 130)
        self.btexit.place(x = 5, y = 130)
        self.updateTbteam()

    def mainLoop(self):
        self.master.mainloop()

    def updateTbteam(self):
        l = Label(self.table_team, text="%10s" % ("Team Id"), relief=RIDGE, width = 10)
        l.grid(row=0, column=0, sticky=NSEW)
        l = Label(self.table_team, text="%10s" % ("Gold"), relief=RIDGE, width = 10)
        l.grid(row=0, column=1, sticky=NSEW)
        l = Label(self.table_team, text="%10s" % ("Iron"), relief=RIDGE, width = 10)
        l.grid(row=0, column=2, sticky=NSEW)
        l = Label(self.table_team, text="%10s" % ("Wood"), relief=RIDGE, width = 10)
        l.grid(row=0, column=3, sticky=NSEW)
        l = Label(self.table_team, text="%10s" % ("Stone"), relief=RIDGE, width = 10)
        l.grid(row=0, column=4, sticky=NSEW)
        for i,team in enumerate(self.list_team):
            l = Label(self.table_team, text="%10s" % (team[0]), relief=RIDGE, width = 10)
            l.grid(row=i+1, column=0, sticky=NSEW)
            l = Label(self.table_team, text="%10s" % (team[1]), relief=RIDGE, width = 10)
            l.grid(row=i+1, column=1, sticky=NSEW)
            l = Label(self.table_team, text="%10s" % (team[2]), relief=RIDGE, width = 10)
            l.grid(row=i+1, column=2, sticky=NSEW)
            l = Label(self.table_team, text="%10s" % (team[3]), relief=RIDGE, width = 10)
            l.grid(row=i+1, column=3, sticky=NSEW)
            l = Label(self.table_team, text="%10s" % (team[4]), relief=RIDGE, width = 10)
            l.grid(row=i+1, column=4, sticky=NSEW)

    def playGame(self, teamId):
        mes = message(0x0101, teamId, None)
        self.client.send(dumps(mes))


    def quit(self):
        self.master.destroy()

    def hide(self):
        self.master.withdraw()

    def Exit(self):
        self.quit()