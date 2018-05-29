import string
import re
class pointer():				#format of the pointer part in Pointer=pointee statement
	def __init__(self,variable, field):
		self.variable=variable
		self.field=field

class pointee():				#format of the pointee part in pointer=pointee statement
	def __init__(self,variable):
		self.variable=variable

class MayPointsTo():
	def computeKill(self,cfg,i):		
		present_flag=0
		if(cfg[i].leftLevel==0):			#if LHS is not pointer variable 
			for (p,v) in cfg[i].ain:
				present_flag=0				#present_flag set if the pair to be killed already exist in the kill array
				if(p.variable==cfg[i].leftVar):
					for j in (cfg[i].kill):
						if(((cfg[i].leftVar) != j[0].variable) and (cfg[i].leftField != j[0].field) and (v != j[1])):	#check if the pair exist in kill
							pass					
						else:
							present_flag=1
							break
					if(present_flag!=1):			#if the pair doesn't exist add the pair in kill array
						pointerVar=pointer(cfg[i].leftVar,cfg[i].leftField)
						pointeeVar=pointee(v.variable)
						cfg[i].kill.append((pointerVar,pointeeVar))
						present_flag=0
		else:				#if the LHS is a pointer variable
			count=0
			temp_pointee=cfg[i].leftVar
			temp_field= cfg[i].leftField
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
								if(p2.variable==temp and p2.field==temp_field):
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
			temp_field=cfg[i].rightField
			temp=""
			for j in range (0,cfg[i].rightLevel+1):
				for (p,v) in cfg[i].ain:
					if(p.variable==temp_pointee):
						temp=v.variable
						if(j==cfg[i].rightLevel):
							if(temp_field==p.field):
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
				k=0
				j=0
				for k in range(0, len(self.symbolTable)):
					if(((p.variable , p.field)) == self.symbolTable[k][0]):						
						break						
				for j in range(0, len(self.symbolTable)):
					if(((v.variable , '*')) == self.symbolTable[j][0]):
						break
				if(self.symbolTable[k][2] == self.symbolTable[j][2] and self.symbolTable[k][1] == self.symbolTable[j][1]+1):
					cfg[i].aout.append((p,v))
				else:
					print("Type mismatch error")
		return 0

	def FlowAnalysis(self,cfg):			
		change=True
		statement_check=""
		while(change):
			change=False
			for i in range(0,len(cfg)):
				self.computeAin(cfg,i)
				if(i!=0 and i!= len(cfg)-1):
					statement_check=cfg[i].data    #check if the statement is use or return 
					if((re.search('^use',statement_check) or re.search('^return',statement_check))):
						cfg[i].definition=[]
						cfg[i].kill=[]
						cfg[i].pointee=[]
					else:				#if statement is neither use nor return compute def,kill and pointee
						self.computeDef(cfg,i)
						self.computeKill(cfg,i)
						self.computePointee(cfg,i)
							
				cfg[i].aoutprev=cfg[i].aout
				self.computeAout(cfg,i)
				if(cfg[i].aout!= cfg[i].aoutprev):		#check if aout has changed
					change=True
		if(self.debugLevel=='1'):					#aout of the final block
			print("\n\nMay point-to analysis")
			print("Aout:",end=" ")
			i=cfg[len(cfg)-1]
			for j in range (0,len(i.aout)):
				print("((",i.aout[j][0].variable,",",i.aout[j][0].field,"),",i.aout[j][1].variable,")  ",end="")
			print("\n\n")
			
		elif(self.debugLevel=='2'):				#cfg and ain and aout of every block
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
			

		elif(self.debugLevel=='3'): 		#cfg and ain,kill,def,pointee,cout of every block
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
					print(i.pointee[j].variable,end="")

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
		self.pointer=""
		self.pointee=""
		self.symbolTable=symbolTable
		for i in range(0,len(cfg)):			#initialize ain and aout
			cfg[i].aout=None
			cfg[i].aoutprev=None
		for i in range (0,len(symbolTable)):	#initialize all pointer variables with ? and store in ain and aout of start block
			if(symbolTable[i][1]>=1):			
				self.pointer=pointer(symbolTable[i][0][0],symbolTable[i][0][1])
				self.pointee=pointee('?')
				cfg[0].ain.append((self.pointer,self.pointee))
		cfg[0].aout=cfg[0].ain
		print("\nStart Relation is : ")
		for i in range (0,len(cfg[0].ain)):		#display the initial ain and aout 
			print("((",cfg[0].ain[i][0].variable,",",cfg[0].ain[i][0].field,"),",cfg[0].ain[i][1].variable,")  ",end="")
		
		self.FlowAnalysis(cfg)