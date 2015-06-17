def lex(script):
    script=script.split('\n')
    for x in range(len(script)):
        script[x]=[y for y in script[x]]
    return(script)
