/*
typedef enum {
    False,
    True,
    Maybe = -1
} Boolean;
*/

/*
struct {
    int foo;
    short bar;
    long long baz;
} foobarbaz;
struct foobarbaz bazInstance;
*/

/*
union {
    int *ptr;
    char* strptr;
} ptrStruct;
*/

int main()
{
    a.b; // SubStruct access
    c->d; // Pointer SubStruct access
    d->baz.bar;
    d->baz->oob; // Double Pointer SubStruct access
    &d; // Address Of
    *d; // Value at
    d[10]; // Array Index
    /*
    (int)r; // Cast
    // Complex Types
    ((foobar)r).c; // Cast and SubStruct access
    */
    d[10].c; // SubStruct of Array value

    return 0;
}

