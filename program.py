# -*- coding: UTF-8 -*-
import ply.lex as ply_lex
import ply.yacc as ply_yacc

# ------------------------------------------ LEXER GENERATION ------------------------------------------
# ------------------------------------------ ^^^^^^^^^^^^^^^^ ------------------------------------------

#                               ------------ Token Declarations ------------

# The original grammar is altered, deleting digits and changing numbers for the token INT,
# which can easily be defined through regular expressions.
tokens = [
    "INT",  # Integers identifier
    "NAME",  # Variables identifier

    "PLUS",  # Addition plus symbol
    "MINUS",  # Subtraction, or negativity, minus symbol
    "MULTIPLY",  # Multiplication star symbol
    "DIVIDE",  # Division slash symbol

    "EQUALS",  # Comparison double equals symbol
    "NOTEQ",  # Comparison different that symbol
    "LOWEREQ",  # Comparison lower or equal than symbol
    "GREATEREQ",  # Comparison greater or equal than symbol
    "LOWER",  # Comparison lower than symbol
    "GREATER",  # Comparison greater than symbol

    "ASSIGN",  # Variable assignment equals symbol
    "READ",  # Read input function delimiter
    "PRINT",  # Print output function delimiter

    "NEXTINST",  # Next instruction semicolon symbol

    "LEFTBRACKET",  # Arguments open parenthesis symbol
    "RIGHTBRACKET",  # Arguments close parenthesis symbol

    "WLEFTBRACKET",  # Instructions open parenthesis symbol
    "WRIGHTBRACKET",  # Instructions closed parenthesis symbol

    "WHILE",  # While loop condition delimiter
    "DO",  # While loop instructions delimiter

    "IF",  # If statement condition delimiter
    "THEN",  # If statement instructions delimiter
    "ELSE"  # If statement else instructions delimiter

]

#                               ------------ Symbol Assignment ------------

# Operators
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'

# Comparators
t_EQUALS = r'\=\='
t_NOTEQ = r'\!\='
t_LOWEREQ = r'\<\='
t_GREATEREQ = r'\>\='
t_LOWER = r'\<'
t_GREATER = r'\>'

# Assignment operator
t_ASSIGN = r'\='

# Instruction separator
t_NEXTINST = r'\;'

# Arguments parenthesis
t_LEFTBRACKET = r'\('
t_RIGHTBRACKET = r'\)'

# Instructions parenthesis
t_WLEFTBRACKET = r'\{'
t_WRIGHTBRACKET = r'\}'

# Ignored Symbols
t_ignore_newline = r'\n+'
t_ignore_tab = r'\t'
t_ignore = r' '

#                               ------------ Semantics of the Tokens ------------


# While loop conditions delimiter
def t_WLOOP(t):
    r'while'
    t.type = 'WHILE'
    return t


# While loop instructions delimiter
def t_DOLOOP(t):
    r'do'
    t.type = 'DO'
    return t


# If statement conditions delimiter
def t_IF(t):
    r'if'
    t.type = 'IF'
    return t


# If statement instructions delimiter
def t_THEN(t):
    r'then'
    t.type = 'THEN'
    return t


# If statement complementary instructions delimiter
def t_ELSE(t):
    r'else'
    t.type = 'ELSE'
    return t


# Read instruction definition
def t_READ(t):
    r'read\(\)'
    t.type = 'READ'
    return t


# Print instruction definition
def t_PRINT(t):
    r'print'
    t.type = 'PRINT'
    return t


# Integer definition
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Variable definition
def t_NAME(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = 'NAME'
    return t


# Error printer
def t_error(t):
    print("Illegal Characters '%s'" % t.value[0])
    t.lexer.skip(1)


# ------------------------------------------ PARSER GENERATION ------------------------------------------
# ------------------------------------------ ^^^^^^^^^^^^^^^^^ ------------------------------------------

#                               ------------ Parsing Rules ------------


# Precedence rules
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

# Program start instruction
start = 'program'


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


# Defines If statement
def p_conditional(p):
    '''
    conditional : IF expression THEN instruction
    '''
    p[0] = ('if', p[2], p[4])


# Defines If statement with else complement
def p_conditional_else(p):
    '''
    conditional : IF expression THEN instruction ELSE instruction
    '''
    p[0] = ('if else', p[2], p[4], p[6])


# Defines While loop
def p_loop(p):
    '''
    loop : WHILE expression DO instruction
    '''
    p[0] = ('while', p[2], p[4])


# Defines Assignment rule
def p_assignment(p):
    '''
    assignment : NAME ASSIGN expression
    '''
    p[0] = ('=', p[1], p[3])


# Defines the Print statement
def p_show(p):
    '''
    show : PRINT LEFTBRACKET expression RIGHTBRACKET
    '''
    p[0] = ('print', p[3])


# Defines the Read statement
def p_input(p):
    '''
    input : NAME ASSIGN READ
    '''
    p[0] = ('read', p[1])


# Defines one symbol derivation
def p_program_finite(p):
    '''
    instruction : conditional
                | loop
                | assignment NEXTINST
                | show NEXTINST
                | input NEXTINST
    '''
    p[0] = ('instruction', p[1])


def p_instruction_bracketed(p):
    '''
    instruction : WLEFTBRACKET instruction WRIGHTBRACKET
                | WLEFTBRACKET code WRIGHTBRACKET
    '''
    p[0] = ('instruction', p[2])


# Defines the Integer as an expression
def p_expression_number(p):
    '''
    expression : INT
    '''
    p[0] = p[1]


# Defines Variables as expressions
def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])


# Defines Parenthesis around expressions as expressions
def p_expression_parenthesis(p):
    '''
    expression : LEFTBRACKET expression RIGHTBRACKET
    '''
    p[0] = p[2]


# Defines Negative expressions as expressions
def p_expression_minus(p):
    '''
    expression : MINUS expression
    '''
    p[0] = ('neg', p[2])


# Defines Arithmetic operations as expressions
def p_expression_arithmetic(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression MULTIPLY expression
               | expression DIVIDE expression
               | expression EQUALS expression
               | expression LOWER expression
               | expression GREATER expression
               | expression NOTEQ expression
               | expression LOWEREQ expression
               | expression GREATEREQ expression
    '''
    p[0] = (p[2], p[1], p[3])


# Defines two symbol derivation
def p_instruction_infinite(p):
    '''
    code : instruction instruction
         | code instruction
         | instruction code
    '''
    p[0] = ('code', p[1], p[2])


def p_final(p):
    '''
    program : code
            | instruction
    '''
    run(p[1])


# Defines Errors
def p_error(p):
    print("Syntax error found when evaluating: \n"+str(p))

# ------------------------------------------ PARSE TREE EXECUTION ------------------------------------------
# ------------------------------------------ ^^^^^^^^^^^^^^^^^^^^ ------------------------------------------

#                               ------------ Program Execution Instructions ------------


# Defines the Environment Variables Dictionary
env_var = {}


# Main Execution of instructions
def run(p):  # TODO: Delete useless comments
    global env_var

    # If many instructions are being evaluated
    if type(p) == tuple:

        # Program management
        if p[0] == 'code':
            run(p[1])
            run(p[2])

        if p[0] == 'instruction':
            run(p[1])

        # Arithmetic operators
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        if p[0] == '-':
            return run(p[1]) - run(p[2])
        if p[0] == '*':
            return run(p[1]) * run(p[2])
        if p[0] == '/':
            return run(p[1]) / run(p[2])
        if p[0] == 'neg':
            return -run(p[1])

        # Comparators
        if p[0] == '==':
            return run(p[1]) == run(p[2])
        if p[0] == '!=':
            return run(p[1]) != run(p[2])
        if p[0] == '<':
            return run(p[1]) < run(p[2])
        if p[0] == '>':
            return run(p[1]) > run(p[2])
        if p[0] == '<=':
            return run(p[1]) <= run(p[2])
        if p[0] == '>=':
            return run(p[1]) >= run(p[2])

        # Assignment
        if p[0] == '=':
            env_var[p[1]] = run(p[2])

        # Variable usage
        if p[0] == 'var':
            # It may not exist
            if p[1] not in env_var:
                return "Variable have not been assigned yet"
            else:
                return env_var[p[1]]

        # If statement
        if p[0] == 'if':
            # If True, execution happens
            if int(run(p[1])) != 0:
                run(p[2])

        # If statement with complementary else
        if p[0] == 'if else':
            # a=1; if (a==2) then {print(1);} else {print(2);}

            # If True, execution happens
            if int(run(p[1])) != 0:
                run(p[2])
            # If False, the complementary instructions execute
            else:
                run(p[3])

        # While loop
        if p[0] == 'while':
            # while (1 < 2) do {print(2);}
            # a=1; while (a != 10) do {a = a + 1; print(a);}

            while int(run(p[1])) != 0:
                run(p[2])

        # Read instruction
        if p[0] == 'read':  # TODO: Fix this
            env_var[p[1]] = input('')
            return env_var[p[1]]

        # Print instruction
        if p[0] == 'print':
            print(run(p[1]))

    # If a single instruction is being evaluated
    else:
        return p


# ------------------------------------------ MAIN ------------------------------------------
# ------------------------------------------ ^^^^ ------------------------------------------

def init():
    lexer = ply_lex.lex()
    parser = ply_yacc.yacc()
    return lexer, parser


# A small example
def main():
    while True:
        filename = input("Enter filename to execute (or press enter to end):\n>> ")
        with open(filename, "r") as file:
            text = file.read()
            lexer, parser = init()
            parser.parse(text, lexer=lexer)


# Ensures program execution
if __name__ == "__main__":
    main()
