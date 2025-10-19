# JPEG Library for AxE RISC-V System

This directory contains an adapted version of the Independent JPEG Group's JPEG-6a library for the AxE RISC-V platform.

## Overview

The JPEG library has been ported from the MiBench consumer benchmark suite to work with the AxE system's memory layout and RISC-V toolchain. It provides complete JPEG encoding and decoding capabilities for embedded applications.

## Files

- `jpeg_main.c` - Main wrapper that calls JPEG applications with hardcoded parameters
- `cjpeg.c` - JPEG encoder (modified: main() renamed to cjpeg_main())
- `djpeg.c` - JPEG decoder (modified: main() renamed to djpeg_main())
- `Makefile` - AxE build configuration with complete source list
- `Makefile_local` - RISC-V toolchain and memory layout settings
- `jconfig.h` - JPEG library configuration for AxE system
- Various `j*.c` files - Core JPEG library implementation (unmodified)
- Test input files: `input_small.ppm`, `input_small.jpg`

## Build Instructions

```bash
make clean
make rv32im
```

This will generate:
- `rv32im_main.elf` - Executable for AxE system
- `rv32im_main.hex` - Hex format for loading

## Adaptations Made for AxE

### 1. Command Line Interface Adaptation
- **Problem**: Original applications expect `main(argc, argv)` command line arguments
- **Solution**: Created `jpeg_main.c` wrapper with hardcoded parameters from `runme_small.sh`
- **Changes**: 
  - Renamed `main()` to `cjpeg_main()` in `cjpeg.c`
  - Renamed `main()` to `djpeg_main()` in `djpeg.c`
  - Created wrapper that calls both with predefined arguments

### 2. Build System Integration
- **Problem**: Original Makefile incompatible with AxE build system
- **Solution**: Created AxE-compatible Makefiles
- **Changes**:
  - `Makefile`: Updated source list and AxE library integration
  - `Makefile_local`: Uses AxE memory layout system and RISC-V startup files
  - Proper startup sequence: `sp_nostart.S` + `start.S` with generated stack pointer

### 3. System Dependencies
- **File I/O**: Uses AxE's newlib stubs (fopen, fclose, fread, fwrite) - no changes needed
- **Memory Management**: Uses AxE's malloc/free through newlib stubs - no changes needed
- **Error Handling**: Uses AxE's exit() function through newlib stubs - no changes needed
- **Standard Library**: All required C functions available in AxE - no changes needed

### 4. Memory Configuration
- **Stack Pointer**: Uses AxE generated value (0x01E00000) instead of hardcoded values
- **Memory Layout**: Integrated with AxE's YAML-based memory configuration system
- **Default Limits**: 6MB maximum memory (configurable in jconfig.h)

### 5. Test Configuration
- **Encoding Test**: `cjpeg -dct int -progressive -opt -outfile output_small_encode.jpeg input_small.ppm`
- **Decoding Test**: `djpeg -dct int -ppm -outfile output_small_decode.ppm input_small.jpg`
- **DCT Algorithm**: Uses integer DCT by default (no floating-point required)

## Library Features

- JPEG baseline, extended-sequential, and progressive compression
- Multiple DCT algorithms: integer (fastest), fast integer, floating-point
- Support for grayscale and color images
- Configurable quality levels (1-100)
- Memory-efficient operation suitable for embedded systems

## Image Format Support

- PPM (Portable Pixmap) - primary format for testing
- GIF, BMP, Targa - additional supported formats
- JPEG input/output for compression/decompression

## Testing

The main application performs complete JPEG workflow:
1. JPEG encoding test with small test image
2. JPEG decoding test with sample JPEG file
3. Both operations use integer DCT for optimal RISC-V performance

## Technical Notes

- Built with RISC-V RV32IM instruction set
- Uses integer-only DCT (no floating-point dependencies)
- Integrated with AxE file I/O system and newlib stubs
- Proper memory layout integration with generated configuration
- All original JPEG library functionality preserved

## Key Insight

The JPEG library required minimal source code changes because:
- AxE's newlib stubs provide all required system functions
- Integer DCT eliminates floating-point dependencies
- Only interface adaptation (command line to embedded) was needed
- Build system integration handled through Makefiles

## Original Source

Based on JPEG-6a from Independent JPEG Group, obtained from MiBench consumer benchmark suite. The library has been adapted for cross-compilation and embedded use while maintaining full functionality.