static inline __attribute__((always_inline)) float fpadd(float rs1, float rs2) {
    float rd;
    asm volatile (
        ".insn r 0x33, 0x3, 0x3, %0, %1, %2"
        : "=r" (rd)
        : "r" (rs1), "r" (rs2)
    );
    return rd;
}

double
__adddf3 (double a, double b)
{
  float x = (float)a;
  float y = (float)b;
  float z =  fpadd(x,y);
  return (double)z;
}