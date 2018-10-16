import sys

# lexan interates through the input file until there is nothing left
def lexan():
    global user_input
    try:
        return(next(user_input))
    except StopIteration:
        return('')

def match(ch):
    global lookahead
    if ch == lookahead:
        lookahead = lexan() # Get the next token
        return True
    else:
        return False

#get_ID checks if lookahead is in dictionary or if it is a keyword. If not - store in the dictionary
def get_ID():
    global lookahead
    global dict
    python_keywords = ["printi","printr","int","real"]
    if lookahead in dict.keys():
        #ID is already in the dictionary
        print("Syntax Error")
        sys.exit(1)
        return False
    elif lookahead in python_keywords:
        # Cannot use keyword as and ID
        print("Syntax Error:")
        sys.exit(1)
        return False
    else:
        #Success
        dict[lookahead] = None
        #print(dict)
        return True

#checks if string is real number
def is_real(tempString):
    try:
        float(tempString)
        return True
    except ValueError:
        return False

#checks if string is int number
def is_int(tempString):
    try:
        int(tempString)
        return True
    except ValueError:
        return False

# <prog> ::= <decl-list> <stmt-list>
def prog():
    global lookahead
    while (lookahead != ""):
        decl_list()
        stmt_list()

# <decl-list> ::= <decl> { <decl> }
def decl_list():
    global lookahead
    
    while((lookahead == "int") or (lookahead == "real")):
        decl()
# <decl> ::= <type> <id_list> ;
def decl():
    global lookahead
    type()
    id_list()
    #check for a semi-colon
    if not match(";"):
        print("Syntax Error")
       
# <type> ::= int | real
def type():
    global lookahead
    typeList = ["int","real"]
    if lookahead in typeList:
        
        lookahead = lexan()

# <id_list> ::= id { , id }
def id_list():
    global lookahead
    #Has ID been declared in the dictionary already?
    if get_ID(): # Does get_ID return True?
       lookahead = lexan()  #Get next token
    else:
       print("Syntax Error")
       sys.exit(1)
    if match(","): # Is there a comma?
        id_list()  #Call id_list until all ID's are in the list


# <stmt_list> ::= <stmt> { <stmt> }
def stmt_list():
    global lookahead
    global dict
    #do while input equals (a declared id, printi, printr)
    while((lookahead in dict.keys()) or (lookahead == "printi") or (lookahead == "printr")):
        stmt()

# <stmt> ::= id = <expr> ; | printi <expr> ; | printr <expr> ;
def stmt():
    global lookahead
    global dict
    global Print_results
    if(lookahead in dict.keys()): # Is the ID in the dictionary?
        id = lookahead
        idVal = 0.0  # floating point number
        lookahead = lexan()  # Call next token
        if(match("=")):   # Is there an equal sign?
            idVal = expr()
            if(match(";")):  # Is there a semi-colon?
                dict[id] = idVal
            elif(match("if")):  # Is there an 'if'
                if(cond()):  # Carry out the if statement
                    dict[id] = idVal
                elif(match("else")):
                    dict[id] = expr()
                    if(not(match(";"))):
                        print("Need Semi-colon")
                        sys.exit(1)
                else:
                    print("Syntax Error: missing else statements")
                    sys.exit(1)
        else:
            print("Syntax Error AT = ")
            sys.exit(1)
    elif(match("printi")): #if printi in dict
        temp1 = expr()
        if(not(match(";"))):
            print("Syntax Error: missing ;")
            sys.exit(1)
        else:
            Print_results.append(int(temp1));
    elif(match("printr")): # Is printr in the dictionary?
        temp2 = expr()
        if(not(match(";"))):
            print("Need semi-colon")
            sys.exit(1)
        else:
            Print_results.append(float(temp2))
    else:
        # print(lookahead)
        print("Syntax Errors 2")
        exit(1)

# <expr> ::= <term> { + <term> | - <term> }
def expr(): #using variable v, from example in notes
    global lookahead
    v = term()
    tempList = ["+","-"]
    while (lookahead in tempList):
        if match("+"): # Is there a plus ?
            v += term()
        elif match("-"):
            # Is there a minus?
            v -= term()
        else:
            print("Syntax Errors 3")
            exit(1)
    return v

# <term> ::= <factor> { * <factor> | / <factor> }
def term():
    global lookahead
    v = factor()
    mdlist = ["*","/"]
    while (lookahead in mdlist):
        if match("*"):
            v *= factor() # Carry out the multiplication
        elif match("/"):
            v /= factor()  # Carry out the division
        else:
            print("Syntax Error")
            sys.exit(1)
    return v

# <factor> ::= <base> ^ <factor> | <base>
#factor() sees if the lookahead = "^" then performs the base() operation
def factor():
    global lookahead
    v = base()
    if match("^"):
        #print("FOUND ^ ")
        v = v ** factor() #<factor> ::= <base> ^ <factor>
    return v

# <base> ::= ( <expr> ) | id | intnum
def base():
    global lookahead
    global dict
    if match("("): #::= ( <expr> )
        temp = expr()
        if(not(match(')'))):
            print("Syntax Error: missing ) bracket")
            exit(1)
        return temp
    elif(lookahead in dict.keys()): #if id in dict
        temp = dict[lookahead]
        lookahead = lexan()
        return temp
    elif(is_real(lookahead)): #if 
        temp = float(lookahead)
        lookahead = lexan()
        return temp
    elif(is_int(lookahead)): #if intnum
        v = int(lookahead)
        lookahead = lexan()
        return v
    else:
        print("Syntax error")
        sys.exit(1)
        
# <oprnd> ::= id | intnum
def cond():
    global lookahead
    pointer1 = oprnd()
    #<cond> ::= <oprnd> < <oprnd> |
    if match("<"):
        pointer2 = oprnd()
        return pointer1 < pointer2
        #<oprnd> <= <oprnd> |
    elif match("<="): 
        pointer2 = oprnd()
        return pointer1 <= pointer2
        #<oprnd> > <oprnd> |
    elif match(">"): 
        pointer2 = oprnd()
        return pointer1 > pointer2
        #<oprnd> >= <oprnd> |
    elif match(">="): 
        pointer2 = oprnd()
        return pointer1 >= pointer2
        #<oprnd> == <oprnd> |
    elif match("=="): 
        pointer2 = oprnd()
        return pointer1 == pointer2
        #<oprnd> != <oprnd>
    elif match("!="): 
        pointer2 = oprnd()
        return pointer1 != pointer2
    else:
        print("Syntax Error at COND")
        exit(1)

# <oprnd> ::= id | intnum
def oprnd():
    global lookahead
    global dict
    if(lookahead in dict.keys()):
        temp = dict[lookahead]
        lookahead = lexan()
        return temp
    elif(is_real(lookahead)):
        temp = float(lookahead)
        lookahead = lexan()
        return temp
    else:
        print("Syntax Error")
        sys.exit(1)



file = open(sys.argv[1],"r") # open the test file
wlist = file.read().split() # read the test file, split the test file
user_input = iter(wlist) #store test file in user_input
lookahead = lexan() #Get new token
dict = {}   # This will be the dictionary to store our variables
Print_results = []  #This is where our results from the test file will be stored
prog()
if lookahead == "":
    for line in Print_results:  # This is just printing the results from Print_results list
        print(line)
else:
    print("Syntax Error")