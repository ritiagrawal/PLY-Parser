import ply.yacc as yacc
import sys
arg1 = sys.argv[1]        # For taking input from command line.

# Get the token map from the lexer.  This is required.
from Scanner import tokens
from astgenrator import *

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
				
    if len(p) == 2:
        if p[1] not in varnames:
            varnames.append(p[1]) 
            print ("varnames",varnames)
        else:
            print ("Multiple declarations",p[1])
    else:
        if p[3] not in varnames:
            varnames.append(p[3])
        else:
            print ("Multiple declarations",p[3])
	
def p_pointervariable(p):
    ''' pointer_variable :  POINTER_OP pointer_variable
						  | variable '''
    if len(p)==2:
        p[0]=p[1]					 
    else:
        p[0]=p[2]
		
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
	''' assignment_statement : expression_term ASSIGN_OP arith_expression ';'
				 | expression_term ASSIGN_OP POINTER_OP expression_term ';'
				 | expression_term ASSIGN_OP ADDRESS_OP expression_term ';' '''
	global interVar
	if len(p)==6:
		print()
		p[0]=AssigOpArth(p[1],p[4],"","")
		p[0].place=p[1].place
		p[0].code=p[4].code + "\t %s = %s %s" %(p[0].place , p[3], p[4].place)
	else:
		print("Going in if while assigning\n")
		p[0]=AssigOpArth(p[1],p[3],"","")
		p[0].place=p[1].place
		p[0].code= p[3].code + "\t %s = %s" %(p[0].place , p[3].place)
	print("\tAssigning",p[0].code)
							
def p_arithexpr(p):
	''' arith_expression : arith_expression '+' arith_expression
						 | arith_expression '-' arith_expression
						 | expression_term '''
	global interVar
	if len(p)==2:
		p[0] = p[1]
		
	if len(p)==4:
		p[0]=ArithOpAst(p[1],p[2],p[3])
		p[0].place="var" + str(interVar)
		interVar += 1
		p[0].code=p[1].code + p[3].code +"\t %s = %s  %s %s\n" %(p[0].place,p[1].place,p[2],p[3].place)
		print(p[0].code)
    		

def p_exprtermvar(p):
	'''expression_term : variable'''
	if p[1] in varnames:	
		print("in Expression Term")
		p[0]=NameAst(p[1])
		p[0].place = p[1]
		p[0].code = ""
	else:
		print ("Undeclared Name '%s' " %(p[1]))
		raise SyntaxError		
	
	
def p_exprtermconstant(p):
	'''expression_term : constant '''
	p[0]=NumberAst(p[1])
	p[0].place = p[1].place
	p[0].code = ""

def p_exprtermprocedure(p):
	'''expression_term : procedure_call'''
	
def p_condgoto(p):
	''' cond_goto : IF '(' ')' uncond_goto '''
	p[0]=p[4]

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
    p[0]=p[1]
				
#for error handling
def p_error(p):
    print("Syntax error at '%s'  '%d' " %(p.value,p.lineno))

#import ply.yacc as yacc
parser = yacc.yacc()

with open(arg1, 'r') as myfile:
    data=myfile.read()

result= parser.parse(data)


		
