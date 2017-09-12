import ply.yacc as yacc
import sys
arg1 = sys.argv[1]        # For taking input from command line.

# Get the token map from the lexer.  This is required.
from Scanner import tokens

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
	"program : procedure_definition"

def p_proceduredefn(p):
	'''procedure_definition : NAME '(' parameter_list ')' '{'  variable_declaration_list ex_statement_list return_stat '}' procedure_definition
							 | empty '''

def p_parameterlist(p):
    ''' parameter_list : VAR pointer_variable parameter_list
						 | pointer_variable parameter_list
						 | ',' parameter_list
						 | empty '''

def p_variabledeclarationlist(p):
    ''' variable_declaration_list : empty
								   | variable_declaration_list variable_declaration	'''
						 
def p_variabledeclaration(p):
    ''' variable_declaration : VAR var_list ';'
							 '''
def p_varlist(p):
	'''var_list : pointer_variable
				| var_list ',' pointer_variable'''
	
def p_pointervariable(p):
    ''' pointer_variable :  POINTER_OP pointer_variable
						  | variable '''
						 
	
def p_exstatlist(p):
	''' ex_statement_list : empty
						  | ex_statement_list statement '''

def p_stmt(p):
	''' statement : assignment_statement
				   | cond_goto
	               | use_stat
				   | label
				   | uncond_goto 
				   | procedure_call '''
				  
def p_asgnstmt(p):
	''' assignment_statement : variable ASSIGN_OP arith_expression ';'
							 | variable ASSIGN_OP POINTER_OP variable ';'
							 | variable ASSIGN_OP ADDRESS_OP variable ';' '''

def p_arithexpr(p):
	''' arith_expression : arith_expression '+' arith_expression
						 | arith_expression '-' arith_expression
						 | expression_term '''

def p_exprterm(p):
	'''expression_term : variable
					   | procedure_call
					   | constant '''
						 
def p_condgoto(p):
	''' cond_goto : IF '(' ')' uncond_goto '''

def p_procedurecall(p): 
    ''' procedure_call : NAME '(' parameter_list ')' ';' '''
	
def p_var(p):
	''' variable : NAME
				  | arr_var
				  '''	

def p_arrayvar(p):
    ''' arr_var : NAME '[' NUM ']' '''		  
	
def p_cons(p):
	''' constant : NUM '''
				 
def p_returnstat(p):
    ''' return_stat : RETURN pointer_variable ';'
					| RETURN ADDRESS_OP variable ';'
					| empty '''

def p_usestat(p):
    ''' use_stat : USE '(' pointer_variable ')' ';' '''
				
def p_label(p):
    ''' label : '<' BB NUM '>' ':' '''
	
def p_ungoto(p):
    ''' uncond_goto : GOTO label '''
				
#for error handling
def p_error(p):
    print("Syntax error at '%s'  '%d' " %(p.value,p.lineno))

#import ply.yacc as yacc
parser = yacc.yacc()

with open(arg1, 'r') as myfile:
    data=myfile.read()

parser.parse(data)