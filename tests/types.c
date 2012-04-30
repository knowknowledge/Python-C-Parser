typedef enum {
    False,
    True,
    Maybe = -1
} Boolean;

struct foobarbaz {
    int foo;
    short bar;
    long long baz;
};
struct foobarbaz bazInstance;

union {
    int *ptr;
    char* strptr;
} ptrStruct;

int main()
{
    return 0;
}

