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
        PROGRAM (rx) : ORIGIN = 0x00000000, LENGTH = 0x00100000
    DATA (rw) : ORIGIN = 0x00101000, LENGTH = 0x00800000
    FILE_IO (rw) : ORIGIN = 0x00902000, LENGTH = 0x00801000
    STACK (rw) : ORIGIN = 0x01E00000, LENGTH = 0x00100000
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
        ASSERT(. <= 0x00100000, "Program section exceeds allocated memory!")

        . = 0x00101000;
        .data : {
            *(.data) *(.data.*)
            *(.sdata) *(.sdata.*)
            . = ALIGN(4);
        } > DATA

        .bss : {
            *(.bss) *(.bss.*)
            *(.sbss) *(.sbss.*)
            . = ALIGN(4);
            _end = .;  /* End of BSS - heap starts here */
            PROVIDE(end = .);
        } > DATA
        ASSERT(. <= 0x00901000, "Data section exceeds allocated memory!")

        . = 0x00902000;
        .file_io_data : {
            *(.file_io_data)
            . = ALIGN(4);
        } > FILE_IO
        ASSERT(. <= 0x01103000, "File I/O section exceeds allocated memory!")

        PROVIDE(_stack_top = 0x01F00000);

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
    