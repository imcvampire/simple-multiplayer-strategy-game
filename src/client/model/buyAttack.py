from tkinter import *
from _pickle import loads, dumps
from model.message import message
from tkinter import messagebox

class buyAttack(object):
    def __init__ (self,client, teamId, master):
        ITEM = {
            'attack': {
                'balista': {
                    'name': 'Ballista',
                    'value': 1000,
                    'resources': {
                        'wood': 1500,
                        'iron': 200,
                    },
                },
                'catapult': {
                    'name': 'Catapult',
                    'value': 3000,
                    'resources': {
                        'wood': 400,
                        'stone': 1500,
                        'iron': 300,
                    },
                },
                'cannon': {
                    'name': 'Cannon',
                    'value': 8000,
                    'resources': {
                        'wood': 500,
                        'stone': 2500,
                        'iron': 1800,
                    },
                },
            },
        }

        self.master = master
        self.client = client
        self.teamId = teamId
        self.checked = StringVar()
        self.choices = [
            (ITEM['attack']['balista'],1),
            (ITEM['attack']['catapult'],2),
            (ITEM['attack']['cannon'],3),

        ]
        Label(self.master, text = "Sellect Item: ", justify = LEFT,padx=20).pack()
        for txt, val in self.choices:
            Radiobutton(self.master, text=txt,padx = 20, variable=self.checked, command=None, value=val).pack(anchor=W)
        button_ok = Button(self.master, text='Ok', command=lambda: self.buyAttack(), width = 10).pack()

    def buyAttack(self):
        check = self.checked.get()
        if check == "":
            messagebox.showwarning("Warning", "You must choice one of this!")
        else:
            mes = message(0x0401, self.teamId, check)
            try:
                self.client.send(dumps(mes))
                mesrcv = loads(self.client.recv(2048))
                if mesrcv.opCode == 0x0402:
                    if mesrcv.teamId == True:
                        messagebox.showinfo("Notify", "Buy success!")
                    else:
                        messagebox.showwarning("Warning", mesrcv.payLoad)
                else:
                    messagebox.showwarning("Warning", "Server send Error! Please try again!")
            except:
                messagebox.showwarning("Warning", "Cannot connect to server!")
        self.master.destroy()