import sys
from abc import ABC
arg1 = sys.argv[1]        						# For taking input from command line.
with open(arg1, 'r') as myfile:
    data=myfile.read()

	
varnames=[]	
multipleVar=""
scope=0
level=0
#parameterlist[]
#SymbolTable

EntryCount=0
varCount=0;
symbolTable = []
class SymbolEntry():
	def __init__(self, var, level,scope):
		self.var=var
		self.level=level
		self.scope=scope
		
#from parserast import *
#For generating new variables in intermediate code
interVar = 0	
varStr = "var"

#For labels in icode
label1 = 0
label2 = 0

#abstract classes representing the left side of the grammer rule
class program(ABC):
	pass

class procedure_defination_list(ABC):
	pass

class procedure_defination(ABC):
	pass

class variable_declarations(ABC):
	pass

class variable_declaration_list(ABC):
	pass
	
class variable_declaration(ABC):
	pass

class structure_variable(ABC):
	pass
	
class var_list(ABC):
	pass

class structure_declaration(ABC):
	pass

class structure_object(ABC):
	pass

class ex_statement_list(ABC):
	pass
	
class statement(ABC):
	pass
	
class def_parameters(ABC):
	pass
	
class def_parameter_list(ABC):
	pass
	
class call_parameters(ABC):
	pass
	
class call_parameter_list(ABC):
	pass
	
class assignment_statement(ABC):
	pass
	
class cond_goto(ABC):
	pass

class uncond_goto(ABC):
	pass

class if_goto(ABC):
	pass
	
class use(ABC):
	pass
	
class procedure_call(ABC):
	pass
	
class expression_term(ABC):
	pass
	
class variable(ABC):
	pass
	
class constant(ABC):
	pass

class ppointer_variable(ABC):
	pass

class pointer_variable(ABC):
	pass
	
class addr_variable(ABC):
	pass

class arithmetic_term(ABC):
	pass
	
class label(ABC):
	pass
	
class return_stat(ABC):
	pass

class program_grammar(program):					#program : variable_declarations procedure_definition_list
	variable_declarations_obj=variable_declarations()
	procedure_defination_list_obj=procedure_defination_list()
	def __init__(self,variable_declarations_obj,procedure_defination_list_obj):
		self.variable_declarations_obj=variable_declarations_obj
		self.procedure_defination_list_obj=procedure_defination_list_obj

class procedure_defination_list_grammar(procedure_defination_list):  #procedure_definition_list : procedure_definition  procedure_definition_list
	procedure_defination_list_obj=procedure_defination_list()
	procedure_defination_obj = procedure_defination()
	def __init__(self,procedure_defination_list_obj, procedure_defination_obj):
		self.procedure_defination_list_obj=procedure_defination_list_obj
		self.procedure_defination_obj=procedure_defination_obj

class procedure_defination_grammar(procedure_defination):			#procedure_definition : NAME '(' def_parameters ')' '{'  variable_declarations ex_statement_list return_stat 
	variable_declarations_obj=variable_declarations()
	def_parameters_obj=def_parameters()
	ex_statement_list_obj=ex_statement_list()
	return_stat_obj=return_stat()
	def __init__(self,name,def_parameters_obj,variable_declarations_obj,ex_statement_list_obj,return_stat_obj):
		self.name=name
		self.def_parameters_obj=def_parameters_obj
		self.variable_declarations_obj=variable_declarations_obj
		self.ex_statement_list_obj=ex_statement_list_obj
		self.return_stat_obj=return_stat_obj
		
class variable_declarations_grammar(variable_declarations):			# variable_declarations: variable_declaration_list
	variable_declaration_list_obj=variable_declaration_list()
	def __init__(self, variable_declaration_list_obj):
		self.variable_declaration_list_obj=variable_declaration_list_obj

class variable_dec_stat(variable_declaration_list):				# variable_declaration_list:variable_declaration_list variable_declaration	
	variable_declaration_list_obj=variable_declaration_list()
	variable_declaration_obj= variable_declaration()
	def __init__(self, variable_declaration_list_obj, variable_declaration_obj):
		self.variable_declaration_list_obj=variable_declaration_list_obj
		self.variable_declaration_obj=variable_declaration_obj
		
class var_variable_list(variable_declaration):			# variable_declaration : VAR var_list ';'
	var_list_obj=var_list()
	def __init__(self, var_list_obj):
		self.var_list_obj=var_list_obj

class	structure_variable_grammar(structure_variable):		 # variable_declaration : structure_declaration 
	structure_declaration_obj=structure_declaration()
	def __init__(self,structure_declaration_obj):
		self.structure_declaration_obj=structure_declaration_obj
	

class structure_declaration_grammar(structure_declaration):	#structure_declaration : 'struct' variable '{' variable_declaration '}' struct_object ';'
	variable_declaration_list_obj= variable_declaration_list()
	variable_obj=variable()
	struct_obj=structure_object()
	def __init__(self, variable_obj,variable_declaration_list_obj,struct_obj):
		self.variable_declaration_list_obj=variable_declaration_list_obj
		self.variable_obj=variable_obj
		self.struct_obj=struct_obj

class structure_object_grammar(structure_object):		#struct_object : var_list
	var_list_obj=var_list()
	def __init__(self, var_list_obj):
		self.var_list_obj=var_list_obj
	
class var_list_ppointer(var_list):						#var_list : ppointer_var
	ppointer_variable_obj=ppointer_variable()
	def __init__(self, ppointer_variable_obj):
		self.ppointer_variable_obj=ppointer_variable_obj
		
class var_list_ppointerlist(var_list):					#varlist: var_list ',' ppointer_var'
	ppointer_variable_obj=ppointer_variable()
	var_list_obj=var_list()
	def __init__(self,var_list_obj,ppointer_variable_obj):
		self.ppointer_variable_obj=ppointer_variable_obj
		self.var_list_obj=var_list_obj
		
class var_list_variable(var_list):						#var_list : variable
	variable_obj=variable()
	def __init__(self, variable_obj):
		self.variable_obj=variable_obj
		
class var_list_variablelist(var_list):					#varlist:var_list ',' variable 
	variable_obj=variable()
	var_list_obj=var_list()
	def __init__(self,var_list_obj,variable_obj):
		self.variable_obj=variable_obj
		self.var_list_obj=var_list_obj

class statement_list(ex_statement_list):				#ex_statement_list : ex_statement_list statement
	ex_statement_list_obj=ex_statement_list()
	statement_obj=statement()
	def __init__(self,ex_statement_list_obj,statement_obj):
		self.ex_statement_list_obj=ex_statement_list_obj
		self.statement_obj=statement_obj
		
class statement_one(ex_statement_list):					#ex_statement_list : statement
	statement_obj=statement()
	def __init__(self,statement_obj):
		self.statement_obj=statement_obj

class assignment_statement_list(statement):				#statement : assignment_statement
	assignment_statement_obj=assignment_statement()
	def __init__(self,assignment_statement_obj):
		self.assignment_statement_obj=assignment_statement_obj

class cond_goto_stat(statement):						#statement :  cond_goto
	cond_goto_obj=cond_goto()
	def __init__(self,cond_goto_obj):
		self.cond_goto_obj=cond_goto_obj

class uncond_goto_stat(statement):
	uncond_goto_obj=uncond_goto()						#statement : uncond_goto
	def __init__(self,uncond_goto_obj):
		self.uncond_goto_obj=uncond_goto_obj

class label_stat(statement):							# statement : label
	label_obj=label()
	def __init__(self,label_obj):
		self.label_obj=label_obj
		
class use_stat(statement):								#statement : use_stat
	use_obj=use()
	def __init__(self,use_obj):
		self.use_obj=use_obj
		
class procedure_call_stat(statement):					#statement : procedure_call
	procedure_call_obj = procedure_call()
	def __init__(self,procedure_call_obj):
		self.procedure_call_obj=procedure_call_obj
		
class calling_procedure(procedure_call):				#procedure_call : NAME '(' parameters ')' ';' 
	call_parameters_obj = call_parameters()
	def __init__(self, name, call_parameters_obj):
		self.name=name
		self.call_parameters_obj=call_parameters_obj

class parameters_for_def(def_parameters):					#def_parameters : VAR ppointer_var def_parameter_list
	ppointer_variable_obj=ppointer_variable()
	def_parameter_list_obj=def_parameter_list()
	def __init__(self,ppointer_variable_obj,def_parameter_list_obj):
		self.ppointer_variable_obj=ppointer_variable_obj
		self.def_parameter_list_obj=def_parameter_list_obj
		
class parameters_for_call(call_parameters):					#call_parameters : ppointer_var call_parameter_list
	ppointer_variable_obj=ppointer_variable()
	call_parameter_list_obj=call_parameter_list()
	def __init__(self,ppointer_variable_obj,call_parameter_list_obj):
		self.ppointer_variable_obj=ppointer_variable_obj
		self.call_parameter_list_obj=call_parameter_list_obj
		
class def_parameter_list_grammar(def_parameter_list):
	def_parameters_obj=def_parameters()
	def __init__(self,def_parameters_obj):			#def_parameter_list : ',' def_parameters
		self.def_parameters_obj=def_parameters_obj

class call_parameter_list_grammar(call_parameter_list):
	call_parameters_obj=call_parameters()
	def __init__(self,call_parameters_obj):			#call_parameter_list : ',' call_parameters
		self.call_parameters_obj=call_parameters_obj
		
class assign(assignment_statement):						# assignment_statement : expression_term ASSIGN_OP arith_expression ';' 
	expression_term_obj=expression_term()
	arithmetic_term_obj=arithmetic_term()
	def __init__(self,expression_term_obj,arithmetic_term_obj):
		self.expression_term_obj=expression_term_obj	
		self.arithmetic_term_obj=arithmetic_term_obj

class exp_var(expression_term):							#expression_term : variable	
	variable_obj=variable()
	def __init__(self,variable_obj):
		self.variable_obj=variable_obj
		
class exp_ppointer_var(expression_term):				#expression_term : ppointer_var
	ppointer_variable_obj=ppointer_variable()
	def __init__(self,ppointer_variable_obj):
		self.ppointer_variable_obj=ppointer_variable_obj
	
		
class exp_addr_var(expression_term):					#expression_term : addr_var
	addr_variable_obj=addr_variable()
	def __init__(self,addr_variable_obj):
		self.addr_variable_obj=addr_variable_obj
		
class exp_constant(expression_term):					#expression_term : constant 
	constant_obj=constant()
	def __init__(self,constant_obj):
		self.constant_obj= constant_obj

class exp_structure(expression_term):							#expression_term : variable '-' '>' variable
	variable_pointer_obj=variable()
	variable_field_obj=variable()
	def __init__(self,variable_pointer_obj,variable_field_obj):
		self.variable_pointer_obj=variable_pointer_obj
		self.variable_field_obj=variable_field_obj
		
class exp_procedure_call(expression_term):
	procedure_call_obj=procedure_call()					#expression_term : procedure_call
	def __init__(self,procedure_call_obj):
		self.procedure_call_obj=procedure_call_obj	
	
class var_name(variable):								#variable : NAME
	def __init__(self, name):
		self.name=name;
		
#class var_array(variable):
#	arr_var_obj = arr_var()						#arr_var() to be done
#	def __init__(self, arr_var_obj):
#		self.arr_var_obj=arr_var_obj
		
class constant_num(constant):							#constant : NUM 
	def __init__(self, num):
		self.num=num
	
class ppointer_var_list(ppointer_variable):				#ppointer_var : POINTER_OP ppointer_var
	ppointer_variable_obj=ppointer_variable()
	def __init__(self,ppointer_variable_obj):
		self.ppointer_variable_obj=ppointer_variable_obj	
	
class ppointer_var(ppointer_variable):					#ppointer_var=pointer_variable 
	pointer_variable_obj=pointer_variable()
	def __init__(self,pointer_variable_obj):
		self.pointer_variable_obj=pointer_variable_obj
	
class addr_variableclass(addr_variable):				#addr_var : ADDRESS_OP variable
	variable_obj=variable()
	def __init__(self,variable_obj):
		self.variable_obj=variable_obj
	
class pointer_op_var(pointer_variable):
	variable_obj=variable()
	def __init__(self,variable_obj):			#pointer_variable :  POINTER_OP variable
		self.variable_obj=variable_obj
	
class arithmetic_term_binop(arithmetic_term):			#arith_expression : arith_expression ADD_OP arith_expression
	arithmetic_term_obj1=arithmetic_term()
	arithmetic_term_obj2=arithmetic_term()
	def __init__(self,arithmetic_term_obj1,bin_op,arithmetic_term_obj2):
		self.bin_op=bin_op
		self.arithmetic_term_obj1=arithmetic_term_obj1
		self.arithmetic_term_obj2=arithmetic_term_obj2
		
class arithmetic_term_exp(arithmetic_term):			#arith_expression : expression_term 
	expression_term_obj=expression_term()  
	def __init__(self,expression_term_obj):
		self.expression_term_obj=expression_term_obj
		
class if_goto_grammer(cond_goto):							#cond_goto : IF '(' ')' if_cond_goto 
	if_goto_obj=if_goto()
	def __init__(self,if_goto_obj):
		self.if_goto_obj=if_goto_obj		

class goto_label(if_goto):						#if_cond_goto : GOTO label
	label_obj=label()
	def __init__(self,label_obj):
		self.label_obj=label_obj

class uncond_goto_label(uncond_goto):			 	# uncond_goto : GOTO label
	label_obj=label()
	def __init__(self,label_obj):
		self.label_obj=label_obj

class use_pointer(use):									#use_stat : USE '(' ppointer_var ')' ';' 
	ppointer_var_obj=ppointer_variable()
	def __init__(self,ppointer_var_obj):
		self.ppointer_var_obj=ppointer_var_obj
		
class label_num(label):									# label : '<' BB NUM '>' ':' 
	def __init__(self,num):
		self.num=num
		
class return_ppointer_var(return_stat):				 	#return_stat : RETURN ppointer_var ';' 
	ppointer_var_obj=ppointer_variable()
	def __init__(self, ppointer_var_obj):
		self.ppointer_var_obj=ppointer_var_obj
		
class return_addr_var(return_stat):						# return_stat : RETURN addr_var ';' 
	addr_variable_obj=addr_variable()
	def __init__(self, addr_variable_obj):
		self.addr_variable_obj=addr_variable_obj

class return_variable(return_stat):						# return_stat : RETURN variable ';' 
	variable_obj=variable()
	def __init__(self, variable_obj):
		self.variable_obj=variable_obj
		
