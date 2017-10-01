class tree_traversal():
	def __init__(self,tree):
		#print(tree)	
		pointers='*'
		variable_declarations=tree.variable_declarations_obj
	
		variable_declaration_list=variable_declarations.variable_declaration_list_obj
		
		while(variable_declaration_list):
			print("var")
			var_list=variable_declaration_list.variable_declaration_obj.var_list_obj
			while(var_list):
				pointers='*'
				try:
					ppointer_variable = var_list.ppointer_variable_obj
					while(ppointer_variable):
						try:
							pointer_variable= ppointer_variable.pointer_variable_obj.variable_obj.name
							print(pointers,pointer_variable)
						except:
							pass
						try:
							ppointer_variable = ppointer_variable.ppointer_variable_obj
							pointers ='*%s'%pointers
						except:
							break
				except:
					pass
					
				try:
					print(var_list.variable_obj.name)						
				except:
					pass

				try:	
					var_list=var_list.var_list_obj
				except:
					break					

				
			try:
				variable_declaration_list=variable_declaration_list.variable_declaration_list_obj	
			except:
				pass

		print("End")

