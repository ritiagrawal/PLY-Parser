class tree_traversal():
	def ppointer_var_traversal(self,ppointer_variable):
		#print("going in funct")
		self.pointers ='*'
		while(ppointer_variable):
			try:
				pointer_variable = ppointer_variable.pointer_variable_obj.variable_obj.name
				#print(self.pointers,pointer_variable)
				if self.flag_p==0:
					self.variables = self.variables + '%s' %self.pointers + '%s' %pointer_variable 
				else:
					self.statement = self.statement + '%s' %self.pointers + '%s' %pointer_variable 
			except:
				pass
			try:
				ppointer_variable = ppointer_variable.ppointer_variable_obj
				self.pointers ='*%s' %self.pointers
			except:
				break

	def def_parameters_traversal(self, def_parameters):
		while(def_parameters):
			try:
				self.ppointer_var_traversal(def_parameters.ppointer_variable_obj)
			except:
				pass
			try:
				def_parameters=def_parameters.def_parameter_list_obj.def_parameters_obj	
			except:
				break
	

	def expression_term_traversal(self, expression_term):
		try:
			variable = expression_term.variable_obj.name 
			self.statement = self.statement + variable
		except:
			pass
		try:
			self.ppointer_var_traversal(expression_term.ppointer_variable_obj)
		except:
			pass
		try:
			addr_var=expression_term.addr_variable_obj.variable_obj.name
			self.statement = self.statement + " & %s" %addr_var
			
		except:
			pass
		try:
			constant= expression_term.constant_obj.num
			self.statement = self.statement + " %s" %constant
		
		except:
			pass
		
	def label_traversal(self,label_obj):
		label = "<bb "+ str(label_obj.num )+">:"
		self.statement = self.statement + " %s" %label
	
	def statement_traversal(self, statement):
		try:
			self.statement=self.statement + "\n"
			assignment_statement= statement.assignment_statement_obj
			try:
				expression_term=assignment_statement.expression_term_obj
				self.expression_term_traversal(expression_term)
				self.statement = "%s = " %self.statement
			except:
				pass
			try:
				
				arithmetic_term=assignment_statement.arithmetic_term_obj
				while(arithmetic_term):
					try:
						expression_term_obj = arithmetic_term.expression_term_obj
						self.expression_term_traversal(expression_term_obj)
					except:
						pass
			
					try:
						arithmetic_term = arithmetic_term.arithmetic_term_obj1 
						flag=1
					except:
						break

				arithmetic_term=assignment_statement.arithmetic_term_obj

				while(arithmetic_term and flag):
					try:
						expression_term = arithmetic_term.expression_term_obj
						self.expression_term_traversal(expression_term)
					except:
						pass
			
					try:
						self.statement = self.statement + " %s" %arithmetic_term.bin_op
						arithmetic_term = arithmetic_term.arithmetic_term_obj2
					except:
						flag=0
						break
			except:
				#print(self.statement)
				pass

		except:
			pass
		try:
			cond_goto=statement.cond_goto_obj
			if_goto = cond_goto.if_goto_obj
			self.statement = self.statement + str("if ()\n")
			self.label_traversal(if_goto.label_obj)
		except:
			pass
		try:
			uncond_goto=statement.uncond_goto_obj
			self.label_traversal(uncond_goto.label_obj)
		except:
			pass
		try:
			label=statement.label_obj
			self.label_traversal(label)
		except:
			pass
		try:
			use=statement.use_obj
			self.statement = self.statement + str("use(")
			self.ppointer_var_traversal(use.ppointer_var_obj)
			self.statement = self.statement + str(")")
		except:
			pass
		try:
			call_procedure_name=statement.procedure_call_obj.name
			self.statement = self.statement + "%s" %call_procedure_name+str("(")
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
			try:
				ex_statement_list = ex_statement_list.ex_statement_list_obj
			except:
				pass

	def var_decl_traversal(self,tree):
		variable_declarations=tree.variable_declarations_obj	
		variable_declaration_list=variable_declarations.variable_declaration_list_obj
		while(variable_declaration_list):
			self.variables='\nvar '
			var_list=variable_declaration_list.variable_declaration_obj
			while(var_list):
				self.pointers='*'
				try:
					ppointer_variable = var_list.ppointer_variable_obj
					self.ppointer_var_traversal(ppointer_variable)
				except:
					pass
					
				try:
					self.variables = self.variables + var_list.variable_obj.name						
				except:
					pass

				try:	
					var_list=var_list.var_list_obj
					self.variables=self.variables + ' '
				except:
					break					

				
			try:
				print(self.variables)
				variable_declaration_list=variable_declaration_list.variable_declaration_list_obj	
			except:
				break
		
	def procedure_def_traversal(self,tree):
		procedure_defination_list = tree.procedure_defination_list_obj
		while(procedure_defination_list):
			try:
				procedure_defination = procedure_defination_list.procedure_defination_obj
				self.statement=self.statement +"%s" %procedure_defination.name
				self.statement=self.statement + str("(")
			except:
				print("EXCEPT 1")
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
				print("EXCEPT 2")
				pass
			try:
				print(self.statement)
				print ("}\n")
				self.statement=""
				procedure_defination_list=procedure_defination_list.procedure_defination_list_obj
			except:
				print("EXCEPT 3")
				break
		

	def __init__(self,tree):
		self.pointers='*'
		self.variables='\nvar'
		self.statement=""
		self.flag_p=0
		self.var_decl_traversal(tree)
		self.flag_p=1
		self.procedure_def_traversal(tree)
