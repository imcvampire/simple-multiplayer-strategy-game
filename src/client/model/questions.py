from tkinter import *
from _pickle import loads, dumps
from model.message import message

class questions(object):
    def __init__ (self, client, teamId, opCode, mineId, resource, master, content, choices):
        self.client =  client
        self.teamId = teamId
        self.opCode = opCode
        self.mineId = mineId
        self.resource = resource
        self.master = master
        self.content = content
        self.choices = choices
        self.answer = StringVar()
        Label(self.master, text = self.content, justify = LEFT,padx=20).pack()
        for val in self.choices:
            Radiobutton(self.master, text=val,padx = 20, variable = self.answer, command=None ,value=val).pack(anchor=W)
        button_ok = Button(self.master, text='Ok', command=lambda: self.sendAnswer(), width = 10).pack()

    def sendAnswer(self):
        answer = self.answer.get()
        if(answer == ""):
            messagebox.showwarning("Warning", "You must choice one of this!")
        else:
            payload = self.mineId, self.resource, answer
            mes = message(self.opCode, self.teamId, payload)
            try:
                self.client.send(dumps(mes))
                mesrcv = loads(self.client.recv(2048))
                if mesrcv.opCode == (self.opCode + 1):
                    if mesrcv.teamId == True:
                        messagebox.showinfo("Notify", "Answer correct!")
                    else:
                        messagebox.showwarning("Notify", mesrcv.payLoad)
                else:
                    messagebox.showwarning("Warning", "Server send Error! Please try again!")
            except:
                messagebox.showwarning("Warning", "Cannot connect to server!")
        self.master.destroy()