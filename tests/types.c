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
    ((10));
    d[10].c; // SubStruct of Array value
    int x[10] = (int)y;
    const int ten[10];
    const int *pten[10];
    char y = (unsigned char*)(x);
    // char (*(*x())[5])()
    // int (*(*foo)(void ))[3]
    // (int (*)(char *x, int y))x
    // (int (*)(char *, int , float ))x
    // const int (* volatile bar)[64]
    // int *x(int )
    // declare bar as volatile pointer to array 64 of const int
    // const int (* volatile bar)[64]

    return 0;
}

