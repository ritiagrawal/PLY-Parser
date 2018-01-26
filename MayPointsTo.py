class MayPointsTo():
	def __init__(self,symbolTable,cfg):
		self.Relation=[]
		self.cfg=cfg
		for i in range(0,len(self.cfg)):
			self.cfg[i].aout=None
			self.cfg[i].aoutprev=None
		for i in range (0,len(symbolTable)):
			if(symbolTable[i].level>=1):
				self.Relation.append((symbolTable[i].var,'?'))
		print(self.Relation)

	def FlowAnalysis():
		change=True
		while(change):
			change=False
			for i in range(0,cfg):
				self.cfg[i].ain=computeAin()
				self.cfg[i].defination=computeDef(i)
				self.cfg[i].kill=computeKill()
				self.cfg[i].pointee=computePointee()
				self.cfg[i].aoutprev=self.cfg[i].aout
				self.cfg[i].aout=computeAout()
				if(self.cfg[i].aout!= self.cfg[i].aoutprev):
					change=True

	def computekill():
		return 0

	def computeAin():
		return 0

	def computeDef(self,i):
		print(";;;;;;;;;;;;;;;;;;;",cfg[i].data)
		return 0

	def computePointee():
		return 0
	
	def computeAout():
		return 0


			

