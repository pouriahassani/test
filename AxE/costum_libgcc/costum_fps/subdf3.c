static inline __attribute__((always_inline)) float fpsub(float rs1, float rs2) {
    float rd;
    asm volatile (
        ".insn r 0x33, 0x4, 0x3, %0, %1, %2"
        : "=r" (rd)
        : "r" (rs1), "r" (rs2)
    );
    return rd;
}

double
__subdf3 (double a, double b)
{
  float x = (float)a;
  float y = (float)b;
  float z =  fpsub(x,y);
  return (double)z;
}