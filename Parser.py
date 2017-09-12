# -----------------------------------------------------------------------------
#Author : Rakshat Ranjan and Alok Kumar
# -----------------------------------------------------------------------------
import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from Scanner import tokens

from astgenerator import *	#import from ast file

precedence = (
	('left','OR'),
	('left','AND'),
	('left', 'NE', 'EQ'),
    ('left', 'GT', 'GE', 'LT', 'LE'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
    ('left','(',')'),
    ('left','ELSE'),
    ('right', 'NT'),
)



start = 'program'


def p_empty(p):
    'empty :'
    pass

#Print the final icode in icode.txt
def p_program(p):
	"program : declaration_list procedure_definition"
	p[0] = ProgramAst(p[2])
	print >> filebuff, p[2].code

def p_declarationlist(p):
	'''declaration_list : procedure_declaration
					    | variable_declaration_list procedure_declaration
					    | procedure_declaration variable_declaration_list'''


def p_proceduredecl(p):
	'''procedure_declaration : VOID NAME '(' ')' ';' '''
	if p[2] != "main":
		print ("Procedure Name must be main")
		raise SyntaxError
	else:
		symtab['void'].append(p[2])	#'main' variable stored in symbol table


#procedure_definition check if main in symbol table
def p_proceduredefn(p):
	'''procedure_definition : NAME '(' ')' '{' optional_variable_declaration_list ex_statement_list '}' '''
	if p[1] in symtab['void']:
		p[0] = ProcedureAst(p[1],p[5],p[6],"")
		p[0].code = "Procedure : main \n" + p[6].code
	else:
		print ("Procedure Name must be main")
		raise SyntaxError

def p_optvardecllist(p):
	'''optional_variable_declaration_list : empty
										  | variable_declaration_list'''
	if p[1] == 'empty':
		p[0] = NULL
	else:
		p[0] = p[1]

# adding symbol table entries in symbol table
def p_vardecllist(p):
	'''variable_declaration_list : variable_declaration '''
	for vaar in flotnames:
		symtab['float'].append(vaar)
	for vaar in intnames:
		symtab['int'].append(vaar)

def p_vardeclistlist(p):
	''' variable_declaration_list : variable_declaration_list variable_declaration'''
	for vaar in flotnames:
		symtab['float'].append(vaar)
	for vaar in intnames:
		symtab['int'].append(vaar)


# check for multiple declaration
def p_vardecl(p):
	''' variable_declaration : FLOAT var_list ';'
							 | INT var_list ';' '''
	global flotnames
	global intnames
	if p[1] == 'float':
		for ard in varvar:
			if ard in flotnames or ard in intnames:
				print ("multiple declaration '%s' " %(ard))
				raise SyntaxError
			else:
				flotnames.append(ard)
		varvar[:] = []
	elif p[1] == 'int':
		for ard in varvar:
			if ard in intnames or flotnames:
				print ("multiple declaration '%s' " %(ard))
				raise SyntaxError
			else:
				intnames.append(ard)
		varvar[:] = []


# check for multiple declaration
def p_varlist(p):
	''' var_list : NAME '''
	#p[0] = p[1]
	if p[1] not in varvar:
		varvar.append(p[1])
	else :
		print ("Multiple declarations '%s' ") %(p[1])
		raise SyntaxError


def p_varli(p):	
	''' var_list : var_list ',' NAME '''
	if p[3] not in varvar:
		varvar.append(p[3])
	else :
		print ("Multiple declarations '%s' ") %(p[3])
		raise SyntaxError


def p_exstatlistemp(p):
	''' ex_statement_list : empty'''
	p[0] = SequenceAst("")

def p_exstatstat(p):
	''' ex_statement_list : ex_statement_list statement '''
	p[1].pushbach(p[2])		#SequenceAst().pushbach() function defined in astgenerator
	p[0]= p[1]
	p[0].code += p[2].code 	#icode of ast's are concatenated


def p_stmt(p):
	''' statement : assignment_statement
				  | if_else_statement
				  | while_statement
				  | compound_statement '''
	p[0] = p[1]

def p_compstmt(p):
	''' compound_statement : '{' ex_statement_list '}' '''
	p[0] = p[2]



def p_asgnstmt(p):
	''' assignment_statement : variable ASSIGN_OP arith_expression ';'
							 | variable ASSIGN_OP cond_comp ';' '''
	if p[1].type != p[3].type:
		print("Type mismatch Line no:%s"%(p.lineno(2)))		# type-check   
		raise SyntaxError				#to ensure no output generated 
	else:
		global interVar
		p[0] = AssignAst(p[1],p[3],"","") 
		p[0].place = "var"+str(interVar)	#new variable generated
		interVar+=1
		p[0].code = p[1].code + p[3].code + "\t%s = %s \n"%(p[1].place,p[3].place)	#related icode


def p_arithexprbin(p):
	''' arith_expression : arith_expression '+' arith_expression
						 | arith_expression '-' arith_expression
						 | arith_expression '*' arith_expression
						 | arith_expression '/' arith_expression'''
						 
	global interVar
	if p[1].type != p[3].type:			#type check
		print("Type mismatch Line no:%s"%(p.lineno(2)))
		raise SyntaxError

	elif p[2]=='+' or p[2]=='-' or p[2]=='*' or p[2]=='/' :
		p[0]= ArithOpAst(p[1],p[2],p[3],"","")
		p[0].place = "var"+str(interVar)
		interVar+=1
		p[0].code = p[1].code + p[3].code + "\t%s = %s %s %s\n"%(p[0].place,p[1].place,p[2],p[3].place)


def p_arithexpunary(p):
	''' arith_expression : '-' arith_expression %prec UMINUS '''
	global interVar
	p[0] = UnaryAst(p[2],"","")
	p[0].place = "var"+str(interVar)
	interVar+=1
	p[0].code = p[2].code  + "\t%s = 'uminus' %s\n"%(p[0].place,p[2].place)


def p_arithbrkt(p):
	''' arith_expression : '(' arith_expression ')' '''
	p[0] = p[2]

def p_arithexpterm(p):
	''' arith_expression : expression_term '''
	p[0] = p[1]

def p_logexpr(p):
	''' logic_expression : arith_expression EQ arith_expression
						 | arith_expression NE arith_expression
						 | arith_expression GT arith_expression
						 | arith_expression GE arith_expression
						 | arith_expression LT arith_expression
						 | arith_expression LE arith_expression'''

	if p[1].type != p[3].type:
		print("Type mismatch Line no:%s"%(p.lineno(2)))
		raise SyntaxError
		
	else:
		global interVar
		p[0] = RelationAst(p[1],p[2],p[3],"","")
		p[0].place = "var"+str(interVar)
		interVar+=1
		p[0].code = p[1].code + p[3].code + "\t%s := %s %s %s \n"%(p[0].place,p[1].place,p[2],p[3].place)

def p_logexp(p):
	''' logic_expression : logic_expression AND logic_expression
						 | logic_expression OR logic_expression'''
	global interVar
	p[0] = RelationAst(p[1],p[2],p[3],"","")
	p[0].place = "var"+str(interVar)
	interVar+=1
	p[0].code = p[1].code + p[3].code + "\t%s := %s %s %s \n"%(p[0].place,p[1].place,p[2],p[3].place)


def p_lognot(p):
	''' logic_expression : NT logic_expression
						 | '(' logic_expression ')' '''
	global interVar
	if len(p) == 3:			#first production
		p[0] = NotAst(p[2],"","")
		p[0].place = "var"+str(interVar)
		interVar+=1
		p[0].code = p[2].code  + "\t%s = 'NOT' %s\n"%(p[0].place,p[2].place)
	elif len(p) == 4:		#second production
		p[0] = p[2]


def p_ifelse(p):
	''' if_else_statement : IF '(' logic_expression ')' statement
						  | IF '(' logic_expression ')' statement ELSE statement '''
	global label1
	global label2
	if len(p) == 6:
		delta = SequenceAst("")
		p[0]= SelectionAst(p[3],p[5],delta,"","")
		p[0].code = "\n " + p[3].code + "\n\tif %s is false, goto Label0%d\n"%(p[3].place,label1) + p[5].code + "\n\tGoto Label1%d \nLabel 0%d:\n"%(label2,label1)  + "\nLabel1%d:\n"%(label2) 
		label2+=1
		label1+=1
	elif len(p) == 8:
		p[0]= SelectionAst(p[3],p[5],p[7],"","")
		p[0].code = "\n " + p[3].code + "\n\tif %s is false, goto Label0%d\n"%(p[3].place,label1) + p[5].code + "\n\tGoto Label1%d \nLabel 0%d:\n"%(label2,label1)  + p[7].code + "\nLabel1%d:\n"%(label2)
		label2+=1
		label1+=1

def p_condcomp(p):
	''' cond_comp : logic_expression '?' arith_expression ':' arith_expression '''
	global interVar
	global label1
	global label2
	if p[3].type != p[5].type:
		print("Type mismatch Line no:%s"%(p.lineno(2)))
		raise SyntaxError
	else:
		p[0] = ConditionAst(p[1],p[3],p[5])
		p[0].place = "var"+str(interVar)
		interVar+=1
		p[0].code = "\n " + p[1].code + "\n\tif %s is false, goto Label0%d\n"%(p[1].place,label1) + p[3].code + "\t%s = %s"%(p[0].place,p[3].place) + "\n\tGoto Label1%d \nLabel 0%d:\n"%(label2,label1)  + p[5].code + "\t%s = %s"%(p[0].place,p[5].place) + "\nLabel1%d:\n"%(label2)
		label2+=1
		label1+=1

def p_whilec(p):
	''' while_statement : WHILE '(' logic_expression ')' statement
						| DO statement WHILE '(' logic_expression ')' ';' '''
	global label1
	global label2
	if len(p) == 6:
		p[0] = IterationAst(p[3],p[5],'false',"","")
		p[0].code =  "Label 0%d:\n"%(label1) + p[3].code + "\n\tif %s is false, goto Label1%d \n"%(p[3].place,label2) + p[5].code + "\tGoto label0%d"%(label1) +"\nLabel 1%d:\n"%(label2)
		label2+=1
		label1+=1  
	elif len(p) == 8:
		p[0] = IterationAst(p[5],p[2],'true',"","")
		p[0].code =  "Label 0%d:\n"%(label1) + p[2].code +  p[5].code + "\n\tif %s is true, goto Label0%d \n"%(p[5].place,label1)
		label2+=1
		label1+=1


def p_exprterm(p):
	'''expression_term : variable '''
	p[0] = p[1]


def p_exprtermcons(p):
	''' expression_term	: constant '''
	p[0] = p[1]

        

def p_var(p):
	''' variable : NAME '''
	global interVar
	if p[1] in intnames or p[1] in flotnames:
		p[0] = NameAst(p[1])
		p[0].place = p[1]
		p[0].code = ""
	else:
		print ("Undeclared name '%s'" %(p[1]))		#undeclared variable error
		raise SyntaxError
		


def p_cons(p):
	''' constant : NUM '''
	global interVar
	p[0] = NumberAst(p[1],"int")
	p[0].place = p[1]
	p[0].code = ""

def p_consf(p):
	''' constant : FNUM '''
	global interVar
	p[0] = NumberAst(p[1],"float")
	p[0].place = p[1]
	p[0].code = "" 

def p_error(p):
    print("Syntax error at '%s'  Line no: '%d' " %(p.value,p.lineno))

parser = yacc.yacc()


parser.parse(data)
