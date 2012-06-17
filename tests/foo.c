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
        int* foo[4];
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
    (1)+(2);
    1.1 / ( z - 1.1 );
    ( z - 2.2 ) - ( 2.2 / ( z - 2.2 ) );
    33.3 / ( ( z - 3.3 ) - ( 3.3 / ( z - 3.3 ) ) );
    ( z - 4.4 ) + ( 44.4 / ( ( z - 4.4 ) - ( 4.4 / ( z - 4.4 ) ) ) );
    (
     r = (
         7.0 - (
             3.0 / (
                 (
                  z - 2.0 
                 ) - (
                     1.0 / (
                         (
                          z - 7.0 
                         ) + (
                             10.0 / (
                                 (
                                  z - 2.0 
                                 ) - (
                                     2.0 / (
                                         z - 3.0 
                                         ) 
                                     ) 
                                 ) 
                             ) 
                         ) 
                     ) 
                 ) 
             ) 
         ) 
    ) ;

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
    foo /= 5 || 10;
    if( foobar ) bax += test;
    else if ( baz )
        bax -= test;
        else {
            bax *= test;
        }
    forever:
    for(;;); // Forever loop
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
