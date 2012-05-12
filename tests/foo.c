int foo(){}

int bar( int a ){}
int bar( int a,int b )
{
    while( 0 ) 1;

    for(i=0;i<10;i+=1)
    {
        blahblah;
        break;
        continue;
        return;
    }
    return 10;
}

int main() {
    int i;
    struct {
        int foo;
        int bar;
        union {
            int baz;
            int zab;
        };
    };

    1;
    a;
    foobar;
    a+b;
    1+2;
    {
        a = b;
        {
            c = d;
        }
    }
    struct {
        int foo;
        int bar;
        union {
            int baz;
            int zab;
        };
    };
    switch( a ) {
        case 1:
            foo();
            break;
        case 2:
            foo();
            break;
        case 3:
            foo();
            break;
        case 4:
            foo();
            break;
        default:
            foo();
            break;
    }
    foobar:
    int bar = 1;
    3;
    foo /= 5 || ;
    if( foobar ) bax += test;
    else if ( baz )
        bax -= test;
    if( 3+2+1 ) {
        baz = 5+4/3*2-1;
        zab = 100;
    }
    else 
    {
        bar = 0x100;
    }
    foo(1,2,3,4,foo());
    if( age < 0 ) {
        goto foobar;
    }
}
