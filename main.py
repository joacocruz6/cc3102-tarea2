# -*- coding: UTF-8 -*-
import ply.lex as lex
import ply.yacc as yacc

#Primero partimos definiendo los simbolos terminales de nuestro programa
#Para esto podemos modificar la gramatica para los digitos dejandolo como un
#simbolo entero
tokens=[
    "INT",
    "PLUS",
    "NAME",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "ASIGN",
    "EQUALS",
    "LOWER",
    "GREATER",
    "LOWEREQ",
    "GREATEREQ"
]
#Simbolos de las operaciones:
t_PLUS=r'\+'
t_MINUS=r'\-'
t_MULTIPLY=r'\*'
t_DIVIDE=r'\/'
t_EQUALS=r'\=\='#comparador de igualdad
t_LOWEREQ=r'\<\='
t_GREATEREQ=r'\>\='

t_ASIGN=r'\=' #asignacion de variables
t_LOWER=r'\<'
t_GREATER=r'\>'
#definicion de los enteros
def t_INT(t):
    r'\d+'
    t.value=int(t.value)
    return t
#definicion de las variables
def t_NAME(t):
    r'[a-z][a-z0-9]*'
    t.type='NAME'
    return t
def t_error(t):
    print("Illegal Characters in the program!")
    t.lexer.skip(1)

#Un pequeño ejemplo
def main():
    lexer=lex.lex()
    lexer.input("1<=2")
    while True:
        tok=lexer.token()
        if not tok:
            break
        print(tok)



if __name__=="__main__":
    main()
