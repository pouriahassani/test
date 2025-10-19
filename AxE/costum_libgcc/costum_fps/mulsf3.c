static inline __attribute__((always_inline)) float fpmul(float rs1, float rs2) {
    float rd;
    asm volatile (
        ".insn r 0x33, 0x1, 0x3, %0, %1, %2"
        : "=r" (rd)
        : "r" (rs1), "r" (rs2)
    );
    return rd;
}

float
__mulsf3 (float a, float b)
{
  return fpmul(a,b);
}