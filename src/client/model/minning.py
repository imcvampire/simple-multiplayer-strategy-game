from tkinter import *
from _pickle import loads, dumps
from model.message import message
from tkinter import messagebox
from model.questions import questions

class minning(object):
    ##### Init #####
    def __init__(self, client, teamId, mineId, master):
        self.client = client
        self.teamId = teamId
        self.master = master
        self.mineId = mineId
        self.checked = StringVar()
        self.choices = [
            "Iron",
            "Wood",
            "Stone"
            ]
        Label(self.master, text="""Choose your resource:""",justify = LEFT,padx = 20).pack()

        for val in self.choices:
            Radiobutton(self.master, text=val,padx = 20, variable=self.checked, command=None,value=val).pack(anchor=W)
        button_ok = Button(self.master, text='Ok', command=lambda: self.getQuestion(), width = 10).pack()

    def getQuestion(self):
        check = self.checked.get()
        if check == "":
            messagebox.showwarning("Warning", "You must choice one of this!")
        else:
            payload = self.mineId, check
            mes = message(0x0201, self.teamId, payload)
            try:
                self.client.send(dumps(mes))
                mesrcv = loads(self.client.recv(2048))
                if mesrcv.opCode == 0x0202:
                    if mesrcv.teamId == True:
                        content, choice = mesrcv.payLoad
                        newFrame = Toplevel()
                        questionFrame = questions(self.client, self.teamId, 0x0301, self.mineId, check, newFrame, content, choice)
                    else:
                        messagebox.showwarning("Warning", mesrcv.payLoad)
                else:
                    messagebox.showwarning("Warning", "Server send Error! Please try again!")
            except:
                messagebox.showwarning("Warning", "Cannot connect to server!")
        self.master.destroy()