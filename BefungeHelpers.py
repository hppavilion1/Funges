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
        'NW':(-1,  1),
        None:(0,   0)
        }
