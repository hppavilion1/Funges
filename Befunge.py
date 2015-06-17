#TBI = To Be Implemented (indicates incomplete feature)
#TBR = To Be Reimplemented (indicates shittily done feature)

import os #For system execution
from random import choice #For the ? instruction
import time #For y instruction
import sys  #For argvs

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

def execute(script rettype='return'): #Execute a lexed script
    global direcs
    pointers = [IP((0, 0), 'E')]
    s = stack() 
    s.push(stack())#Befunge-98-style Stack Stack.

    def TOSSpop():
        toss = s.pop()
        r = toss.pop()
        s.push(toss)
        return r

    def TOSSpopstr():
        p = None
        r = ''
        while p != '\0':
            p = TOSSpop()
            r += str(p)
        return r

    def TOSSpush(v):
        toss = s.pop()
        toss.push(v)
        s.push(toss)
    
    while len(pointers)>0:
        ipid = 0
        for pointer in pointers: #Iterate through pointers epointerecuting commands
            ins = script[pointer.loc[1]][pointer.loc[0]]
            if pointer.sm: #Only applies in string mode
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

                elif ins == ']': #Turn Right (TBR)
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

                elif ins == '[': #Turn Left (TBR)
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

                elif ins == 'x': #Absolute Vector
                    dy = TOSSpop()
                    dx = TOSSpop()

                    pointer.delta = value2key(direcs, (dx, dy))

                elif ins == '#': #Trampoline
                    pointer.loc[0] += pointer.vector[0]
                    pointer.loc[1] += pointer.vector[1]

                elif ins == '@': #Stop
                    pointer.delta = None

                elif ins == ';': #Jump Over
                    while not script[pointer.loc[1]][pointer.loc[0]] == ';':
                        pointer.loc[0] += pointer.vector[0]
                        pointer.loc[1] += pointer.vector[1]

                elif ins == 'j': #Jump Forward
                    for x in range(TOSSpop()):
                        pointer.loc[0] += pointer.vector[0]
                        pointer.loc[1] += pointer.vector[1]

                elif ins == 'q': #Quit
                    break

                elif ins == 'k': #Iterate
                    todo = TOSSpop()
                    pointer.loc[0] += pointer.vector[0]
                    pointer.loc[1] += pointer.vector[1]
                    ins = script[pointer.loc[1]][pointer.loc[0]]
                    subscript = ins*todo
                    state = execute(subscript, 'state')
                    s = state[0]
                    pointers = state[1]

                elif ins == '!': #Negate
                    TOSSpush(int(not TOSSpop()))

                elif ins == '`': #Greater Than
                    TOSSpush(int(TOSSpop() > TOSSpop()))

                elif ins == '_': #Horizontal if
                    if TOSSpop():
                        pointer.delta = 'W'
                    else:
                        pointer.delta = 'E'

                elif ins == '|': #Vertivle if
                    if TOSSpop():
                        pointer.delta = 'S'
                    else:
                        pointer.delta = 'N'

                elif ins == 'w':
                    a = TOSSpop()
                    b = TOSSpop()

                    if a < b: #Turn Left
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
                            
                    elif a > b: #Turn right
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

                elif re.match(ins, r'[0-f]'): #Push 0-15 on the stack (mapped to hex)
                    TOSSpush(int(ins, 16))

                elif ins == '+': #Addition
                    TOSSpush(TOSSpop()+TOSSpop())

                elif ins == '*': #Multiplication
                    TOSSpush(TOSSpop()*TOSSpop())
                    
                elif ins == '-': #Subtraction
                    a = TOSSpop()
                    b = TOSSpop()
                    TOSSpush(b-a)

                elif ins == '/': #Division
                    a = TOSSpop()
                    b = TOSSpop()
                    try:
                        TOSSpush(b/a)
                    except ZeroDivisionError:
                        TOSSpush(raw_input())

                elif ins == '%': #Modulus
                    a = TOSSpop()
                    b = TOSSpop()
                    try:
                        TOSSpush(b%a)
                    except ZeroDivisionError:
                        s.pus(raw_input())

                elif ins == '"': #Toggle Stringmode
                    TOSSpush('\0')
                    pointer.sm = True

                elif ins == '\'': #Fetch Character
                    pointer.loc[0] += pointer.vector[0]
                    pointer.loc[1] += pointer.vector[1]

                    char = script[pointer.loc[1]][pointer.loc[0]]

                    TOSSpush(char)

                elif ins == 's': #Store Character
                    pointer.loc[0] += pointer.vector[0]
                    pointer.loc[1] += pointer.vector[1]

                    script[pointer.loc[1]][pointer.loc[0]] = TOSSpop()

                elif ins == '$': #Pop
                    TOSSpop()

                elif ins == ':': #Duplicate
                    x = TOSSpop()
                    TOSSpush(x)
                    TOSSpush(x)

                elif ins == '\\': #Swap
                    a = TOSSpop()
                    b = TOSSpop()

                    TOSSpush(a)
                    TOSSpush(b)

                elif ins == 'n': #Clear stack
                    s = stack()

                elif ins == '{': #Begin Block (???)
                    raise NotYetImplemented('The { function is Not Yet Implemented')

                elif ins == '}': #End Block (???)
                    raise NotYetImplemented('The } function is Not Yet Implemented')

                elif ins == 'u': #Stack under Stack Block (???)
                    raise NotYetImplemented('The { function is Not Yet Implemented')

                elif ins == 'g': #Get
                    y = TOSSpop()
                    x = TOSSpop()

                    TOSSpush(script[y][x])

                elif ins == 'p' #Put
                    y = TOSSpop()
                    x = TOSSpop()

                    script[y][x] = TOSSpop()

                elif ins == '.': #Output Decimal
                    print(ord(str(TOSSpop())))

                elif ins == ',': #Output Character
                    print(str(TOSSpop()))

                elif ins == '&': #Input decimal
                    TOSSpush(int(re.sub(r'[^0-9a-fA-F]', '', raw_input())), 16)

                elif ins == '~': #Input character
                    TOSSpush(getch())

                elif ins == 'i': #Input File (TBI)
                    f = TOSSpopstr()

                    flags = TOSSpop() #Flags. (TBI)
                    
                    t = open(f, 'r+').read()
                    
                    y = TOSSpop()
                    x = TOSSpop()

                    pos = (x, y)

                    for char in t:
                        script[pos[1]][pos[0]] = char
                        pos[0]+=1
                    
                elif ins == 'o': #Output File (TBI)
                    f = TOSSpopstr()

                    flags = TOSSpop() #Flags. (TBI)

                    open(f, 'w+')
    
                elif ins == '=': #Execute (system())
                    os.system(TOSSpopstr())

                elif ins == 'y': #Get SysInfo
                    yvars.append('\0'.join(sys.argv)+'\0') #Argvs
                    
                    yvars.append(0) #size-of-stack-stack cells containing size of each stack, listed from TOSS to BOSS (TBI)
                    
                    yvars.append(len(s)) #Stack stack count
                    
                    yvars.append(0) #current (hour * 256 * 256) + (minute * 256) + (second) (TBI)
                    
                    yvars.append(0) #current ((year - 1900) * 256 * 256) + (month * 256) + (day of month) (TBI)
                    
                    yvars.append(0) #greatest point which contains a non-space cell, relative to the least point 
                    yvars.append(0)
                    
                    yvars.append(0) #Least point containing a non-space cell relative to origin (TBI)
                    yvars.append(0)
                    
                    yvars.append(0) #Storage offset for current IP (?)
                    yvars.append(0)
                    
                    yvars.append(pointer.vector[1]) #Delta for current IP
                    yvars.append(pointer.vector[0])
                    
                    yvars.append(pointer.loc[1]) #Vector for current IP
                    yvars.append(pointer.loc[0])
                    
                    yvars.append(0) #Team number for current IP (!?)
                    
                    yvars.append(ipid) #IP id
                    
                    yvars.append(2) #Scalars/vector
                    
                    yvars.append(os.sep) #Separator
                    
                    yvars.append(1) #Operating Paradigm
                    
                    yvars.append(07) #Version
                    
                    yvars.append(0) #Handprint (Fix this later)
                    
                    yvars.append(4) #Bytes/cell
                    
                    flagcell = '' #Flag Cell (duh)
                    flagcell += '0'*28 #Blank space
                    flagcell += '1' #Buffers on io
                    flagcell += '0' #o implemented
                    flagcell += '0' #i implemented
                    flagcell += '1' #Concurrent
                    yvars.append(int(flagcell, 2))

                    arg = TOSSpop()
                    if int(arg)<1:
                        for var in yvars:
                            TOSSpush(var)
                    else:
                        TOSSpush(yvars[arg-1])
            elif 
                        
                    

        else: #Stringmode
            if ins != ' ' and ins != '"':
                TOSSpush(ins)
            elif ins == ' ': #Space groups processed as a single space
                while ins == ' ':
                    pointer.loc[0] += pointer.vector[0]
                    pointer.loc[1] += pointer.vector[1]

                    ins = script[pointer.loc[1]][pointer.loc[0]]

                pointer.loc[0] -= pointer.vector[0] #To avoid an off-by-one error (?)
                pointer.loc[1] -= pointer.vector[1]
                TOSSpush(' ')
            elif ins == '"':
                pointer.sm = False

        if pointer.delta in direcs:
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
            if pointers[pointer].state == 'stopped': 
                del pointers[x]
    
    if rettype == 'return':
        return TOSSpop()
    
    elif rettype == 'state':
        return (s, pointers)

def interpret(script):
    return(execute(lex(script)))
