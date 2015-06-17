from random import choice #For the ? instruction
import re #To simplify instruction mapping when an instruction is a group
from stack import stack #The stack (as Befunge is a stack-based language)

class BefungeError(Exception): #Base Error Class
    pass

def value2key(dictionary, desiredvalue): #Search a dict for a value and return the first key mapping to it
    for key, value in dictionary.items():
        if value == desiredvalue:
            return key

direcs = { #A map mapping direction names to vectors
        'N' :(0,   1),
        'NE':(1,   1),
        'E' :(1,   0),
        'SE':(1,  -1),
        'S' :(0,  -1),
        'SW':(-1, -1),
        'W' :(-1,  0),
        'NW':(-1,  1)
            }

class IP:
    def __init__(self, pos, delta):
        global direcs
        sm = False #Is in string mode?
        self.pos = pos #Instruction Pointer Position
        self.delta = delta #Instruction Pointer Delta (N|NE|E|SE|S|SW|W|NW)
        self.vector = direcs[delta] #Vector mapped to the delta

    def __call__(self, ins):
        global direcs
        if sm: #Only applies in string mode
            if ins == '>': #Go East
                delta = 'E'

            elif ins == '<': #Go West
                delta = 'W'

            elif ins == '^': #Go North
                delta = 'N'

            elif ins == 'v': #Go South
                delta = 'S'

            elif ins == '?': #Go Away
                delta = choice(direcs.keys())

            elif ins == ']': #Turn Right
                if delta == 'N':
                    delta = 'E'
                elif delta == 'NE':
                    delta = 'SE'
                elif delta == 'E':
                    delta = 'S'
                elif delta == 'SE':
                    delta = 'SW'
                elif delta == 'S':
                    delta = 'W'
                elif delta == 'SW':
                    delta = 'NW'
                elif delta == 'W':
                    delta = 'N'
                elif delta == 'NW':
                    delta = 'NE'

            elif ins == '[': #Turn Left
                if delta == 'N':
                    delta = 'W'
                elif delta == 'NE':
                    delta = 'NW'
                elif delta == 'E':
                    delta = 'N'
                elif delta == 'SE':
                    delta = 'NE'
                elif delta == 'S':
                    delta = 'E'
                elif delta == 'SW':
                    delta = 'SE'
                elif delta == 'W':
                    delta = 'S'
                elif delta == 'NW':
                    delta = 'SW'

            elif ins == 'r': #Reflect
                delta = value2key(direcs, (direcs[delta][0]*-1, direcs[delta][1]*-1))

            elif ins == 'x': #Absolute Vector
                dy = s.pop()
                dx = s.pop()

                delta = value2key(direcs, (dx, dy))

            elif ins == '#': #Trampline
                loc[0] += self.vector[0]
                loc[1] += self.vector[1]

            elif ins == '@':
                del self
            
        else:
            pass

        if delta in direcs:
            self.vector = direcs[delta]
            
            loc[0] += self.vector[0]
            loc[1] += self.vector[1]
        else:
            raise BefungeError('Invalid Delta')

def lex(script): #Lex a script
    script=script.split('\n') #Split newlines
    
    for x in range(len(script)): #Take each line and split it into individual characters
        script[x]=[y for y in script[x]]
        
    return(script)

def execute(script): #Execute a lexed script
    pointers = [IP((0, 0), 'E')] #The Instruction Pointer (IP) array
    s = stack()

    while len(pointers)>0:
        for x in pointers:
            x(script[x.pos[0]][x.pos[1]])

def interpret(script):
    return(execute(lex(script)))
