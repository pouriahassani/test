#!/usr/bin/env python3
"""
AxE Hex File Path Resolution Test Script

This script verifies that all hex file paths can be resolved correctly
using the centralized path management system.
"""

import os
import sys
from pathlib import Path

def get_axe_root():
    """Get AxE project root directory."""
    axe_root = os.environ.get('AXE_ROOT')
    if axe_root:
        return Path(axe_root)
    
    # Fallback: detect from current working directory
    cwd = Path.cwd()
    
    # Look for AxE project markers
    for parent in [cwd] + list(cwd.parents):
        if (parent / "soc_frame").is_dir() and (parent / "CLAUDE.md").is_file():
            return parent
    
    # Try to detect from path components
    cwd_str = str(cwd)
    if 'soc_frame' in cwd_str:
        return Path(cwd_str.split('soc_frame')[0].rstrip('/'))
    
    raise RuntimeError("AXE_ROOT not set and cannot auto-detect project root")

def test_hex_path_resolution():
    """Test that all hex file paths resolve correctly."""
    
    print("=" * 60)
    print("AxE Hex File Path Resolution Test")
    print("=" * 60)
    
    try:
        axe_root = get_axe_root()
        print(f"✓ AXE_ROOT detected: {axe_root}")
    except RuntimeError as e:
        print(f"✗ ERROR: {e}")
        return False
    
    success = True
    
    # Test main memory file
    memory_hex = axe_root / "test.hex"
    if memory_hex.exists():
        size = memory_hex.stat().st_size
        print(f"✓ Main memory hex: {memory_hex} ({size} bytes)")
    else:
        print(f"✗ Main memory hex missing: {memory_hex}")
        success = False
    
    # Test tools directory
    tools_dir = axe_root / "soc_frame" / "tools"
    if tools_dir.exists():
        print(f"✓ Tools directory: {tools_dir}")
    else:
        print(f"✗ Tools directory missing: {tools_dir}")
        success = False
    
    # Test routing tables
    print("\nNoC Routing Table Files:")
    routing_found = 0
    routing_table_dir = tools_dir / "Routing_Table"
    
    if routing_table_dir.exists():
        print(f"✓ Routing table directory: {routing_table_dir}")
        
        routing_patterns = [
            "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_*.hex",
            "mesh_20RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_4RTsPerRow_5RTsPerCol_routing_*.hex"
        ]
        
        for pattern in routing_patterns:
            routing_files = list(routing_table_dir.glob(pattern))
            if routing_files:
                print(f"✓ Found {len(routing_files)} files matching {pattern}")
                for f in sorted(routing_files)[:3]:  # Show first 3
                    print(f"  - {f.name}")
                if len(routing_files) > 3:
                    print(f"  - ... and {len(routing_files) - 3} more")
                routing_found += len(routing_files)
            else:
                print(f"⚠ No files found matching {pattern}")
        
        # Check specific expected files
        expected_routing_files = [
            "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_0.hex",
            "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_1.hex",
            "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_2.hex",
            "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_3.hex"
        ]
        
        print(f"\nExpected 2x2 Routing Tables:")
        for filename in expected_routing_files:
            routing_file = routing_table_dir / filename
            if routing_file.exists():
                size = routing_file.stat().st_size
                print(f"✓ {filename} ({size} bytes)")
            else:
                print(f"✗ {filename} - MISSING")
                success = False
    else:
        print(f"✗ Routing table directory missing: {routing_table_dir}")
        success = False
    
    # Test RTL paths
    print(f"\nRTL Directory Structure:")
    rtl_dir = axe_root / "soc_frame" / "rtl"
    if rtl_dir.exists():
        print(f"✓ RTL directory: {rtl_dir}")
        
        # Check for defines_paths.vh
        defines_file = rtl_dir / "defines_paths.vh"
        if defines_file.exists():
            print(f"✓ Path definitions: {defines_file}")
        else:
            print(f"✗ Path definitions missing: {defines_file}")
            success = False
            
        # Check memory module
        bram_file = rtl_dir / "memory" / "bram.sv"
        if bram_file.exists():
            print(f"✓ BRAM module: {bram_file}")
            # Check if it includes defines_paths.vh
            with open(bram_file, 'r') as f:
                content = f.read()
                if 'defines_paths.vh' in content:
                    print(f"✓ BRAM includes path definitions")
                else:
                    print(f"⚠ BRAM may not include path definitions")
        else:
            print(f"✗ BRAM module missing: {bram_file}")
    else:
        print(f"✗ RTL directory missing: {rtl_dir}")
        success = False
    
    # Test build system
    print(f"\nBuild System:")
    makefile_include = axe_root / "soc_frame" / "Makefile_include"
    if makefile_include.exists():
        print(f"✓ Makefile_include: {makefile_include}")
        
        with open(makefile_include, 'r') as f:
            content = f.read()
            if 'AXE_ROOT_DEFINE' in content:
                print(f"✓ Makefile supports AXE_ROOT_DEFINE")
            else:
                print(f"⚠ Makefile may not support AXE_ROOT_DEFINE")
    else:
        print(f"✗ Makefile_include missing: {makefile_include}")
        success = False
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("✓ All hex file paths can be resolved successfully!")
        print(f"  - Main memory: test.hex")
        print(f"  - Routing tables: {routing_found} files found")
        print(f"  - RTL integration: Ready")
        print(f"  - Build system: Ready")
    else:
        print("✗ Some hex file paths have issues!")
        print("  Check the missing files listed above.")
    print("=" * 60)
    
    return success

def print_environment_info():
    """Print relevant environment information."""
    print(f"\nEnvironment Information:")
    print(f"Current directory: {Path.cwd()}")
    print(f"AXE_ROOT env var: {os.environ.get('AXE_ROOT', 'Not set')}")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")

if __name__ == "__main__":
    try:
        success = test_hex_path_resolution()
        print_environment_info()
        
        if not success:
            print(f"\nTo fix issues:")
            print(f"1. Set AXE_ROOT: export AXE_ROOT={Path.cwd()}")
            print(f"2. Create missing hex files")
            print(f"3. Run: python3 {__file__}")
            sys.exit(1)
        else:
            print(f"\nHex path resolution test PASSED!")
            sys.exit(0)
            
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)