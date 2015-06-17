from random import choice #For the ? instruction
import re #To simplify instruction mapping when an instruction is a group
from stack import stack #The stack (as Befunge is a stack-based language)

class BefungeError(Exception):
    pass

def value2key(dictionary, desiredvalue): #Search a dict for a value and return the first key mapping to it
    for key, value in dictionary.items():
        if value == desiredvalue:
            return key

def lex(script): #Lex a script
    script=script.split('\n') #Split newlines
    for x in range(len(script)): #Take each line and split it into individual characters
        script[x]=[y for y in script[x]]
        
    return(script)

def execute(script): #Execute a lexed script
    loc = (0, 0) #The Instruction Pointer (IP)
    s = stack()
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
    
    delta = 'E' #The direction of the IP

    sm = False #Is in string mode?

    while not script[loc[0]][loc[1]] == '@':
        ins = script[loc[0]][loc[1]]
        
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

            elif ins == 'r':
                delta = value2key(direcs, (direcs[delta][0]*-1, direcs[delta][1]*-1))
                

        if delta in direcs:
            loc[0] += direcs[delta][0]
            loc[1] += direcs[delta][1]
        else:
            raise BefungeError('Invalid Delta')
 
def interpret(script):
    return(execute(lex(script)))
