// Minimal test - jump directly to custom instruction
void my_main()
{
    // Direct custom instruction without any library calls
    asm volatile (".word 0x0EA5850B");  // Custom print instruction
    asm volatile (".word 0x0EA5850B");  // Repeat to see output
    asm volatile (".word 0x0EA5850B");  // One more time
    
    // Infinite loop to keep running
    while(1);
}