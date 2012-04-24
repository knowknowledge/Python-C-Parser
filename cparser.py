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

unary_operations = ["-","+"]
binary_operations = ["+","-","/","*",
                     "^","&","|"]

def is_keyword(token):
    return token in keywords

# Break the text into tokens
def tokenize( s ):
    curtoken = ""
    symbols = string.punctuation.replace("_","")
    for c in s:
        if c in symbols:
            #TODO: Should be handled more gracefully
            #TODO: Add double-character symbols
            #       +=, -=, /=, *=, &=, ^=, |=, %=
            #       >>, <<, &&, ||, 
            #TODO: Add triple-character symbols
            #       >>=, <<=
            if not curtoken == "":
                yield curtoken
            yield c
            curtoken = ""
        elif c in string.whitespace:
            if not curtoken == "":
                yield curtoken
            #if c == "\n":
            #    yield c
            curtoken = ""
        elif c in string.digits:
            print "Digit", c
            curtoken += c
        elif curtoken.startswith("0x") and c in string.hexdigits:
            print "Hexit", c
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
        print "Value",unary,name
        return ('Value',unary,name),tokens
    elif is_keyword(tokens[0]):
        print "Parse Error - Value Expected at %s, found keyword" % tokens[0]
    elif tokens[0] in string.punctuation:
        print "Parse Error - Value Expected at %s, found punctuation" % tokens[0]
    else:
        name = tokens.pop(0)
        print "Value",name
        return ('Value',name),tokens

def parse_expression( tokens ):
    expression = []
    print "In Expression at ", tokens[0]
    while len(tokens):
        #TODO: Add Ternary Operators
        #TODO: Add Comma
        if tokens[0] == "(":
            tokens.pop(0)
            inner,tokens = parse_expression( tokens )
            expression.append( inner )
            if tokens[0] != ")":
                print "Parse Error - ')' expected after expression %s" % inner
            tokens.pop(0)
            break
        elif tokens[0] == ";":
            break
        elif tokens[0] == ")":
            break
        else:
            value,tokens = parse_value( tokens )
            expression.append( value )
            # TODO: Add Right/Left Associations
            if tokens[0] in binary_operations:
                expression.append( tokens.pop(0) )
    print "Expression", expression
    return ("Expression", expression),tokens    

def parse_statement( tokens ):
    statement = []
    if tokens[0] in types:
        type = tokens.pop(0)
        print "Type %s" % type
        statement = ["Assignment", type]
        while len(tokens):
            name = tokens.pop(0)
            print "Name %s" % name
            if not is_keyword(name):
                if tokens[0]=="=":
                    # Assignment value
                    tokens.pop(0)
                    expression,tokens = parse_expression( tokens )
                    statement.append((name,"=",expression))
                else:
                    # Non-Assignmed value
                    statement.append(name)
            if tokens[0]==",":
                tokens.pop(0)
                continue
            elif tokens[0]==";":
                break
            if len(tokens):
                print "Parse Error - unknown token encountered at '%s'" % tokens[0]
    else:
        statement,tokens = parse_expression(tokens)
    if tokens[0]==";":
        tokens.pop(0)
    else:
        print "Parse Error - Statements must end in a semicolon:"
    print "Statement",statement,"\n"
    return statement, tokens

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
            statement, tokens = parse_statement( tokens )

