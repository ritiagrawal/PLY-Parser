import ply.yacc as yacc
import sys
arg1 = sys.argv[1]        # For taking input from command line.
debugLevel = sys.argv[2]

# Get the token map from the lexer.  This is required.
from Scanner import tokens
from astgenerator import *
from TreeTraversal import *

precedence = (
	('left', '+', '-'),
)
#defines the starting grammar rule (top level rule)
start = 'program'

#handle empty productions
def p_empty(p):
    'empty :'
    pass

#following is the grammar
def p_program(p):
	"program : variable_declarations procedure_definition_list"
	p[0]=program_grammar(p[1],p[2])
	print ("..SUCCESSFULLY PARSED...")
	
def p_proceduredefn_list(p):
	''' procedure_definition_list : procedure_definition  procedure_definition_list
								| empty'''
	if len(p)==3:
		print("\n-------------------------\nSYMBOL TABLE\n\nVarName\tlevel\tscope")
		for i in range(len(symbolTable)):
			print(symbolTable[i].var,"\t",symbolTable[i].level,"\t",symbolTable[i].scope)    
		print("\n-------------------------\n")
		p[0]= procedure_defination_list_grammar(p[2],p[1])

		
	
def p_proceduredefn(p):
	"""procedure_definition : NAME '(' def_parameters ')' '{'  variable_declarations ex_statement_list return_stat '}' 
	"""
	global level
	if len(p)==10:
		p[0]=procedure_defination_grammar(p[1],p[3],p[6],p[7],p[8])
	level=0

	
def p_parametersfordef(p):
	''' def_parameters : VAR ppointer_var def_parameter_list
					| empty  '''
	global level
	if len(p)==4:
		p[0]=parameters_for_def(p[2],p[3])
	level=0
	
def p_defparameterlist(p):
	'''def_parameter_list : ',' def_parameters
						| empty '''
	if len(p) == 3:
		p[0] = def_parameter_list_grammar(p[2])

def p_parameterforcall(p):
	'''	call_parameters : ppointer_var call_parameter_list
						| empty  '''
	global level
	if len(p) == 3:
		p[0]=parameters_for_call(p[1], p[2])
	level=0
	
def p_callparameterlist(p):
	'''call_parameter_list : ',' call_parameters
						| empty '''
	if len(p)==3:
		p[0]=call_parameter_list_grammar(p[2])
    
def p_variable_declarations(p):
	'''variable_declarations : variable_declaration_list'''
	global scope
	
	scope=scope+1
	if len(p)==2:
		p[0]=variable_declarations_grammar(p[1])

def p_fieldvariabledeclaration_list(p):
	''' field_variable_declaration_list : empty
				  | field_variable_declaration field_variable_declaration_list '''
	if len(p)==3:
		p[0]=variable_dec_stat(p[2],p[1])

def p_fieldvariabledeclaration(p):
	''' field_variable_declaration : VAR field_var_list ';'
				 | structure_declaration '''
	if len(p)==4:	
		p[0]=var_variable_list(p[2])
	else:
		p[0]=structure_variable_grammar(p[1])

def p_variabledeclarationlist(p):
	''' variable_declaration_list : empty
				  | variable_declaration variable_declaration_list '''
	if len(p)==3:
		p[0]=variable_dec_stat(p[2],p[1])
						 
def p_variabledeclaration(p):
	''' variable_declaration : VAR var_list ';'
				 | structure_declaration '''
	if len(p)==4:	
		p[0]=var_variable_list(p[2])
	else:
		p[0]=structure_variable_grammar(p[1])
	
def p_structuredeclaration(p):
	''' structure_declaration : STRUCT field_variable '{' field_variable_declaration_list '}' struct_object ';' '''
	p[0]=structure_declaration_grammar(p[2],p[4],p[6])

def p_structobject(p):
	''' struct_object : var_list '''
	p[0]=structure_object_grammar(p[1])

def p_fieldvarlistpointer(p):
	'''field_var_list : field_ppointer_var
		| field_var_list  ',' field_ppointer_var '''

	if len(p)==2:
		p[0]=var_list_ppointer(p[1])
	else:
		p[0]=var_list_ppointerlist(p[1],p[3])

def p_varlistpointer(p):
	'''var_list : ppointer_var
		| var_list  ',' ppointer_var '''
	global level
	global varCount
	global multipleVar
	global scope
	flag=0
	length=len(symbolTable)-1
	if len(symbolTable)==0:
		varEntry = SymbolEntry(varnames[varCount-1], level,scope)
		symbolTable.append(varEntry)
	else:
		if varnames[varCount-1] in symbolTable[length].var:
			print ("Multiple declarations of ",multipleVar)
			flag=1
		
		if (flag != 1):
			varEntry= SymbolEntry(varnames[varCount-1], level,scope)
			symbolTable.append(varEntry)
			flag=0
	level=0
	if len(p)==2:
		p[0]=var_list_ppointer(p[1])
	else:
		p[0]=var_list_ppointerlist(p[1],p[3])

def p_varlist(p):
	'''var_list : variable
	     | var_list ',' variable '''
	global level
	global varCount
	global scope
	flag=0
	global multipleVar
	length=len(symbolTable)-1
	if len(symbolTable)==0:
		varEntry = SymbolEntry(varnames[varCount-1], level,scope)
		symbolTable.append(varEntry)
	else: 
		if varnames[varCount-1] in symbolTable[length].var :
				flag=1

		if (flag != 1):
			varEntry = SymbolEntry(varnames[varCount-1], level,scope)
			symbolTable.append(varEntry)
			flag=0
			
	level=0
	if len(p)==2:
		p[0]=var_list_variable(p[1])
	else:
		p[0]=var_list_variablelist(p[1],p[3])

def p_fieldpointervariable(p):
	''' field_pointer_variable :  POINTER_OP field_variable''' 
	p[0]=pointer_op_var(p[2])

def p_fieldppointervariable(p):
	'''field_ppointer_var : POINTER_OP field_ppointer_var
			 | field_pointer_variable  '''
	global interVar
	global varCount
	global level
	if len(p)==2:
		p[0]=p[1]
		level+=1
		p[0]=ppointer_var(p[1])
	if len(p)==3:
		level +=1
		p[0]=ppointer_var_list(p[2])

def p_pointervariable(p):
	''' pointer_variable :  POINTER_OP variable''' 
	p[0]=pointer_op_var(p[2])

def p_ppointervariable(p):
	'''ppointer_var : POINTER_OP ppointer_var
			 | pointer_variable  '''
	global interVar
	global varCount
	global level
	if len(p)==2:
		p[0]=p[1]
		level+=1
		p[0]=ppointer_var(p[1])
	if len(p)==3:
		level +=1
		p[0]=ppointer_var_list(p[2])
	
	
def p_addrvariable(p):
	'''addr_var : ADDRESS_OP variable'''
	p[0]=addr_variableclass(p[2])
	
def p_exstatlist(p):
	''' ex_statement_list : empty
				| statement ex_statement_list  '''
	if len(p)==3:
		p[0]=statement_list(p[2],p[1])
	
	
def p_stmt(p):
	''' statement : assignment_statement'''
	p[0]=assignment_statement_list(p[1])
	
def p_stmt_cond_goto(p):
	'''statement :  cond_goto'''
	p[0]=cond_goto_stat(p[1])

def p_stmt_uncond_goto(p):
	'''statement : uncond_goto'''
	p[0]=uncond_goto_stat(p[1])
	
def p_stmt_use_stat	(p):
	'''statement : use_stat'''
	p[0]=use_stat(p[1])
	
	    	       
def p_stmtlabel(p):
	''' statement : label'''
	p[0]=label_stat(p[1])

def p_stmt_procedure_call(p):
	'''statement : procedure_call'''
	p[0]=procedure_call_stat(p[1])
  
def p_asgnstmt(p):
	''' assignment_statement : expression_term ASSIGN_OP arith_expression ';' '''
	global interVar
	p[0]=assign(p[1],p[3])
							
def p_arithexpr(p):
	''' arith_expression : arith_expression '+' arith_expression
				| arith_expression '-' arith_expression
				| expression_term '''
	global interVar
	if len(p)==2:
		p[0]=arithmetic_term_exp(p[1])
	
	if len(p)==4:
		p[0]=arithmetic_term_binop(p[1],p[2],p[3])
    		

def p_exprtermvar(p):
	'''expression_term : variable'''
	p[0]=exp_var(p[1])
	

def p_exprtermpointervar(p):
	'''expression_term : ppointer_var'''
	global level
	p[0]=exp_ppointer_var(p[1])
	level=0

def p_exprtermaddrvar(p):
	'''expression_term : addr_var'''
	p[0]=exp_addr_var(p[1])


def p_exprtermconstant(p):
	'''expression_term : constant '''
	p[0]=exp_constant(p[1])

def p_exptermstructure(p):
	''' expression_term : variable '-' '>' field_variable '''
	p[0] = exp_structure(p[1],p[4])

def p_exprtermprocedure(p):
	'''expression_term : procedure_call'''
	p[0]=exp_procedure_call(p[1])

def p_condgoto(p):
	''' cond_goto : IF '(' ')' if_cond_goto '''
	p[0]=if_goto_grammer(p[4])
	
def p_ungoto(p):
	''' uncond_goto : GOTO label '''
	p[0]=uncond_goto_label(p[2])
	
def p_ifgoto(p):
	'''if_cond_goto : GOTO label '''
	p[0]=goto_label(p[2])

def p_procedurecall(p): 
    ''' procedure_call : NAME '(' call_parameters ')' ';' '''
    p[0] = calling_procedure(p[1],p[3])
	
def p_var(p):
	''' variable : NAME'''		
	global varCount
	global multipleVar
	varflag=0	
	flag=0
	for entry in range(0,len(symbolTable)-1):
		if p[1]==varnames[entry] and scope == symbolTable[entry].scope:
				multipleVar=p[1]
				flag=1
				break
	if (flag == 0):
		varnames.append(p[1])
		varCount+=1
		flag=0

	p[0]=var_name(p[1])

def p_fieldvar(p):
	''' field_variable : NAME '''
	p[0]=var_name(p[1])

def p_arr_var(p):
	''' variable : arr_var'''	
	global varCount
	global multipleVar
	p[0]=p[1]
	if p[1] in varnames:
		multipleVar=p[1]
		pass
	else:
		varnames.append(p[1]) 
		varCount+=1
   
def p_arrayvar(p):
    ''' arr_var : NAME '[' NUM ']' '''		 
    p[0]=p[1]
	
def p_cons(p):
	''' constant : NUM '''
	p[0]=constant_num(p[1])
	
				 
def p_returnppointer(p):
	''' return_stat : RETURN ppointer_var ';' '''
	global level
	level=0
	p[0]=return_ppointer_var(p[2])
	
def p_return_addrvar(p):
	''' return_stat : RETURN addr_var ';' '''
	global level
	level=0
	p[0]=return_variable(p[2])

def p_return_var(p):
	''' return_stat : RETURN variable ';' '''
	global level
	level=0
	p[0]=return_variable(p[2])

def p_returnempty(p):
	''' return_stat : empty '''

def p_usestat(p):
	''' use_stat : USE '(' ppointer_var ')' ';' '''
	global level
	level=0
	p[0]=use_pointer(p[3])
	
				
def p_label(p):
    ''' label : '<' BB NUM '>' ':' '''
    p[0]=label_num(p[3])
				
#for error handling
def p_error(p):
    print("Syntax error at '%s'  '%d' " %(p.value,p.lineno))

#import ply.yacc as yacc
parser = yacc.yacc()

with open(arg1, 'r') as myfile:
    data=myfile.read()

result= parser.parse(data)

tree_traversal(symbolTable,result,debugLevel)

