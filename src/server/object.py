class CauHoi:
	def __init__(self, cauhoi, cautraloi1,cautraloi2, cautraloi3, cautraloi4, dapan, idCauHoi):
		self.cauhoi = cauhoi
		self.cautraloi4 = cautraloi4
		self.cautraloi3 = cautraloi3
		self.cautraloi2 = cautraloi2
		self.cautraloi1 = cautraloi1
		self.dapan = dapan
        self.idCauHoi

class LauDai:
    def __init__(self, idLauDai,idCauHoi):
        self.idLauDai = idLauDai
        self.idCauHoi = idCauHoi
    
    def getQuestion(self):
        return self.idCauHoi

