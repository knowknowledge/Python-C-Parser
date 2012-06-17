int foo(){
    (1)+(2);
    if( !a )
        return -1;
}
int mult(int one, int two) { return one * two; }
int div(int one, int two) { return one / two; }
int add(int one, int two) { return one + two; }
int sub(int one, int two) { return one - two; }
int main() {
    int a = 5, b = 6;
    int total;
    // Do some math
    total = mult( a,b );
    total += div(a*10,b);
    total += add(a,10);
    total += sub(a,b);

    b = 1 + 4 * ( 2 + 1 ) ;
    ++b;
    b++;
    --b;
    b--;

    b = ++a + b--;
    
    1?2:3;
    y = (x)?2:3;
    y = (x)?asdf:3 ? asdf : 4;

   printf("A: %d\n", i+j+(k!=7)?1:11); //prints 1
   printf("B: %d\n", i+j+((k!=7)?1:11)); //prints 22

    y = (x < -10) ? BIG_NEGATIVE :
        (x <   0) ?     NEGATIVE :
        (x ==  0) ?         ZERO :
        (x >  10) ? BIG_POSITIVE :
                        POSITIVE ;

    return total;
}

