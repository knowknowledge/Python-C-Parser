import string

keywords = [
    "short", "int", "long", "float", "double", "char", "void", "enum",
    "struct", "union", "typedef",
    "if", "else", "goto",
    "for", "do", "while", 
    "continue", "break", 
    "return", 
    "switch", "case", "default", 
    "const", "volatile", "extern", "static", "register",
    "signed", "unsigned",
    "sizeof",
]

def tokenize( s ):
    curtoken = ""
    symbols = string.punctuation.replace("_","")
    for c in s:
        if c in symbols:
            if not curtoken == "":
                yield curtoken
            yield c
            curtoken = ""
        elif c in string.whitespace:
            if not curtoken == "":
                yield curtoken
            if c == "\n":
                yield c
            curtoken = ""
        elif c in string.digits:
            if not curtoken == "":
                yield curtoken
                curtoken = ""
            curtoken += c
        elif curtoken.startswith("0x") and c in string.hexdigits:
                curtoken += c
        else:
            curtoken += c
    yield curtoken

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
        for token in tokenize( data ):
            print token

