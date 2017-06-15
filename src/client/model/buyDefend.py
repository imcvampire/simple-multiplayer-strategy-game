from tkinter import *
from _pickle import loads, dumps
from message import message
from tkinter import messagebox

class buyDefend(object):
    def __init__ (self, client, teamId, castleId, master):
        ITEM = {
            'defence': {
                'fence': {
                    'name': 'Fence',
                    'value': 200,
                    'resources': {
                        'wood': 200,
                        'stone': 50,
                    }
                },
                'wood': {
                    'name': 'Wood wall',
                    'value': 1000,
                    'resources': {
                        'wood': 1000,
                        'stone': 100,
                        'iron': 100,
                    },
                },
                'stone': {
                    'name': 'Stone wall',
                    'value': 3000,
                    'resources': {
                        'wood': 200,
                        'stone': 1000,
                        'iron': 200,
                    },
                },
                'legend': {
                    'name': 'Legend wall',
                    'value': 8000,
                    'resources': {
                        'wood': 1000,
                        'stone': 2000,
                        'iron': 1000,
                    },
                },
            },
        }

        self.master = master
        self.client = client
        self.teamId = teamId
        self.castleId = castleId
        self.checked = StringVar()
        self.choices = [
            (ITEM['defence']['fence'],"fence"),
            (ITEM['defence']['wood'],"wood"),
            (ITEM['defence']['stone'],"stone"),
            (ITEM['defence']['legend'],"legend"),
        ]
        Label(self.master, text = "Sellect Item: ", justify = LEFT,padx=20).pack()
        for txt, val in self.choices:
            Radiobutton(self.master, text=txt,padx = 20, variable=self.checked, command=None,value=val).pack(anchor=W)
        button_ok = Button(self.master, text='Ok', command=lambda: self.buyDefend(), width = 10).pack()

    def buyDefend(self):
        check = self.checked.get()
        if check == "":
            messagebox.showwarning("Warning", "You must choice one of this!")
        else:
            payload = self.castleId, check
            mes = message(0x0601, self.teamId, payload)
            try:
                self.client.send(dumps(mes))
                mesrcv = loads(self.client.recv(2048))
                if mesrcv.opCode == 0x0602:
                    if mesrcv.teamId == True:
                        messagebox.showinfo("Notify", "Buy success!")
                    else:
                        messagebox.showwarning("Warning", mesrcv.payLoad)
                else:
                    messagebox.showwarning("Warning", "Server send Error! Please try again!")
            except:
                messagebox.showwarning("Warning", "Cannot connect to server!")
        self.master.destroy()