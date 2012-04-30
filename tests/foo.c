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
}
