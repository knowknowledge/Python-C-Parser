import string


# C Keywords
types = ["short", "int", "long", "float", "double", "char", "void"]
containers = ["enum", "struct", "union", "typedef"]
modifiers = [ "const", "volatile", "extern", "static", "register", "signed", "unsigned"]
flow = [ "if", "else",
         "goto", 
         "case", "default", 
         "continue", "break", ]
loops = ["for", "do", "while" "switch", ]
keywords = types + containers + modifiers + flow + loops + [ "return", "sizeof" ]

unary_operations = ["-","+","*","&"]
binary_operations = ["+","-","/","*",
                     "^","&","|",
                     "<<",">>",
                     "<",">", "<=",">=",
                     "&&","||","==","!=",
                     "=",
                     "+=","-=","/=","*=",
                     "^=","&=","|=",
                     "<<=",">>=",]
def is_keyword(token):
    return token in keywords

def isonly(s,chars):
    return len(s) and all(map(lambda c: c in chars, s))

# Break the text into tokens
def tokenize( s ):
    # TODO: Need to seperate some tokens better, example if(foo); 
    curtoken = ""
    symbols = string.punctuation.replace("_","")
    line = 1
    pos = 0
    for c in s:
        pos += 1
        #print (c,curtoken)
        if c in symbols:
            if (curtoken+c) in binary_operations:
                curtoken = (curtoken+c)
            else:
                if curtoken != "":
                    yield curtoken
                curtoken = c
        else:
        # Non-Symbols
            if isonly(curtoken, symbols):
                yield curtoken
                curtoken = ""
            if c in string.whitespace:
                if curtoken != "":
                    yield curtoken
                if c == "\n":
                    #yield c
                    line += 1
                    pos = 0
                curtoken = ""
            elif c in string.digits:
                curtoken += c
            elif curtoken.startswith("0x") and c in string.hexdigits and isonly(curtoken[2:],string.digits):
                curtoken += c
            elif curtoken == "0" and c in "xX":
                curtoken += c
            else:
                curtoken += c
    if curtoken not in string.whitespace:
        yield curtoken

# Parse a Value
def parse_value(tokens):
    if tokens[0] in unary_operations:
        unary = tokens.pop(0)
        name = tokens.pop(0)
        #print "Value",unary,name
        return ('Value',unary,name),tokens
    elif is_keyword(tokens[0]):
        print "Parse Error - Value Expected at %s, found keyword" % tokens[0]
        assert(0)
    elif tokens[0] in string.punctuation:
        print "Parse Error - Value Expected at %s, found punctuation" % tokens[0]
        assert(0)
    else:
        name = tokens.pop(0)
        #print "Value",name
        return ('Value',name),tokens

def parse_if( tokens ):
    if tokens[0] not in ["if"]:
        print "Parse Error - if must start with 'if', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    
    if tokens[0]!="(":
        print "Parse Error - if must have '(', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)

    test,tokens = parse_expression( tokens )

    if tokens[0]!=")":
        print "Parse Error - if must have ')', found %s instead" % tokens[0]
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
        print "Parse Error - while must start with 'while', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    
    if tokens[0]!="(":
        print "Parse Error - while must have '(', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)

    test,tokens = parse_expression( tokens )

    if tokens[0]!=")":
        print "Parse Error - if must have ')', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)

    action,tokens = parse_statement_or_block(tokens)

    #print "While",test,action
    return ("While",(test,action)), tokens

def parse_for( tokens ):
    if tokens[0] not in ["for"]:
        print "Parse Error - for must start with 'for', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    
    if tokens[0]!="(":
        print "Parse Error - for must have '(', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)

    init,tokens = parse_expression( tokens )

    if tokens[0]!=";":
        print "Parse Error - for must have first ';', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    test,tokens = parse_expression( tokens )

    if tokens[0]!=";":
        print "Parse Error - for must have second ';', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    step,tokens = parse_expression( tokens )

    if tokens[0]!=")":
        print "Parse Error - if must have ')', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)

    action,tokens = parse_statement_or_block(tokens)

    #print "For",init,test,step,action
    return ("For",(init,test,step,action)), tokens

def parse_expression( tokens ):
    # This should be a tree not a list
    expression = []
    while len(tokens):
        #TODO: Add Unary Operators
        #TODO: Add Ternary Operator "?:"
        #TODO: Add Comma
        #TODO: Symbol Symbol should be illegal
        if tokens[0] == "(":
            tokens.pop(0)
            inner,tokens = parse_expression( tokens )
            expression.append( inner )
            if tokens[0] != ")":
                print "Parse Error - ')' expected after expression %s" % inner
                assert(0)
            tokens.pop(0)
            break
        elif tokens[0] == ";":
            break
        elif tokens[0] == ",":
            break
        elif tokens[0] == ")":
            break
        else:
            value,tokens = parse_value( tokens )
            expression.append( value )
            # TODO: Add Right/Left Associations
            if tokens[0] in binary_operations:
                symbol = tokens.pop(0)
                right,tokens = parse_expression( tokens )
                expression.append( ("Math", (symbol, right) ) )
    #print "Expression", tuple(expression)
    return ("Expression", tuple(expression)),tokens

def parse_struct( tokens ):
    struct = []
    if tokens[0] not in ["struct","union"]:
        print "Parse Error - struct must start with 'struct' or 'union', found %s instead" % tokens[0]
        assert(0)
    kind = "Struct" if (tokens.pop(0) == "struct") else "Union"
    if tokens[0]!="{":
        print "Parse Error - Blocks must start with 'struct {', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    while len(tokens):
        if tokens[0]=="}":
            break
        if tokens[0]=="struct" or tokens[0]=="union":
            inner,tokens = parse_struct(tokens)
            struct.append(inner)
            if tokens[0]!=";":
                print "Parse Error - struct values must end in ';', found %s instead" % tokens[0]
                assert(0)
            tokens.pop(0)
        else:
            type = tokens.pop(0)
            name = tokens.pop(0)
            if tokens[0]!=";":
                print "Parse Error - struct values must end in ';', found %s instead" % tokens[0]
                assert(0)
            tokens.pop(0)
            struct.append(("Assignment", [(type,name)]))
    if tokens[0]!="}":
        print "Parse Error - Blocks must start with 'struct {', found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    
    print kind, struct
    return (kind, struct), tokens

def parse_assignment( tokens ):
    assignments = []
    type = tokens.pop(0)
    print "Type %s" % type
    while len(tokens):
        name = tokens.pop(0)
        print "Name %s" % name
        if not is_keyword(name):
            if tokens[0]=="=":
                # Assignment value
                tokens.pop(0)
                expression,tokens = parse_expression( tokens )
                assignments.append((type,name,expression))
            else:
                # Non-Assignmed value
                assignments.append((type,name))
        if tokens[0]==",":
            tokens.pop(0)
            continue
        elif tokens[0]==";":
            break
        if len(tokens):
            print "Parse Error - unknown token encountered at '%s'" % tokens[0]
            assert(0)
    return ("Assignment", assignments), tokens

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
    elif tokens[0] in types:
        statement,tokens = parse_assignment( tokens )
    elif tokens[0]=="struct" or tokens[0]=="union":
        statement,tokens = parse_struct(tokens)
    else:
        statement,tokens = parse_expression(tokens)
    if needsemicolon:
        if tokens[0]==";":
            tokens.pop(0)
        else:
            print "Parse Error - Statements must end in a semicolon: found %s instead" % tokens[0]
            assert(0)
    #print "Statement",statement,"\n"
    return statement, tokens

def parse_block( tokens ):
    if tokens[0]!="{":
        print "Parse Error - Blocks must start with a {, found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    block = []
    while len(tokens) and tokens[0] != "}":
        statement,tokens = parse_statement_or_block(tokens)
        block.append( statement )
    if tokens[0]!="}":
        print "Parse Error - Blocks must end with a }, found %s instead" % tokens[0]
        assert(0)
    tokens.pop(0)
    #print "Block", block
    return ("Block",block), tokens

def parse_statement_or_block( tokens ):
    if tokens[0]=="{":
        return parse_block( tokens )
    else:
        return parse_statement( tokens )

def print_thing( thing, depth=0 ):
    name,value = thing
    #print "\t"*depth+ "THING:", name,value
    if name == "Block":
        print "\t"*depth+ "Block"
        print "\t"*depth+ "{"
        for statement in value:
            print_thing(statement,depth+1)
        print "\t"*depth+ "}"
    elif name == "Statement":
        print "\t"*depth+ "Statement"
        pass
    elif name == "Math":
        symbol, expression = value
        print "\t"*depth+symbol
        print_thing(expression,depth+1)
    elif name == "Value":
        print "\t"*depth+ value
    elif name == "Assignment":
        print "\t"*depth+ name
        for assignment in value:
            if len(assignment) == 2:
                type,name = assignment
                print "\t"*depth+ type,name 
            else:
                type,name,expression = assignment
                print "\t"*depth+ type,name, "= ("
                print_thing(expression,depth+1)
                print "\t"*depth+ ")"
    elif name == "Expression":
        print "\t"*depth+ name
        print "\t"*depth+ "("
        for expression in value:
            print_thing(expression,depth+1)
        print "\t"*depth+ ")"
    elif name=="Struct" or name=="Union":
        print "\t"*depth+ name
        print "\t"*depth+ "{"
        for expression in value:
            print_thing(expression,depth+1)
        print "\t"*depth+ "}"
    elif name=="If":
        test,action,alternative = value
        print "\t"*depth+ name
        print "\t"*depth+ "("
        print_thing(test,depth+1)
        print "\t"*depth+ ")"
        print "\t"*depth+ "{"
        print_thing(action,depth+1)
        print "\t"*depth+ "}"
        if alternative:
            print "\t"*depth+ "else"
            print "\t"*depth+ "{"
            print_thing(alternative,depth+1)
            print "\t"*depth+ "}"
    elif name=="While":
        test,action = value
        print "\t"*depth+ name
        print "\t"*depth+ "("
        print_thing(test,depth+1)
        print "\t"*depth+ ")"
        print "\t"*depth+ "{"
        print_thing(action,depth+1)
        print "\t"*depth+ "}"
    elif name=="For":
        init,test,step,action = value
        print "\t"*depth+ name
        print "\t"*depth+ "("
        print "\t"*depth+ "INIT"
        print_thing(init,depth+1)
        print "\t"*depth+ "TEST"
        print_thing(test,depth+1)
        print "\t"*depth+ "STEP"
        print_thing(step,depth+1)
        print "\t"*depth+ ")"
        print "\t"*depth+ "{"
        print_thing(action,depth+1)
        print "\t"*depth+ "}"
    else:
        print "\t"*depth+ name
        print "\t"*depth+ value

if __name__ == "__main__":
    import sys
    import glob
    files = []
    for arg in sys.argv[1:]:
        for filenames in glob.glob( arg ):
                files.append( filenames )
    for filename in files:
        print
        data = open(filename,"r").read()
        for i,token in enumerate(tokenize( data )):
            print "%d:%s" % (i,token)
        tokens = list(tokenize( data ))
        print tokens
        while len(tokens):
            block, tokens = parse_statement_or_block( tokens )
            print_thing(block)
            
