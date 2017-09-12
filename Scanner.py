# -----------------------------------------------------------------------------
#Author : Rakshat Ranjan and Alok Kumar
# -----------------------------------------------------------------------------


import ply.lex as lex
import sys
arg1 = sys.argv[1]        # For taking input from command line.

#Dictionary of special names/IDs stored in key:value form.
# 'reserved' is not inbuilt, we could have used any variable name for declaring this dictionary data type.
reserved = {
   'if' : 'IF',
   #'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'float' : 'FLOAT',
   'int'  : 'INT',
   'void' : 'VOID',
   'do'  : 'DO', 
}


#List of all boolean and relational operators
#Didn't define them together as one type because output must show individual operator type when the associated token is matched.
#For example: Line: 12   Token Name: LT    Token: < , token name is LT rather than REL_OP or OPERATOR 
operators = [
    'AND',
    'OR',
    'EQ',
    'NT',
    'NE',
    'GE',
    'GT',
    'LE',
    'LT',
]

# List of token names.   This is always required, and cannot be declared with some other name.
# Appended with list of reserved values and operators 
tokens = [
   'FNUM',
   'NUM',
   'NAME',
   'ASSIGN_OP',
   #'ARITHOP',
   #'METACHAR',
   #'LPAREN',
   #'RPAREN',
] + list(reserved.values())  + operators
 

# A regular expression rule with some action code

#Lexemes with single-line comment is ignored
#Should be defined before division definition because of precedence
def t_COMMENT(t):
    r'//.*'
    #print("Line: %d \t Ignored lexeme" % t.lineno)
    pass

#Definition for normal type NAME tokens, as well as reserved tokens 
#get method used: if token matches with one of the values in Dictionary reserved, then that is the token type, else the default type 'NAME' 
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

#Definition for arithmetic operators. 
#Unlike operators in list 'operators', output should have them having single type name 'ARITHOP' 
#def t_myARITHOP(t):
    #r'[\+*/-]'
    #t.type = 'ARITHOP'
    #return t

#Definition of meta-characters.
#def t_METACHAR(t):
 #   r'[\{},;:)(?]'
  #  t.type = 'METACHAR'
   # return t

literals = ['(',')','{','}', ',' , ';', ':', '?', '+', '-', '*', '/' ]

# Regular expression rules for simple tokens
t_EQ = r'\=='
t_ASSIGN_OP = r'\='
t_AND     = r'\&&'
t_OR      = r'\|\|'
t_NE = r'\!='
t_NT     = r'\!'
t_GE = r'\>='
t_GT   = r'\>'
t_LE  = r'\<='
t_LT    = r'\<'

#changes made
#t_LPAREN = r'\('
#t_RPAREN = r'\)'

def t_FNUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)    
    return t
    
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)    
    return t

#Definition of new print function we use for our purpose
def myprint(t):
    print("Line: %d \t Token Name: %s \t Token: %s" % (t.lineno,t.type,t.value))


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

# Build the lexer
lexer = lex.lex()

#Input data read from file, and being converted into string
with open(arg1, 'r') as myfile:
    data=myfile.read()

lexer.input(data)

# Tokenize
#while True:
    #tok = lexer.token()
    #if not tok: 
     #   break      # No more input
    #myprint(tok)


    
