import sys
arg1 = sys.argv[1]        						# For taking input from command line.
with open(arg1, 'r') as myfile:
    data=myfile.read()

	
varnames=[]	
multipleVar=""
level=0
#parameterlist[]
#SymbolTable

EntryCount=0
varCount=0;
symbolTable = []
class SymbolEntry():
	def __init__(self, var, level):
		self.var=var
		self.level=level
		
#from parserast import *
#For generating new variables in intermediate code
interVar = 0	
varStr = "var"

#For labels in icode
label1 = 0
label2 = 0

#For numbers
class NumberAst():
	def __init__(self,value,typedef):          
		self.type = typedef
		self.value = value
		self.place = self.value
		self.code = ""
		
class NameAst():
    	def __init__(self,name):
    	    	self.left=name
    	    	self.type="variable"
    	    	self.place=self.left
    	    	self.code=""

class ArithOpAst():
	def __init__(self,left,op,right):
		self.left=left
		self.op=op
		self.right=right
		self.place=""
		self.code=""
		
class AssigOpArth():
	def __init__(self,left,right,code, place):
		self.left=left
		self.right=right
		self.place=place
		self.code=code

class GotoAst():
	def __init__(self, left, code , place):
		self.left= left
		self.code= code
		self.place= place
		
class UseStatementAst():
	def __init__(self, left ,code, place):
		self.left = left
		self.code = code
		self.place = place

class ProcedureCallAst():
	def __init__(self, left, right, code, place):
		self.left = left
		self.right = right
		self.place = place
		self.code = code

