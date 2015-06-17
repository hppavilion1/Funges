from BefungeLexer import lex
from BefungeExecuter import execute

def interpret(script):
    return(execute(lex(script)))
