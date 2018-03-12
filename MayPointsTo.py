import string
import re
class pointer():
	def __init__(self,variable, field):
		self.variable=variable
		self.field=field

class pointee():
	def __init__(self,variable):
		self.variable=variable

class MayPointsTo():
	def computeKill(self,cfg,i):
		present_flag=0
		if(cfg[i].leftLevel==0):
			for (p,v) in cfg[i].ain:
				present_flag=0
				if(p.variable==cfg[i].leftVar):
					for j in (cfg[i].kill):
						if(((cfg[i].leftVar) != j[0].variable) and (cfg[i].leftField != j[0].field) and (v != j[1])):
							pass
						else:
							present_flag=1
							break
					if(present_flag!=1):
						pointerVar=pointer(cfg[i].leftVar,cfg[i].leftField)
						pointeeVar=pointee(v.variable)
						cfg[i].kill.append((pointerVar,pointeeVar))
						present_flag=0
		else:
			count=0
			temp_pointee=cfg[i].leftVar
			temp=""
			p1=pointer(None,None)
			v1=pointee(None)
			for j in range (0,cfg[i].leftLevel):
				count=0
				for (p,v) in cfg[i].ain:
					if(p.variable==temp_pointee):
						temp=v.variable
						if(j==cfg[i].leftLevel-1):
							for (p2,v2) in cfg[i].ain:
								if(p2.variable==temp):
									p1=p2
									v1=v2
									count=count+1
							if(count==1):
								if((p1,v1) not in cfg[i].kill):
									cfg[i].kill.append((p1,v1))
				temp_pointee=temp
			
						
						

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
				if(len(cfg[i].definition)==0):
					pointerVar=pointer(cfg[i].leftVar,cfg[i].leftField)
					cfg[i].definition.append(pointerVar)
				else:
					for defVar in cfg[i].definition:
						if(cfg[i].leftVar != defVar.variable and cfg[i].leftField != defVar.field):
							pointerVar=pointer(cfg[i].leftVar,cfg[i].leftField)
							cfg[i].definition.append(pointerVar)
			else:
				temp_pointer=cfg[i].leftVar
				temp=""
				for j in range (0,cfg[i].leftLevel):
					for (p,v) in cfg[i].ain:
						if(p.variable==temp_pointer):
							temp=v.variable
							if(j==cfg[i].leftLevel-1):
								if(len(cfg[i].definition)==0):
									pointerVar=pointer(v.variable,cfg[i].leftField)
									cfg[i].definition.append(pointerVar)
								else:
									for defVar in cfg[i].definition:
										if(v.variable != defVar.variable and cfg[i].leftField != defVar.field):
											pointerVar=pointer(v.variable,cfg[i].rightField)
											cfg[i].definition.append(pointerVar)
					temp_pointer=temp
					'''####
							print("=================",(v.variable,cfg[i].leftField),"\t\t",cfg[i].definition)
							if((v.variable,cfg[i].leftField) not in cfg[i].definition and j==cfg[i].leftLevel-1):
								pointerVar=pointer(v.variable,cfg[i].leftField)
								cfg[i].definition.append(pointerVar)'''

		 

	def computePointee(self,cfg,i):
		if(cfg[i].rightLevel == -1):
			if(len(cfg[i].pointee)==0):
				pointeeVar=pointee(cfg[i].rightVar)
				cfg[i].pointee.append(pointeeVar)
			else:
				for var in cfg[i].pointee:
					if(cfg[i].rightVar != var.variable):
						pointeeVar=pointee(cfg[i].rightVar)
						cfg[i].pointee.append(pointeeVar)
		else:
			temp_pointee=cfg[i].rightVar
			temp=""
			for j in range (0,cfg[i].rightLevel+1):
				for (p,v) in cfg[i].ain:
					if(p.variable==temp_pointee):
						temp=v.variable
						if(j==cfg[i].rightLevel):
							if (len(cfg[i].pointee) ==0):		
								pointeeVar=pointee(v.variable)
								cfg[i].pointee.append(pointeeVar)
							else:
								for var in cfg[i].pointee:
									if(v.variable != var.variable):
										pointeeVar=pointee(v.variable)
										cfg[i].pointee.append(pointeeVar)
				temp_pointee=temp

	
	def computeAout(self,cfg,i):
		cfg[i].aout=[]
		for (p,v) in cfg[i].ain:
			cfg[i].aout.append((p,v))
		for (p,v) in cfg[i].kill:
			for (p1,v1) in (cfg[i].aout):
				if((p.variable== p1.variable) and (p.field== p1.field) and (v.variable== v1.variable)):
					cfg[i].aout.remove((p1,v1))
		for p in cfg[i].definition:
			for v in cfg[i].pointee:
				cfg[i].aout.append((p,v))
			
		return 0

	def FlowAnalysis(self,cfg):
		change=True
		check=""
		while(change):
			change=False
			for i in range(0,len(cfg)):
				self.computeAin(cfg,i)
				if(i!=0 and i!= len(cfg)-1):
					check=cfg[i].data
					if((re.search('^use',check) or re.search('^return',check))):
						cfg[i].definition=[]
						cfg[i].kill=[]
						cfg[i].pointee=[]
					else:
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
				print("((",i.aout[j][0].variable,",",i.aout[j][0].field,"),",i.aout[j][1].variable,")  ",end="")
			print("\n\n")
			
		elif(self.debugLevel=='2'):
			print("\n\nMay point-to analysis")
			for i in cfg:
				print("******  At block no. ",i.label,"*********")
				print("Ain:")
				j=0
				for j in range (0,len(i.ain)):
					print("((",i.ain[j][0].variable,",",i.ain[j][0].field,"),",i.ain[j][1].variable,")  ",end="")

				print("\nAout:")
				for j in range (0,len(i.aout)):
					print("((",i.aout[j][0].variable,",",i.aout[j][0].field,"),",i.aout[j][1].variable,")  ",end="")
				print("\n\n")
			

		elif(self.debugLevel=='3'):
			print("\n\nMay point-to analysis")
			for i in cfg:
				print("******  At block no. ",i.label,"*********")
				print("Ain:")
				j=0
				for j in range (0,len(i.ain)):
					print("((",i.ain[j][0].variable,",",i.ain[j][0].field,"),",i.ain[j][1].variable,")  ",end="")

				print("\nDefinition")
				for j in range (0,len(i.definition)):
					print("(",i.definition[j].variable,",",i.definition[j].field,") ",end="")

				print ("\nPointee:")
				for j in range (0,len(i.pointee)):
					print(i.pointee[j].variable,",",end="")

				print ("\nKill:")
				for j in range (0,len(i.kill)):
					print("((",i.kill[j][0].variable,",",i.kill[j][0].field,"),",i.kill[j][1].variable,")  ",end="")

				print("\nAout:")
				for j in range (0,len(i.aout)):
					print("((",i.aout[j][0].variable,",",i.aout[j][0].field,"),",i.aout[j][1].variable,")  ",end="")
				print("\n\n")
				print("\n\n")


	def __init__(self,symbolTable,cfg,debugLevel):
		self.debugLevel=debugLevel
		self.Relation=[]
		self.pointer=""
		self.pointee=""
		for i in range(0,len(cfg)):
			cfg[i].aout=None
			cfg[i].aoutprev=None
			#for i in range(0,len(self.symbolTable1)):
			#	print(self.symbolTable1[i][0],"\t",self.symbolTable1[i][1])
		for i in range (0,len(symbolTable)):
			if(symbolTable[i][1]>=1):
				self.pointer=pointer(symbolTable[i][0][0],symbolTable[i][0][1])
				self.pointee=pointee('?')
				self.Relation.append((self.pointer,self.pointee))
				cfg[0].ain.append((self.pointer,self.pointee))
		cfg[0].aout=self.Relation
		print("\nStart Relation is : ")
		for i in range (0,len(self.Relation)):
			print("((",self.Relation[i][0].variable,",",self.Relation[i][0].field,"),",self.Relation[i][1].variable,")  ",end="")

		self.FlowAnalysis(cfg)

