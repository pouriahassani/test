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
        PROGRAM (rx) : ORIGIN = 0x00000000, LENGTH = 0x000B2000
    DATA (rw) : ORIGIN = 0x000B2000, LENGTH = 0x00033000
    FILE_IO (rw) : ORIGIN = 0x000E5000, LENGTH = 0x00017000
    STACK (rw) : ORIGIN = 0x00F00000, LENGTH = 0x00100000
}

SECTIONS
{
    . = 0x00000000;
        .text : {
            *start.o(.text)
            *(.text.my_start)
            *(.text) *(.text.*)
            *(.rodata) *(.rodata.*)
            . = ALIGN(4);
        } > PROGRAM
        ASSERT(. <= 0x000B2000, "Program section exceeds allocated memory!")

        . = 0x000B2000;
        .data : {
            *(.data) *(.data.*)
            *(.sdata) *(.sdata.*)
            . = ALIGN(4);
        } > DATA

        .bss : {
            *(.bss) *(.bss.*)
            *(.sbss) *(.sbss.*)
            . = ALIGN(4);
        } > DATA
        ASSERT(. <= 0x000E5000, "Data section exceeds allocated memory!")

        . = 0x000E5000;
        .file_io_data : {
            *(.file_io_data)
            . = ALIGN(4);
        } > FILE_IO
        ASSERT(. <= 0x000FC000, "File I/O section exceeds allocated memory!")

        PROVIDE(_stack_top = 0x01000000);

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
    