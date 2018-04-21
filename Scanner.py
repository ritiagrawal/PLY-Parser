import ply.lex as lex
import sys
arg1 = sys.argv[2]

reserved = {
    'var' : 'VAR',
    'if' : 'IF',
	'return' : 'RETURN',
	'use' : 'USE',
	'bb' : 'BB',
	'goto' : 'GOTO',
	'struct' : 'STRUCT'
}

tokens = [
    'NUM',
    'NAME',
    'ASSIGN_OP',
    'ADDRESS_OP',
    'POINTER_OP',
    'STR_OP',
] + list(reserved.values())

def t_COMMENT(t):
    r'//.*'
    pass

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

literals = ['(',')','{','}', ',' , ';','-','+', ':', '?','<' ,'>' , '[' , ']' ]

# Regular expression rules for simple tokens
t_ASSIGN_OP = r'\='
t_ADDRESS_OP = r'\&'
t_POINTER_OP=r'\*'
t_STR_OP=r'\->'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t
	
#Definition of new print function we use for our purpose
def myprint(t):
    print("Line: %d \t Token Name: %s \t\t Token: %s" % (t.lineno,t.type,t.value))

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    t.lexer.lineno += len(t.value)
    #print("Line: %d \t Ignored NEWLINE character" % t.lineno)
    
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Line: %d \t Illegal character '%s'" % (t.lineno,t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

with open(arg1, 'r') as myfile:
    data=myfile.read()
	
lexer.input(data)