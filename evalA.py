import sys


var_map = {}
var_list = []
lookahead_list = list()
lookahead = None
lookahead_counter = -1
counter = 0

if len(sys.argv) != 2:
    print("Usage: %s filename" % sys.argv[0])
    sys.exit(1)

file = open(sys.argv[1], "r")


class Variable:
    def __init__(self, id=None, value=None, type=None):
        self.id = id
        self.value = value
        self.type = type

class Node:
    def __init__(self, data=None):
        self.data = data
        self.children = list()

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child=0):
        self.children.remove(child)

    def eval(self):
        if self.data == '+': # Addition
            return self.children[0].eval() + self.children[1].eval()
        elif self.data == '-': # Subtraction
            return self.children[0].eval() - self.children[1].eval()
        elif self.data == '*': # Multiplication
            return self.children[0].eval() * self.children[1].eval()
        elif self.data == '/': # Division
            return self.children[0].eval() / self.children[1].eval()
        elif self.data == '^': # Factorization
            return self.children[0].eval() ** self.children[1].eval()
        elif self.data in var_map: # Variable
            var = var_map[self.data] # Save variable Object
            if var.type == 'int': # Integer type
                return int(var.value)
            elif var.type == 'real': # Real (float) type
                return float(var.value)
        else: # Number
            # Attempt to parse the number as an Integer, then Float
            try:user_var
                return int(self.data)
            except ValueError:
                return float(self.data)

def main():
    global lookahead
    print("--Main")
    # Check command line arguments


    prog()

def perror(expected, got):
    print("--Perror")
    print("Syntax error: Expected %s but got %s" % (expected, got))
    print("Lookahead_counter: %d" % lookahead_counter)
    print("Tokens: %s" % lookahead)
    sys.exit(1)

def lexan():
    global user_input
    print("--lexan")
    global lookahead
    print(lookahead, "lexan")
    try:
        return(next(user_input))
    except StopIteration:
        return ('')


def match(ch):
    print("--Match")
    global lookahead

    if ch == lookahead:
        lookahead = lexan()

    else:
        print("Syntax Error")
        exit()


# <prog> ::= <decl-list> <stmt-list>
def prog():
    print("--prog")
    global lookahead

    decl_list() # Evaluate the variable declarations
    print(lookahead,"PRO")
    if lookahead == '':
        return
    stmt_list() # Evaluate each statement (call the stmt_list function)

# <decl-list> ::= <decl> { <decl> }
def decl_list():
    print("--Decl_list")
    global lookahead
    print(lookahead)
    while ((lookahead == 'int') or (lookahead == 'real')):
        decl()


# <decl> ::= <type> <id_list> ;
def decl():
    global var_list, lookahead
    print("--Decl")
    var_type = get_type()
    id_list()

    for vara in var_list:
        var_map[vara] = var_type, None

    # Check for semi-colon
    print(var_map, "varmap")
    if lookahead != ';':
        perror(';', lookahead)
    lookahead = lexan()
    print(lookahead, "Decl")

# <type> ::= int | real
def get_type():
    global lookahead
    print("--Get_type")
    print(lookahead)
    if ((lookahead == 'int') or (lookahead == 'real')): # is it a valid type?
        print("get_type sucess")
        var_type = lookahead
        lookahead = lexan()
        print(lookahead,"type***")# store the lookahead as type
        return var_type

# <id_list> ::= id { , id }
def id_list():
    print("--Id_list")
    global var_list, lookahead
    print(lookahead,"ID")
    var_list.append(lookahead)
    lookahead = lexan()
    print(lookahead)
    if lookahead == ",":
        lookahead = lexan()
        id_list()
    print(var_list,"**var list**") # Save current lookahead as a variable

# <stmt_list> ::= <stmt> { <stmt> }
def stmt_list():
    print("--Stmt_list")
    global lookahead, var_map
    print(lookahead, "STMT")
    if lookahead in var_map:   # If the variable = <expr>
        var = var_map[lookahead]
        lookahead = lexan() # next token or lookahead
        print(lookahead, "if in var_map")
        # Now we can check if the id is followed by an '=' sign
        if lookahead != '=':
            perror('=', lookahead)
        lookahead = lexan()

        right_expr = expr()

        # Does the statement end with a semi-colon ';' ?
        if lookahead != ';':
            perror(';', lookahead)
        lookahead = lexan()
        print("Update")
        # Update variable
        var_map[var.id] = Variable(var.id, right_expr.eval(), var.type)
    elif lookahead == 'printi': #Is it an integer print statement
        lexan()

        right_expr = expr()


        # Does the statement end with a semi-colon?
        if lookahead != ';':
            perror(';', lookahead)
        lexan()

        # Display the evaluated expression as an int
        print(int(right_expr.eval()))

    elif lookahead == 'printr': # Real print statement

        lexan()


        #Evaluate

        right_expr = expr()


        # Does the statement end with a semi-colon?
        if lookahead != ';':
            perror(';', lookahead)
        lexan()


        # Display evaluated expression
        print(float(right_expr.eval()))

    else: # not valid
        perror('Variable or Print Statement', lookahead)


# <stmt> ::= id = <expr> ; | printi <expr> ; | printr <expr> ;
def stmt():
    print("--Stmt")
    global lookahead
    expr()

# <expr> ::= <term> { + <term> | - <term> }
def expr():
    print("--Expr")
    term()
    while ((lookahead == "+") or (lookahead == "-")):
        if lookahead == "+":
            match('+')

        elif lookahead == "-":
            match('-')
        



# <term> ::= <factor> { * <factor> | / <factor> }
def term():
    print("--Term")
    global lookahead
    left = factor()
    while (lookahead == "*") or (lookahead == "/"):
        if lookahead == "*":
            match('*')
            global lookahead_counter
            lookahead_counter += term()

        elif lookahead == "/":
            match('/')
            lookahead_counter -= term()

# <factor> ::= <base> ^ <factor> | <base>
def factor():
    print("--Factor")
    left = base()
    global lookahead


# <base> ::= ( <expr> ) | id | intnum
def base():
    print("--Base")
    global lookahead
    if lookahead == "(":  # Parenthesis
        lookahead = lexan()  # token -> <expr>

        # Evaluate the left-hand expression
        left_expr = expr()
        print(left_expr)

        # Check if there is a closing parenthesis
        if lookahead != ")":
            op = Node(lookahead)  # Save operator Node
            lookahead = lexan()  # token -> <right-hand expr>

            # Evaluate the right side of expression
            right_expr = expr()

            # Set the left and right Nodes as children to the operator Node and
            # set the operator Node as the new left Node
            op.add_child(left_expr)
            op.add_child(right_expr)
            left = op
        lookahead= lexan()  # token -> <next token>

        # Return only the final "left" Node
        return left_expr
    else:  # Number or variable
        print(lookahead, "baseelse")
        base = Node(lookahead)  # Save token Node
        lookahead = lexan()  # token -> <next token>

        # Return the final "base" Node
        return base

def oprnd():
    print("--Oprnd")
    global lookahead
        
    print(lookahead)

# <oprnd> ::= id | intnum
def cond():
    print("--cond")
    global lookahead

  # <oprnd> < <oprnd>
    if lookahead == '<':
        match('<')
        # <oprnd> <= <oprnd>
    elif lookahead == '<=':
        match('<=')
        # <oprnd> > <oprnd>
    elif lookahead == '>':
        match('>')
        # <oprnd> >= <oprnd>
    elif lookahead == '>=':
        match('>=')
        # <oprnd> == <oprnd>
    elif lookahead == '==':
        match('==')
        # <oprnd> != <oprnd>
    elif lookahead == '!=':
        match('!=')
    else:
        perror("Invalid", lookahead)

print("start")
for line in file:
        print(line)
        wlist = line.split()
        user_input = iter(wlist)
        print(wlist)
        lookahead = lexan()
        print(lookahead)
        main()

if lookahead == '':
    print("pass") #print pass if the text file fits the grammar
else:
    print("Syntax error") #throw an error if it doesn't'
