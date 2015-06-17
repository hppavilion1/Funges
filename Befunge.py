from random import choice #For the ? instruction
import re #To simplify instruction mapping when an instruction is a group
from stack import stack #The stack (as Befunge is a stack-based language)
from BefungeLexer import lex #The lexer function
from BefungeHelpers import *

class IP:
    def __init__(self, pos, delta):
        global direcs
        sm = False #Is in string mode?
        self.state = None
        self.pos = pos #Instruction Pointer Position
        self.delta = delta #Instruction Pointer delta (N|NE|E|SE|S|SW|W|NW)
        self.vector = direcs[self.delta] #Vector mapped to the delta

def execute(script): #Execute a lexed script
    global direcs
    pointers = [IP((0, 0), 'E')]
    s = stack()

    while len(pointers)>0:
        for pointer in pointers: #Iterate through pointers epointerecuting commands
            if sm: #Only applies in string mode
                if ins == '>': #Go East
                    pointer.delta = 'E'

                elif ins == '<': #Go West
                    pointer.delta = 'W'

                elif ins == '^': #Go North
                    pointer.delta = 'N'

                elif ins == 'v': #Go South
                    pointer.delta = 'S'

                elif ins == '?': #Go Away
                    pointer.delta = choice(direcs.keys())

                elif ins == ']': #Turn Right
                    if pointer.delta == 'N':
                        pointer.delta = 'E'
                    elif pointer.delta == 'NE':
                        pointer.delta = 'SE'
                    elif pointer.delta == 'E':
                        pointer.delta = 'S'
                    elif pointer.delta == 'SE':
                        pointer.delta = 'SW'
                    elif pointer.delta == 'S':
                        pointer.delta = 'W'
                    elif pointer.delta == 'SW':
                        pointer.delta = 'NW'
                    elif pointer.delta == 'W':
                        pointer.delta = 'N'
                    elif pointer.delta == 'NW':
                        pointer.delta = 'NE'

                elif ins == '[': #Turn Left
                    if pointer.delta == 'N':
                        pointer.delta = 'W'
                    elif pointer.delta == 'NE':
                        pointer.delta = 'NW'
                    elif pointer.delta == 'E':
                        pointer.delta = 'N'
                    elif pointer.delta == 'SE':
                        pointer.delta = 'NE'
                    elif pointer.delta == 'S':
                        pointer.delta = 'E'
                    elif pointer.delta == 'SW':
                        pointer.delta = 'SE'
                    elif pointer.delta == 'W':
                        pointer.delta = 'S'
                    elif pointer.delta == 'NW':
                        pointer.delta = 'SW'

                elif ins == 'r': #Reflect
                    pointer.delta = value2key(direcs, (direcs[pointer.delta][0]*-1, direcs[pointer.delta][1]*-1))

                elif ins == 'pointer': #Absolute Vector
                    dy = s.pop()
                    dx = s.pop()

                    pointer.delta = value2key(direcs, (dx, dy))

                elif ins == '#': #Trampoline
                    loc[0] += self.vector[0]
                    loc[1] += self.vector[1]

                elif ins == '@': #Stop
                    pointer.delta = None

                elif ins == ';': #Jump Over (to be implemented)
                    pass

                elif ins == 'j'
            
        else:
            pass

        if self.delta in direcs:
            pointer.vector = direcs[pointer.delta]
            
            pointer.loc[0] += pointer.vector[0]
            pointer.loc[1] += pointer.vector[1]
        else:
            raise BefungeError('Invalid delta')

        if pointer.vector[0] == 0 and pointer.vector[1] == 0:
            pointer.state = 'stopped'
            
        elif pointer.vector[0] == 0 or pointer.vector[1] == 0:
            pointer.state = 'moving'

        else:
            pointer.state = 'flying'
            
        for pointer in range(len(pointers)): #Delete stopped pointers
            if pointers[pionter].state == 'stopped': 
                del pointers[x]

def interpret(script):
    return(execute(lex(script)))
