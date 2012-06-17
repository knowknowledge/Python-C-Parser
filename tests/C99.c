#include <stdio.h>
#include <math.h>
#include <float.h>
#include <fenv.h>
#include <tgmath.h>
#include <stdbool.h>

int error;
 
double compute_fn(double z)
{
        #pragma STDC FENV_ACCESS ON  // [1]
 
        assert( FLT_EVAL_METHOD == 2 ); // [2]
 
        if (isnan(z)) printf("z is not a number\n"); // [3]
        if (isinf(z)) printf("z is infinite\n");
 
        double r;  // [4]
 
        r = 7.0 - 3.0 / (z - 2.0 - 1.0/(z - 7.0 + 10.0/(z - 2.0 - 2.0/(z - 3.0)))); // [5]
        
        // int x = r > 3 ? 10 : -10;

        feclearexcept(FE_DIVBYZERO); // [6]
 
        bool raised = fetestexcept(FE_OVERFLOW); // [7]
        if (raised) printf("Unanticipated overflow.\n");
 
        return r;
}
 
int main(void)
{
#ifndef __STDC_IEC_559__
        printf("Warning: __STDC_IEC_559__ not defined. IEEE 754 floating point not fully supported.\n"); // [8]
#endif
 
       #pragma STDC FENV_ACCESS ON 
 
        #ifdef TEST_NUMERIC_STABILITY_UP
        fesetround(FE_UPWARD);                   // [9]
        #elif TEST_NUMERIC_STABILITY_DOWN
        fesetround(FE_DOWNWARD); 
        #endif
 
        printf("%.7g\n", compute_fn(3.0));
        printf("%.7g\n", compute_fn(NAN));
 
        return 0;
}

