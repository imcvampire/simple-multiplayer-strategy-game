from tkinter import *

class table(object):

	def __init__(self, master, row, colum):
		self.master = master
		self.row = row
		self.colum = colum
		self.createTable()

	def createTable(self):
		self.table = []
		for i in range(self.row):
			listRow = []
			for j in range(self.colum):
				lab = Label(self.master, text="", relief=RIDGE, width = 15)
				lab.grid(row=i, column=j, sticky=NSEW)
				listRow.append(lab)
			self.table.append(listRow)

	def updateTable(self, array):
		for i in range(self.row):
			for j in range(self.colum):
				self.table[i][j]['text'] = str(array[i][j])