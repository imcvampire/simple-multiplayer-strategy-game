
class QuestionFrame:
    def __init__ (self, client, master, parent, content, choices):
        self.client =  client
        self.master = master
        self.parent = parent
        self.content = content
        self.choices = choices
        self.answer = StringVar()
        Label(self.master, text = self.content, justify = LEFT,padx=20).pack()
        for txt, val in self.choices:
            Radiobutton(self.master, text=txt,padx = 20, variable=self.answer, command=lambda: self.ShowChoice(),value=val).pack(anchor=W)
        button_ok = Button(self.master, text='Ok', command=lambda: self.update(), width = 10).pack()


    def ShowChoice(self):
        pass

    def update(self):
        answer = self.answer.get()
        if(answer==""):
            pass
        else:

            self.client.send()