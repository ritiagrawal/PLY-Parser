class tree_traversal():
	def __init__(self,tree):
		#print(tree)	
		variable_declarations=tree.variable_declarations_obj
	
		variable_declaration_list=variable_declarations.variable_declaration_list_obj
		
		while(variable_declaration_list):
			var_list=variable_declaration_list.variable_declaration_obj.var_list_obj
			while(var_list):
				try:
					print("*",var_list.ppointer_variable_obj.pointer_variable_obj.variable_obj.name)						
				except:
					pass
				try:
					print("**",var_list.ppointer_variable_obj.ppointer_variable_obj.pointer_variable_obj.variable_obj.name)						
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

