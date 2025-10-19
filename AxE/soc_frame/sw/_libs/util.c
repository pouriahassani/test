#include "util.h"
#include <stdlib.h>
// #include "print.h"
// int fpadd_counter = 0;
int fpmul(int rs1, int rs2)
{
    int rd;
    asm __volatile__ (".word 0x02A5850B\n");
    asm __volatile__ ("addi %0, x10, 0" : "=r" (rd)); //TODO: what is addi? Assembly? May have to be edited to also designate the custom instruction used (PCPI_FPADD)
    
    return rd;
}


__attribute__((noinline))
int fpmul_approx(int rs1, int rs2)
{
    int rd;
    asm __volatile__ (".word 0x82C5850B\n");
    asm __volatile__ ("addi %0, x10, 0" : "=r" (rd)); //TODO: what is addi? Assembly? May have to be edited to also designate the custom instruction used (PCPI_FPMUL_APPROX)
    
    return rd;
}


__attribute__((noinline))
int fpadd(int rs1, int rs2)
{
    int rd;
    asm __volatile__ (".word 0x00A5850B\n");
    asm __volatile__ ("addi %0, x10, 0" : "=r" (rd)); //TODO: what is addi? Assembly? May have to be edited to also designate the custom instruction used (PCPI_FPADD)

    return rd;
}

__attribute__((noinline))
int amul(int rs1, int rs2)
{
    int rd;
    asm __volatile__ (".word 0xFEA5857F\n");
    asm __volatile__ ("addi %0, x10, 0" : "=r" (rd)); //TODO: what is addi? Assembly? May have to be edited to also designate the custom instruction used (PCPI_FPADD)
    
    return rd;
}

__attribute__((noinline))
int emul(int rs1, int rs2)
{
    int rd;
    asm __volatile__ (".word 0x02A58533\n");
    asm __volatile__ ("addi %0, x10, 0" : "=r" (rd)); //TODO: what is addi? Assembly? May have to be edited to also designate the custom instruction used (PCPI_FPADD)
    
    return rd;
}


__attribute__((noinline))
int fpsub(int rs1, int rs2)
{
    int rd;
    asm __volatile__ (".word 0x04A5850B\n");
    asm __volatile__ ("addi %0, x10, 0" : "=r" (rd)); //TODO: what is addi? Assembly? May have to be edited to also designate the custom instruction used (PCPI_FPADD)
    
    return rd;
}


__attribute__((noinline))
int fpdiv(int rs1, int rs2)
{
    int rd;
    asm __volatile__ (".word 0x06A5850B\n");
    asm __volatile__ ("addi %0, x10, 0" : "=r" (rd)); //TODO: what is addi? Assembly? May have to be edited to also designate the custom instruction used (PCPI_FPADD)
    
    return rd;
}

__attribute__((noinline))
void checkprint_str(int rs1, int rs2)
{
    asm __volatile__ (".word 0x0EA5850B\n");
}
__attribute__((noinline))
void checkprint_float(int rs1)
{


    asm __volatile__ (".word 0x0EA5950B\n");//0ea5a50b
}
__attribute__((noinline))
void checkprint_int(int rs1)
{
    asm __volatile__ (".word 0x0EA5A50B\n");//0ea5a50b
}
void display_print(int is_digit,int value,char* str){
    int rs1 = 0;
    int rs2 = 0;
    if(is_digit == 2){
        checkprint_int(value);
    }
    else if(is_digit == 1){
        checkprint_float((float)value);
    }
    else{
        int i = 0;
        int j = 0;
        while(str[i] != '\0'){
            
            if(j == 0){
                rs1 = str[i];
            }
            else{
                if(j == 8){
                    checkprint_str(rs1,rs2);
                    rs1 = 0;
                    rs2 = 0;
                    j = -1;
                    i-=1;
                }
                else{
                    if(j < 4){
                        rs1 <<= 8;
                        rs1 += str[i];
                        // printf("\n%c",rs1);
                    }
                    else{
                        if(j==4)
                            rs2 = str[i];
                        else{
                            rs2 <<= 8;
                            rs2 += str[i];
                        }
                        // printf("\n%d %d %c",i,j,rs2);
                    }
                }

            }
            j+=1;
            i+=1;
        }
        if(j!=0)
            checkprint_str(rs1,rs2);
    }
}

// Used to print float values
void display_print_float(float value){
    asm __volatile__ (".word 0x0EA5950B\n");//0ea5a50b
}

// is now done in the asm file.

/*signal_fin() is used when the node ran out of charge and is called in trap()
function. I have commented it out because it is writing to emory and 
causes some undefined behaviour*/
// TO BE FIXED
void signal_fin()
{
    *((volatile int*)FINISHED) = FINISHED;
}

/*I didnt see any use of signal_kill_sim() 
It is used to signal the user to kill me. The sim_main.cpp
is using it*/
void signal_kill_sim()
{
    *((volatile int*)OUTPORT) = 0x04;
}
// -----------------------------------------------------------------------------
// 
// P R I N T
// 
// -----------------------------------------------------------------------------

// TODO - add some define to supress debug output. do it here so you don't
// have to worry about it when adding new output.

// char
// -------------------------------------

// str
// -------------------------------------

// -------------------------------------


// print_assert
// -------------------------------------
void emb_assert( unsigned int line, const char *file, const char *exp ){}

// Helper function to extract the sign bit from a float32_t number
uint32_t extractSign(float32_t a) {
    return a.value >> 31;
}

// Helper function to extract the sign bit from a float32_t number
uint32_t fp_ExtractSign(uint32_t a) {
    return a >> 31;
}

// Helper function to extract the exponent bits from a float32_t 	$(CC) -march=$(ARCH) $(CFLAGS) -nostartfiles -o ./$(ARCH)_main.elf $(LINK) ../sp.S -DSTACK_POINTER=$(STACK_POINTER) ../crt0.o ../start.S $(SRC) ./main.cnumber
uint32_t extractExponent(float32_t a) {
    return (a.value >> 23) & 0xFF;
}

// Helper function to extract the exponent bits from a float32_t 	$(CC) -march=$(ARCH) $(CFLAGS) -nostartfiles -o ./$(ARCH)_main.elf $(LINK) ../sp.S -DSTACK_POINTER=$(STACK_POINTER) ../crt0.o ../start.S $(SRC) ./main.cnumber
uint32_t fp_ExtractExponent(uint32_t a) {
    return (a >> 23) & 0xFF;
}

// Helper function to extract the fraction bits from a float32_t number
uint32_t extractFraction(float32_t a) {
    return a.value & 0x7FFFFF;
}

// Helper function to extract the fraction bits from a float32_t number
uint32_t fp_ExtractFraction(uint32_t a) {
    return a & 0x7FFFFF;
}


// Helper function to create a float32_t number from sign, exponent, and fraction
float32_t makeFloat(uint32_t sign, uint32_t exponent, uint32_t fraction) {
    if(exponent == 0)
        return (float32_t){0};
    return (float32_t){(sign << 31) | (exponent << 23) | fraction};
}

void multiply_fractions(uint32_t a, uint32_t b, uint32_t* result_fraction, uint32_t* result_exp) {
    // Perform multiplication of fractions
    uint32_t a_lo = a & 0xFFFF;
    uint32_t a_hi = a >> 16;
    uint32_t b_lo = b & 0xFFFF;
    uint32_t b_hi = b >> 16;

    // Calculate partial products
    uint32_t prod_lo = a_lo * b_lo;
    uint32_t prod_mid1 = a_lo * b_hi;
    uint32_t prod_mid2 = a_hi * b_lo;
    uint32_t prod_hi = a_hi * b_hi;

    // Add mid products to the result
    uint32_t carry = 0;
    prod_mid1 += prod_mid2;
    if (prod_mid1 < prod_mid2) carry = 1;
    prod_lo += (prod_mid1 << 16);
    if (prod_lo < (prod_mid1 << 16)) carry = 1;

    // Add carry to higher bits
    prod_mid1 += (carry << 16);
    prod_hi += (prod_mid1 >> 16);
    uint32_t LSB_prod_hi;
    while(prod_hi>=1){
        LSB_prod_hi = prod_hi & 0x00000001;
        *result_exp +=1;
        prod_lo = prod_lo >> 1;
        prod_lo = (prod_lo | (LSB_prod_hi << 31));
        prod_hi >>=1;
    }
    while(prod_lo >= 0x1000000){
        *result_exp +=1;
        prod_lo >>=1;
    }
    *result_exp -= 23;
    *result_fraction = prod_lo &0x7FFFFF;
}

// Function to perform subtraction of two float32_t numbers
float32_t float_mul(float32_t a, float32_t b){
    uint32_t signA = extractSign(a);
    uint32_t signB = extractSign(b);
    uint32_t exponentA = extractExponent(a);
    uint32_t exponentB = extractExponent(b);
    uint32_t fractionA = extractFraction(a);
    uint32_t fractionB = extractFraction(b);

    uint32_t fractionResult;
    uint32_t expResult = 0;

    multiply_fractions((fractionA | 0x800000), (fractionB | 0x800000),&fractionResult,&expResult);

    uint32_t exponentResult = exponentB + exponentB + expResult -127;
    uint32_t signResult = signA ^ signB;
    return makeFloat(signResult,exponentResult,fractionResult);
}


// Function to add two floats using integer operations
float32_t float_add(float32_t a, float32_t b) {
    // Extract sign, exponent, and fraction from each number
    uint32_t signA = extractSign(a);
    uint32_t signB = extractSign(b);
    uint32_t exponentA = extractExponent(a);
    uint32_t exponentB = extractExponent(b);
    uint32_t fractionA = extractFraction(a);
    uint32_t fractionB = extractFraction(b);

    // Perform addition of significands with proper alignment
    if ((exponentA < exponentB) | ( (exponentA == exponentB) & (fractionA < fractionB))) {
        // Swap a and b
        uint32_t temp;
        temp = signA; signA = signB; signB = temp;
        temp = exponentA; exponentA = exponentB; exponentB = temp;
        temp = fractionA; fractionA = fractionB; fractionB = temp;
    }

    uint32_t signResult;
    uint32_t fractionResult;
    fractionA |= 0x800000;
    fractionB |= 0x800000;
    if(signA == signB) {
        // Combine signs
        fractionB >>= (exponentA - exponentB);
        signResult = signA;

        // Add fractions
        fractionResult = fractionA + fractionB;

        // Check for overflow
        if (fractionResult >= (1u << 23)) {
            fractionResult >>= 1;
            exponentA++;
        }
    } else {
        // Combine signs
        signResult = signA;

        // Add fractions with proper alignment
        fractionResult = fractionA - (fractionB >> (exponentA - exponentB));

        // Handle normalization and exponent adjustment
        if (fractionResult == 0)
            return makeFloat(0, 0, 0);

        while (fractionResult < (1u << 23)) {
            fractionResult <<= 1;
            exponentA--;

            if (exponentA == 0)
                return makeFloat(0, 0, 0);
        }

        fractionResult &= 0x7FFFFF; // Mask out excess bits
    }

    // Combine exponent
    uint32_t exponentResult = exponentA;

    // Construct the result
    return makeFloat(signResult, exponentResult, fractionResult);
}

// Function to perform subtraction of two float32_t numbers
float32_t float_sub(float32_t a, float32_t b){
    uint32_t signB = extractSign(b);
    if(signB == 0)
        b.value |= (0x80000000);
    else
        b.value &= 0x7FFFFFFF;
    return float_add(a,b);
}

// Function to convert fraction to binary
uint32_t fractionToBinary_int_exist(uint32_t fraction, uint32_t numBits,uint32_t digits) {
    int bit = 0;
    int tmp = 0;
    // Calculate fractional part in binary

    for (int i = 0; i < numBits; i++) {
        fraction *=2;

        int a = fraction - digits;
        int b = 0;
        if(a >= 0){
            fraction -= digits;
            b = 1;
        }
        bit = (bit << 1) | b;
    }

    return bit;
}


// Function to convert fraction to binary
uint32_t fractionToBinary_int_non_exist(uint32_t fraction,uint32_t digits,uint32_t *Exp_shift,char *iszero) {
    int bit = 0;
    int tmp = 0;
    // Calculate fractional part in binary
        while(bit == 0){
            fraction *=2;
            *Exp_shift +=1;

            int a = fraction - digits;
            int b = 0;
            if(a >= 0){
                fraction -= digits;
                b = 1;
                break;
            }
            if(*Exp_shift > 127)
            break;
        }
        if(*Exp_shift >= 127){
            *iszero = '1';
            return bit;
        }
            

        for (int i = 0; i < 23; i++) {
            fraction *=2;

            int a = fraction - digits;
            int b = 0;
            if(a >= 0){
                fraction -= digits;
                b = 1;
            }
            bit = (bit << 1) | b;
        }
    return bit;
}

float32_t stringToFloat(const char *str) {
    // Skip leading whitespace
    while (*str == ' ' || *str == '\t' || *str == '\n')
        str++;

    // Extract sign
    uint32_t sign = 0;
    if (*str == '-') {
        sign = 1;
        str++;
    } else if(*str == '+') {
        str++;
    }

    // Extract integer part
    uint32_t integerPart = 0;
    uint32_t integerLenthBit = 0;
    while (*str >= '0' && *str <= '9') {
        integerPart = integerPart * 10 + (*str - '0');
        str++;
    }
    
    uint32_t integerPartHold = integerPart;
    // Extract fractional part
    uint32_t fractionPart = 0;
    uint32_t fractionPartBit = 0;
    uint32_t fractionLength = 0;
    uint32_t Exp_shift = 0;
    if (*str == '.') {
        str++;
        while (*str >= '0' && *str <= '9') {
            fractionPart = fractionPart * 10 + (*str - '0');
            fractionLength++;
            str++;
        }
    }

    // Combine integer and fractional parts
    uint32_t exponent = 127; // Bias for single-precision exponent
    if(integerPart >= 1)
        exponent--;
    while (integerPart >= 1) {
        integerPart >>= 1;
        exponent++;
        integerLenthBit +=1;
    }
     uint32_t digits = 1;
     char iszero = '0';
     if(integerLenthBit > 23){
        integerPartHold -= 1u<<(integerLenthBit-1);
        return makeFloat(sign, exponent, integerPartHold);
    }   
    for(int i = 0 ; i<fractionLength ; i++)
            digits *= 10;

    if(integerLenthBit == 0){
        fractionPartBit = fractionToBinary_int_non_exist(fractionPart ,digits,&Exp_shift,&iszero);
        if(iszero == '1')
            return makeFloat(0, 0, 0);
        exponent -= Exp_shift;
        return makeFloat(sign, exponent, fractionPartBit);
    }
    fractionPartBit = fractionToBinary_int_exist(fractionPart, 24 - integerLenthBit,digits);
    integerPartHold -= 1u<<(integerLenthBit-1);


    integerPartHold = (integerPartHold << (24 - integerLenthBit)) + fractionPartBit;
    // Normalize fraction part

    // Construct the result
    return makeFloat(sign, exponent, integerPartHold);
}

// / Perform division of two floats using integer operations
float32_t float_divide(float32_t a, float32_t b) {
    // Extract sign, exponent, and fraction from each number
    uint32_t signA = extractSign(a);
    uint32_t signB = extractSign(b);
    uint32_t exponentA = extractExponent(a) ;
    uint32_t exponentB = extractExponent(b);
    uint32_t fractionA = extractFraction(a) | 0x800000;
    uint32_t fractionB = extractFraction(b) | 0x800000;

    // Check for special cases: division by zero or infinity
    if (fractionB == 0 || exponentB == 0xFF) {
        // Handle division by zero or infinity
        // You may want to implement error handling or return appropriate values here
        return makeFloat(0, 0, 0);
    }

    // Perform division of significands
    int quotientExponent = (int)exponentA - (int)exponentB + 127; // Bias for single-precision exponent
    int shift = 0;
    uint32_t quotientFraction = 0;

    // Normalize numerator fraction
    while (fractionA < fractionB) {
        fractionA <<= 1;
        shift++;
    }

    // Perform division
    for (int i = 0; i < 24; i++) {
        quotientFraction <<= 1;
        if (fractionA >= fractionB) {
            fractionA -= fractionB;
            quotientFraction |= 1;
        }
        fractionA <<= 1;

    }
    // Adjust exponent for normalization
    quotientExponent -= shift;
    quotientFraction &= 0x7FFFFF;
    // Create and return the result
    return makeFloat(signA ^ signB, (uint32_t)quotientExponent, quotientFraction);
}

// Function to compute the inverse sine (asin) using polynomial approximation
float32_t float_asin(float32_t x) {
    // Constants for the polynomial approximation
    float32_t A1 = makeFloat(0, 0x7F, 0x490DA4); // 1.5707288
    float32_t A2 = makeFloat(0, 0x7C, 0x593484); // 0.2121144
    float32_t A3 = makeFloat(0, 0x7B, 0x181627); // 0.0742610
    float32_t A4 = makeFloat(0, 0x79, 0x196E36); // 0.0187293


    // Absolute value of x
    float32_t abs_x = x;
    if (extractSign(x)){
        abs_x.value = x.value & 0x7FFFFFFF;
    }
    // Compute asin using the polynomial approximation
    float32_t x_squared = float_mul(abs_x, abs_x);
    float32_t term1 = float_mul(A4, x_squared);
    float32_t term2 = float_mul(A3, x_squared);
    term2 = float_add(term2, A2);
    term1 = float_add(term1, term2);
    term1 = float_mul(term1, x_squared);
    term1 = float_add(term1, A1);

    // Adjust the sign of the result
    float32_t result = term1;
    if (extractSign(x))
        result = float_sub(makeFloat(0, 0, 0), result);

    return result;
}

// Function to compute the inverse sine (asin) using polynomial approximation
uint32_t fp_Asin_simple(uint32_t x) {
    // Constants for the polynomial approximation

    int A1 = 0x3fc90da4; // 1.5707288
    int A2 = 0x3e593484; // 0.2121144
    int A3 = 0x3d981627; // 0.0742610
    int A4 = 0x3c996e30; // 0.0187293

    // Absolute value of x
    int abs_x = x;
    if (fp_ExtractSign(x)){
        abs_x = x & 0x7FFFFFFF;
    }
    // Compute asin using the polynomial approximation
    int x_squared = fpmul(abs_x, abs_x);
    int term1 = fpmul(A4, x_squared);
    int term2 = fpmul(A3, x_squared);
    term2 = fpadd(term2, A2);
    term1 = fpadd(term1, term2);
    term1 = fpmul(term1, x_squared);
    term1 = fpadd(term1, A1);

    // Adjust the sign of the result
    int result = term1;
    if (fp_ExtractSign(x))
        result &= 0x7FFFFFFF;

    return result;
}


// Function to compute the inverse sine (asin) using polynomial approximation
uint32_t fp_Asin(uint32_t x) {
    // Constants for the polynomial approximation
    uint32_t A3 = 0x3e2aaaab;//0.166666667
    uint32_t A5 = 0x3d99999a;//0.075
    uint32_t A7 = 0x3d36db6e;//0.04464285714
    uint32_t A9 = 0x3cf8e38e;//0.030381944



    // Compute asin using the polynomial approximation
    uint32_t x_2 = fpmul(x, x);
    uint32_t x_3 = fpmul(x_2, x);
    uint32_t x_5 = fpmul(x_3, x_2);
    uint32_t x_7 = fpmul(x_5, x_2);
    uint32_t x_9 = fpmul(x_7, x_2);

    uint32_t term1 = fpmul(x_3, A3);
    uint32_t term2 = fpmul(x_5, A5);
    uint32_t term3 = fpmul(x_7, A7);
    uint32_t term4 = fpmul(x_9, A9);

    uint32_t result = x;
    result = fpadd(x,term1);
    result = fpadd(result,term2);
    result = fpadd(result,term3);
    result = fpadd(result,term4);
    
    return result;
}

// Function to compute the inverse sine (asin) using polynomial approximation
float32_t float_asin_Taylor_series(float32_t x) {
    // Constants for the polynomial approximation
    float32_t A3;
    A3.value = 0x3e2aaaab;//0.333333
    float32_t A5;
    A5.value = 0x3d99999a;
    float32_t A7;
    A7.value = 0x3d36db6e;
    float32_t A9;
    A9.value = 0x3cf8e38e;



    // Compute asin using the polynomial approximation
    float32_t x_2 = float_mul(x, x);
    float32_t x_3 = float_mul(x_2, x);
    float32_t x_5 = float_mul(x_3, x_2);
    float32_t x_7 = float_mul(x_5, x_2);
    float32_t x_9 = float_mul(x_7, x_2);

    float32_t term1 = float_mul(x_3, A3);
    float32_t term2 = float_mul(x_5, A5);
    float32_t term3 = float_mul(x_7, A7);
    float32_t term4 = float_mul(x_9, A9);

    float32_t result = x;
    result = float_add(x,term1);
    result = float_add(result,term2);
    result = float_add(result,term3);
    result = float_add(result,term4);
    
    return result;
}


// Function to compute the inverse sine (asin) using polynomial approximation
float32_t float_Sqrt_Taylor_series(float32_t y) {
        // Constants for the polynomial approximation
    float32_t x;
    float32_t const_15;
    float32_t const_N_one;
    const_N_one.value = 0xbf800000;
    const_15.value = 0x41700000;
    x = float_divide(y,const_15);
    x = float_divide(x,const_N_one);
    float32_t Devider;
    Devider.value = 0x4077dee8;
    float32_t A1;
    A1.value = 0x3f000000;
    float32_t A2;
    A2.value = 0xbe000000;//0.333333
    float32_t A3;
    A3.value = 0x3d800000;
    float32_t A4;
    A4.value = 0xbd200000;
    float32_t A5;
    A5.value = 0x3ce00000;



    // Compute asin using the polynomial approximation
    float32_t x_2 = float_mul(x, x);
    float32_t x_3 = float_mul(x_2, x);
    float32_t x_4 = float_mul(x_3, x);
    float32_t x_5 = float_mul(x_4, x);



    float32_t term1 = float_mul(x, A1);
    float32_t term2 = float_mul(x_2, A2);
    float32_t term3 = float_mul(x_3, A3);
    float32_t term4 = float_mul(x_4, A4);
    float32_t term5 = float_mul(x_5, A5);
    float32_t result = x;
    float32_t constant;
    constant.value = 0x3f800000; 
    result = float_add(constant,term1);
    result = float_add(result,term2);
    result = float_add(result,term3);
    result = float_add(result,term4);
    result = float_add(result,term5);
    result = float_mul(result,Devider);
    return result;
}

//  Function to compute the sqrt(x) using polynomial approximation

/*
NOTE: This function is an apporximation of sqrt(x) where 0 < x < 30.
If your x is not in this range consider normalizing by adjusting the value
of const_15 and the Devider
the approximation is g(x) = sqrt(x+1)  for -1 < x < 1. You need to bring the range of your x to this range 
using follwoing formula:  
your function ==> f(x) for  n < x < m
f(x) = sqrt(m-n) * g(x/(m-n) - 1) for -1 < x < 1
*/
uint32_t fp_Sqrt(uint32_t n) {
  // Max and min are used to take into account numbers less than 1
  uint32_t lo,hi,mid;
  uint32_t Const001 = 0x3c23d70a;//0.01
  uint32_t Const01 = 0x3dcccccd;//0.1
  uint32_t Const1 = 0x3f800000;//1.0
  uint32_t Const10 = 0x41200000;//10.0
  uint32_t Const100 = 0x42c80000;//100.0
  uint32_t Const2 = 0x40000000;//2.0

  //Calculate lo 
  uint32_t tmp_min = fpsub(n,1);
  if(!fp_ExtractSign(tmp_min))
    lo = 0x3f800000;//1.0
  else 
    lo = n;

  //Calculate hi
  if(fp_ExtractSign(tmp_min))
    hi = 0x3f800000;//1.0
  else 
    hi = n;


  // Update the bounds to be off the target by a factor of 10
  while(fp_ExtractSign( fpsub(fpmul(fpmul(Const100,lo),lo) , n))) lo = fpmul(lo,Const10);
  while(!fp_ExtractSign( fpsub(fpmul(fpmul(Const001,hi),hi) , n))) hi = fpmul(hi,Const01);


  for(int i = 0 ; i < 100 ; i++){
      mid = fpdiv(fpadd(lo,hi),Const2);
      if(fpmul(mid,mid) == n) return mid;
      if(!fp_ExtractSign(fpsub(fpmul(mid,mid), n))) hi = mid;
      else lo = mid;
  }
  return mid;
}
uint32_t fp_Sqrt_x_lt_30(uint32_t y) {
    //     // Constants for the polynomial approximation
    //     static int counterF = 0;
    // float* yF = &y;
    // if(*yF >30.0){
    //     counterF+=1;
    //     // printf("\n%d %f",counterF,*yF);
    // }
    // uint32_t x;
    // uint32_t const_15 = 0x41700000;
    // uint32_t const_N_one = 0xbf800000;
    // x = fpdiv(y,const_15);
    // x = fpdiv(x,const_N_one);
    // uint32_t Devider = 0x4077dee8;
    // uint32_t A1 = 0x3f000000;
    // uint32_t A2 = 0xbe000000;//0.333333
    // uint32_t A3 = 0x3d800000;
    // uint32_t A4 = 0xbd200000;
    // uint32_t A5 = 0x3ce00000;



    // // Compute sqrt(x) using the polynomial approximation
    // uint32_t x_2 = fpmul(x, x);
    // uint32_t x_3 = fpmul(x_2, x);
    // uint32_t x_4 = fpmul(x_3, x);
    // uint32_t x_5 = fpmul(x_4, x);



    // uint32_t term1 = fpmul(x, A1);
    // uint32_t term2 = fpmul(x_2, A2);
    // uint32_t term3 = fpmul(x_3, A3);
    // uint32_t term4 = fpmul(x_4, A4);
    // uint32_t term5 = fpmul(x_5, A5);
    // uint32_t result = x;
    // uint32_t constant = 0x3f800000; 
    // result = fpadd(constant,term1);
    // result = fpadd(result,term2);
    // result = fpadd(result,term3);
    // result = fpadd(result,term4);
    // result = fpadd(result,term5);
    // // Denormalize the result
    // result = fpmul(result,Devider);
    return 0;
}


// Function to compute the cos using polynomial approximation
float32_t float_Cos_Taylor_series(float32_t x) {
// Constants for the polynomial approximation

    float32_t A2;
    A2.value = 0xbf000000;//0.333333
    float32_t A4;
    A4.value = 0x3d2aaaab;
    float32_t A6;
    A6.value = 0xbab60b61;



    // Compute cos using the polynomial approximation
    float32_t x_2 = float_mul(x, x);
    float32_t x_4 = float_mul(x_2, x_2);
    float32_t x_6 = float_mul(x_4, x_2);

    float32_t term2 = float_mul(x_2, A2);
    float32_t term4 = float_mul(x_4, A4);
    float32_t term6 = float_mul(x_6, A6);

    float32_t result = x;
    float32_t constant;
    constant.value = 0x3f800000; 
    result = float_add(constant,term2);
    result = float_add(result,term4);
    result = float_add(result,term6);
    return result;
}


// Function to compute the cos using polynomial approximation
uint32_t fp_Cos(uint32_t x) {
// Constants for the polynomial approximation
// display_print(0,0,"value to enter cosed: ");display_print(1,x,"");
    uint32_t sign = fp_ExtractSign(x);
    if(sign)
        x &= 0x7FFFFFFF;
// Bring x to the range of -pi and pi
    uint32_t y = fpdiv(x,0x40c90fdb);
    y = cast_Fp_To_Int(y);
    y = int_to_float(y);
    x = fpsub(x,fpmul(y,0x40c90fdb));
    uint32_t flag_singed_reverse = 0;
    if(fp_ExtractSign(fpsub(x,0x3fc90fdb))){
        x = fpsub(0x40490fdb,x);
        flag_singed_reverse = 1;
    }
    else if(fp_ExtractSign(fpsub(0x4096cbe4,x))){
        x = fpsub(0x4116cbe4,x);
        flag_singed_reverse = 1;
    }

    x = fpsub(x,0x40490fdb);
    // display_print(0,0,"value to be cosed: ");display_print(1,x,"");
    uint32_t A2 = 0x3f000000;//0.5
    uint32_t A4 = 0xbd2aaaab;//-0.041666668 = -1/24
    uint32_t A6 = 0x3ab60b60;//0.0013888888 = 1/720
    uint32_t A8 = 0xb7d00998;//-0.0000248 = -1/40320
    uint32_t A10 = 0x3493f27e;//0.000000275573192 = 1/3628800
    uint32_t A12 = 0xb2b35479;

    // Compute cos using the polynomial approximation
    uint32_t x_2 = fpmul(x, x);
    uint32_t x_4 = fpmul(x_2, x_2);
    uint32_t x_6 = fpmul(x_4, x_2);
    uint32_t x_8 = fpmul(x_6, x_2);
    uint32_t x_10 = fpmul(x_8, x_2);
    uint32_t x_12 = fpmul(x_10, x_2);

    uint32_t term2 = fpmul(x_2, A2);
    uint32_t term4 = fpmul(x_4, A4);
    uint32_t term6 = fpmul(x_6, A6);
    uint32_t term8 = fpmul(x_8, A8);
    uint32_t term10 = fpmul(x_10,A10);
    uint32_t term12 = fpmul(x_12,A12);

    uint32_t result = x;
    uint32_t constant = 0xbf800000; 
    result = fpadd(constant,term2);
    result = fpadd(result,term4);
    result = fpadd(result,term6);
    result = fpadd(result,term8);
    result = fpadd(result,term10);
    result = fpadd(result,term12);
    // display_print(0,0,"cos results ");display_print(1,result,"");
    if(flag_singed_reverse){
        if(fp_ExtractSign(result))
            result &= 0x7FFFFFFF;
        else
            result |= 0x80000000;
    }
        
    return result;
}

uint32_t fp_Sin(uint32_t x){
// Constants for the polynomial approximation
// check the value's sign
// display_print(0,0,"value to enter sined: ");display_print(1,x,"");
    uint32_t sign  = fp_ExtractSign(x);
    if(sign)
        x &= 0x7FFFFFFF;
// Bring x to the range of 0 and 2*pi
    uint32_t y = fpdiv(x,0x40c90fdb);
    y = cast_Fp_To_Int(y);
    y = int_to_float(y);
    x = fpsub(x,fpmul(y,0x40c90fdb));
    if(fp_ExtractSign(fpsub(x,0x3fc90fdb)))
        x = fpsub(0x40490fdb,x);
    else if(fp_ExtractSign(fpsub(0x4096cbe4,x)))
        x = fpsub(0x4116cbe4,x);
    x = fpsub(x,0x40490fdb);
    // if(sign)
    //     x = fpsub(0,x);
    // display_print(0,0,"value to be sined: ");display_print(1,x,"");
    uint32_t A1 = 0xbf800000;//-1
    uint32_t A3 = 0x3e2aaaab;//0.1666666667 = 1/6
    uint32_t A5 = 0xbc088889;//0.008333333333 = -1/120
    uint32_t A7 = 0x39500d01;//0.000198412698 = 1/5040
    uint32_t A9 = 0xb493f27e;//-0.000000275573192 = -1/3628800
    uint32_t A11 = 0x32d7322b;
    // Compute cos using the polynomial approximation
    uint32_t x_1 = x;
    uint32_t x_2 = fpmul(x_1,x_1);
    uint32_t x_3 = fpmul(x_1, x_2);
    uint32_t x_5 = fpmul(x_3, x_2);
    uint32_t x_7 = fpmul(x_5, x_2);
    uint32_t x_9 = fpmul(x_7, x_2);
    uint32_t x_11 = fpmul(x_9, x_2);

    uint32_t term1 = fpmul(x_1, A1);
    uint32_t term3 = fpmul(x_3, A3);
    uint32_t term5 = fpmul(x_5, A5);
    uint32_t term7 = fpmul(x_7, A7);
    uint32_t term9 = fpmul(x_9, A9);
    uint32_t term11 = fpmul(x_11, A11);

    uint32_t result = x;
    // int constant = 0x3f800000; 
    result = fpadd(term1,term3);
    result = fpadd(result,term5);
    result = fpadd(result,term7);
    result = fpadd(result,term9);
    result = fpadd(result,term11);
    if(sign)
        result = fpsub(0,result);
    // display_print(0,0,"sin results ");display_print(1,result,"");
    return result;
}

// Function to compute the pow(x,y) assuming that y doesnt have integer     
float32_t power(float32_t base, float32_t exponent_t) {
    float32_t result;
    result.value = 0x3f800000;
    float32_t const_1;
    const_1.value = 0x3f800000;
    int i;
    uint32_t exponent = extractExponent(exponent_t) - 127;
    // Handle negative exponents
    if (exponent < 0) {
        base = float_divide(const_1,base);
    }
    uint32_t itr = (1u << exponent);
    for (i = 0; i < itr; i++) {
        result = float_mul(result,base);
    }

    return result;
}


// Function to compute the pow(x,y) using polynomial approximation 
//  Here we assume that exponent is normalized and not in the denormalized range
uint32_t fp_Pow(uint32_t base, uint32_t exponent) {

    // if exponent is zero return 1.0
    int result = 0x3f800000;// result  = 1.0
    if(exponent == 0)
        return 0x3f800000;// return 1.0


    int eSign = fp_ExtractSign(exponent);
    int eExponet = fp_ExtractExponent(exponent);
    int eFraction = fp_ExtractFraction(exponent);
    int intPower = 0;
    if(eExponet >=150){
        intPower = ((eFraction|0x800000) << (eExponet - 150));
        for(int i=0 ; i < intPower ; i++)
            result = fpmul(result,base);
        return result;
    }
    if(eExponet >= 127 && eExponet < 150){
        intPower = (eFraction | 0x800000) >> (150 - eExponet);
        for(int i = 0 ; i < intPower ; i++)
            result = fpmul(result,base);
        // fp_Pow_taylor()
        return result;
    }
    return 1;
}

// Function to compute the pow(x,y) using polynomial approximation 
//  Here we assume that exponent is normalized and not in the denormalized range
// int pow_fp_itr(int base, int exponent) {
//         // if exponent is zero return 1.0
//     int result = 0x3f800000;// result  = 1.0
//     if(exponent == 0)
//         return 0x3f800000;// return 1.0

//     if(base == 0x3f800000)// if base == 1.0
//         return 0x3f800000;// return 1.0

//     if(base == 0)
//      return 0;

//     for(int i=0 ; i < exponent ; i++)
//         result = fpmul(result,base);
//     return result;
// }

// calculate absolute value of floating point number x
uint32_t fp_Fabs(uint32_t x) {
    if(fp_ExtractExponent(x))
        x &= 0x7FFFFFFF;
    return x;
}

uint32_t fp_Reg2deg(uint32_t x){
    int coeff = 0x3c8ee7a7;
    return fpmul(coeff,x);
}

uint32_t eg2rad(uint32_t x){
    int coeff = 0x42654ca3;
    return fpmul(coeff,x);
}

uint32_t fp_Acos(uint32_t x){
    int Pi_2 = 0x3fc8f5c3;
   return fpsub(Pi_2 , fp_Asin(x));
}


// Function to convert an integer to a string
void intToString(uint32_t num, char* str) {
    if (num == 0) {
        str[0] = '0';
        str[1] = '\0';
        return;
    }

    int i = 0;
    if (num < 0) {
        str[i++] = '-';
        num = -num;
    }

    int len = 0;
    int temp = num;
    while (temp > 0) {
        temp /= 10;
        len++;
    }

    str[i + len] = '\0'; // Null-terminate the string

    for (int j = i + len - 1; j >= i; j--) {
        str[j] = num % 10 + '0'; // Convert digit to character
        num /= 10;
    }
}

uint32_t fp_Exp(uint32_t x){                                              //|//     double integer = trunc(x);          
    // uint32_t Exponent = fp_ExtractExponent(x);                            //|//     // X is now the fractional part of the number.                                                                    
    // uint32_t Fraction = fp_ExtractFraction(x);                            //|//     x = x - integer;                                       
    // uint32_t Sign = fp_ExtractSign(x);                                //|//                                   
    // uint32_t X_Fraction = 0x3F800000 | (Fraction);          //|//     // Use a 4-part polynomial to approximate exp(x);                                                        
    // uint32_t Integer;
    // uint32_t Decimal_Fraction;

    // float* valF = &x;

    // // printf("\ninput to exp %f\n",*valF);
    // if(Exponent <127){
    //     Integer = 0;
    //     Decimal_Fraction = (x & 0x7FFFFFFF);
    // }
    // else if(Exponent>=127 && Exponent <=150){
    //     Integer = ((Fraction | 0x800000) >> (150-Exponent));
    //     if(Integer > 88){//printf("\nIngeter is big sign is %d",Sign);
    //         if(Sign)
    //             return 0;
    //         else{
    //             // printf("\nThe fp_exp recieved a very big number");
    //             exit(1);
    //         }
    //     }
    //     Decimal_Fraction = Fraction  << (Exponent - 118);
    //     Decimal_Fraction >>= (9);
       
    //     int shift = 0;
    //     if(Decimal_Fraction != 0){        

    //     while(!(Decimal_Fraction & 0x400000)){
    //         shift+=1;
    //         Decimal_Fraction <<=1;
    //     }
    //     Decimal_Fraction = ((Decimal_Fraction <<1)&0x7FFFFF) | ((127 - shift-1)<<23);
    //     }
    // }    
    // else if(Exponent > 150){
    //     // printf("\nThe fp_exp recieved very big number");
    //     exit(1);
    // }    
    // uint32_t A1 = 0x3e8f8857;                                             //|//                      
    // uint32_t A2 = 0x3ed9c12f;                                             //|//     // Use Horner's method to evaluate the polynomial.                     
    // uint32_t A3 = 0x3f81a159;                                             //|     double val = c[3] + x * (c[2] + x * (c[1] + x * (c[0])));                     
    // uint32_t A4 = 0x3f8006dd;                                             //|//     return val * EXP_TABLE[(unsigned)integer + table_zero_idx];                     

    // uint32_t expA_1 = fpmul(Decimal_Fraction,A1);
    // uint32_t expA_2 = fpadd(expA_1,A2);
    // uint32_t expA_3 = fpmul(Decimal_Fraction,expA_2);
    // uint32_t expA_4 = fpadd(expA_3,A3);
    // uint32_t expA_5 = fpmul(Decimal_Fraction,expA_4);
    // uint32_t expA_6 = fpadd(expA_5,A4);

    // uint32_t expInteger[104] = {  0x3f800000, 0x402df854, 0x40ec7326, 0x41a0af2e, 0x425a6481, 0x431469c5, 0x43c9b6e3, 0x44891443
    //                             , 0x453a4f54, 0x45fd38ac, 0x46ac14ee, 0x4769e224, 0x481ef0b3, 0x48d805ad, 0x4992cd62, 0x4a478665
    //                             , 0x4b07975f, 0x4bb849a4, 0x4c7a7910, 0x4d2a36c8, 0x4de75844, 0x4e9d3710, 0x4f55ad6e, 0x5011357a
    //                             , 0x50c55bfe, 0x51861e9d, 0x52364993, 0x52f7c118, 0x53a85dd2, 0x5464d572, 0x551b8238, 0x55d35bb3
    //                             , 0x568fa1fe, 0x5743379a, 0x5804a9f1, 0x58b44f11, 0x597510ad, 0x5a2689fe, 0x5ae2599a, 0x5b99d21f
    //                             , 0x5c51106a, 0x5d0e12e4, 0x5dc1192b, 0x5e833952, 0x5f325a0e, 0x5ff267bb, 0x60a4bb3e, 0x615fe4a9
    //                             , 0x621826b5, 0x62cecb81, 0x638c881f, 0x643f009e, 0x6501ccb3, 0x65b06a7b, 0x666fc62d, 0x6722f184
    //                             , 0x67dd768b, 0x68967ff0, 0x694c8ce5, 0x6a0b01a3, 0x6abcede5, 0x6b806408, 0x6c2e804a, 0x6ced2bef
    //                             , 0x6da12cc1, 0x6e5b0f2e, 0x6f14ddc1, 0x6fca5487, 0x70897f64, 0x713ae0ee, 0x71fdfe91, 0x72ac9b6a
    //                             , 0x736a98ec, 0x741f6ce9, 0x74d8ae7f, 0x7593401c, 0x76482254, 0x77080156, 0x77b8d9aa, 0x787b3ccf
    //                             , 0x792abbce, 0x79e80d11, 0x7a9db1ed, 0x7b56546b, 0x7c11a6f5, 0x7cc5f63b, 0x7d86876d, 0x7e36d809
    //                             , 0x7ef882b7, 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000
    //                             , 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000, 0x7f800000};
    
    // uint32_t result = fpmul(expInteger[Integer],expA_6);
    // if(Sign)
    //     return fpdiv(0x3f800000,result);
    return x;
}
// Casting float to integer. if x is greater than the range of integer the result is invalid
// This is equivalent of (int)x where x is a float
int cast_Fp_To_Int(uint32_t x){
    uint32_t S = fp_ExtractSign(x);
    uint32_t F = fp_ExtractFraction(x);
    uint32_t E = fp_ExtractExponent(x);
    int exponent = E - 127; 
    uint32_t result = F | 0x800000;
// float* xf = &x;printf("\nin cast %f %d %u",*xf, exponent,F);
    if (exponent >= 23) {
        result <<= (exponent - 23);  // Shift left if exponent is larger
    } else if (exponent >= 0) {
        result >>= (23 - exponent);  // Shift right if exponent is smaller
    } else {
          // If the exponent is too small, the result is 0 (as integer)
        return 0;
    }

    // Apply the sign bit
    
    int result_int = result;
    if (S) {
        result_int = -1*(int)result;
    }
    return result_int;
}


uint32_t int_to_float(int x) {
    // Handle special case for zero
    if (x == 0) {
        return 0;  // IEEE 754 representation of 0 is all bits zero
    }
    
    // Step 1: Determine the sign bit
    uint32_t sign = x < 0 ? 1 : 0;

    // Step 2: Compute the absolute value
    uint32_t abs_x = sign ? -x : x;

    // Step 3: Find the position of the highest set bit (MSB)
    uint32_t exponent = 0;
    uint32_t temp = abs_x;
    while (temp != 0) {
        exponent++;
        temp >>= 1;
    }

    // Step 4: Normalize the absolute value (shift left to have MSB at the 24th position)
    uint32_t normalized = abs_x;
    if (exponent > 0 && exponent <= 24) {
        normalized = abs_x << (23 - (exponent - 1));
    }

    if(exponent > 24)
        normalized = abs_x >> (exponent - 24);
    // Step 5: Mask the 23 bits of the fraction
    uint32_t fraction = normalized & 0x7FFFFF; // Mask out the lower 23 bits for fraction
    // printf("\n%d %u %u %u",x,fraction,exponent,sign);
    // Step 6: Adjust the exponent with the bias (127)
    exponent = (exponent - 1) + 127;

    // Step 7: Combine sign, exponent, and fraction to form the floating-point representation
    uint32_t result = (sign << 31) | (exponent << 23) | fraction;

    return result;
}
void memset_Char_t(unsigned char* ptr,char value,uint32_t size){}

void memset_Int_t(uint32_t* ptr,uint32_t value,uint32_t size){}




// uint32_t call_fpmul_py_CAPI(uint32_t RS1,uint32_t RS2){
//     float *af = &RS1;
//     float *bf = &RS2;
//     // printf("\na = %f, b = %f",*af,*bf);
//    // Set PYTHONPATH TO working directory
//     setenv("PYTHONPATH", ".", 1);
//     unsigned int result;
//     PyObject *pName, *pModule, *pDict, *pFunc, *pArgs, *pResult;

//     // Initialize the Python Interpreter
//     Py_Initialize();

//     // Build the name object
//     pName = PyUnicode_FromString("AFPM");

//     // Load the module object
//     pModule = PyImport_Import(pName);

//     // Check if the module was loaded successfully
//     if (pModule != NULL) {
//         // pDict is a borrowed reference 
//         pDict = PyModule_GetDict(pModule);

//         // pFunc is also a borrowed reference 
//         pFunc = PyDict_GetItemString(pDict, "AFPM");

//         if (PyCallable_Check(pFunc)) {
//             // Prepare the arguments (two unsigned integers)
//             pArgs = Py_BuildValue("(II)", RS1, RS2);

//             // Call the Python function with the arguments
//             pResult = PyObject_CallObject(pFunc, pArgs);

//             // Check for errors in the function call
//             if (pResult != NULL) {
//                 // Convert the result back to an unsigned int
//                 result = (unsigned int)PyLong_AsUnsignedLong(pResult);
//                 // printf("Result is %u\n", result);

//                 // Decrement the reference count for the result
//                 Py_DECREF(pResult);
//             } else {
//                 PyErr_Print();
//             }

//             // Decrement the reference count for the arguments
//             Py_DECREF(pArgs);
//         } else {
//             PyErr_Print();
//         }

//         // Decrement the reference count for the module and name objects
//         Py_DECREF(pModule);
//         Py_DECREF(pName);
//     } else {
//         PyErr_Print();
//     }

//     // Finish the Python Interpreter
//     Py_Finalize();
//     return result;
// }

/*
void pr_uint32(char space,uint32_t x){
    float *y = &x;
    printf("%c%5.20f",space,*y); 
}
*/

/// YR

/// to Invert float nums sign
uint32_t signInv(uint32_t x){
    uint32_t sign = fp_ExtractSign(x);
    uint32_t inversedNum;
    if(sign){
        inversedNum = x & 0x7FFFFFFF; 
    }
    else{
        inversedNum = x | 0x80000000;
    }
    return inversedNum;
}

/// to print int without whitespace
void PrintInt(uint32_t num){
    if(num == 0){
        checkprint_str((uint32_t)('0'),0);
        return;
    }
    if(num>>31){
        checkprint_str((uint32_t)('-'),0);
        num = 0 - num;
    }
    uint32_t numcpy = num;
    uint32_t revnum[12];
    int n=0;
    while(numcpy>0){
        revnum[n] = numcpy%10;
        numcpy/=10;
        n++;
    }
    n--;
    while(n>=0){
        checkprint_str((uint32_t)('0'+revnum[n]),0);
        n--;
    }

}

/// printf like function
/// args should be in PRINTVARS
/// Currently only   %.*s %.4s %d %f %s %c %08lx   are implemented
/// todo: %02d
void Print(char *str,printvar *var){
    // int flag = 0;
    // int counter = 0;
    // int iter = 0;
    // int rs1 = 0;;
    // int rs2 = 0;
    // int numflag = 0;
    // while(str[iter]!='\0'){
    //     if(counter == 8) goto y;
        
    //     else if(flag == 1){
    //         flag=0;
    //         if(str[iter]=='%'){
    //             goto x;
    //         }
    //         else{
    //             numflag = 1;
    //             if(counter!=0) goto y;
    //             z:
    //             if(str[iter]=='0' && str[iter+1]=='8'&& str[iter+2]=='l' && str[iter+3]=='x'){
    //                 printHex(var->number);
    //                 iter +=3;
    //             }
    //             else if(str[iter]=='.' && str[iter+1]=='*'&& str[iter+2]=='s'){
    //                 for(int i=0;i<var->number;i++){
    //                     Print("%c",PRINTVARS(*((var+1)->str+i)));
    //                 }
    //                 var++;
    //                 iter +=2;
    //             }
    //             else if(str[iter]=='.' && str[iter+1]=='4'&& str[iter+2]=='s'){
    //                 for(int i=0;i<4;i++){
    //                     Print("%c",PRINTVARS(*((var)->str+i)));
    //                 }
    //                 iter +=2;
    //             }
    //             else if(str[iter]=='d'){
    //                 PrintInt(var->number);
    //             }
    //             else if(str[iter]=='f'){
    //                 checkprint_float(var->number);
    //                 rs1 = 0x08080808;
    //                 rs2 = 0x08080000;
    //                 checkprint_str(rs1,rs2);
    //                 rs1 = 0x20202020;
    //                 rs2 = 0x20200000;
    //                 checkprint_str(rs1,rs2);
    //                 rs1 = 0x08080808;
    //                 rs2 = 0x08080000;
    //                 checkprint_str(rs1,rs2);
    //                 rs1=0;
    //                 rs2=0;
    //                 if(var->number == 0){
    //                     checkprint_str(0x30300000,0);
    //                 }
    //             }
    //             else if(str[iter]=='s'){
    //                 Print(var->str,0);    
    //             }
    //             else if(str[iter]=='c'){
    //                 char output[1] = {var->str};
    //                 Print(output,0);
    //             }
    //             var++;
    //             numflag = 0;
    //         }
    //     }
    //     else if(str[iter]=='%'){
    //         flag = 1;
    //     }
    //     else{
    //     x:  
    //         if(counter<4){
    //             rs1 = (rs1 << 8) + (uint32_t)str[iter];
    //         }
    //         else{
    //             rs2 = (rs2 << 8) + (uint32_t)str[iter];
    //         }
    //         counter++;
    //     }
    //     iter++;
    //     continue;
    //     y:  checkprint_str(rs1,rs2);
    //         rs1 = 0;
    //         rs2 = 0;
    //         counter = 0;
    //         if(numflag) goto z;
    // }
    // if(counter!=0){
    //     checkprint_str(rs1,rs2);
    // }
}

/// snprintf like function
/// args should be in PRINTVARS
/// Currently only   %d %f %s %c   are implemented
/// todo: Print float numbers with low or high power in e+x / e-x format
void snPrint(char* buffer,int n,char *str,printvar*var){
    int flag = 0;
    int iter = 0;
    int bufit = 0;
    while(1){
        if(flag == 1){
            flag=0;
            if(str[iter]=='%'){
                buffer[bufit] = str[iter];
                bufit++;
            }
            else{
                if(str[iter]=='d'){
                    if(var->number>>31){
                        buffer[bufit] = '-';
                        bufit++;
                        var->number ^= 0xFFFFFFFF;
                        var->number += 1;   
                    }
                    uint32_t numcpy = var->number;
                    uint32_t revnum = 0;
                    int m=0;
                    while(numcpy>0){
                        if(numcpy%10==0) m++;
                        revnum = revnum * 10 + numcpy%10;
                        numcpy/=10;
                    }
                    while(revnum>0){
                        if(bufit == n-2)  goto x;
                        buffer[bufit] = '0'+revnum%10;
                        revnum /= 10;
                        bufit++;
                    }
                    while(m>0){
                        if(bufit == n-2)  goto x;
                        buffer[bufit] = '0';
                        m--;
                        bufit++;
                    }
                }
                else if(str[iter]=='f'){
                    if(var->number>>31){
                        buffer[bufit] = '-';
                        bufit++; 
                    }
                    int exponent = ((var->number >> 23) & 0xFF) - 127;
                    int mantissa = var->number & 0x7FFFFF;
                    mantissa |= 0x800000;
                    if(var->number == 0) {mantissa = 0; exponent = 0;}
                    uint32_t integer_part = 0;
                    if(exponent>30){
                        integer_part = 0;
                    }
                    else if (exponent > 23) {
                        integer_part = mantissa << (exponent - 23);
                        mantissa = 0;
                    } else if (exponent >= 0) {
                        integer_part = mantissa >> (23 - exponent);
                        mantissa &= (1 << (23 - exponent)) - 1;
                        mantissa = mantissa << (exponent+1);
                    } else {
                        integer_part = 0;
                    }
                    if(integer_part){
                        int numcpy = integer_part;
                        int revnum = 0;
                        int m=0;
                        while(numcpy>0){
                            if(numcpy%10==0) m++;
                            revnum = revnum * 10 + numcpy%10;
                            numcpy/=10;
                        }
                        while(revnum>0){
                            if(bufit == n-2)  goto x;
                            buffer[bufit] = '0'+revnum%10;
                            bufit++;
                            revnum /= 10; 
                        }
                        while(m>0){
                            if(bufit == n-2)  goto x;
                            buffer[bufit] = '0';
                            bufit++;
                            m--;
                        }
                    }
                    else{
                        if(exponent>30){
                            if(bufit == n-2)  goto x;
                            char x[]="Inf";
                            for(int i =0 ; i<3 ; i++){
                                buffer[bufit] = x[i];
                                bufit++;
                            }
                            mantissa = 0;
                        }
                        else{
                            if(bufit == n-2)  goto x;
                            buffer[bufit] = '0';
                            bufit++;
                        }
                    }
                    if(bufit == n-2)  goto x; 
                    if(mantissa){
                        buffer[bufit] = '.';
                        bufit++;
                        uint32_t fractional_part = 0;
                        uint32_t fractional_scale = 2;
                        while(exponent<-1){
                            fractional_scale = fractional_scale * 2;
                            exponent++;
                        }
                        if(exponent<-14 || exponent == 0){
                            mantissa = 0;
                        }
                        while(mantissa) {
                            mantissa= mantissa << 1;
                            fractional_part = fractional_part * 2 + (mantissa >> 23);
                            mantissa &= 0x7FFFFF;
                            fractional_scale *= 2;
                        }
                        for (int i = 0; i < 8; i++) {
                            if(bufit == n-2)  goto x;
                            fractional_part *= 10;
                            if(fractional_part / fractional_scale){
                                buffer[bufit] = (fractional_part / fractional_scale) + '0';
                                bufit++;
                            }
                            fractional_part %= fractional_scale;
                        }
                    }
                    else if(exponent<=30){
                        buffer[bufit] = '.';
                        bufit++;
                        buffer[bufit] = '0';
                        bufit++;
                    }
                }
                else if(str[iter]=='s'){
                    int i=0;
                    while(var->str[i]){
                        if(bufit == n-2)  goto x;
                        buffer[bufit] = var->str[i];
                        bufit++;
                        i++;
                    }
                }
                var++;
            }
        }
        else if(str[iter]=='%'){
            flag = 1;
        }
        else{
            buffer[bufit] = str[iter];
            bufit++;
        }
        iter++;
        if(bufit==n-2 || str[iter]=='\0')   break;
        continue;
        x: break;
    }
    buffer[bufit] = '\0';
}

/// Print 32 bit Numbers in Hex format 
void printHex(uint32_t x){
    char *hexDigits[] = {"0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"};
    int i = 8;
    while(i>0){
      uint32_t digitToPrint = (x & 0xF0000000) >> 28;
      display_print(0,0,hexDigits[digitToPrint]);
      x = x << 4;
      i--;
    }
}

/// length of string returns
int strlen(char *str){
    if (!str)
        return 0;
    int counter=0;
    for(int i=0; *(str+i)!='\0';i++){
        counter++;
    }
    return counter;
}

/// strncpy like function
void strncpy(char *dest, const char *src, size_t n) {
    size_t i = 0;

    while (i < n && src[i] != '\0') {
        dest[i] = src[i];
        i++;
    }

    while (i < n) {
        dest[i] = '\0';
        i++;
    }
}

/// strcpy like function
void strcpy(char *dest, const char *src) {
    while (*src != '\0') {
        *dest = *src;
        dest++;
        src++;
    }
    *dest = '\0';
}

/// Initialize random number generator
void Srand(unsigned int seed){
  int i;
  mt_initialized = 1;
  for (i=0;i<N;i++)
  {
    mt[i] = seed & 0xffff0000;
    seed = 69069 * seed + 1;
    mt[i] |= (seed & 0xffff0000) >> 16;
    seed = 69069 * seed + 1;
  }
  mti = N;
}

/// Generate random number
unsigned int Rand(void){
  if (!mt_initialized){
    display_print(0,0,"ERROR: rng is not initialized, call Srand()!\n");
  }
  unsigned int y;
  static unsigned int mag01[2]={0x0, MATRIX_A};

  if (mti >= N)
  {
    int kk;

    if (mti == N+1)
      Srand(4357);

    for (kk=0;kk<N-M;kk++)
    {
      y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
      mt[kk] = mt[kk+M] ^ (y >> 1) ^ mag01[y & 0x1];
    }
    for (;kk<N-1;kk++)
    {
      y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
      mt[kk] = mt[kk+(M-N)] ^ (y >> 1) ^ mag01[y & 0x1];
    }
    y = (mt[N-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);
    mt[N-1] = mt[M-1] ^ (y >> 1) ^ mag01[y & 0x1];

    mti = 0;
  }

  y = mt[mti++];
  y ^= TEMPERING_SHIFT_U(y);
  y ^= TEMPERING_SHIFT_S(y) & TEMPERING_MASK_B;
  y ^= TEMPERING_SHIFT_T(y) & TEMPERING_MASK_C;
  y ^= TEMPERING_SHIFT_L(y);

  return y & RAND_MAX;
}

/// Compare two strings
int strcmp(const char *str1, const char *str2) {
    while (*str1 && *str2) {
        if (*str1 != *str2) {
            return *str1 - *str2;
        }
        str1++;
        str2++;
    }
    return *str1 - *str2;
}

/// Convert string to float
/// It only works for low precision float numbers
uint32_t Atof(const char *str){
    uint32_t output = 0;
    uint32_t base = 0;
    int counter = 0;
    if(*str=='+' || *str == '-'){
        if(*str == '-'){
            output |= 0x8FFFFFFF;
        }
        str++;
    }
    while(*str!='.' && *str && (*str-48 <10)){
        base *= 10;
        base += *str-48;
        str++;
    }
    if(*str == '.') str++;
    while(*str && *str-48 < 10){
        base *= 10;
        base += *str-48;
        counter++;
        str++;
    }
    output = int_to_float(base) | output;
    while(counter>0){
        output = fpdiv(output,0x41200000); /// 10
        counter--;
    }
    return output;
}

/// -2147483520 to 2147483520
// uint32_t floor(uint32_t x){
//     uint32_t sign = fp_ExtractSign(x);
//     uint32_t exp = fp_ExtractExponent(x);
//     uint32_t mant = fp_ExtractFraction(x);
//     mant |= 0x800000;
//     if(exp<127){
//         return int_to_float((0+sign)*(sign?-1:1));
//     }
//     else{
//         if(exp<151){
//             mant = mant >> (150-exp);
//             return int_to_float(((int)mant+sign)*(sign?-1:1));
//         }
//         else{
//             mant = mant << (exp-150);
//             return int_to_float(((int)mant+sign)*(sign?-1:1));
//         }
//     }
// }

/// Convert string to integer
int atoi(const char *s)
{
	int n=0, neg=0;
	while (*s==' ') s++;
    if(*s =='+' || *s=='-'){
        switch (*s) {
        case '-': neg=1;
        case '+': s++;
        }
    }
	while (*s && (*s-48)<9)
		n = 10*n - (*s++ - '0');
	return neg ? n : -n;
}

/// open an in-memory file
void mopen(MFILE *mfile, const char *mode)
{
  if (strcmp(mode, "r") != 0)
  {
    display_print(0,0,"ERROR: Only the file reads supported\n");
  }

  mfile->rdptr = 0;
}

/// at end of in-memory file
/// 1=Yes   0=No
int meof(MFILE *mfile)
{
  return mfile->rdptr >= mfile->data_sz;
}

/// read a buffer from the in-memory file
__SIZE_TYPE__ mread(void *_ptr, __SIZE_TYPE__ size, MFILE *mfile)
{
  if (meof(mfile))
    return 0;

  char *ptr = _ptr;
  __SIZE_TYPE__ cnt = 0;
  while (mfile->rdptr < mfile->data_sz && cnt < size && !meof(mfile))
  {
    *ptr++ = mfile->data[mfile->rdptr++];
    cnt++;
  }
  return cnt;
}

/// get a string from the in-memory file
char * mgets(char *s, size_t size, MFILE *mfile)
{
  if (meof(mfile))
    return NULL;

  char *p = s;
  size_t cnt;
  
  for (cnt=0; mfile->data[mfile->rdptr] != '\n' && cnt < (size-1) && !meof(mfile); cnt++)
    *p++ = mfile->data[mfile->rdptr++];

  if (mfile->data[mfile->rdptr] == '\n')
    mfile->rdptr++;

  *p = '\0';

  return s;
}

/// The absolute value of an integer number
int abs(int i)
{
  return i < 0 ? -i : i;
}

/// Copy bytes in memory
void bcopy(const void *src, void *dest, size_t n) {
    const char *src_ptr = (const char *)src;
    char *dest_ptr = (char *)dest;
    
    for (size_t i = 0; i < n; i++) {
        dest_ptr[i] = src_ptr[i];
    }
}

char * strchr(const char *s, char c)
{
  do
  {
    if (*s == c)
	    return (char*)s;
  } while (*s++);
  return NULL;
}

#define IN(l,a,r) (((l) <= (a)) && ((a) <= (r)))
long strtol(const char  *nptr, char** endptr, int base)
{
  int			c;		/* current character value */
  int			digit;		/* digit value */
  static const char *digits = "0123456789abcdefghijklmnopqrstuvxwyz";
  int		is_negative;	/* false for positive, true for negative */
  long		number;		/* the accumulating number */
  const char		*pos;		/* pointer into digit list */
  const char		*q;		/* pointer past end of digits */

  if (!(IN(2,base,36) || (base == 0) || (nptr != (const char*)NULL)))
  {
    if (endptr != (char**)NULL)
	    *endptr = (char*)nptr;
    return (0L);
  }

  while (isspace((int)*nptr))
	  nptr++;				/* ignore leading whitespace */

  switch (*nptr)			/* set number sign */
  {
  case '-':
    is_negative = 1; 
    nptr++;
    break;

  case '+':
    is_negative = 0;
    nptr++;
    break;

  default:
    is_negative = 0;
    break;
  }

  q = nptr;
  if (base == 0)			/* variable base; set by lookahead */
  {
	  if (*q == '0')
	    base = ((*(q+1) == 'x') || (*(q+1) == 'X')) ? 16 : 8;
	else
	    base = 10;
  }

  /* eliminate optional "0x" or "0X" prefix */
  if ((base == 16) && (*q == '0') && ((*(q+1) == 'x') || (*(q+1) == 'X')) )
	  q += 2;

  number = 0L;

  /* Number conversion is done by shifting rather than multiplication
     when the base is a power of 2, in order that the results not be
     impacted by integer overflow. */
  switch (base)
  {
  case 2:
  	while (IN('0',*q,'1'))
  	{
	    number <<= 1;
	    number |= *q - '0';
	    q++;
  	}
    break;

  case 4:
  	while (IN('0',*q,'3'))
    {
	    number <<= 2;
	    number |= *q - '0';
	    q++;
	  }
	  break;

  case 8:
	  while (IN('0',*q,'7'))
	  {
	    number <<= 3;
	    number |= *q - '0';
	    q++;
	  }
	  break;


  case 16:
	  for (;;)
	  {
	    if (*q == '\0')
		    break;
	    c = (int)(unsigned)*q;
	    if (isupper(c))
		    c = tolower(c);
	    pos = strchr(digits,c);
	    if (pos == (char*)NULL)
		    break;
	    digit = (int)(pos - digits);
	    if (!IN(0,digit,15))
		    break;
	    number <<= 4;
	    number |= digit;
	    q++;
	  }
	  break;

    default:		/* all other bases done by multiplication */
	  for (;;)	/* accumulate negative so most negative */
	  {		/* number on two's-complement is handled */
	    if (*q == '\0')
		    break;
	    c = (int)(unsigned)*q;
	    if (isupper(c))
		    c = tolower(c);
	    pos = strchr(digits,c);
	    if (pos == (char*)NULL)
		    break;
	    digit = (int)(pos - digits);
	    if (!IN(0,digit,base-1))
		    break;
	    number *= base;
	    number -= digit;
	    q++;
	  }
	  if (endptr != (char**)NULL)
	    *endptr = (char*)q;
	  if (is_negative)
	    return(number);
	  number = -number;
	  break;
  }
  if (is_negative)
	  number = -number;
  if (endptr != (char**)NULL)
	  *endptr = (char*)q;
  return (number);
}
/// neg?
uint32_t Num2Bin(int Num,int SUPUNI){
    uint32_t temp;
    uint32_t output=0;
    int count=0;
    if(SUPUNI){
        while(Num){
            temp <<=1;
            temp |= Num%2;
            Num/=2;
            count++;
        }
        while(count){
            output <<=1;
            output |= (temp & 1);
            temp >>=1;
            count--;
        }
    }
    else{
        int order=1;
        int Numcpy = Num;
        while(Numcpy){
            order*=10;
            Numcpy/=10;
        }
        count = 32;
        while(count && Num){
            output <<=1;
            Num *= 2;
            output |= (Num/order);
            Num = Num%order;
            count--;
        }
        while(count){
            output <<=1;
            count--;
        }
    }
    return output;
}

uint32_t bin64toieee (uint32_t highnib,uint32_t lownib){
    int whereis1 = -1;
    int counter=0;
    if(highnib!=0){
        counter = 32;
        uint32_t highnibcp = highnib;
        while(!(highnibcp & 0x80000000) && counter){
            highnibcp <<=1;
            counter--;
        }
        whereis1 = 31 + counter;
    }
    else if(lownib!=0){
        counter = 32;
        uint32_t lownibcp = lownib;
        while(!(lownibcp & 0x80000000) && counter){
            lownibcp <<=1;
            counter--;
        }
        whereis1 = counter-1;
    }
    int exp = whereis1 - 32 + 127;
    uint32_t mantissa=0;
    if(whereis1>54){
        mantissa = 0x007FFFFF & (highnib >> (whereis1-55));
    }
    else if(whereis1>31){
        mantissa = 0x007FFFFF & (highnib << (55-whereis1));
        mantissa |= lownib >> (32- (24-(whereis1-31)));
    }
    else if(whereis1>22){
        mantissa =  0x007FFFFF & (lownib >> (whereis1-23));
    }
    else if(whereis1>-1){
        mantissa =  0x007FFFFF & (lownib << (23-whereis1));
    }
    else{
        mantissa = 0;
    }
    return ((exp << 23) | mantissa);
}

/// sscanf like
/// SCANVARS(...)
int Sscanf(const char *buf, const char *fmt, scanvar*var){
    int i, j=0, ret=0;
    char *out_loc;
 	i = 0;
 	while (fmt && fmt[i] && buf[j])
 	{
    if (fmt[i] == '%') 
    {
      i++;
      switch (fmt[i]) 
      {
        case 'c': 
        {
	        *(var->ch)= buf[j];
	        j++;
	        ret++;
	        break;
        }
        case 'd': 
        {
	         *(var->number)= strtol(&buf[j], &out_loc, 10);
	         j += (out_loc - &buf[j]);
	         ret++;
	         break;
        }
        case 'x': 
        {
	        *(var->number)= strtol(&buf[j], &out_loc, 16);
	        j += (out_loc - &buf[j]);
	        ret++;
	        break;
        }
        case 'f':
        {
            uint32_t UP = Num2Bin(strtol(&buf[j],&out_loc,10),1);
            j += (out_loc - &buf[j]);
            j++;
            uint32_t DOWN = Num2Bin(strtol(&buf[j],&out_loc,10),0);
            j += (out_loc - &buf[j]);
            *(var->number) = bin64toieee(UP,DOWN);
            ret++;
            break;
        }
      }
      var++;
    } 
    else 
    {
      // buf[j] = fmt[i];
      j++;
    }
    i++;
  }
  return ret;
}

/// The bzero() function erases the data in the n bytes of the memory
/// starting at the location pointed to by s, by writing zeros
void bzero(void *s, size_t len) {
    memset(s, 0, len);
}
///  converts a u_long from host to TCP/IP network byte order (which is big-endian).
uint32_t htonl(uint32_t hostlong) {
    uint32_t result = ((hostlong >> 24) & 0x000000FF) | 
                      ((hostlong >> 8) & 0x0000FF00) | 
                      ((hostlong << 8) & 0x00FF0000) | 
                      ((hostlong << 24) & 0xFF000000);
    return result;
}

/// convert a string containing float number to IEEE754
uint32_t str2ieee(const char *str){
    // uint32_t output;
    // Sscanf(str,"%f",SCANVARS(&output));
    return 0;
}

/// write a buffer to the in-memory file
__SIZE_TYPE__ mwrite(void *_ptr, __SIZE_TYPE__ size, MFILE *mfile)
{
  if (meof(mfile))
    return 0;

  const char *ptr = _ptr;
  __SIZE_TYPE__ cnt = 0;
  while (mfile->rdptr < mfile->data_sz && cnt < size && !meof(mfile))
  {
    mfile->data[mfile->rdptr++] = *ptr++;
    cnt++;
  }
  return cnt;
}


/// YR

//Pouria
//Dynamic Memory Allocation functions
// These functions have the same name as stdlib.h header Dynamic memory Allocation functions.
//  But since the linker first try to resolve the symbols by searching in the compiled objects
// it will find these ones and it won't search the stdlib and no multiple definition will happen
// Now the question is what if a sybmol is sed and it only exists in stdlib. Then it will link stdlib and there will be cnflict
// between these costum memory functions and the standard ones.
//  The offical solution would be to overwrite the syscalls provided by newlib
void *malloc(size_t size) {
    return memmgr_alloc(size);
}

void free(void *ptr) {
    memmgr_free(ptr);
}


void *calloc(size_t num, size_t size) {
    void *ptr = memmgr_alloc(num * size);
    if (ptr) {
        memset(ptr, 0, num * size);
    }
    return ptr;
}