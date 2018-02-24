import string

class MayPointsTo():
	def computeKill(self,cfg,i):
		if(cfg[i].leftLevel==0):
			for p,v in cfg[i].ain:
				if(p==cfg[i].leftVar):
					if((cfg[i].leftVar,v) not in cfg[i].kill):
						cfg[i].kill.append((cfg[i].leftVar,v))
		else:
			count=0
			pointee=cfg[i].leftVar
			temp=""
			for j in range (0,cfg[i].leftLevel):
				count=0
				for p,v in cfg[i].ain:
					if(p==pointee):
						temp=v
						if(j==cfg[i].leftLevel-1):
							for p,v in cfg[i].ain:
								if(p==temp):
									p1=p
									v1=v
									count=count+1
							if(count==1):
								if((p1,v1) not in cfg[i].kill):
									cfg[i].kill.append((p1,v1))
				pointee=temp
			
						
						

	def computeAin(self,cfg,i):
		if(i>=1):
			for j in (cfg[i].pred):
				for (p,v) in cfg[j].aout:
					if((p,v) not in cfg[i].ain):
						cfg[i].ain.append((p,v))
			
	def computeDef(self,cfg,i):
		
		if(cfg[i].rightVar==None):
			pass
		else:
			if(cfg[i].leftLevel==0):
				if(cfg[i].leftVar not in cfg[i].definition):	
					cfg[i].definition.append(cfg[i].leftVar)
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
		 

	def computePointee(self,cfg,i):
		if(cfg[i].rightLevel==-1):
			if(cfg[i].rightVar not in cfg[i].pointee):
				cfg[i].pointee.append(cfg[i].rightVar)
		else:
			pointee=cfg[i].rightVar
			temp=""
			for j in range (0,cfg[i].rightLevel+1):
				for p,v in cfg[i].ain:
					if(p==pointee):
						temp=v
						if(v not in cfg[i].pointee and j==cfg[i].rightLevel):
							cfg[i].pointee.append(v)
				pointee=temp

	
	def computeAout(self,cfg,i):
		cfg[i].aout=[]
		for (a,b) in cfg[i].ain:
			cfg[i].aout.append((a,b))
		for p,v in cfg[i].kill:
			if( (p,v) in cfg[i].aout):
				cfg[i].aout.remove((p,v))
		for p in cfg[i].definition:
			for v in cfg[i].pointee:
				cfg[i].aout.append((p,v))
			
		return 0

	def FlowAnalysis(self,cfg):
		change=True
		while(change):
			change=False
			for i in range(0,len(cfg)):
				self.computeAin(cfg,i)
				self.computeDef(cfg,i)
				self.computeKill(cfg,i)
				self.computePointee(cfg,i)
				cfg[i].aoutprev=cfg[i].aout
				self.computeAout(cfg,i)
				if(cfg[i].aout!= cfg[i].aoutprev):
					change=True
		if(self.debugLevel=='1'):
			print("\n\nMay point-to analysis")
			print("Aout:",end=" ")
			i=cfg[len(cfg)-1]
			for j in range (0,len(i.aout)):
				print("(",i.aout[j][0],",",i.aout[j][1],")  ",end="")
			print("\n\n")
			
		elif(self.debugLevel=='2'):
			print("\n\nMay point-to analysis")
			for i in cfg:
				print("******  At block no. ",i.label,"*********")
				print("Ain:")
				j=0
				for j in range (0,len(i.ain)):
					print("(",i.ain[j][0],",",i.ain[j][1],")  ",end="")

				print("\nAout:")
				for j in range (0,len(i.aout)):
					print("(",i.aout[j][0],",",i.aout[j][1],")  ",end="")
				print("\n\n")
			

		elif(self.debugLevel=='3'):
			print("\n\nMay point-to analysis")
			for i in cfg:
				print("******  At block no. ",i.label,"*********")
				print("Ain:")
				j=0
				for j in range (0,len(i.ain)):
					print("(",i.ain[j][0],",",i.ain[j][1],")  ",end="")

				print ("\n\nDef:",*i.definition,sep='    ')

				print ("\nPointee:",*i.pointee,sep='    ')

				print ("\nKill:")
				for j in range (0,len(i.kill)):
					print("(",i.kill[j][0],",",i.kill[j][1],")  ",end="")

				print("\nAout:")
				for j in range (0,len(i.aout)):
					print("(",i.aout[j][0],",",i.aout[j][1],")  ",end="")
				print("\n\n")
				print("\n\n")


	def __init__(self,symbolTable,cfg,debugLevel):
		self.debugLevel=debugLevel
		self.Relation=[]
		for i in range(0,len(cfg)):
			cfg[i].aout=None
			cfg[i].aoutprev=None
		for i in range (0,len(symbolTable)):
			if(symbolTable[i].level>=1):
				self.Relation.append((symbolTable[i].var,'?'))
				cfg[0].ain.append((symbolTable[i].var,'?'))
		cfg[0].aout=self.Relation
		print("\nStart Relation is : ")
		for i in range (0,len(self.Relation)):
			print("(",self.Relation[i][0],",",self.Relation[i][1],")  ",end="")
		#print("(",self.Relation[i][0],",",self.Relation[i][1],")",end="")
		

		self.FlowAnalysis(cfg)



			

