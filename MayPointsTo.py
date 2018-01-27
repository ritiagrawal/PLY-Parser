class MayPointsTo():
	def computeKill(self,cfg):
		return 0

	def computeAin(self,cfg):
		return 0

	def computeDef(self,cfg,i):
		if(cfg[i].leftLevel==0):
			return cfg[i].leftVar
		else:
			pointee=cfg[i].leftVar
			temp=""
			for j in range (0,cfg[i].leftLevel):
				for p,v in cfg[i].ain:
					if(p==pointee):
						temp=v
						if(v not in cfg[i].definition and j==cfg[i].leftLevel-1):
							cfg[i].definition.append(v)
				pointee=temp
						
			print(cfg[i].definition)
		 
		return 0

	def computePointee(self,cfg):
		return 0
	
	def computeAout(self,cfg):
		return 0

	def FlowAnalysis(self,cfg):
		change=True
		while(change):
			change=False
			for i in range(0,len(cfg)):
				#cfg[i].ain=self.computeAin(cfg)
				self.computeDef(cfg,i)
				cfg[i].kill=self.computeKill(cfg)
				cfg[i].pointee=self.computePointee(cfg)
				cfg[i].aoutprev=cfg[i].aout
				cfg[i].aout=self.computeAout(cfg)
				if(cfg[i].aout!= cfg[i].aoutprev):
					change=True


	def __init__(self,symbolTable,cfg):
		self.Relation=[('x','b'),('z','?'),('y','a'),('c','?'),('a','c')]
		for i in range(0,len(cfg)):
			cfg[i].aout=None
			cfg[i].aoutprev=None
		#for i in range (0,len(symbolTable)):
		#	if(symbolTable[i].level>=1):
		#		self.Relation.append((symbolTable[i].var,'?'))
		cfg[0].aout=self.Relation
		cfg[1].ain=cfg[0].aout
		print(self.Relation)
		self.FlowAnalysis(cfg)



			

