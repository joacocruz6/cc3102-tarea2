# -*- coding: UTF-8 -*-
import ply.lex as lex
import ply.yacc as yacc

#######################################################
############ LEXIC TOOLS ##############################
#######################################################

#Primero partimos definiendo los simbolos terminales de nuestro programa
#Para esto podemos modificar la gramatica para los digitos dejandolo como un
#simbolo entero
tokens=[
    "INT",
    "TRUE",
    "FALSE",
    "PLUS",
    "NAME",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "ASSIGN",
    "EQUALS",
    "LOWER",
    "GREATER",
    "LOWEREQ",
    "GREATEREQ",
    "NOTEQ",
    "NEXTINST",
    "LEFTBRACKET",
    "RIGHTBRACKET",
    "WLEFTBRACKET",
    "WRIGHTBRACKET",
    "WHILE",
    "DO",
    "IF",
    "THEN",
    "ELSE",
    "READ",
    "PRINT",
]
#Simbolos de las operaciones:
t_PLUS=r'\+'
t_MINUS=r'\-'
t_MULTIPLY=r'\*'
t_DIVIDE=r'\/'
t_EQUALS=r'\=\='#comparador de igualdad
t_LOWEREQ=r'\<\='
t_GREATEREQ=r'\>\='
t_NEXTINST=r'\;'
t_NOTEQ=r'\!\='

t_ASSIGN=r'\=' #asignacion de variables
t_LOWER=r'\<'
t_GREATER=r'\>'
t_LEFTBRACKET=r'\('
t_RIGHTBRACKET=r'\)'
t_WLEFTBRACKET=r'\{'
t_WRIGHTBRACKET=r'\}'
#reconocer saltos de linea e ignorarlos
t_ignore_newline=r'\n+'
t_ignore=r' ' #corregir el ignore
#definicion de instrucciones reservadas del lenguaje
def t_WLOOP(t):
    r'while'
    t.type='WHILE'
    return t
def t_DOLOOP(t):
    r'do'
    t.type='DO'
    return t
def t_IF(t):
    r'if'
    t.type='IF'
    return t
def t_ELSE(t):
    r'else'
    t.type='ELSE'
    return t
def t_THEN(t):
    r'then'
    t.type='THEN'
    return t
def t_READ(t):
    r'read'
    t.type='READ'
    return t
def t_PRINT(t):
    r'print'
    t.type='PRINT'
    return t
#definicion de los enteros
def t_INT(t):
    r'\d+'
    t.value=int(t.value)
    return t
#definicion de los booleanos
def t_TRUE(t):
    r'true'
    t.value=True
    return t
def t_FALSE(t):
    r'false'
    t.value=False
    return t
#definicion de las variables
def t_NAME(t):
    r'[a-z][a-z0-9]*'
    t.type='NAME'
    return t
#ciertos errores
def t_error(t):
    print("Illegal Characters '%s'" % t.value[0])
    t.lexer.skip(1)

##############################################
##########    Parser Tools    ################
##############################################
precedence=(
    ('left','PLUS','MINUS'),
    ('left','MULTIPLY','DIVIDE')
)
def p_empty(p):
    '''
    empty :
    '''
    p[0]=None
#define la derivacion en dos simbolos
def p_program_finite(p):
    '''
    program : variables NEXTINST
            | input NEXTINST
            | show NEXTINST
            | program program
    '''
    p[0]=(p[1],p[2])
#define la derivacion de un simbolo
def p_program_infinite(p):
    '''
    program : conditional
            | loop
            | empty
    '''
    p[0]=p[1]
#asignador de variables
def p_variables(p):
    '''
    variables : NAME ASSIGN  expression
    '''
    p[0]=p[1]
#comparaciones y loops
def p_conditional(p):
    '''
    conditional : IF LEFTBRACKET booleanexpression RIGHTBRACKET THEN WLEFTBRACKET program WRIGHTBRACKET
    '''
    p[0]=('if',p[3],p[7]) #todo revisar esto, no se si esta bien
def p_conditional_else(p):
    '''
    conditional : IF LEFTBRACKET booleanexpressionRIGHTBRACKET THEN WLEFTBRACKET program WRIGHTBRACKET ELSE WLEFTBRACKET program WRIGHTBRACKET
    '''
    p[0]=('ifelse',p[3],p[7],p[11]) #todo revisar
def p_loop(p):
    '''
    loop : WHILE LEFTBRACKET booleanexpression RIGHTBRACKET DO WLEFTBRACKET program WRIGHTBRACKET
    '''
    p[0]=('while',p[3],p[7])
#lectura y impresiones en pantalla
def p_show(p):
    '''
    show : PRINT LEFTBRACKET expression RIGHTBRACKET
    '''
    p[0]=('print',p[3])
def p_input(p):
    '''
    input :  NAME EQUALS READ LEFTBRACKET RIGHTBRACKET
    '''
    p[0]=('read',p[1])
#expresiones
#todo, las expresiones, que pueden ser booleanos o normales. Los booleanos pueden ser comparativos o true o false. Los otros como calc.


#Un pequeño ejemplo
def main():
    lexer=lex.lex()
    lexer.input("print 1+2; \n a=read(); \n 1!=3; \n while true==false")
    while True:
        tok=lexer.token()
        if not tok:
            break
        print(tok)


if __name__=="__main__":
    main()
