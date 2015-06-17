from lexer import lex
from executer import execute

def interpret(script):
    return(execute(lex(script)))
