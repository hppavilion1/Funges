from random import choice #For the ? instruction
import re #To simplify instruction mapping when an instruction is a group
from stack import stack #The stack (as Befunge is a stack-based language)
from BefungeLexer import lex #The lexer function
from BefungeHelpers import *

class IP:
    def __init__(self, pos, self.delta):
        global direcs
        sm = False #Is in string mode?
        self.state = None
        self.pos = pos #Instruction Pointer Position
        self.delta = delta #Instruction Pointer self.delta (N|NE|E|SE|S|SW|W|NW)
        self.vector = direcs[self.delta] #Vector mapped to the self.delta

    def __call__(self, ins):
        global direcs
        if sm: #Only applies in string mode
            if ins == '>': #Go East
                self.delta = 'E'

            elif ins == '<': #Go West
                self.delta = 'W'

            elif ins == '^': #Go North
                self.delta = 'N'

            elif ins == 'v': #Go South
                self.delta = 'S'

            elif ins == '?': #Go Away
                self.delta = choice(direcs.keys())

            elif ins == ']': #Turn Right
                if self.delta == 'N':
                    self.delta = 'E'
                elif self.delta == 'NE':
                    self.delta = 'SE'
                elif self.delta == 'E':
                    self.delta = 'S'
                elif self.delta == 'SE':
                    self.delta = 'SW'
                elif self.delta == 'S':
                    self.delta = 'W'
                elif self.delta == 'SW':
                    self.delta = 'NW'
                elif self.delta == 'W':
                    self.delta = 'N'
                elif self.delta == 'NW':
                    self.delta = 'NE'

            elif ins == '[': #Turn Left
                if self.delta == 'N':
                    self.delta = 'W'
                elif self.delta == 'NE':
                    self.delta = 'NW'
                elif self.delta == 'E':
                    self.delta = 'N'
                elif self.delta == 'SE':
                    self.delta = 'NE'
                elif self.delta == 'S':
                    self.delta = 'E'
                elif self.delta == 'SW':
                    self.delta = 'SE'
                elif self.delta == 'W':
                    self.delta = 'S'
                elif self.delta == 'NW':
                    self.delta = 'SW'

            elif ins == 'r': #Reflect
                self.delta = value2key(direcs, (direcs[self.delta][0]*-1, direcs[self.delta][1]*-1))

            elif ins == 'x': #Absolute Vector
                dy = s.pop()
                dx = s.pop()

                self.delta = value2key(direcs, (dx, dy))

            elif ins == '#': #Trampline
                loc[0] += self.vector[0]
                loc[1] += self.vector[1]

            elif ins == '@': #Stop instruction
                self.delta = None
            
        else:
            pass

        if self.delta in direcs:
            self.vector = direcs[self.delta]
            
            loc[0] += self.vector[0]
            loc[1] += self.vector[1]
        else:
            raise BefungeError('Invalid self.delta')

        if self.vector[0] == 0 and self.vector[1] == 0:
            self.state = 'stopped'
            
        elif self.vector[0] == 0 or self.vector[1] == 0:
            self.state = 'moving'

        else:
            self.state = 'flying'

def execute(script): #Execute a lexed script
    s = stack()

    while len(pointers)>0:
        for x in pointers:
            x(script[x.pos[0]][x.pos[1]])

def interpret(script):
    return(execute(lex(script)))
