import sys


var_map = dict()
lookahead_list = list()
lookahead = None
lookahead_counter = -1
counter = 0

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
            try:
                return int(self.data)
            except ValueError:
                return float(self.data)

def main():
    global lookahead

# Check command line arguments
if len(sys.argv) != 2:
    print("Usage: %s filename" % sys.argv[0])
    sys.exit(1)

    file = open(sys.argv[1], "r")
    wlist = file.read().split()

    user_input = iter(wlist)

    prog()

def perror(expected, got):
    print("Syntax error: Expected %s but got %s" % (expected, got))
    print("Lookahead_ounter: %d" % lookahead_counter)
    print("Tokens: %s" % lookahead)
    sys.exit(1)

def lexan():
    global lookahead, lookahead_counter

    lookahead_counter += 1   #Move to next token
    if lookahead_counter >= len(lookahead_list):
        lookahead = None
        return

    # have pointer go to the new index in the list
    lookahead = lookahead_list[lookahead_counter]


def match(ch):
    global lookahead

    if ch == lookahead:
        lookahead = lexan()

    else:
        print("Syntax Error")

exit()

if lookahead == '':
    print("pass")
else:
    print("Syntax Error")


# <prog> ::= <decl-list> <stmt-list>
def prog():
    global lookahead
    lexan()
    decl_list() # Evaluate the variable declarations
    stmt_list() # Evaluate each statement (call the stmt_list function)

# <decl-list> ::= <decl> { <decl> }
def decl_list():
    global lookahead
    while ((lookahead == 'int') or (lookahead == 'real')):
        decl()


# <decl> ::= <type> <id_list> ;
def decl():
    var_type = type()
    var_list = id_list()

    for var in var_list:
        var_map[var] = Variable(var, None, var_type)

        # Check for semi-colon

        if lookahead != ';':
            perror(';', lookahead)

        lexan()

# <type> ::= int | real
def get_type():
        if ((lookahead == 'int') or (lookahead == 'real')): # is it a valid type?
            var_type = lookahead # store the lookahead as type
            lexan()
            return var_type

# <id_list> ::= id { , id }
def id_list():
    global lookahead
    user_var = [lookahead]  # Save current lookahead as a variable
    lexan()
    vars.extend(id_list())

# <stmt_list> ::= <stmt> { <stmt> }
def stmt_list():
    global lookahead
    global var_map

    if lookahead in var_map:   # If the variable = <expr>
        var = var_map[lookahead]
        lexan() # next token or lookahead

        # Now we can check if the id is followed by an '=' sign
        if lookahead != '=':
            perror('=', lookahead)
        lexan()

        right_expr = expr()

        # Does the statement end with a semi-colon ';' ?
        if lookahead != ';':
            perror(';', lookahead)
        lexan()

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
    global lookahead
    expr()

# <expr> ::= <term> { + <term> | - <term> }
def expr(getType):

    global lookahead
    while ((lookahead == "+") or (lookahead == "-")):
        if lookahead == "+":
            match('+')

        elif lookahead == "-":
            match('-')



# <term> ::= <factor> { * <factor> | / <factor> }
def term():
    global lookahead

    while (lookahead == "*") or (lookahead == "/"):
        if lookahead == "*":
            match('*')
            global lookahead_counter
            lookahead_counter += term()

        elif lookahead == "/":
            match('/')
            lookahead_counter -= term()

# <factor> ::= <base> ^ <factor> | <base>
def factor(getType):
    global lookahead


# <base> ::= ( <expr> ) | id | intnum
def base():
  global lookahead
  if lookahead == "(":  # Parenthesis
      lexan()  # token -> <expr>

      # Evaluate the left-hand expression
      left_expr = expr()

      # Check if there is a closing parenthesis
      if lookahead != ")":
          op = Node(lookahead)  # Save operator Node
          lexan()  # token -> <right-hand expr>

          # Evaluate the right side of expression
          right_expr = expr()

          # Set the left and right Nodes as children to the operator Node and
          # set the operator Node as the new left Node
          op.add_child(left_expr)
          op.add_child(right_expr)
          left = op
      lexan()  # token -> <next token>

      # Return only the final "left" Node
      return left_expr
  else:  # Number or variable
      base = Node(lookahead)  # Save token Node
      lexan()  # token -> <next token>

      # Return the final "base" Node
      return base


# <oprnd> ::= id | intnum
def oprnd():

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

main()

