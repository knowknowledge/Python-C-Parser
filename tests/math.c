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
    

    return total;
}

