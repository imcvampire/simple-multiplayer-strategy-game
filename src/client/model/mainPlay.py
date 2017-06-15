from tkinter import *
from _pickle import loads, dumps
from message import message
from model.table import table
from model.minning import minning
from model.questions import questions
from model.buyAttack import buyAttack
from model.buyDefend import buyDefend
from tkinter import messagebox
class mainPlay(object):

    def __init__(self, client, teamId, master, parent):
        ##### Init #####
        self.parent = parent
        self.client = client
        self.teamId = teamId
        self.master = master
        self.master.title("Game Play")
        self.master.geometry("670x550")

        ##### Mines #####
        self.mo1 = Frame(self.master)
        self.mo1.place(x= 20, y = 200)
        self.mo2 = Frame(self.master)
        self.mo2.place(x= 20, y = 240)
        self.mo3 = Frame(self.master)
        self.mo3.place(x= 20, y = 280)
        self.mo4 = Frame(self.master)
        self.mo4.place(x= 20, y = 320)
        self.mo5 = Frame(self.master)
        self.mo5.place(x= 20, y = 360)
        self.mo6 = Frame(self.master)
        self.mo6.place(x= 20, y = 400)
        #Mines 1
        label_mo1 = Label(self.mo1, text="Mines 1", fg = 'green').grid(row=1,column=1,sticky=W)
        self.button_quest1 = Button(self.mo1, text='Question', command=lambda: self.select(1), width = 10)
        self.button_quest1.grid(row=1, column=2, sticky=W, pady=4)
        #Mines 2
        label_mo2 = Label(self.mo2, text="Mines 2", fg = 'green').grid(row=2,column=1,sticky=W)
        self.button_quest2 = Button(self.mo2, text='Question', command=lambda: self.select(2), width = 10)
        self.button_quest2.grid(row=2, column=2, sticky=W, pady=4)
        #Mines 3
        label_mo3 = Label(self.mo3, text="Mines 3", fg = 'green').grid(row=3,column=1,sticky=W)
        self.button_quest3 = Button(self.mo3, text='Question', command=lambda: self.select(3), width = 10)
        self.button_quest3.grid(row=3, column=2, sticky=W, pady=4)
        #Mines 4
        label_mo4 = Label(self.mo4, text="Mines 4", fg = 'green').grid(row=4,column=1,sticky=W)
        self.button_quest4 = Button(self.mo4, text='Question', command=lambda: self.select(4), width = 10)
        self.button_quest4.grid(row=4, column=2, sticky=W, pady=4)
        #Mines 5
        label_mo5 = Label(self.mo5, text="Mines 5", fg = 'green').grid(row=5,column=1,sticky=W)
        self.button_quest5 = Button(self.mo5, text='Question', command=lambda: self.select(5), width = 10)
        self.button_quest5.grid(row=5, column=2, sticky=W, pady=4)
        #Mines 6
        label_mo6 = Label(self.mo6, text="Mines 6", fg = 'green').grid(row=6,column=1,sticky=W)
        self.button_quest6 = Button(self.mo6, text='Question', command=lambda: self.select(6), width = 10)
        self.button_quest6.grid(row=6, column=2, sticky=W, pady=4)

        ##### Castle #####
        #Castle 1
        self.castle1 = Frame(self.master)
        self.castle1.place(x= 250, y = 200)
        self.label_castl1 = Label(self.castle1, text = "Castle 1").grid(row=0, column= 0, sticky = W)
        self.button_attack1 = Button(self.castle1, text='Attack', fg = 'red', command=lambda: self.Attack(1), width = 10)
        self.button_attack1.grid(row=0, column=3, sticky=W, pady=4)
        self.button_defend1 = Button(self.castle1, text='Buy_Defend', command=lambda: self.buy_defend(1), width = 10)
        self.button_defend1.grid(row=0, column=1, sticky=W, pady=4)
        self.label1_castl1 = Label(self.castle1, text = "Defend:", fg = 'blue').grid(row=1, column= 0, sticky = W)
        self.castle1_defend = Label(self.castle1, text = "", relief=RIDGE, width = 13).grid(row=1, column= 1, sticky = W)
        self.label2_castl1 = Label(self.castle1, text = "Team Owner:", fg = 'blue').grid(row=1, column= 2, sticky = W)
        self.castle1_owner = Label(self.castle1, text = "", relief=RIDGE, width = 13).grid(row=1, column= 3, sticky = W)
        #Castle 2
        self.castle2 = Frame(self.master)
        self.castle2.place(x= 250, y = 260)
        self.label_castl2 = Label(self.castle2, text = "Castle 2").grid(row=0, column= 0, sticky = W)
        self.button_attack2 = Button(self.castle2, text='Attack', fg = 'red', command=lambda: self.Attack(2), width = 10)
        self.button_attack2.grid(row=0, column=3, sticky=W, pady=4)
        self.button_defend2 = Button(self.castle2, text='Buy_Defend', command=lambda: self.buy_defend(2), width = 10)
        self.button_defend2.grid(row=0, column=1, sticky=W, pady=4)
        self.label1_castl2 = Label(self.castle2, text = "Defend:", fg = 'blue').grid(row=1, column= 0, sticky = W)
        self.castle2_defend = Label(self.castle2, text = "", relief=RIDGE, width = 13).grid(row=1, column= 1, sticky = W)
        self.labe2_castl2 = Label(self.castle2, text = "Team Owner:", fg = 'blue').grid(row=1, column= 2, sticky = W)
        self.castle2_owner = Label(self.castle2, text = "", relief=RIDGE, width = 13).grid(row=1, column= 3, sticky = W)
        #Castle 3
        self.castle3 = Frame(self.master)
        self.castle3.place(x= 250, y = 320)
        self.label_castl3 = Label(self.castle3, text = "Castle 3").grid(row=0, column= 0, sticky = W)
        self.button_attack3 = Button(self.castle3, text='Attack', fg = 'red', command=lambda: self.Attack(3), width = 10)
        self.button_attack3.grid(row=0, column=3, sticky=W, pady=4)
        self.button_defend3 = Button(self.castle3, text='Buy_Defend', command=lambda: self.buy_defend(3), width = 10)
        self.button_defend3.grid(row=0, column=1, sticky=W, pady=4)
        self.label1_castl3 = Label(self.castle3, text = "Defend:", fg = 'blue').grid(row=1, column= 0, sticky = W)
        self.castle3_defend = Label(self.castle3, text = "", relief=RIDGE, width = 13).grid(row=1, column= 1, sticky = W)
        self.labe2_castl3 = Label(self.castle3, text = "Team Owner:", fg = 'blue').grid(row=1, column= 2, sticky = W)
        self.castle3_owner = Label(self.castle3, text = "", relief=RIDGE, width = 13).grid(row=1, column= 3, sticky = W)

        ##### Buy attack #####
        self.frameBuyattack = Frame(self.master)
        self.frameBuyattack.place(x = 400, y = 400)
        self.button_buyattack = Button(self.frameBuyattack, text='Buy_Attack', command=lambda: self.buy_attack(), width = 10)
        self.button_buyattack.grid(row=0, column=0, sticky=W, pady=4)

        ##### Button Quit #####
        self.button_quit = Button(self.master, text='Quit', command=lambda: self.quit(),width = 10)
        self.button_quit.grid(row=8, column=8, sticky=W, pady=4)
        self.button_quit.place(x=550, y=500)

        ##### Table Team Info #####
        self.labelTableTeam = Label(self.master, text = "Table Team Info", fg = 'blue').place(x = 20, y = 20)
        self.tableFrame = Frame(self.master)
        self.tableFrame.place(x = 20, y = 50)
        self.tableTeamInfo = table(self.tableFrame, 4, 5)
    ## Main Loop ##
    def mainLoop(self):
        self.master.mainloop()

    ## Hide ##
    def hide(self):
        self.master.withdraw()

    ## Quit ##
    def quit(self):
        self.master.destroy()
        self.parent.destroy()
    ## Attack ##
    def Attack(self, castleId):
        yesorno = messagebox.askyesno("Question", "Do you want to attack?")
        if yesorno == True:
            payload = castleId
            try:
                mes = message(0x0501, self.teamId, payload)
                self.client.send(dumps(mes))
                mesrcv = loads(self.client.recv(2048))
                if mesrcv.opCode == 0x0502:
                    if mesrcv.teamId == True:
                        messagebox.showinfo("Notify", "Attack complete! Please answer the question of castle!")
                        content, choice = mesrcv.payLoad
                        newFrame = Toplevel()
                        questionFrame = questions(self.client, self.teamId, 0x0701, castleId, None, newFrame, content, choice)
                    else:
                        messagebox.showwarning("Notify", mesrcv.payLoad)
            except:
                messagebox.showwarning("Warning", "Cannot connect to server!")
        else:
            pass

    ## Select Mines ##
    def select(self, mineId):
        newFrame = Toplevel()
        choiceFrame = minning(self.client, self.teamId, mineId, newFrame)

    ## Buy attack ##
    def buy_attack(self):
        newFrame = Toplevel()
        buyAttackFrame = buyAttack(self.client, self.teamId, newFrame)

    ## Buy Defend ##
    def buy_defend(self, castleId):
        newFrame = Toplevel()
        buyDefendFrame = buyDefend(self.client, self.teamId, castleId, newFrame)
