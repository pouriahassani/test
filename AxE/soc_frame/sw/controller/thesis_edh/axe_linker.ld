/*
 * AxE Linker Script for Controller with Math Library Support
 * 
 * This ensures my_start is at address 0x00000000 even when linking with -lm
 */

ENTRY(my_start)

SECTIONS
{
    /* Ensure AxE startup code is placed first at address 0 */
    . = 0x00000000;
    
    .text : {
        /* Force start.S to be first */
        *start.o(.text)
        *(.text.my_start)
        /* Then place all other code */
        *(.text)
        *(.text.*)
        *(.rodata)
        *(.rodata.*)
    }
    
    /* Data sections */
    .data : {
        *(.data)
        *(.data.*)
        *(.sdata)
        *(.sdata.*)
    }
    
    /* BSS section */
    .bss : {
        *(.bss)
        *(.bss.*)
        *(.sbss)
        *(.sbss.*)
    }
    
    /* Stack grows down from this address */
    PROVIDE(_stack_top = 0x0002fff8);
}