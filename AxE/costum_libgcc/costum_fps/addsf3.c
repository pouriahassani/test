static inline __attribute__((always_inline)) float fpadd(float rs1, float rs2) {
    float rd;
    asm volatile (
        ".insn r 0x33, 0x3, 0x3, %0, %1, %2"
        : "=r" (rd)
        : "r" (rs1), "r" (rs2)
    );
    return rd;
}

float
__addsf3 (float a, float b)
{ 
  return fpadd(a,b);
}



