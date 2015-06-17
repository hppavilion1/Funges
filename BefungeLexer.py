def lex(script): #Lex a script
    script=script.split('\n') #Split newlines
    
    for x in range(len(script)): #Take each line and split it into individual characters
        script[x]=[y for y in script[x]]
        
    return(script)
