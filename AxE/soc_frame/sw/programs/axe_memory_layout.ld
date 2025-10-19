/* ****************************************************************************
 * AxE SoC Memory Layout Linker Script (Auto-generated)
 * 
 * This file ensures proper section placement according to memory_layout.yaml
 * Auto-adjusted based on program requirements
 * 
***************************************************************************** */

ENTRY(my_start)

MEMORY
{
    PROGRAM (rx)   : ORIGIN = 0x00000000, LENGTH = 0x0000D000  /* 52KB program */
    DATA (rw)      : ORIGIN = 0x0000D000, LENGTH = 0x00008000  /* 32KB data */
    FILE_IO (rw)   : ORIGIN = 0x00015000, LENGTH = 0x-0004000  /* -16KB file I/O */
    STACK (rw)     : ORIGIN = 0x00F00000, LENGTH = 0x00100000  /* 1MB stack */
}

SECTIONS
{
    /* Program code section */
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
        . = ALIGN(4);
    } > PROGRAM
    
    /* Ensure we don't exceed program memory */
    ASSERT(. <= 0x0000D000, "Program section exceeds allocated memory!")
    
    /* Data sections - placed at DATA region */
    . = 0x0000D000;
    .data : {
        *(.data)
        *(.data.*)
        *(.sdata)
        *(.sdata.*)
        . = ALIGN(4);
    } > DATA
    
    /* BSS section - continues in DATA region */
    .bss : {
        *(.bss)
        *(.bss.*)
        *(.sbss)
        *(.sbss.*)
        . = ALIGN(4);
        _end = .;  /* End of BSS - heap starts here */
        PROVIDE(end = .);
    } > DATA
    
    /* Ensure data+bss don't exceed data memory */
    ASSERT(. <= 0x00015000, "Data section exceeds allocated memory!")
    
    /* File I/O section - placed at FILE_IO region */
    . = 0x00015000;
    .file_io_data : {
        *(.file_io_data)
        . = ALIGN(4);
    } > FILE_IO
    
    /* Ensure file I/O section doesn't exceed allocated memory */
    ASSERT(. <= 0x00011000, "File I/O section exceeds allocated memory!")
    
    /* Stack pointer (grows down from top of stack region) */
    PROVIDE(_stack_top = 0x01000000);  /* Top of stack region */
    
    /* Debug sections */
    .comment 0 : { *(.comment) }
    .debug_info 0 : { *(.debug_info) }
    .debug_abbrev 0 : { *(.debug_abbrev) }
    .debug_line 0 : { *(.debug_line) }
    .debug_frame 0 : { *(.debug_frame) }
    .debug_str 0 : { *(.debug_str) }
    .debug_aranges 0 : { *(.debug_aranges) }
    .debug_ranges 0 : { *(.debug_ranges) }
    .debug_loc 0 : { *(.debug_loc) }
}