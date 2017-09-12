import ply.yacc as yacc
import sys
arg1 = sys.argv[1]        # For taking input from command line.

# Get the token map from the lexer.  This is required.
from basicScannerCond import tokens

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('left','(',')'),
)

#defines the starting grammar rule (top level rule)
start = 'program'

#handle empty productions
def p_empty(p):
    'empty :'
    pass

#following is the grammar
def p_program(p):
	"program : declaration_list procedure_definition"

def p_declarationlist(p):
	'''declaration_list : procedure_declaration
					    | variable_declaration_list procedure_declaration
			 		    | procedure_declaration variable_declaration_list'''

def p_proceduredecl(p):
	'''procedure_declaration : VOID NAME '(' ')' ';' '''
	print("procedure_declaration \n")

def p_proceduredefn(p):
	'''procedure_definition : NAME '(' ')' '{' block goto_stat optional_variable_declaration_list ex_statement_list end_stat '}' '''

def p_optvardecllist(p):
	'''optional_variable_declaration_list : empty
										  | variable_declaration_list'''

def p_vardecllist(p):
	'''variable_declaration_list : variable_declaration
								 | variable_declaration_list variable_declaration'''

def p_vardecl(p):
	''' variable_declaration : FLOAT var_list ';'
							 | INT var_list ';' '''

def p_varlist(p):
	''' var_list : NAME
				 | var_list ',' NAME '''

def p_exstatlist(p):
	''' ex_statement_list : empty
						  | ex_statement_list block statement goto_stat'''

def p_stmt(p):
	''' statement : assignment_statement
				   | if_else_statement
	               | use_stat '''
				  
def p_asgnstmt(p):
	''' assignment_statement : variable ASSIGN_OP arith_expression ';'
							 | variable ASSIGN_OP POINTER_OP variable ';'
							 | variable ASSIGN_OP ADDRESS_OP variable ';' '''

def p_arithexpr(p):
	''' arith_expression : arith_expression '+' arith_expression
						 | arith_expression '-' arith_expression
						 | arith_expression '*' arith_expression
						 | arith_expression '/' arith_expression
						 | '-' arith_expression %prec UMINUS
						 | '(' arith_expression ')'
						 | expression_term '''

def p_ifelse(p):
	''' if_else_statement : IF '(' COND ')' goto_stat statement '''

def p_exprterm(p):
	'''expression_term : variable
					   | constant '''
        

def p_var(p):
	''' variable : NAME '''

def p_cons(p):
	''' constant : NUM
				 | FNUM '''

def p_endstatement(p):
    ''' end_stat :  block return_stat
                    | block use_stat	
					| block empty '''
				 
def p_returnstat(p):
    ''' return_stat : RETURN POINTER_OP POINTER_OP variable ';'
					| RETURN ADDRESS_OP variable ';' '''

def p_usestat(p):
    ''' use_stat : USE '(' variable ')' ';' 
	              | USE '(' POINTER_OP variable ')' ';' '''
				
def p_block(p):
    ''' block : '<' BB NUM '>' ':' 
				| empty '''
def p_goto(p):
    ''' goto_stat : GOTO block 
					| empty '''
				
#for error handling
def p_error(p):
    print("Syntax error at '%s'  '%d' " %(p.value,p.lineno))

#import ply.yacc as yacc
parser = yacc.yacc()

with open(arg1, 'r') as myfile:
    data=myfile.read()

parser.parse(data)