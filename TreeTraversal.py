import importlib

class node:										#node for CFG
	def __init__(self,label,data,pred,succ):
		self.label=label
		self.leftLevel=0
		self.leftField='*'
		self.rightField='*'
		self.rightLevel=0
		self.leftVar=None
		self.rightVar=None
		self.data=data
		self.pred=list()
		self.succ=list()
		self.predecessor=list()
		self.successor=list()
		self.ain=[]
		self.aout=[]
		self.aoutprev=[]
		self.definition=list()
		self.kill=list()
		self.pointee=list()

class block:									#block node to save each block data
	def __init__(self,num,start,end):
		self.number=num
		self.start=start
		self.end=end
		
global labels									#represents total nodes in CFG at a given point in program
labels=0

arr=list()										#to store all the nodes of CFG
bbArray=list()									#to store all block nodes
	
Head=node(0,0,None, None)						#start node
arr.append(Head)

class tree_traversal():
	def ppointer_var_traversal(self,ppointer_variable):			#for traversal of pointer variables
		self.pointers ='*'
		while(ppointer_variable):
			try:
				pointer_variable = ppointer_variable.pointer_variable_obj.variable_obj.name
				if self.flag_p==0:									#if pointer variable appears in var declaration
					self.variables = self.variables + '%s' %self.pointers + '%s' %pointer_variable 
					if(self.struct_flag==0):						#if var is not a structure var
						self.symbolTable1.append(((pointer_variable,'*'),len(self.pointers),"var"))
					else:										#if struct var then add the var as obj or field of struct
						if(self.object_flag==0):				
							self.fields.append((pointer_variable,len(self.pointers)))
						else:
							self.objects.append((pointer_variable,len(self.pointers)))
						
				else:								#if pointer variable in statement
					self.statement = self.statement + '%s' %self.pointers + '%s' %pointer_variable 
					if(self.onestmt == "" or self.use_flag==1):			
						self.onestmt = self.onestmt + '%s' %self.pointers + '%s' %pointer_variable	#one_stmt represents current single statement
						self.leftVar=pointer_variable
						self.leftLevel=len(self.pointers)
						self.rightField='*'
						self.leftField='*'
						self.o_flag=1							#o_flag to represent one_stmt is not empty
					elif(self.onestmt != "" and (self.o_flag==1 or self.return_flag==0)):		#o_flag to represent the current onestmt
						self.onestmt = self.onestmt + '%s' %self.pointers + '%s' %pointer_variable
						self.rightVar=pointer_variable
						self.rightLevel=len(self.pointers)
						global labels
						labels=labels+1
						if(self.TreePass==1):		#if first tree traversal pass then create and store the cfg node	
							self.return_flag=1
							node1=node(labels,self.onestmt,(), ())
							node1.leftLevel=self.leftLevel
							node1.leftVar=self.leftVar
							node1.rightLevel=self.rightLevel
							node1.rightVar=self.rightVar
							node1.rightField=self.rightField
							node1.leftField=self.leftField
							arr.append(node1)
							self.rightField='*'
							self.leftField='*'
							self.onestmt = self.onestmt + '\ngoto <%s>' %(labels+1)+ '\n%s :' %(labels+1)
						else:						#else restore the data and allocate predecessor and successor
							if(self.goto_flag!=1):
								if(self.skip!=1):
									if(arr[self.current].label not in arr[labels].pred):
										arr[labels].pred.append(arr[self.current].label)
										arr[labels].predecessor.append(arr[self.current])
									if(arr[labels].label not in arr[self.current].succ):	
										arr[self.current].succ.append(arr[labels].label)
										arr[self.current].successor.append(arr[labels])
								self.skip=0
								self.current+=1
						self.onestmt=""
						self.o_flag=0

			except:
				pass
			try:				#for multiple pointer variables
				ppointer_variable = ppointer_variable.ppointer_variable_obj
				self.pointers ='*%s' %self.pointers
				
			except:
				break

	def def_parameters_traversal(self, def_parameters):				#to traverse parameters of the function
		while(def_parameters):
			try:
				self.ppointer_var_traversal(def_parameters.ppointer_variable_obj)
			except:
				pass
			try:													#for multiple parameters
				def_parameters=def_parameters.def_parameter_list_obj.def_parameters_obj	
			except:
				break
	

	def expression_term_traversal(self, expression_term):		#to traverse expression terms in the statements 
		global labels
		try:													#for struct variable as expression term
			variable_pointer = expression_term.variable_pointer_obj.name
			variable_field = expression_term.variable_field_obj.name
			self.statement = self.statement + variable_pointer + '-' + '>'+variable_field
			if(self.onestmt == ""):							#if struct var is on LHS
				self.onestmt = self.onestmt + variable_pointer
				self.leftVar=self.onestmt
				self.onestmt = self.onestmt + '-' + '>'
				self.leftLevel=1
				self.o_flag=1
				self.leftField=variable_field
				self.onestmt = self.onestmt + self.leftField
			elif(self.onestmt != "" and self.o_flag==1):	#else if struct var is on RHS
				self.onestmt = self.onestmt + variable_pointer
				self.rightVar=variable_pointer
				self.onestmt = self.onestmt + '-' + '>'
				self.rightLevel=1
				self.rightField=variable_field
				self.onestmt = self.onestmt + self.rightField				
				global labels
				labels=labels+1
				if(self.TreePass==1):				#if first tree traversal pass then create and store the cfg node	
					node1=node(labels,self.onestmt,(),())
					node1.leftVar=self.leftVar
					node1.rightVar=self.rightVar
					node1.leftLevel=self.leftLevel
					node1.rightLevel=self.rightLevel
					node1.rightField=self.rightField
					node1.leftField=self.leftField
					arr.append(node1)
					self.rightField='*'
					self.leftField='*'
					self.onestmt = self.onestmt + '\ngoto <%s>' %(labels+1)+ '\n%s :' %(labels+1)
				else:
					if(self.goto_flag!=1):
						if(self.skip!=1):				#skip is used to skip the statement after unconditional goto
							if(arr[self.current].label not in arr[labels].pred):
								arr[labels].pred.append(arr[self.current].label)
								arr[labels].predecessor.append(arr[self.current])
							if(arr[labels].label not in arr[self.current].succ):
								arr[self.current].succ.append(arr[labels].label)
								arr[self.current].successor.append(arr[labels])
						self.skip=0
						self.current+=1
				self.onestmt=""
				self.o_flag=0
			

		except:
			pass
		try:													#variable as expression term
			variable = expression_term.variable_obj.name 
			self.statement = self.statement + variable
			if(self.onestmt == ""):								#on LHS of statement
				self.onestmt = self.onestmt + variable
				self.leftVar=self.onestmt
				self.leftLevel=0
				self.o_flag=1
				self.rightField='*'
				self.leftField='*'

			elif(self.onestmt != "" and self.o_flag==1):		#on RHS of the statement
				self.onestmt = self.onestmt + variable
				self.rightVar=variable
				self.rightLevel=0
				labels=labels+1
				if(self.TreePass==1):			#if first tree traversal pass then create and store the cfg node	
					node1=node(labels,self.onestmt,(),())
					node1.leftVar=self.leftVar
					node1.rightVar=self.rightVar
					node1.leftLevel=self.leftLevel
					node1.rightLevel=self.rightLevel
					node1.rightField=self.rightField
					node1.leftField=self.leftField
					arr.append(node1)
					self.rightField='*'
					self.leftField='*'
					self.onestmt = self.onestmt + '\ngoto <%s>' %(labels+1)+ '\n%s :' %(labels+1)
				else:
					if(self.goto_flag!=1):
						if(self.skip!=1):				#skip is used to skip the statement after unconditional goto
							if(arr[self.current].label not in arr[labels].pred):
								arr[labels].pred.append(arr[self.current].label)
								arr[labels].predecessor.append(arr[self.current])
							if(arr[labels].label not in arr[self.current].succ):
								arr[self.current].succ.append(arr[labels].label)
								arr[self.current].successor.append(arr[labels])
						self.skip=0
						self.current+=1
				self.onestmt=""
				self.o_flag=0
				
		except:
			pass
		try:									#pointer variable as expression term
			self.ppointer_var_traversal(expression_term.ppointer_variable_obj)
		except:
			pass
		try:									#address variable as expression term
			addr_var=expression_term.addr_variable_obj.variable_obj.name
			self.statement = self.statement + " & %s" %addr_var
			self.onestmt=self.onestmt+" & %s" %addr_var
			self.rightVar=addr_var
			self.rightLevel=-1
			labels=labels+1
			if(self.TreePass==1):
				node1=node(labels,self.onestmt,(), ())		#first tree pass create node with data but empty predecessor and successor			
				node1.rightLevel=-1
				node1.leftVar=self.leftVar
				node1.leftLevel=self.leftLevel
				node1.rightVar=self.rightVar
				node1.rightLevel=self.rightLevel
				node1.rightField=self.rightField
				node1.leftField=self.leftField
				arr.append(node1)
				self.rightField='*'
				self.leftField='*'
				self.onestmt = self.onestmt + '\ngoto <%s>' %(labels+1)+ '\n%s :' %(labels+1)
			else:
				if(self.goto_flag!=1):					#if prev statement is not a goto statement
					if(self.skip!=1):					
						if(arr[self.current].label not in arr[labels].pred):
							arr[labels].pred.append(arr[self.current].label)
							arr[labels].predecessor.append(arr[self.current])
						if(arr[labels].label not in arr[self.current].succ):
							arr[self.current].succ.append(arr[labels].label)
							arr[self.current].successor.append(arr[labels])
					self.skip=0
					self.current+=1
			self.onestmt=""
		except:
			pass
		try:									#constant as expression term
			constant= expression_term.constant_obj.num
			self.statement = self.statement + " %s" %constant
		
		except:
			pass
		
		
	def label_traversal(self,label_obj):						#to traverse blocks 
		label = "<bb "+ str(label_obj.num)+">:"
		self.statement = self.statement + " %s" %label
		if(self.TreePass!=1 and self.bb_skip!=1):				#in 2nd tree traversal assign the predecessor and successor
			if(arr[bbArray[label_obj.num-1].start].label not in arr[self.current].succ):
				arr[self.current].succ.append(arr[bbArray[label_obj.num-1].start].label)
				arr[self.current].successor.append(arr[bbArray[label_obj.num-1].start])
			if(arr[self.current].label not in arr[bbArray[label_obj.num-1].start].pred):
				arr[bbArray[label_obj.num-1].start].predecessor.append(arr[self.current])
				arr[bbArray[label_obj.num-1].start].pred.append(arr[self.current].label)
			self.goto_flag=0
		self.bb_skip=0
			
	
	def statement_traversal(self, statement):
		self.use_flag=0	
		global labels
		try:							#to traverse the assignment statements
			global labels
			self.statement=self.statement + "\n"
			assignment_statement= statement.assignment_statement_obj
			try:						#expression term in the statement
				expression_term=assignment_statement.expression_term_obj
				self.expression_term_traversal(expression_term)
				self.statement = "%s = " %self.statement
				self.onestmt= "%s = " %self.onestmt
			except:
				pass
			try:						#arithmetic statement
				arithmetic_term=assignment_statement.arithmetic_term_obj
				while(arithmetic_term):
					try:				#expression term in the arithmetic statement
						expression_term_obj = arithmetic_term.expression_term_obj
						self.expression_term_traversal(expression_term_obj)
					except:
						pass
			
					try:				#2nd expression term in the binary operation of arithmetic statement
						arithmetic_term = arithmetic_term.arithmetic_term_obj1 
						binary_flag=1		#to represent binary arithmetic statement	
					except:
						break

				arithmetic_term=assignment_statement.arithmetic_term_obj

				while(arithmetic_term and binary_flag):
					try:
						expression_term = arithmetic_term.expression_term_obj
						self.expression_term_traversal(expression_term)		
					except:
						pass
			
					try:
						self.statement = self.statement + " %s" %arithmetic_term.bin_op
						arithmetic_term = arithmetic_term.arithmetic_term_obj2
					except:
						binary_flag=0
						break
			except:
				pass

		except:
			pass
		try:							#to traverse the conditional goto statements
			cond_goto=statement.cond_goto_obj
			if_goto = cond_goto.if_goto_obj
			self.statement = self.statement + str("if ()\n")
			self.goto_flag=1
			self.statement = self.statement + str("goto")
			self.label_traversal(if_goto.label_obj)
		except:
			pass
		try:							#to traverse the unconditional goto statements
			uncond_goto=statement.uncond_goto_obj
			self.skip=1
			self.statement = self.statement + str("goto")
			self.label_traversal(uncond_goto.label_obj)
		except:
			pass
		try:						#to traverse block labels
			global labels
			label=statement.label_obj
			self.bb_skip=1
			self.label_traversal(label)
			if(self.TreePass==1):
				if(len(bbArray)!=0):
					bbArray[len(bbArray)-1].end=labels
					
				bb=block(label.num,labels+1,-1)
				bbArray.append(bb)
		except:
			pass
		try:						#to traverse use statements
			
			use=statement.use_obj
			self.statement = self.statement + str("use(")
			self.onestmt = str("use(")
			self.goto_flag=0
			self.use_flag=1;
			self.ppointer_var_traversal(use.ppointer_var_obj)
			self.onestmt = self.onestmt + str(")")
			self.statement = self.statement + str(")")
			labels = labels+1
			if(self.TreePass==1):
				node1= node(labels,self.onestmt,(), ())
				node1.leftVar=self.leftVar
				node1.leftLevel=self.leftLevel
				arr.append(node1)
				self.onestmt = self.onestmt + '\ngoto <%s>' %(labels+1)+ '\n%s :' %(labels+1)
			else:
				if(self.goto_flag!=1):
					if(self.skip!=1):				
						if(arr[self.current].label not in arr[labels].pred):
							arr[labels].pred.append(arr[self.current].label)
							arr[labels].predecessor.append(arr[self.current])
						if(arr[labels].label not in arr[self.current].succ):	
							arr[self.current].succ.append(arr[labels].label)
							arr[self.current].successor.append(arr[labels])
					self.skip=0
					self.current+=1
			self.onestmt=""
			self.o_flag=0
		except:
			pass
		try:				#to traverse procedure calls
			call_procedure_name=statement.procedure_call_obj.name
			self.statement = self.statement + "%s" %call_procedure_name+str("(")
			self.goto_flag=1
			try:
				call_parameters=statement.procedure_call_obj.call_parameters_obj
				while(call_parameters):
					self.ppointer_var_traversal(call_parameters.ppointer_variable_obj)
					call_parameters=call_parameters.call_parameter_list_obj.call_parameters_obj
					self.statement = self.statement + str(",")
				self.statement = self.statement + str(")")
			except:
				self.statement = self.statement + str(")")
		except:
			pass

	def ex_statement_list_traversal(self,ex_statement_list):
		while(ex_statement_list):
			try:
				statement=ex_statement_list.statement_obj
				self.statement_traversal(statement)
			except:
				pass
			try:							#for multiple statements
				ex_statement_list = ex_statement_list.ex_statement_list_obj
			except:
				pass

	def var_decl_traversal(self,tree):				#to traverse variable declarations
		variable_declarations=tree.variable_declarations_obj	
		variable_declaration_list=variable_declarations.variable_declaration_list_obj
		while(variable_declaration_list):
			try:									#var variable declaration
				var_list=variable_declaration_list.variable_declaration_obj.var_list_obj
				self.variables=self.variables +'\nvar '
				while(var_list):					
					self.pointers='*'
					try:							#pointer variables
						ppointer_variable = var_list.ppointer_variable_obj
						self.ppointer_var_traversal(ppointer_variable)
					except:
						pass
					
					try:													
						self.variables = self.variables + var_list.variable_obj.name	
						self.symbolTable1.append(((var_list.variable_obj.name,'*'),0,"var"))					
					except:
						pass

					try:							#for multiple vars in single var declaration statement 
						var_list=var_list.var_list_obj
						self.variables=self.variables + ' '
					except:
						break					
			except:
				pass
			try:						#structure variable declaration
				structure_declaration=variable_declaration_list.variable_declaration_obj.structure_declaration_obj
				self.variables= self.variables +'\nstruct '
				self.struct_flag=1
				self.variables = self.variables + structure_declaration.variable_obj.name
				self.variables = self.variables + '{\n' 
				variable_declaration_list_structure=structure_declaration.variable_declaration_list_obj		#variable as fields
				while(variable_declaration_list_structure):
					try:
						self.variables = self.variables + '\nvar '
						var_list=variable_declaration_list_structure.variable_declaration_obj
						while(var_list):
							self.pointers='*'
							try:
								ppointer_variable = var_list.ppointer_variable_obj
								self.ppointer_var_traversal(ppointer_variable)
							except:
								pass
				
							try:
								self.variables = self.variables + var_list.variable_obj.name	
								self.fields.append((var_list.variable_obj.name,0))					
							except:
								pass

							try:	
								var_list=var_list.var_list_obj
								self.variables=self.variables + ' '
							except:
								break					
					except:
						pass
							
					
					try:				#for multiple variable declaration statements as fields on structure
						variable_declaration_list_structure=variable_declaration_list_structure.variable_declaration_list_obj	
					except:
						break
				self.variables = self.variables + '\n}' 
				var_list=structure_declaration.struct_obj	#structure objects
				self.object_flag=1
				while(var_list):
					self.pointers='*'
					try:
						ppointer_variable = var_list.ppointer_variable_obj
						self.ppointer_var_traversal(ppointer_variable)
					except:
						pass
		
					try:	
						self.variables = self.variables + var_list.variable_obj.name			
						self.objects.append((var_list.variable_obj.name,0))		#store the objs of structure in objects
					
					except:
						pass

					try:	
						var_list=var_list.var_list_obj
						self.variables=self.variables + ' '
					except:
						break					
				self.variables = self.variables + ';\n'
				self.object_flag=0
				self.struct_flag=0 
				
				for o in self.objects:			#make an entry on symbol table with all objs and fields
					for f in self.fields:
						if(o[1]==0	):
							self.symbolTable1.append(((o[0],f[0]),o[1]+f[1],"var"))
					self.symbolTable1.append(((o[0],'*'),o[1],structure_declaration.variable_obj.name))
	
				self.fields=[]
				self.objects=[]
			except:
				pass
			

			try:
				variable_declaration_list=variable_declaration_list.variable_declaration_list_obj	
			 	
			except:
				break
		print(self.variables)
		
	def procedure_def_traversal(self,tree):			#to traverse the procedure
		global labels
		procedure_defination_list = tree.procedure_defination_list_obj
		while(procedure_defination_list):
			try:
				procedure_defination = procedure_defination_list.procedure_defination_obj
				self.statement=self.statement +"%s" %procedure_defination.name
				self.statement=self.statement + str("(")
			except:
				pass
			try:
				def_parameters = procedure_defination_list.procedure_defination_obj.def_parameters_obj
				self.def_parameters_traversal(def_parameters)
				self.statement = self.statement + str("){")
			except:
				pass
			try:
				ex_statement_list = procedure_defination_list.procedure_defination_obj.ex_statement_list_obj
				self.ex_statement_list_traversal(ex_statement_list)
			except:
				pass
			try:					#to traverse the return statements
				ret_statement=procedure_defination_list.procedure_defination_obj.return_stat_obj.ppointer_var_obj
				self.statement=self.statement+str("\nreturn ");
				self.onestmt=("return ")
				self.ppointer_var_traversal(ret_statement)
				
				if(self.TreePass==1):
					labels=labels+1
					if(self.return_flag==0):
						
						node1=node(labels,self.onestmt,(), ())
						arr.append(node1)
						self.onestmt = self.onestmt + '\ngoto <%s>' %(labels+1)+ '\n%s :' %(labels+1)
						
				else:

					if(self.goto_flag!=1):
						if(self.skip!=1):
							if(arr[self.current].label not in arr[labels].pred and arr[labels].label!=self.current):
												
								arr[labels].pred.append(arr[self.current].label)
								arr[labels].predecessor.append(arr[self.current])
								
							if(arr[labels].label not in arr[self.current].succ and arr[labels].label!=self.current):						
												
								arr[self.current].succ.append(arr[labels].label)
								arr[self.current].successor.append(arr[labels])
								
						self.skip=0
						self.current+=1
			except:
				pass
			try:
				ret_statement=procedure_defination_list.procedure_defination_obj.return_stat_obj.variable_obj.name
				self.statement=self.statement+str("\nreturn %s " %ret_statement)
				self.onestmt="return  %s" %ret_statement
				labels=labels+1
				
				if(self.TreePass==1):
					node1=node(labels,self.onestmt,(),())
					arr.append(node1)
					self.onestmt = self.onestmt + '\ngoto <%s>' %(labels+1)+ '\n%s :' %(labels+1)
				else:
					if(self.goto_flag!=1):
						if(self.skip!=1):
							if(arr[self.current].label not in arr[labels].pred):				
								arr[labels].pred.append(arr[self.current].label)
								arr[labels].predecessor.append(arr[self.current])
							if(arr[labels].label not in arr[self.current].succ):				
								arr[self.current].succ.append(arr[labels].label)
								arr[self.current].successor.append(arr[labels])
						self.skip=0
						self.current+=1
				self.onestmt=""
				
			except:
				pass
			try:
				ret_statement=procedure_defination_list.procedure_defination_obj.return_stat_obj.variable_obj.variable_obj.name
				self.statement=self.statement+str("\nreturn  &%s " %ret_statement)
				self.onestmt="return  &%s" %ret_statement
				labels=labels+1
				
				if(self.TreePass==1):
					
					node1=node(labels,self.onestmt,(), ())
					arr.append(node1)
					self.onestmt = self.onestmt + '\ngoto <%s>' %(labels+1)+ '\n%s :' %(labels+1)
				else:
					
					if(self.goto_flag!=1):
						if(self.skip!=1):
							if(arr[self.current].label not in arr[labels].pred):				
								arr[labels].pred.append(arr[self.current].label)
								arr[labels].predecessor.append(arr[self.current])
							if(arr[labels].label not in arr[self.current].succ):				
								arr[self.current].succ.append(arr[labels].label)
								arr[self.current].successor.append(arr[labels])
						self.skip=0
						self.current+=1
				self.onestmt=""				
			except:
				pass
			try:
				if(self.TreePass!=1):
					print("END OF TRAVERSAL")
				else:
					print(self.statement)
					print ("}\n")
				self.statement=""
				procedure_defination_list=procedure_defination_list.procedure_defination_list_obj
			except:
				break

	def __init__(self,tree,debugLevel,pta):
		global labels
		module = __import__(pta)		#to load the pta class
		self.symbolTable1=[]
		self.struct_flag=0
		self.fields=[]
		self.object_flag=0
		self.objects=[]
		self.lhs=0	
		self.rhs=0
		self.skip=0						#to skip the statement after unconditional goto
		self.bb_skip=0					#to represent block
		self.TreePass=1					#Tree traversal pass number
		self.pointers='*'
		self.leftVar=""
		self.rightVar=""
		self.leftLevel=""
		self.rightLevel=""
		self.variables='\n'			
		self.statement=""				#to store all the statements in a procedure		
		self.onestmt=""					#to store complete statement for CFG
		self.flag_p=0					#to represent traversal of variable declaration part		
		self.var_decl_traversal(tree)
		self.flag_p=1
		self.return_flag=0
		self.procedure_def_traversal(tree)
		self.TreePass+=1				#tree traversal 2
		labels=0
		self.return_flag=0
		self.current=0
		self.skip=0						#before starting new pass, skip should be initialized to 1
		self.goto_flag=0
		self.procedure_def_traversal(tree)
		endNode=node(labels+1,-1,None,None)			#End Node of CFG
		endNode.pred.append(labels)
		endNode.predecessor.append(arr[labels])
		arr[labels].succ.append(labels+1)
		arr[labels].successor.append(endNode)
		arr.append(endNode)
		print("------------SYMBOL TABLE-------------\n")
		print("Variable tuple","\t","Level","\t","Type")
		for i in range(0,len(self.symbolTable1)):
				print(self.symbolTable1[i][0],"\t",self.symbolTable1[i][1],"\t",self.symbolTable1[i][2])
		if(debugLevel!='1'):
			print("**CGF**")						#Printing CFG
			for label in range (len(arr)):
				print ("-------------------")
				print ("Current Label",arr[label].label)
				print ("DATA : ",arr[label].data)
				print ("Predeccesor Label",arr[label].pred)
				print ("Successor Label",arr[label].succ)
				print ("-------------------")
		self.o_flag=0
		ptaClass = getattr(module, pta)				#get instance of the class with whatever attributes the constructor needs
		ptaClass(self.symbolTable1,arr,debugLevel)	#call pta algorithm constructor