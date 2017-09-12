# -----------------------------------------------------------------------------
#Author : Rakshat Ranjan and Alok Kumar
# -----------------------------------------------------------------------------
import sys
arg1 = sys.argv[1]        # For taking input from command line.
with open(arg1, 'r') as myfile:
    data=myfile.read()

outfile =  arg1.replace('parse', 'icode')
outfile = outfile.replace('.c', '.c.ic')
filebuff = open(outfile, 'w')	# output file for icode, can be found in directory testcases/icode
outfile2 = outfile.replace('icode','ast')
outfile2 = outfile2.replace('.c.ic','.c.ast')
filebuf = open(outfile2, 'w')	#output file for ast, can be found in directory testcases/ast


# variables will be first stored in varvar, then stored in intnames or floatnames depending on 
# whether FLOAT or INT comes before variable list, then accordingly will be stored in symbol table
intnames = []
flotnames = []
varvar = []

#SymbolTable
symtab = {
	'int': [],
	'float': [],
	'void' : []

}
#from parserast import *
#For generating new variables in intermediate code
interVar = 0	
varStr = "var"

#For labels in icode
label1 = 0
label2 = 0
#For purpose of ast file inendation
sequenceString = "    "
astString = "       "
subastString = "          "

#Base class
class Expr: pass

#For arithmetic operators
class ArithOpAst(Expr):
    global astString
    global subastString
    def __init__(self,left,op,right,place,code):		#constructor
        
        self.left = left
        self.right = right
        self.op = op
        if self.left.type == 'int':
        	self.type  = 'int'
        elif self.left.type == 'float':
        	self.type = 'float'
       	self.code = code
        self.place = place

    def numprint(self):				#print function
    	print >> filebuf, "\n %s Arith: %s \n %s LHS (" % (astString,self.op, subastString),
    	self.left.numprint()
    	print >> filebuf, ")"
    	print >> filebuf, "%s  RHS (" %(subastString),
    	self.right.numprint()
    	print >> filebuf, ")",

	
#For program rule at the top
class ProgramAst(Expr):
	def __init__(self,left):
		self.left = left
		print >> filebuf, "Program:"
		print >> filebuf, "\t Procedure : main, Return Type : void"
		self.left.numprint()


#For Assignment statement
class AssignAst(Expr):
	global astString
	def __init__(self,left,right,place,code):
		self.left = left
		self.right = right
		self.place =place
		self.code = code

	def numprint(self):
		print >> filebuf, " \n%s Asgn: \n %s LHS(" %(astString,subastString),
		self.left.numprint()
		print >> filebuf, ")" 
		print >> filebuf, " %s RHS(" %(subastString), 
		self.right.numprint()
		print >> filebuf, ")", 


#For UnaryOperator
class UnaryAst(Expr):
	global subastString
	def __init__(self,left,code,place):
		self.code = code
		self.left = left
		if self.left.type == 'int':
			self.type = 'int'
		elif self.left.type == 'float':
			self.type = 'float'

		self.place = place	

	def numprint(self):
		print >> filebuf, "\n %s Arith : UMINUS \n %s     LHS (" %(subastString,subastString),  #%s ) " %(left)
		self.left.numprint()
		print >> filebuf, ")",


#For Relational Operator except NOT
class RelationAst(Expr):
	global subastString
	global astString
	def __init__(self,left,op,right,place,code):
		self.left = left
		self.op = op
		self.right = right
		self.place =place
		self.code = code

	def numprint(self):
		print >> filebuf, "\n %s Condition : %s \n \t %s LHS (" %(subastString,self.op,astString),
		self.left.numprint()
		print >> filebuf, ")" 
		print >> filebuf, "\t %s RHS (" %(astString),
		self.right.numprint(),
		print >> filebuf, ")",


#For Procedure Definition
class ProcedureAst(Expr):
	def __init__(self,left,op,right,code):
		self.left=left
		self.op=op
		self.right = right
		self.code = code

	def numprint(self):
		self.right.numprint()


#For statement list
class SequenceAst(Expr):
	global sequenceString
	def __init__(self,code):
		self.aststmt = []
		self.code = code
		
	def numprint(self):
		print >> filebuf, " \n %s Sequence Ast: \n" %(sequenceString)
		
		if len(self.aststmt)!=0 :
			for ast in self.aststmt:
				ast.numprint()		
	
	def pushbach(self,ast):		#For appending statements into the statement list
		self.aststmt.append(ast)


#For if-else statement
class SelectionAst(Expr):
	def __init__(self,cond,thenp,elsep,code,place):
		self.cond = cond
		self.thenp = thenp
		self.elsep = elsep
		self.code = code
		self.place =place

	def numprint(self):
		print >> filebuf, "\n%s IF :  \n %s CONDITION (" %(astString,astString),
		self.cond.numprint()
		print >> filebuf, ")"
		print >> filebuf, "%s THEN (" %(astString)
		self.thenp.numprint()
		print >> filebuf, ")"
		print >> filebuf, "%s ELSE (" %(astString)
		if self.elsep != "NULL":
			
			self.elsep.numprint()
		print >> filebuf, ")"


#For while, do-while statement
class IterationAst(Expr):
	global astString

	def __init__(self,cond,body,doform,place,code):
		self.cond = cond
		self.body = body
		self.doform = doform
		self.place = place
		self.code = code

	def numprint(self):
		if self.doform == "false":
			print >> filebuf, "\n%s WHILE :  \n %s CONDITION (" %(astString,astString),
			self.cond.numprint()
			print >> filebuf, ")"
			print >> filebuf, "%s BODY (" %(astString)
			self.body.numprint()
			print >> filebuf, ")"
		else:
			print >> filebuf, "\n%s DO (" %(astString)
			self.body.numprint()
			print >> filebuf, ")"
			print >> filebuf, "\n%s WHILE CONDITION (" %(astString)
			self.cond.numprint()
			print >> filebuf, ")"	


#For conditional expression
class ConditionAst(Expr):
	def __init__(self,cond,left,right):
		self.cond = cond
		self.left = left
		self.right = right
		if self.left.type == 'int':
			self.type = 'int'
		elif self.left.type == 'float':
			self.type = 'float'

	def numprint(self):
		print >> filebuf, "\n%s Arith : Conditional \n %s CONDITION (" %(astString,astString),
		self.cond.numprint()
		print >> filebuf, ")"
		print >> filebuf, "%s LHS (" %(astString)
		self.left.numprint()
		print >> filebuf, ")"
		print >> filebuf, "%s RHS (" %(astString)
		self.right.numprint()
		print >> filebuf, ")"



#For NOT operator
class NotAst(Expr):
	def __init__(self,left,place,code):
		self.place = place
		self.left = left
		self.code = code

	def numprint(self):
		print >> filebuf, "\n %s Condition : NOT \n \t %s RHS (" %(subastString,astString),
		self.left.numprint()
		print >> filebuf, ")", 


#For Variable names
class NameAst(Expr):
	global symtab

	def __init__(self,left):
		self.left = left
		if self.left in symtab['int']:
			self.type = "int"
		elif self.left in symtab['float']:
			self.type = "float"
		self.place = self.left
		self.code = ""

	def numprint(self):
		print >> filebuf, "Name : %s" %(self.left),


#For numbers
class NumberAst(Expr):
	def __init__(self,value,typedef):          
		self.type = typedef
		self.value = value
		self.place = self.value
		self.code = ""

	def numprint(self):
		if self.type == "int":
			print >> filebuf, "Num : %d" %(self.value),
		else:
			print >> filebuf, "Num : %.2f" %(self.value),