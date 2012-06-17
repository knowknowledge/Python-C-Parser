import string

# C Keywords
# ------------------------------------------------------------------------
types = ["short", "int", "long", "float", "double", "char", "void", "bool", "FILE"]
containers = ["enum", "struct", "union", "typedef"]
modifiers = [ "const", "volatile", "extern", "static", "register", "signed", "unsigned"]
flow = [ "if", "else",
         "goto",
         "case", "default",
         "continue", "break", ]
loops = ["for", "do", "while" "switch", ]
keywords = types + containers + modifiers + flow + loops + [ "return", "sizeof" ]


prefix_operations = ["-","+","*","&","~","!","++","--"]
postfix_operations = ["++", "--"]
selection_operations = [".","->"] # Left-to-Right
multiplication_operations = ["*","/","%"] # Left-to-Right
addition_operations = ["+","-"] # Left-to-Right
bitshift_operations = ["<<",">>"] # Left-to-Right
relation_operations = ["<","<=",">",">="] # Left-to-Right
equality_operations = ["==","!="] # Left-to-Right
bitwise_operations = ["&", "^", "|"] # Left-to-Right
logical_operations = ["&&","||"]
# Ternary () ? () : ()
assignment_operations = ["=", # Right-to-Left
                        "+=","-=",
                        "/=","*=","%="
                        "<<=",">>=",
                     "&=","^=","|=",
                    ]
binary_operations = multiplication_operations + \
                    addition_operations + \
                    bitshift_operations + \
                    relation_operations + \
                    equality_operations + \
                    bitwise_operations  + \
                    logical_operations  + \
                    assignment_operations + selection_operations

operators = prefix_operations +  binary_operations
precedence = [
    selection_operations,
    multiplication_operations,
    addition_operations,
    bitshift_operations,
    relation_operations,
    equality_operations,
    ["&"],["^"],["|"],
    logical_operations,
    assignment_operations,
    ]

# Utitlity Functions
# ------------------------------------------------------------------------
def is_keyword(token):
    return token in keywords

def isonly(s,chars):
    return len(s) and all(map(lambda c: c in chars, s))

def intersection(list1,list2):
    try:
        return len(set(list1) & set(list2)) > 0
    except TypeError:
        print "Can't find the intersection of these:"
        print list1
        print list2
        assert(0)

def first_instance(haystack, needles ):
    for i,hay in enumerate(haystack):
        if hay in needles:
            return i
    raise ValueError("%s does not contain one of %s"%(str(haystack),str(needles)))

def len_type(tokens):
    index = 0
    while tokens[index] in modifiers:
        index += 1 # The modifier
    index += 1 # the type
    if tokens[index] == "*":
        index += 1 # the pointer
    return index

# Token Lexer
# ------------------------------------------------------------------------
class Token(str):
    def set(self,line=0,pos=0):
        self.line = line
        self.pos = pos
    def position(self):
        return (self.line,self.pos)
    def trim(self):
        ret = Token( str(self)[:-1] )
        ret.set(self.line, self.pos )
        return ret
    def __add__(self,other):
        ret = Token( str(self) + str(other))
        ret.set(self.line, self.pos )
        return ret

def escape_character( c, line, pos ):
    if c == "n":
        curtoken = Token("\n")
        curtoken.set(line,pos)
    elif c == "f":
        curtoken = Token("\f") # Form Feed, whatever that is
        curtoken.set(line,pos)
    elif c == "t":
        curtoken = Token("\t")
        curtoken.set(line,pos)
    elif c == "'":
        curtoken = Token("\'")
        curtoken.set(line,pos)
    elif c == '"':
        curtoken = Token("\"")
        curtoken.set(line,pos)
    elif c == '\\':
        curtoken = Token("\\")
        curtoken.set(line,pos)
    elif c == "0":
        curtoken = Token("\0")
        curtoken.set(line,pos)
    else:
        print "Lex Error at Line %d / Char %d - Character '%c' cannot be escaped" % (line, pos, c)
        #assert(0)
        curtoken = Token(c)
        curtoken.set(line,pos)
    return curtoken


def tokenize( s ):
    symbols = string.punctuation.replace("_","")
    digital = string.digits
    floating = string.digits + "."
    hexal = string.hexdigits
    line = 1
    pos = 0
    curtoken = Token("")
    curtoken.set(line,pos)
    in_string = False
    in_char = False
    in_comment = False
    in_pragma = False
    for c in s:
        pos += 1
        #print (c,curtoken)
        if in_comment or in_pragma:
            if c=="\n":
                if curtoken.startswith("//") or curtoken.startswith("#") :
                    curtoken = Token("")
                    curtoken.set(line,pos)
                    in_comment = False
                    in_pragma = False
                line += 1
                pos = 0
            elif c=='/' and curtoken.endswith("*"):
                curtoken = Token("")
                curtoken.set(line,pos)
                in_comment = False
            else:
                curtoken += c
        elif c == '"' and not in_char:
            if not in_string:
                # Start of new String
                if curtoken != "":
                    yield curtoken
                in_string = True
                curtoken = Token('"')
                curtoken.set(line,pos)
            elif len(curtoken) and curtoken[-1] == '\\':
                curtoken = Token(curtoken[:-1] + "\"")
                curtoken.set(line,pos)
            else:
                # End of String
                in_string = False
                curtoken += c
                yield curtoken
                curtoken = Token("")
                curtoken.set(line,pos)
        elif in_string:
            if curtoken.endswith('\\'):
                # Char Symbols
                #curtoken = curtoken.trim()
                #curtoken += escape_character( c, line, pos )
                curtoken += Token(c)
            else:
                curtoken += Token(c)
        elif in_char:
            if curtoken.endswith("\\"):
                # Escape this Character
                #curtoken = curtoken.trim()
                #curtoken += escape_character(c, line, pos)
                curtoken += c
            elif c == "'":
                # End of Character:
                curtoken += c
                if len(curtoken) != 3:
                    print "Lex Error at Line %d / Char %d - Character '%s' is too long." % (curtoken.line, curtoken.pos, c)
                yield curtoken
                in_char = False
                curtoken = Token("")
                curtoken.set(line,pos)
            else:
                curtoken += c
        elif c == "'" and not in_string:
            # Start of Character:
            if curtoken != "":
                yield curtoken
            curtoken = Token("'")
            curtoken.set(line,pos)
            in_char = True
        elif c == "#":
            if curtoken != "":
                yield curtoken
            curtoken = Token("#")
            curtoken.set(line,pos)
            in_pragma = True
        elif curtoken=="/" and c=="*":
            curtoken += Token(c)
            in_comment = True
        elif c == "/" and curtoken == "/":
            curtoken += Token(c)
            in_comment = True
        elif c in symbols:
            if (curtoken+c) in operators:
                curtoken = Token((curtoken+c))
                curtoken.set(line,pos)
            elif c=='.' and isonly(curtoken, floating):
                curtoken += Token(c)
            else:
                if curtoken != "":
                    yield curtoken
                curtoken = Token(c)
                curtoken.set(line,pos)
        else:
        # Non-Symbols
            if isonly(curtoken, symbols):
                yield curtoken
                curtoken = Token("")
                curtoken.set(line,pos)
            if c in string.whitespace:
                if curtoken != "":
                    yield curtoken
                if c == "\n":
                    #yield c
                    line += 1
                    pos = 0
                curtoken = Token("")
                curtoken.set(line,pos)
            # Int
            elif c in digital and isonly(curtoken,digital):
                curtoken += Token(c)
            # Float
            elif c in floating and isonly(curtoken, floating):
                curtoken += Token(c)
            # Hex
            elif curtoken.startswith("0x") and c in hexal and isonly(curtoken[2:], hexal):
                curtoken += Token(c)
            elif curtoken == "0" and c in "xX":
                curtoken += Token(c)
            else:
                curtoken += Token(c)
    if curtoken not in string.whitespace:
        yield curtoken

# Token Parser
# ------------------------------------------------------------------------
def parse_value(tokens):
    if tokens[0] in prefix_operations:
        unary = tokens.pop(0)
        value,tokens = parse_value( tokens )
        inner = ('Prefix',(unary,value))
    elif is_keyword(tokens[0]):
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Value Expected at '%s', found keyword" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    elif tokens[0] in string.punctuation:
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Value Expected at '%s', found punctuation" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    elif tokens[1] == "(":
        inner,tokens = parse_call( tokens )
    elif tokens[1] == "[":
        name = tokens.pop(0)
        if tokens[0]!="[":
            print >>sys.stderr, "Parse Error at Line %d / Char %d - Array Accessor must have '[', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
            assert(0)
        tokens.pop(0)
        index,tokens = parse_expression( tokens )
        if tokens[0]!="]":
            print >>sys.stderr, "Parse Error at Line %d / Char %d - Array Accessor must have ']', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
            assert(0)
        tokens.pop(0)
        inner = ('Index',(name, index) )
    elif tokens[0][0] == '"':
        name = tokens.pop(0)
        str = name[1:-1]
        inner = ('String',str)
    else:
        name = tokens.pop(0)
        inner = ('Value',name)
        #print "Value",name
    # Check for postfix unaray operations
    if tokens[0] in postfix_operations:
        unary = tokens.pop(0)
        #print "Value",unary,name
        inner = ('Postfix',(inner,unary))
    return inner,tokens

def parse_call(tokens ):
    name = tokens.pop(0)
    if tokens[0]!="(":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Function must have '(', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    # Get the Arguements
    arguments = []
    while len(tokens):
        # Reached end of Argument List
        if tokens[0]==")":
            break
        arg,tokens = parse_expression( tokens )
        arguments.append( arg )
        if tokens[0]!=",":
            break
        else:
            tokens.pop(0)
    
    if tokens[0]!=")":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Function must have ')', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    return ('Call',(name,arguments)),tokens

def parse_if( tokens ):
    if tokens[0] not in ["if"]:
        print >>sys.stderr, "Parse Error at Line %d / Char %d - if must start with 'if', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    if tokens[0]!="(":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - if must have '(', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    test,tokens = parse_expression( tokens )
    
    if tokens[0]!=")":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - if must have ')', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    action,tokens = parse_statement_or_block(tokens)
    
    alternative = None
    if tokens[0]=="else":
        tokens.pop(0)
        alternative,tokens = parse_statement_or_block(tokens)
    
    #print "If",test,action
    return ("If",(test,action,alternative)), tokens

def parse_while( tokens ):
    if tokens[0] not in ["while"]:
        print >>sys.stderr, "Parse Error at Line %d / Char %d - while must start with 'while', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    if tokens[0]!="(":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - while must have '(', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    test,tokens = parse_expression( tokens )
    
    if tokens[0]!=")":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - if must have ')', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    action,tokens = parse_statement_or_block(tokens)
    
    #print "While",test,action
    return ("While",(test,action)), tokens

def parse_for( tokens ):
    if tokens[0] not in ["for"]:
        print >>sys.stderr, "Parse Error at Line %d / Char %d - for must start with 'for', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    if tokens[0]!="(":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - for must have '(', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    init,tokens = parse_expression( tokens )
    
    if tokens[0]!=";":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - for must have first ';', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    test,tokens = parse_expression( tokens )
    
    if tokens[0]!=";":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - for must have second ';', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    step,tokens = parse_expression( tokens )
    
    if tokens[0]!=")":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - if must have ')', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    action,tokens = parse_statement_or_block(tokens)
    
    #print "For",init,test,step,action
    return ("For",(init,test,step,action)), tokens

def parse_cast( tokens ):
    # This enforces (int)x or (int)(x), rather than int(x), that's not quite right
    if tokens[0]!="(":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - cast must start with '(', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    # Get the Cast Type
    cast_type,tokens = parse_type(tokens)
    if tokens[0] != ")":
        for e in expression:
            print e
        print >>sys.stderr, "Parse Error at Line %d / Char %d - ')' expected after expression %s" % (tokens[0].line, tokens[0].pos, str(inner))
        assert(0)
    tokens.pop(0)
    # Get the Casted Value
    if tokens[0] == "(":
        tokens.pop(0)
        cast_value,tokens = parse_expression(tokens)
        if tokens[0] != ")":
            print >>sys.stderr, "Parse Error at Line %d / Char %d - ')' expected after expression %s" % (tokens[0].line, tokens[0].pos, str(inner))
            assert(0)
        tokens.pop(0)
    else:
        cast_value,tokens = parse_value( tokens )
    return ("Cast",(cast_type,cast_value)), tokens

def parse_expression( tokens ):
    # This should be a tree not a list
    expression = []
    while len(tokens):
        #TODO: Add Ternary Operator "?:"
        #TODO: Add Comma
        #TODO: Symbol Symbol should be illegal
        if tokens[0] == "(":
            # Is this an inner expression or a cast?
            if tokens[1] in types+modifiers:
                inner,tokens = parse_cast( tokens )
                expression.append( inner )
            else:
                tokens.pop(0)
                inner,tokens = parse_expression( tokens )
                expression.append( inner )
                if tokens[0] != ")":
                    for e in expression:
                        print e
                    print >>sys.stderr, "Parse Error at Line %d / Char %d - ')' expected after expression %s" % (tokens[0].line, tokens[0].pos, str(inner))
                    assert(0)
                tokens.pop(0)
                #break
            if tokens[0] in binary_operations:
                symbol = tokens.pop(0)
                expression.append( ("Math", (symbol) ) )
        elif tokens[0] == ";":
            break
        elif tokens[0] == ",":
            break
        elif tokens[0] == ")":
            break
        elif tokens[0] == "]":
            break
        elif tokens[0] in binary_operations:
            symbol = tokens.pop(0)
            expression.append( ("Math", (symbol) ) )
        # Get the next value
        else:
            value,tokens = parse_value( tokens )
            expression.append( value )
            # TODO: Add Right/Left Associations
            if tokens[0] in binary_operations:
                symbol = tokens.pop(0)
                expression.append( ("Math", (symbol) ) )
            else:
                #print "Didn't find an operator, found",str(tokens[0]),"instead"
                pass
    # Fix precedence
    if len(expression) > 2:
        while len(expression) > 2:
            # The expressions should always be of the form:
            # Value Math Value Math Value
            symbols = [ sym[1] for sym in expression[1::2] ]
            for ops in precedence:
                if intersection( symbols, ops):
                    #print "Precedence Level",ops
                    i = (2 * first_instance( symbols, ops )) + 1
                    symbol = expression[i][1]
                    before,after = expression[:i-1],expression[i+2:]
                    right,left = expression[i-1],expression[i+1]
                    math = ("Binary",(symbol,right,left))
                    #print math
                    expression = before + [math] + after
                    break
    elif len(expression) == 2:
        if expression[0][0] == "Math" and expression[0][1] in prefix_operations:
            return ("Prefix",(expression[0][1],expression[1])),tokens
        elif expression[1][0] == "Math" and expression[0][1] in postfix_operations:
            return ("Postfix",(expression[1][1],expression[0])),tokens
    #
    if len(expression) == 1:
        return expression[0],tokens
    elif len(expression) == 0:
        return ("Expression",[]),tokens
    else:
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Couldn't compress expression into tree" % (tokens[0].line, tokens[0].pos)
        for e in expression:
            print >>sys.stderr, e
        assert(0)

def parse_struct( tokens ):
    struct = []
    if tokens[0] not in ["struct","union"]:
        print >>sys.stderr, "Parse Error at Line %d / Char %d - struct must start with 'struct' or 'union', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    kind = "Struct" if (tokens.pop(0) == "struct") else "Union"
    if tokens[0]!="{":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Blocks must start with 'struct {', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    while len(tokens):
        if tokens[0]=="}":
            break
        if tokens[0]=="struct" or tokens[0]=="union":
            inner,tokens = parse_struct(tokens)
            struct.append(inner)
        else:
            declaration,tokens = parse_declaration(tokens)
            struct.append(declaration)
        if tokens[0]!=";":
            print >>sys.stderr, "Parse Error at Line %d / Char %d - struct values must end in ';', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
            assert(0)
        tokens.pop(0)
    if tokens[0]!="}":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Blocks must start with 'struct {', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    #print kind, struct
    return (kind, struct), tokens

def parse_switch(tokens):
    if tokens[0] not in ["switch"]:
        print >>sys.stderr, "Parse Error at Line %d / Char %d - switch must start with 'switch', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    if tokens[0]!="(":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - for must have '(', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    test,tokens = parse_expression( tokens )
    
    if tokens[0]!=")":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - functions arguments must have ')', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)

    block,tokens = parse_block( tokens )

    return ( "Switch", (test,block) ), tokens

def parse_type(tokens):
    mods = []
    while tokens[0] in modifiers:
        mods.append( tokens.pop(0) )
    if not ( tokens[0] in types ):
        print >>sys.stderr, "Parse Error at Line %d / Char %d - expected type but found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert( tokens[0] in types )
    type = tokens.pop(0)
    isPointer = False
    if tokens[0] == "*":
        isPointer = True
        tokens.pop(0)
    #print "Type %s" % (" ".join(mods) + type + ("*" if isPointer else ""))
    return ("Type", (mods, type, isPointer)), tokens

def parse_declaration( tokens ):
    assignments = []
    type, tokens = parse_type( tokens )
    while len(tokens):
        if tokens[0] == "*":
            type = ("Type", (type[0][0], type[0][1], True))
            tokens.pop(0)
        # Check if it's a pointer
        name = tokens.pop(0)
        #print "Name %s" % name
        length = None
        if tokens[0]=="[":
            tokens.pop(0)
            length,tokens = parse_expression( tokens )
            if tokens[0]!="]":
                print >>sys.stderr, "Parse Error at Line %d / Char %d - Array Definition must end with ']', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
                assert(0)
            tokens.pop(0)
        if not is_keyword(name):
            if tokens[0]=="=":
                # Declaration value
                tokens.pop(0)
                expression,tokens = parse_expression( tokens )
                assignments.append((type,name,length,expression))
            else:
                # Non-Assignmed value
                assignments.append((type,name,length,None))
        if tokens[0]==",":
            tokens.pop(0)
            continue
        elif tokens[0]==";":
            break
        if len(tokens):
            print >>sys.stderr, "Parse Error at Line %d / Char %d - unknown token encountered at '%s'" % (tokens[0].line, tokens[0].pos, tokens[0])
            assert(0)
        type = ("Type", (type[0][0], type[0][1], False))
    return ("Declaration", assignments), tokens

def parse_function( tokens ):
    returntype,tokens = parse_type(tokens)

    name = tokens.pop(0)
    
    if tokens[0]!="(":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Function must have '(', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    # Arguements
    arguments = []
    while len(tokens):
        # Reached end of Argument List
        if tokens[0]==")":
            break
        if tokens[0]== "void" and tokens[1]==")":
            tokens.pop(0)
            break
        type,tokens = parse_type(tokens)
        argname = tokens.pop(0)
        if is_keyword(name):
            print >>sys.stderr, "Parse Error at Line %d / Char %d - Function argument #%d's name '%s' cannot be a keyword" % (len(arguments)+1, name)
            assert(0)
        arguments.append( (type,argname) )
        if tokens[0]!=",":
            break
        else:
            tokens.pop(0)
    
    if tokens[0]!=")":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Functions arguments must have ')', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    
    if tokens[0]=="{":
        block,tokens = parse_block( tokens );
    elif tokens[0]==";":
        tokens.pop(0)
        block = None
    else:
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Functions must have '{', found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    return ("Function",(returntype,name,arguments,block)), tokens

def parse_statement( tokens ):
    statement = []
    needsemicolon = True
    if tokens[0] == "if":
        statement,tokens = parse_if( tokens )
        needsemicolon = False
    elif tokens[0] == "while":
        statement,tokens = parse_while( tokens )
        needsemicolon = False
    elif tokens[0] == "for":
        statement,tokens = parse_for( tokens )
        needsemicolon = False
    elif tokens[0] in types + modifiers:
        statement,tokens = parse_declaration( tokens )
    elif tokens[0]=="struct" or tokens[0]=="union":
        statement,tokens = parse_struct(tokens)
    elif tokens[0] == "switch":
        statement,tokens = parse_switch(tokens)
        needsemicolon = False
    elif tokens[0] == "break":
        statement = ("Break",None)
        tokens.pop(0)
    elif tokens[0] == "continue":
        statement = ("Continue",None)
        tokens.pop(0)
    elif tokens[0] == "case":
        tokens.pop(0)
        literal,tokens = parse_value(tokens)
        statement = ("Case",literal)
        if tokens[0]!=":":
            print >>sys.stderr, "Parse Error at Line %d / Char %d - case must end in a colon: found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(tokens[0] == ":")
        tokens.pop(0)
        needsemicolon = False
    elif tokens[0] == "default":
        tokens.pop(0)
        statement = ("default",None)
        if tokens[0]!=":":
            print >>sys.stderr, "Parse Error at Line %d / Char %d - default must end in a colon: found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(tokens[0] == ":")
        tokens.pop(0)
        needsemicolon = False
    elif tokens[1] == ":":
        label = tokens.pop(0)
        statement = ("Label",label)
        assert(tokens[0] == ":")
        tokens.pop(0)
        needsemicolon = False
    elif tokens[0] == "goto":
        tokens.pop(0)
        label = tokens.pop(0)
        statement = ("Goto",label)
    elif tokens[0] == "return":
        tokens.pop(0)
        expression,tokens = parse_expression( tokens );
        statement = ("Return",expression)
    else:
        expression,tokens = parse_expression(tokens)
        statement = ("Statement",expression)
    if needsemicolon:
        if tokens[0]==";" or tokens[0]==",":
            tokens.pop(0)
        else:
            print >>sys.stderr, "Parse Error at Line %d / Char %d - Statements must end in a semicolon: found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
            assert(tokens[0]==";")
    #print "Statement",statement,"\n"
    return statement, tokens

def parse_block( tokens ):
    if tokens[0]!="{":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Blocks must start with a {, found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    block = []
    while len(tokens) and tokens[0] != "}":
        statement,tokens = parse_statement_or_block(tokens)
        block.append( statement )
    if tokens[0]!="}":
        print >>sys.stderr, "Parse Error at Line %d / Char %d - Blocks must end with a }, found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
        assert(0)
    tokens.pop(0)
    #print "Block", block
    return ("Block",block), tokens

def parse_statement_or_block( tokens ):
    if tokens[0]=="{":
        return parse_block( tokens )
    else:
        return parse_statement( tokens )

def parse_root( tokens ):
    if tokens[ len_type(tokens) + 1 ] == "(":
        return parse_function( tokens )
    else:
        declaration = parse_declaration( tokens )
        if tokens[0]==";":
            tokens.pop(0)
        else:
            print >>sys.stderr, "Parse Error at Line %d / Char %d - Non-Function Declarations must end in a semicolon: found %s instead" % (tokens[0].line, tokens[0].pos, tokens[0])
            assert(tokens[0]==";")
        return declaration

# Print Abstract Syntax Tree (AST)
# ------------------------------------------------------------------------
def print_thing( thing, depth=0 ):
    def p(str,d=0):
        print "\t"*(depth+d)+ str
    try:
        name,value = thing
    except ValueError:
        print "Can't Unpack this variable:"
        print thing
        assert(0)
    #p("THING:", name,value)
    if name == "Block":
        p("Block")
        for num,statement in enumerate(value):
            print "\t"*(depth)+ "Statement %d" %(num+1)
            print_thing(statement,depth+1)
    elif name == "Statement":
        print_thing(value,depth)
    elif name == "Math":
        symbol = value
        p("Math")
        p(symbol)
        assert(0)
    elif name == "Cast":
        type,expression = value
        p("Cast")
        print_thing(expression,depth+1)
        p("To")
        print_thing(type,depth+1)
    elif name == "Prefix":
        p("Prefix")
        symbol, expression = value
        p(symbol)
        print_thing(expression,depth+1)
    elif name == "Postfix":
        p("Postfix")
        expression, symbol = value
        print_thing(expression,depth+1)
        p(symbol)
    elif name == "Binary":
        symbol,left,right = value
        p("(")
        p("Math '%s'" % symbol)
        print_thing(left,depth+1)
        p(symbol)
        print_thing(right,depth+1)
        p(")")
    elif name == "String":
        p("String")
        p('"%s"'%value)
    elif name == "Value":
        p("Value")
        p(value)
    elif name == "Index":
        p("Index")
        name, expression = value
        p(name)
        p("[")
        print_thing(expression,depth+1)
        p("]")
    elif name == "Type":
        p("Type")
        mods, type, isPointer = value
        if len(mods):
            type = " ".join(mods) + " " + type
        if isPointer:
            type = "Pointer to " + type
        p(type,1)
    elif name == "Declaration":
        p(name)
        for declaration in value:
            type,name,length,assignment = declaration
            if length:
                p("Array of length",1)
                print_thing(length,depth+2)
            print_thing(type,depth+1)
            p("Name",1)
            p(name,2)
            if assignment:
                p("Assigned the value",1)
                print_thing(assignment,depth+2)
    elif name == "Expression":
        p(name)
        p("(")
        if value:
            print_thing(value,depth+1)
        p(")")
    elif name=="Struct" or name=="Union":
        p(name)
        p("{")
        for expression in value:
            print_thing(expression,depth+1)
        p("}")
    elif name=="If":
        test,action,alternative = value
        p(name)
        p("TEST",1)
        print_thing(test,depth+2)
        p("DO",1)
        print_thing(action,depth+2)
        if alternative:
            p("ELSE",1)
            print_thing(alternative,depth+2)
    elif name=="While":
        test,action = value
        p(name)
        p("TEST",1)
        print_thing(test,depth+2)
        p("DO",1)
        print_thing(action,depth+2)
    elif name=="For":
        init,test,step,action = value
        p(name)
        p("INIT",1)
        print_thing(init,(depth+1)+1)
        p("TEST",1)
        print_thing(test,(depth+1)+1)
        p("STEP",1)
        print_thing(step,(depth+1)+1)
        p("DO",1)
        print_thing(action,depth+2)
    elif name=="Break":
        p(name)
    elif name=="Continue":
        p(name)
    elif name=="Return":
        p(name)
        print_thing(value,depth+1)
    elif name=="Case":
        p(name)
        print_thing(value,depth+1)
    elif name=="Label":
        p(name)
        p(value,1)
    elif name=="Goto":
        p(name)
        p(value,1)
    elif name=="default":
        p(name)
    elif name=="Function":
        returntype,name,arguments,block = value
        if block:
            p("Function Declaration")
        else:
            p("Function Header")
        print_thing(returntype,depth+1)
        p(name,1)
        if len(arguments):
            p("With %d Argument%s" %(len(arguments), "s" if len(arguments) > 1 else ""))
            for num,(argtype,argname) in enumerate(arguments):
                p("Argument %d:" %(num+1),1)
                print_thing(argtype,depth+2)
                p("Name",2)
                p(argname,3)
        else:
            p("With No Arguments")
        if block:
            p("{")
            print_thing(block,depth+1)
            p("}")
    elif name=="Call":
        func,arguments = value
        p(name)
        p(func)
        p("(")
        for num,arg in enumerate(arguments):
            print_thing(arg,depth+1)
            if num != len(arguments)-1:
                p(",")
        p(")")
    elif name=="Switch":
        test,block = value
        p(name)
        p("(")
        print_thing(test,depth+1)
        p(")")
        p("{")
        print_thing(block,depth+1)
        p("}")
    else:
        p("Warning!  Unknown type '", name,"'")
        p(str(name))
        p(str(value))

def print_c( thing, depth, comments ):
    def comment(str):
        if comments:
            p("// "+ str)
    def p(str,d=0):
        print "\t"*(depth+d)+ str
    try:
        name,value = thing
    except ValueError:
        print "Can't Unpack this variable:"
        print thing
        assert(0)
    comment( "THING: %s %s" % (name,str(value)) )
    comment( name )
    if name == "Block":
        p("{")
        for num,statement in enumerate(value):
            comment( "Statement %d" %(num+1) )
            print_c(statement,depth+1,comments)
        p("}")
    elif name == "Cast":
        type,expression = value
        p("(")
        print_c(type,depth+1,comments)
        p(")")
        print_c(expression,depth+1,comments)
    elif name == "Prefix":
        symbol, expression = value
        p(symbol)
        print_c(expression,depth+1,comments)
    elif name == "Postfix":
        expression, symbol = value
        print_c(expression,depth+1,comments)
        p(symbol)
    elif name == "Binary":
        symbol,left,right = value
        p("(")
        print_c(left,depth+1,comments)
        p(symbol)
        print_c(right,depth+1,comments)
        p(")")
    elif name == "String":
        p('"%s"'%value)
    elif name == "Value":
        p(value)
    elif name == "Index":
        var, expression = value
        p(var)
        p("[")
        print_c(expression,depth+1,comments)
        p("]")
    elif name == "Type":
        mods, type, isPointer = value
        if len(mods):
            type = " ".join(mods) + " " + type
        if isPointer:
            type += "*"
        p(type)
    elif name == "Declaration":
        for declaration in value:
            type,name,length,assignment = declaration
            print_c(type,depth+1,comments)
            p(name,1)
            if length:
                p("[",1)
                print_c(length,depth+2,comments)
                p("]",1)
            if assignment:
                p("=",1)
                print_c(assignment,depth+2,comments)
            p(";")
    elif name == "Expression":
        p("(")
        if value:
            print_c(value,depth+1,comments)
        p(")")
    elif name=="Struct" or name=="Union":
        if name == "Struct":
            p("struct")
        if name == "Union":
            p("union")
        p("{")
        for expression in value:
            print_c(expression,depth+1,comments)
        p("};")
    elif name=="If":
        test,action,alternative = value
        p("if(")
        comment( "TEST" )
        print_c(test,depth+2,comments)
        p(")")
        comment( "DO" )
        p("{")
        print_c(action,depth+2,comments)
        p("}")
        if alternative:
            comment( "ELSE" )
            p("else {",1)
            print_c(alternative,depth+2,comments)
            p("}",1)
    elif name=="While":
        test,action = value
        p("while(")
        comment( "TEST" )
        print_c(test,depth+2,comments)
        p(")")
        comment( "DO" )
        p("{",1)
        print_c(action,depth+2,comments)
        p("}",1)
    elif name=="For":
        init,test,step,action = value
        p("for(")
        comment( "INIT" )
        print_c(init,(depth+1)+1,comments)
        p(";")
        comment( "TEST" )
        print_c(test,(depth+1)+1,comments)
        p(";")
        comment( "STEP" )
        print_c(step,(depth+1)+1,comments)
        p(")")
        comment( "DO" )
        p("{")
        print_c(action,depth+2,comments)
        p("}")
    elif name=="Break":
        p("break;")
    elif name=="Continue":
        p("continue;")
    elif name=="Return":
        p("return")
        print_c(value,depth+1,comments)
        p(";")
    elif name=="Case":
        p("case")
        print_c(value,depth+1,comments)
        p(":")
    elif name=="Label":
        p(value,1)
        p(":")
    elif name=="Goto":
        p(value,1)
        p(";")
    elif name=="default":
        p("default:")
    elif name=="Statement":
        print_c(value,depth,comments)
        p(";")
    elif name=="Function":
        returntype,name,arguments,block = value
        if block:
            comment( "Function Declaration" )
            pass
        else:
            comment( "Function Header" )
            pass
        print_c(returntype,depth+1,comments)
        p(name,1)
        p("(")
        if len(arguments):
            comment( "With %d Argument%s" %(len(arguments), "s" if len(arguments) > 1 else "") )
            for num,(argtype,argname) in enumerate(arguments):
                comment( "Argument %d:" %(num+1) )
                print_c(argtype,depth+2,comments)
                comment( "Name" )
                p(argname,3)
                if num != len(arguments)-1:
                    p(",",3)
                    
        else:
            comment( "With No Arguments" )
            p("void")
        p(")")
        if block:
            print_c(block,depth,comments)
        else:
            p(";")
    elif name=="Call":
        func,arguments = value
        p(func)
        p("(")
        for num,arg in enumerate(arguments):
            print_c(arg,depth+1,comments)
            if num != len(arguments)-1:
                p(",")
        p(")")
    elif name=="Switch":
        test,block = value
        p("switch")
        p("(")
        print_c(test,depth+1,comments)
        p(")")
        p("{")
        print_c(block,depth+1,comments)
        p("}")
    else:
        p("Warning!  Unknown type '", name,"'")
        p(str(name))
        p(str(value))

if __name__ == "__main__":
    import os
    import sys
    import glob
    from optparse import OptionParser

    # Option Parser
    parser = OptionParser()
    parser.add_option("-s", "--save", dest="save", default=False,
                      action="store_true",
                      help="Save" )
    parser.add_option("-d", "--dir", dest="directory",
                      action="store", type="string", default="results",
                      help="Output directory", metavar="DIR")
    parser.add_option("-c", "--code",
                      action="store_true", dest="code", default=False,
                      help="Output AST as C")
    parser.add_option("--comments",
                      action="store_true", dest="comments", default=False,
                      help="Output comments in the code")
    parser.add_option("-a", "--ast",
                      action="store_true", dest="ast", default=False,
                      help="Output AST as readable AST")
    parser.add_option("-t", "--tokens",
                      action="store_true", dest="tokens", default=False,
                      help="Output parsed tokens")
    (options, args) = parser.parse_args()

    # expand options
    files = []
    for arg in args:
        for filenames in glob.glob( arg ):
                files.append( filenames )
    output_to_files = options.save
    dirname = options.directory
    if output_to_files:
        if not os.path.exists( dirname ):
            os.mkdir( dirname )
    real_out = sys.stdout

    # Do the stuff
    for filename in files:
        print filename
        dirpath,filebase = os.path.split(filename)
        base,ext = os.path.splitext(filebase)
        data = open(filename,"r").read()
        tokens = list(tokenize( data ))

        # Print out the Lexer
        if options.tokens:
            if output_to_files:
                sys.stdout = open(os.path.join(dirname, base+".tok"),"w")
            print "Lexical Analysis of " + filename
            for i,token in enumerate( tokens ):
                loc = ("%d (%d,%d): " %(i, token.line, token.pos)).ljust(16)
                print loc,token
        
        # Parse tokens
        if output_to_files:
            if options.ast:
                astfile = open(os.path.join(dirname, base+".ast"),"w")
                sys.stdout = astfile
                print "AST code of " + filename
            if options.code:
                cfile = open(os.path.join(dirname, base+".c"),"w")
                sys.stdout = cfile
                print "// C code of " + filename

        while len(tokens):
            block, tokens = parse_root( tokens )
            if options.ast:
                sys.stdout = astfile
                print_thing(block)
            if options.code:
                sys.stdout = cfile
                print_c(block, 0, options.comments)
        print
        if output_to_files:
            sys.stdout = real_out

