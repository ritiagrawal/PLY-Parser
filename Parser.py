import ply.yacc as yacc
import sys
arg1 = sys.argv[1]        # For taking input from command line.

# Get the token map from the lexer.  This is required.
from Scanner import tokens
from astgenerator import *

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
	"""procedure_definition : NAME '(' parameters ')' '{'  variable_declaration_list ex_statement_list return_stat '}' procedure_definition 
							 | empty
	"""
	global level
	if len(p)==11:
		p[0]=p[7]
	level=0
	
def p_parameters(p):
	''' parameters : VAR ppointer_var parameter_list
		    | ppointer_var parameter_list
		    | empty  '''
	global level
	if len(p) == 3:
		p[0]=p[1]
	level=0

def p_parameterlist(p):
	'''parameter_list : ',' parameters
			    | empty '''
    
def p_variabledeclarationlist(p):
    ''' variable_declaration_list : empty
				  | variable_declaration_list variable_declaration	'''
    
						 
def p_variabledeclaration(p):
	''' variable_declaration : VAR var_list ';'
							 '''
	
def p_varlistpointer(p):
	'''var_list : ppointer_var
		| var_list ',' ppointer_var'''
	global level
	global varCount
	global multipleVar
	flag=0
	length=len(symbolTable)-1
	
	if varnames[varCount-1] in symbolTable[length].var :
		print ("Multiple declarations of =====",multipleVar)
		flag=1
		
	if (flag != 1):
		varEntry= SymbolEntry(varnames[varCount-1], level)
		print("level=====",level)	
		symbolTable.append(varEntry)
		for i in range (len(symbolTable)):
			print(symbolTable[i].var, "\t", symbolTable[i].level,"\n")
	level=0
def p_varlist(p):
	'''var_list : variable
	     | var_list ',' variable '''
	global level
	global varCount
	flag=0
	if len(p)==2:
		for i in range (len(symbolTable)):
			if p[1] in symbolTable[i].var :
				print ("Multiple declarations of ",p[1])
				flag=1
				break
	else:
		for i in range (len(symbolTable)):
			if p[3] in symbolTable[i].var :
				print ("Multiple declarations of ",p[3])
				flag=1
				break
	if (flag != 1):
		varEntry= SymbolEntry(varnames[varCount-1], level)
		print("level=====",level)	
		symbolTable.append(varEntry)
		for i in range (len(symbolTable)):
			print(symbolTable[i].var, "\t", symbolTable[i].level,"\n")
	level=0
	
def p_pointervariable(p):
	''' pointer_variable :  POINTER_OP variable'''
	global interVar
	p[0]=NameAst(p[2])
	p[0].place="var"+ str(interVar)
	interVar+=1
	p[0].code="\t %s=%s %s" %(p[0].place,p[1], p[2]) 
	
	
def p_ppointervariable(p):
	'''ppointer_var : POINTER_OP ppointer_var
			 | pointer_variable  '''
	global interVar
	global varCount
	global level
	if len(p)==2:
		p[0]=p[1]
		level+=1
	else:
		level +=1
		p[0]=NameAst(p[2].place)
		p[0].place="var"+ str(interVar)
		interVar+=1
		p[0].code=p[2].code + "\n\t %s=%s %s" %(p[0].place,p[1],p[2].place)
		print(p[0].code) 
	
def p_addrvariable(p):
	'''addr_var : ADDRESS_OP variable'''
	global interVar
	p[0]=NameAst(p[2])
	p[0].place="var"+ str(interVar)
	interVar+=1
	p[0].code="\t %s=%s %s" %(p[0].place,p[1], p[2]) 
		
def p_exstatlist(p):
	''' ex_statement_list : empty
				| ex_statement_list statement '''

def p_stmt(p):
	''' statement : assignment_statement
		       | cond_goto
	               | use_stat
		       | uncond_goto 
	    	       | procedure_call '''
	p[0]=p[1]
	print("\n\tStatement::",p[0].code)

def p_stmtlabel(p):
	''' statement : label'''

				  
def p_asgnstmt(p):
	''' assignment_statement : expression_term ASSIGN_OP arith_expression ';' '''
	global interVar
	p[0]=AssigOpArth(p[1],p[3],"","")
	p[0].place=p[1].place
	p[0].code= p[3].code + "\n\t %s = %s" %(p[0].place , p[3].place)
	#print(p[3].place)
	print("\t Assigning",p[0].code)
							
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
	#if p[1] in varnames:	
	p[0]=NameAst(p[1])
	p[0].place = p[1]
	p[0].code = ""
	#else:
	#	print ("Undeclared Name '%s' " %(p[1]))
	#	raise SyntaxError		

def p_exprtermpointervar(p):
	'''expression_term : ppointer_var'''
	global level
	p[0]=p[1]	
	level=0

def p_exprtermaddrvar(p):
	'''expression_term : addr_var'''
	global interVar
	p[0]=p[1]

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
	p[0].code= "\n\tIF ( ) %s" %(p[4].code)
	print(p[0].code)
	

def p_procedurecall(p): 
    ''' procedure_call : NAME '(' parameters ')' ';' '''
    p[0] = ProcedureCallAst(p[1], p[3], "", "")
    p[0].place = ""
    p[0].code = p[3].code + "\n\t%s ( %s )" %(p[1], p[3].place)
    print (p[0].code)
	
def p_var(p):
	''' variable : NAME
				| arr_var
	'''	
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
	p[0] = NumberAst(p[1],"int")
				 
def p_returnstat(p):
	''' return_stat : RETURN ppointer_var ';'
		| RETURN addr_var ';'
		| RETURN variable ';'
		| empty '''
	global level
	level=0

def p_usestat(p):
	''' use_stat : USE '(' ppointer_var ')' ';' '''
	global level
	p[0] = UseStatementAst(p[3],"","")
	p[0].place= p[3].place
	p[0].code= p[3].code + "\n\tUSE ( %s )" %(p[0].place)
	print(p[0].code)
	level=0
				
def p_label(p):
    ''' label : '<' BB NUM '>' ':' '''
    p[0]=p[3]  
	
	
def p_ungoto(p):
    ''' uncond_goto : GOTO label '''
    p[0]=GotoAst(p[2],"","")
    p[0].place = ""
    p[0].code = "\t%s %s"%(p[1], p[2])
    print (p[0].code)
				
#for error handling
def p_error(p):
    print("Syntax error at '%s'  '%d' " %(p.value,p.lineno))

#import ply.yacc as yacc
parser = yacc.yacc()

with open(arg1, 'r') as myfile:
    data=myfile.read()

result= parser.parse(data)
