import ply.yacc as yacc
import sys
arg1 = sys.argv[1]        # For taking input from command line.

# Get the token map from the lexer.  This is required.
from Scanner import tokens
class Node:
    def __init__(self,type,children=None,parent=None):
        self.type=type
        if children:
            self.children = children
        else:
            self.children = None
        self.parent=parent          
	
class Expr:
    def __init__(self, value, type):
        self.type= type
        self.value=value
	
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
    print ("Sucessfully parsed")
	
def p_proceduredefn(p):
    """procedure_definition : NAME '(' parameter_list ')' '{'  variable_declaration_list ex_statement_list return_stat '}' procedure_definition 
							 | empty
    """
    #if len(p) == 2:
        #print("Printinhg")
			
def p_parameterlist(p):
    ''' parameter_list : VAR pointer_variable parameter_list
						 | pointer_variable parameter_list
						 | ',' parameter_list
						 | empty '''
    #if len(p) == 4:
        #print(p[1])
    
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
				
    if len(p)==5:
        p[0]=Node("AssignmentOperation",[p[1],p[3]],p[2])
        print(p[0].type)
        print(p[0].parent)
        print(p[0].children)
		
							
def p_arithexpr(p):
    ''' arith_expression : arith_expression '+' arith_expression
						 | arith_expression '-' arith_expression
						 | expression_term '''
    if len(p)==2:
        p[0]=p[1]
    if len(p)==4:
        p[0]=("ArithmaticExpression",[p[1],p[3]],p[2])
        print("type",p[0])
        #print("parent",p[0].parent)
        #print("child",p[0].children)
    		

def p_exprterm(p):
    '''expression_term : variable
					   | procedure_call
					   | constant '''
    p[0]=p[1]
						 
def p_condgoto(p):
	''' cond_goto : IF '(' ')' uncond_goto '''

def p_procedurecall(p): 
    ''' procedure_call : NAME '(' parameter_list ')' ';' '''
	
def p_var(p):
    ''' variable : NAME
				  | arr_var
    '''	
	p[0]=p[1]

def p_arrayvar(p):
    ''' arr_var : NAME '[' NUM ']' '''		  
    p[0]=p[1]
	
def p_cons(p):
    ''' constant : NUM '''
	p[0] = NumberAst(p[1],"int")
	p[0].place = p[1]
	p[0].code = ""
				 
def p_returnstat(p):
    ''' return_stat : RETURN pointer_variable ';'
					| RETURN ADDRESS_OP variable ';'
					| empty '''

def p_usestat(p):
    ''' use_stat : USE '(' pointer_variable ')' ';' '''
				
def p_label(p):
    ''' label : '<' BB NUM '>' ':' '''
    p[0]=p[2]
	
def p_ungoto(p):
    ''' uncond_goto : GOTO label '''
				
#for error handling
def p_error(p):
    print("Syntax error at '%s'  '%d' " %(p.value,p.lineno))

#import ply.yacc as yacc
parser = yacc.yacc()

with open(arg1, 'r') as myfile:
    data=myfile.read()

result= parser.parse(data)


		