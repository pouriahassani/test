#!/usr/bin/env python3
"""
AxE SoC Memory Layout Validator and Generator

This tool validates memory layout configurations and generates C/SystemVerilog
headers with memory definitions for the build system.
"""

import yaml
import sys
import os
import argparse
from pathlib import Path

class MemoryLayoutValidator:
    def __init__(self, config_file):
        """Initialize validator with configuration file"""
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.layout = self.config['memory_layout']
        self.validation = self.config['validation']
        self.hardware = self.config['hardware']
        self.errors = []
        self.warnings = []
    
    def _to_int(self, value):
        """Convert hex string or int to integer"""
        if isinstance(value, str):
            return int(value, 16) if value.startswith('0x') else int(value)
        return int(value)
    
    def validate_alignment(self, region_name, base, alignment):
        """Check if address is properly aligned"""
        base_int = self._to_int(base)
        alignment_int = self._to_int(alignment)
        if base_int % alignment_int != 0:
            self.errors.append(
                f"{region_name}: Base address 0x{base_int:08X} is not aligned to 0x{alignment_int:X}"
            )
    
    def validate_overlap(self, region1_name, region1_base, region1_size, 
                        region2_name, region2_base, region2_size, min_gap=0):
        """Check for memory region overlaps"""
        region1_base_int = self._to_int(region1_base)
        region1_size_int = self._to_int(region1_size)
        region2_base_int = self._to_int(region2_base)
        region2_size_int = self._to_int(region2_size)
        min_gap_int = self._to_int(min_gap)
        
        region1_end = region1_base_int + region1_size_int
        region2_end = region2_base_int + region2_size_int
        
        # Check if regions overlap
        if (region1_base_int < region2_end) and (region2_base_int < region1_end):
            self.errors.append(
                f"Memory overlap detected between {region1_name} "
                f"(0x{region1_base_int:08X}-0x{region1_end:08X}) and {region2_name} "
                f"(0x{region2_base_int:08X}-0x{region2_end:08X})"
            )
        
        # Check minimum gap
        if min_gap_int > 0:
            if region1_end <= region2_base_int:
                gap = region2_base_int - region1_end
                if gap < min_gap_int:
                    self.warnings.append(
                        f"Gap between {region1_name} and {region2_name} "
                        f"({gap} bytes) is less than recommended minimum ({min_gap_int} bytes)"
                    )
    
    def validate_finish_signal(self):
        """Validate finish signal placement"""
        finish_addr = self._to_int(self.layout['finish_signal']['address'])
        
        # Check if finish signal conflicts with stack
        stack_base = self._to_int(self.layout['stack']['base'])
        stack_size = self._to_int(self.layout['stack']['size'])
        stack_end = stack_base + stack_size
        
        # Stack grows downward, so check if finish signal is in stack range
        if stack_base <= finish_addr <= stack_end:
            self.errors.append(
                f"CRITICAL: Finish signal at 0x{finish_addr:08X} conflicts with stack region "
                f"(0x{stack_base:08X}-0x{stack_end:08X})"
            )
    
    def validate_file_io_consistency(self):
        """Validate file I/O configuration consistency"""
        file_io = self.layout['file_io']
        max_files = self._to_int(file_io['max_files'])
        buffer_size = self._to_int(file_io['buffer_size'])
        total_size = self._to_int(file_io['size'])
        
        required_size = max_files * buffer_size
        if required_size > total_size:
            self.errors.append(
                f"File I/O configuration error: {max_files} files * {buffer_size} bytes "
                f"= {required_size} bytes, but only {total_size} bytes allocated"
            )
    
    def validate_physical_memory(self):
        """Validate against physical memory constraints"""
        phys_size = self._to_int(self.hardware['physical_memory_size'])
        
        # Find highest used address
        highest_addr = 0
        for region_name, region in self.layout.items():
            if isinstance(region, dict) and 'base' in region and 'size' in region:
                region_end = self._to_int(region['base']) + self._to_int(region['size'])
                if region_end > highest_addr:
                    highest_addr = region_end
        
        if highest_addr > phys_size:
            self.errors.append(
                f"Virtual memory usage (0x{highest_addr:08X}) exceeds "
                f"physical memory size (0x{phys_size:08X})"
            )
    
    def validate_all(self):
        """Run all validation checks"""
        print("Validating AxE memory layout configuration...")
        
        # Extract regions for easier processing
        regions = []
        for name, region in self.layout.items():
            if isinstance(region, dict) and 'base' in region and 'size' in region:
                regions.append((name, region['base'], region['size']))
        
        # Validate alignments
        val = self.validation
        if 'alignment_program' in val:
            self.validate_alignment('program', self.layout['program']['base'], 
                                  val['alignment_program'])
        if 'alignment_data' in val:
            self.validate_alignment('data', self.layout['data']['base'], 
                                  val['alignment_data'])
        if 'alignment_file_io' in val:
            self.validate_alignment('file_io', self.layout['file_io']['base'], 
                                  val['alignment_file_io'])
        if 'alignment_stack' in val:
            self.validate_alignment('stack', self.layout['stack']['base'], 
                                  val['alignment_stack'])
        
        # Validate overlaps between consecutive regions
        program = (self.layout['program']['base'], self.layout['program']['size'])
        data = (self.layout['data']['base'], self.layout['data']['size'])
        file_io = (self.layout['file_io']['base'], self.layout['file_io']['size'])
        mmio = (self.layout['mmio']['base'], self.layout['mmio']['size'])
        stack = (self.layout['stack']['base'], self.layout['stack']['size'])
        
        # Check overlaps with minimum gaps
        self.validate_overlap('program', program[0], program[1], 
                            'data', data[0], data[1], 
                            val.get('min_gap_program_data', 0))
        
        self.validate_overlap('data', data[0], data[1], 
                            'file_io', file_io[0], file_io[1], 
                            val.get('min_gap_data_file_io', 0))
        
        self.validate_overlap('file_io', file_io[0], file_io[1], 
                            'mmio', mmio[0], mmio[1], 
                            val.get('min_gap_file_io_mmio', 0))
        
        self.validate_overlap('mmio', mmio[0], mmio[1], 
                            'stack', stack[0], stack[1], 
                            val.get('min_gap_mmio_stack', 0))
        
        # Validate specific checks
        self.validate_finish_signal()
        self.validate_file_io_consistency()
        self.validate_physical_memory()
        
        # Report results
        if self.errors:
            print(f"\n❌ VALIDATION FAILED - {len(self.errors)} error(s):")
            for error in self.errors:
                print(f"  ERROR: {error}")
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} warning(s):")
            for warning in self.warnings:
                print(f"  WARNING: {warning}")
        
        if not self.errors:
            print("\n✅ Memory layout validation PASSED")
            return True
        else:
            return False

    def generate_c_header(self, output_file):
        """Generate C header file with memory definitions"""
        with open(output_file, 'w') as f:
            f.write("""/* ****************************************************************************
 * AxE SoC Memory Layout Definitions (Auto-generated)
 * 
 * This file is automatically generated from memory_layout.yaml
 * DO NOT EDIT MANUALLY - Changes will be overwritten
 * 
***************************************************************************** */

#ifndef AXE_MEMORY_LAYOUT_H
#define AXE_MEMORY_LAYOUT_H

#include <stdint.h>

/* Virtual Memory Layout */
""")
            
            # Program region
            prog = self.layout['program']
            prog_base = self._to_int(prog['base'])
            prog_size = self._to_int(prog['size'])
            f.write(f"#define PROGRAM_BASE_ADDR     0x{prog_base:08X}UL\n")
            f.write(f"#define PROGRAM_SIZE          0x{prog_size:08X}UL\n")
            f.write(f"#define PROGRAM_END_ADDR      0x{prog_base + prog_size:08X}UL\n\n")
            
            # Data region
            data = self.layout['data']
            data_base = self._to_int(data['base'])
            data_size = self._to_int(data['size'])
            f.write(f"#define DATA_BASE_ADDR        0x{data_base:08X}UL\n")
            f.write(f"#define DATA_SIZE             0x{data_size:08X}UL\n")
            f.write(f"#define DATA_END_ADDR         0x{data_base + data_size:08X}UL\n\n")
            
            # File I/O region
            file_io = self.layout['file_io']
            file_io_base = self._to_int(file_io['base'])
            file_io_size = self._to_int(file_io['size'])
            file_io_max_files = self._to_int(file_io['max_files'])
            file_io_buffer_size = self._to_int(file_io['buffer_size'])
            f.write(f"#define FILE_IO_BASE_ADDR     0x{file_io_base:08X}UL\n")
            f.write(f"#define FILE_IO_SIZE          0x{file_io_size:08X}UL\n")
            f.write(f"#define FILE_IO_END_ADDR      0x{file_io_base + file_io_size:08X}UL\n")
            f.write(f"#define FILE_IO_MAX_FILES     {file_io_max_files}\n")
            f.write(f"#define FILE_IO_BUFFER_SIZE   0x{file_io_buffer_size:08X}UL\n\n")
            
            # MMIO region
            mmio = self.layout['mmio']
            mmio_base = self._to_int(mmio['base'])
            mmio_size = self._to_int(mmio['size'])
            f.write(f"#define MMIO_BASE_ADDR        0x{mmio_base:08X}UL\n")
            f.write(f"#define MMIO_SIZE             0x{mmio_size:08X}UL\n")
            f.write(f"#define MMIO_END_ADDR         0x{mmio_base + mmio_size:08X}UL\n\n")
            
            # File trigger addresses
            triggers = mmio['file_triggers']
            triggers_base = self._to_int(triggers['base'])
            f.write(f"#define FILE_TRIGGERS_BASE    0x{triggers_base:08X}UL\n")
            f.write(f"#define FILE_OPEN_TRIGGER     (FILE_TRIGGERS_BASE + 0x00)\n")
            f.write(f"#define FILE_READ_TRIGGER     (FILE_TRIGGERS_BASE + 0x04)\n")
            f.write(f"#define FILE_WRITE_TRIGGER    (FILE_TRIGGERS_BASE + 0x08)\n")
            f.write(f"#define FILE_CLOSE_TRIGGER    (FILE_TRIGGERS_BASE + 0x0C)\n")
            f.write(f"#define FILE_SIZE_TRIGGER     (FILE_TRIGGERS_BASE + 0x10)\n\n")
            
            # Finish signal
            finish = self.layout['finish_signal']
            finish_addr = self._to_int(finish['address'])
            f.write(f"#define FINISH_SIGNAL_ADDR    0x{finish_addr:08X}UL\n\n")
            
            # Stack
            stack = self.layout['stack']
            stack_base = self._to_int(stack['base'])
            f.write(f"#define STACK_BASE_ADDR       0x{stack_base:08X}UL\n")
            stack_size = self._to_int(stack['size'])
            f.write(f"#define STACK_SIZE            0x{stack_size:08X}UL\n")
            f.write(f"#define STACK_TOP_ADDR        STACK_BASE_ADDR\n")
            f.write(f"#define STACK_BOTTOM_ADDR     (STACK_BASE_ADDR + STACK_SIZE)\n\n")
            
            # Hardware configuration
            hw = self.hardware
            hw_phys_mem_size = self._to_int(hw['physical_memory_size'])
            hw_axi_offset_step = self._to_int(hw['axi_offset_step'])
            f.write(f"#define PHYSICAL_MEMORY_SIZE  0x{hw_phys_mem_size:08X}UL\n")
            f.write(f"#define AXI_OFFSET_STEP       0x{hw_axi_offset_step:08X}UL\n\n")
            
            # Additional compile-time constants for assembly/linker
            f.write("/* Compile-time constants for assembly and linker scripts */\n")
            f.write(f"#define STACK_POINTER_VALUE   0x{stack_base:08X}UL\n")
            f.write(f"#define PROGRAM_START_ADDR    0x{prog_base:08X}UL\n") 
            f.write(f"#define DATA_START_ADDR       0x{data_base:08X}UL\n")
            f.write(f"#define FILE_IO_START_ADDR    0x{file_io_base:08X}UL\n\n")
            
            # Memory validation macros
            f.write("/* Memory validation macros */\n")
            f.write("#define IS_PROGRAM_ADDR(addr)   ((addr) >= PROGRAM_BASE_ADDR && (addr) < PROGRAM_END_ADDR)\n")
            f.write("#define IS_DATA_ADDR(addr)      ((addr) >= DATA_BASE_ADDR && (addr) < DATA_END_ADDR)\n")
            f.write("#define IS_FILE_IO_ADDR(addr)   ((addr) >= FILE_IO_BASE_ADDR && (addr) < FILE_IO_END_ADDR)\n")
            f.write("#define IS_MMIO_ADDR(addr)      ((addr) >= MMIO_BASE_ADDR && (addr) < MMIO_END_ADDR)\n")
            f.write("#define IS_STACK_ADDR(addr)     ((addr) >= STACK_BASE_ADDR && (addr) < STACK_BOTTOM_ADDR)\n\n")
            
            f.write("""#endif /* AXE_MEMORY_LAYOUT_H */
""")

    def generate_systemverilog_header(self, output_file):
        """Generate SystemVerilog header file with memory definitions"""
        with open(output_file, 'w') as f:
            f.write("""/* ****************************************************************************
 * AxE SoC Memory Layout Definitions (Auto-generated)
 * 
 * This file is automatically generated from memory_layout.yaml
 * DO NOT EDIT MANUALLY - Changes will be overwritten
 * 
***************************************************************************** */

`ifndef AXE_MEMORY_LAYOUT_VH
`define AXE_MEMORY_LAYOUT_VH

// Virtual Memory Layout
""")
            
            # File trigger addresses for hardware
            triggers = self.layout['mmio']['file_triggers']
            f.write(f"`define FILE_TRIGGERS_BASE    32'h{triggers['base']:08X}\n")
            f.write(f"`define FILE_OPEN_TRIGGER     (`FILE_TRIGGERS_BASE + 32'h00000000)\n")
            f.write(f"`define FILE_READ_TRIGGER     (`FILE_TRIGGERS_BASE + 32'h00000004)\n")
            f.write(f"`define FILE_WRITE_TRIGGER    (`FILE_TRIGGERS_BASE + 32'h00000008)\n")
            f.write(f"`define FILE_CLOSE_TRIGGER    (`FILE_TRIGGERS_BASE + 32'h0000000C)\n")
            f.write(f"`define FILE_SIZE_TRIGGER     (`FILE_TRIGGERS_BASE + 32'h00000010)\n\n")
            
            # Finish signal
            finish = self.layout['finish_signal']
            f.write(f"`define FINISH_SIGNAL_ADDR    32'h{finish['address']:08X}\n\n")
            
            # Hardware configuration
            hw = self.hardware
            f.write(f"`define PHYSICAL_MEMORY_SIZE  32'h{hw['physical_memory_size']:08X}\n")
            f.write(f"`define AXI_OFFSET_STEP       32'h{hw['axi_offset_step']:08X}\n")
            f.write(f"`define VERILATOR_MEM_SIZE    ({hw['verilator_mem_size'] // 4})  // In 32-bit words\n\n")
            
            f.write("`endif // AXE_MEMORY_LAYOUT_VH\n")

    def generate_makefile_vars(self, output_file):
        """Generate Makefile variables for build system"""
        with open(output_file, 'w') as f:
            f.write("# AxE SoC Memory Layout Variables (Auto-generated)\n")
            f.write("# DO NOT EDIT MANUALLY - Changes will be overwritten\n\n")
            
            stack = self.layout['stack']
            stack_base = self._to_int(stack['base'])
            stack_size = self._to_int(stack['size'])
            f.write(f"STACK_POINTER = 0x{stack_base:08X}\n")
            f.write(f"STACK_SIZE = 0x{stack_size:08X}\n\n")
            
            hw = self.hardware
            hw_verilator_mem_size = self._to_int(hw['verilator_mem_size'])
            hw_physical_memory_size = self._to_int(hw['physical_memory_size'])
            f.write(f"MEM_SIZE = {hw_verilator_mem_size // 4}\n")
            f.write(f"PHYSICAL_MEMORY_SIZE = 0x{hw_physical_memory_size:08X}\n")


    def generate_linker_script(self, output_file):
        """Generate GNU linker script based on memory layout"""
        with open(output_file, 'w') as f:
            f.write("""/* ****************************************************************************
    * AxE SoC Memory Layout Linker Script (Auto-generated)
    * 
    * This file ensures proper section placement according to memory_layout.yaml
    * Auto-adjusted based on program requirements
    * 
    ***************************************************************************** */

    ENTRY(my_start)

    MEMORY
    {
    """)

            def mem_line(name, base, size, perms):
                f.write(f"    {name.upper()} ({perms}) : ORIGIN = 0x{base:08X}, LENGTH = 0x{size:08X}\n")

            # Extract memory regions
            prog = self.layout['program']
            data = self.layout['data']
            file_io = self.layout['file_io']
            stack = self.layout['stack']

            mem_line("PROGRAM", self._to_int(prog['base']), self._to_int(prog['size']), "rx")
            mem_line("DATA", self._to_int(data['base']), self._to_int(data['size']), "rw")
            mem_line("FILE_IO", self._to_int(file_io['base']), self._to_int(file_io['size']), "rw")
            mem_line("STACK", self._to_int(stack['base']), self._to_int(stack['size']), "rw")

            f.write("}\n\nSECTIONS\n{\n")

            # Generate .text
            f.write(f"""    . = 0x{self._to_int(prog['base']):08X};
        .text : {{
            *start.o(.text)
            *(.text.my_start)
            *(.text) *(.text.*)
            *(.rodata) *(.rodata.*)
            . = ALIGN(4);
        }} > PROGRAM
        ASSERT(. <= 0x{self._to_int(prog['base']) + self._to_int(prog['size']):08X}, "Program section exceeds allocated memory!")

    """)

            # Generate .data and .bss
            f.write(f"""    . = 0x{self._to_int(data['base']):08X};
        .data : {{
            *(.data) *(.data.*)
            *(.sdata) *(.sdata.*)
            . = ALIGN(4);
        }} > DATA

        .bss : {{
            *(.bss) *(.bss.*)
            *(.sbss) *(.sbss.*)
            . = ALIGN(4);
            _end = .;  /* End of BSS - heap starts here */
            PROVIDE(end = .);
        }} > DATA
        ASSERT(. <= 0x{self._to_int(data['base']) + self._to_int(data['size']):08X}, "Data section exceeds allocated memory!")

    """)

            # Generate .file_io
            f.write(f"""    . = 0x{self._to_int(file_io['base']):08X};
        .file_io_data : {{
            *(.file_io_data)
            . = ALIGN(4);
        }} > FILE_IO
        ASSERT(. <= 0x{self._to_int(file_io['base']) + self._to_int(file_io['size']):08X}, "File I/O section exceeds allocated memory!")

    """)

            # Stack top
            f.write(f"    PROVIDE(_stack_top = 0x{self._to_int(stack['base']) + self._to_int(stack['size']):08X});\n")

            # Debug
            f.write("""
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
    """)


def main():
    parser = argparse.ArgumentParser(description='AxE Memory Layout Validator and Generator')
    parser.add_argument('config', help='Memory layout configuration file (YAML)')
    parser.add_argument('--validate-only', action='store_true', 
                       help='Only validate, do not generate files')
    parser.add_argument('--output-dir', default='generated', 
                       help='Output directory for generated files')
    parser.add_argument('--app-config', help='Application-specific configuration override')
    
    args = parser.parse_args()
    
    # Load base configuration
    validator = MemoryLayoutValidator(args.config)
    
    # Apply application-specific overrides if specified
    if args.app_config:
        if args.app_config in validator.config.get('applications', {}):
            app_config = validator.config['applications'][args.app_config]
            print(f"Applying application configuration: {args.app_config}")
            
            # Deep merge application config into layout
            for section, values in app_config.items():
                if section in validator.layout:
                    validator.layout[section].update(values)
        else:
            print(f"ERROR: Application configuration '{args.app_config}' not found")
            return 1
    
    # Validate configuration
    if not validator.validate_all():
        print("\nBuild aborted due to memory layout validation errors.")
        return 1
    
    if args.validate_only:
        print("Validation complete.")
        return 0
    
    # Generate output files
    os.makedirs(args.output_dir, exist_ok=True)
    
    c_header = os.path.join(args.output_dir, 'axe_memory_layout.h')
    sv_header = os.path.join(args.output_dir, 'axe_memory_layout.vh')
    makefile_vars = os.path.join(args.output_dir, 'memory_vars.mk')
    ld_script = os.path.join(args.output_dir, 'axe_memory_layout.ld')
    validator.generate_linker_script(ld_script)
    validator.generate_c_header(c_header)
    validator.generate_systemverilog_header(sv_header)
    validator.generate_makefile_vars(makefile_vars)
    
    print(f"\nGenerated files:")
    print(f"  Linker script:     {ld_script}")
    print(f"  C header:         {c_header}")
    print(f"  SystemVerilog:    {sv_header}")
    print(f"  Makefile vars:    {makefile_vars}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())