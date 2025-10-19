#!/usr/bin/env python3
"""
Complete AxE Hex File Path Integration Test

This script tests the complete hex file path management system:
1. Python tool integration via axe_paths.py
2. RTL path management via defines_paths.vh  
3. Build system integration via Makefile_include
4. End-to-end path resolution consistency
"""

import os
import sys
import subprocess
from pathlib import Path

# Add tools directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "soc_frame" / "tools"))

try:
    from axe_paths import (
        AXE_PATHS, 
        get_memory_hex_path, 
        get_routing_table_path,
        list_available_routing_tables
    )
except ImportError as e:
    print(f"❌ Failed to import axe_paths: {e}")
    sys.exit(1)

def test_python_integration():
    """Test Python hex file path integration"""
    print("=== Python Integration Test ===")
    
    # Test memory hex path
    memory_hex = get_memory_hex_path()
    print(f"Memory hex path: {memory_hex}")
    if memory_hex.exists():
        size = memory_hex.stat().st_size
        print(f"✅ Memory hex file exists ({size} bytes)")
    else:
        print(f"⚠️ Memory hex file missing: {memory_hex}")
    
    # Test routing table paths
    routing_tables = list_available_routing_tables()
    print(f"✅ Found {len(routing_tables)} routing table files")
    
    # Test specific routing table access
    routing_0 = get_routing_table_path(0)
    print(f"Routing table 0: {routing_0}")
    if routing_0.exists():
        print(f"✅ Routing table 0 exists")
    else:
        print(f"❌ Routing table 0 missing")
    
    return memory_hex.exists() and routing_0.exists()

def test_rtl_integration():
    """Test RTL defines_paths.vh integration"""
    print("\n=== RTL Integration Test ===")
    
    # Check defines_paths.vh exists and has correct content
    defines_file = AXE_PATHS.rtl / "defines_paths.vh"
    if not defines_file.exists():
        print(f"❌ defines_paths.vh missing: {defines_file}")
        return False
    
    print(f"✅ defines_paths.vh exists: {defines_file}")
    
    # Check content
    with open(defines_file, 'r') as f:
        content = f.read()
    
    checks = [
        ("AXE_ROOT_DEFINE", "Environment variable support"),
        ("MEMORY_HEX_PATH", "Memory hex path definition"),
        ("ROUTING_TABLE_0", "Routing table definitions"),
        ("Routing_Table/", "Correct routing table directory")
    ]
    
    success = True
    for check, description in checks:
        if check in content:
            print(f"✅ {description}: Found {check}")
        else:
            print(f"❌ {description}: Missing {check}")
            success = False
    
    return success

def test_build_system_integration():
    """Test build system integration"""
    print("\n=== Build System Integration Test ===")
    
    # Check Makefile_include
    makefile = AXE_PATHS.soc_frame / "Makefile_include"
    if not makefile.exists():
        print(f"❌ Makefile_include missing: {makefile}")
        return False
    
    print(f"✅ Makefile_include exists: {makefile}")
    
    # Check environment variable support
    with open(makefile, 'r') as f:
        content = f.read()
    
    checks = [
        ("AXE_ROOT", "AXE_ROOT environment variable"),
        ("AXE_ROOT_DEFINE", "AXE_ROOT_DEFINE preprocessor flag"),
        ("-DAXE_ROOT_DEFINE", "Verilator preprocessor define")
    ]
    
    success = True
    for check, description in checks:
        if check in content:
            print(f"✅ {description}: Found {check}")
        else:
            print(f"❌ {description}: Missing {check}")
            success = False
    
    return success

def test_verilator_compilation():
    """Test that Verilator compilation works with new paths"""
    print("\n=== Verilator Compilation Test ===")
    
    # Change to a system directory
    system_dir = AXE_PATHS.systems / "2x2_16_priority_input_approx"
    if not system_dir.exists():
        print(f"❌ System directory missing: {system_dir}")
        return False
    
    print(f"Testing compilation in: {system_dir}")
    
    # Set environment variable
    env = os.environ.copy()
    env['AXE_ROOT'] = str(AXE_PATHS.axe_root)
    
    try:
        # Run make clean first
        result = subprocess.run(
            ["make", "clean"], 
            cwd=system_dir, 
            env=env,
            capture_output=True, 
            text=True,
            timeout=30
        )
        
        # Run make compile
        result = subprocess.run(
            ["make", "compile"], 
            cwd=system_dir, 
            env=env,
            capture_output=True, 
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("✅ Verilator compilation successful")
            
            # Check if executable was created
            executable = system_dir / "obj_dir" / "Vtop"
            if executable.exists():
                print("✅ Executable created successfully")
                return True
            else:
                print("⚠️ Compilation succeeded but executable not found")
                return False
        else:
            print(f"❌ Verilator compilation failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Compilation timed out")
        return False
    except Exception as e:
        print(f"❌ Compilation test failed: {e}")
        return False

def test_path_consistency():
    """Test that RTL and Python paths are consistent"""
    print("\n=== Path Consistency Test ===")
    
    # Compare memory hex paths
    python_memory = get_memory_hex_path()
    print(f"Python memory path: {python_memory}")
    
    # Expected RTL path (when AXE_ROOT_DEFINE is set)
    expected_rtl_memory = AXE_PATHS.axe_root / "test.hex"
    print(f"Expected RTL path: {expected_rtl_memory}")
    
    if python_memory == expected_rtl_memory:
        print("✅ Memory hex paths are consistent")
        memory_consistent = True
    else:
        print("❌ Memory hex paths are inconsistent")
        memory_consistent = False
    
    # Compare routing table paths  
    python_routing = get_routing_table_path(0)
    expected_rtl_routing = AXE_PATHS.tools / "Routing_Table" / "mesh_4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol_routing_0.hex"
    
    print(f"Python routing path: {python_routing}")
    print(f"Expected RTL path: {expected_rtl_routing}")
    
    if python_routing == expected_rtl_routing:
        print("✅ Routing table paths are consistent")
        routing_consistent = True
    else:
        print("❌ Routing table paths are inconsistent")
        routing_consistent = False
    
    return memory_consistent and routing_consistent

def main():
    """Run complete integration test suite"""
    print("AxE Hex File Path Complete Integration Test")
    print("=" * 50)
    
    # Set environment variable for consistent testing
    os.environ['AXE_ROOT'] = str(AXE_PATHS.axe_root)
    print(f"Using AXE_ROOT: {AXE_PATHS.axe_root}")
    
    tests = [
        ("Python Integration", test_python_integration),
        ("RTL Integration", test_rtl_integration), 
        ("Build System Integration", test_build_system_integration),
        ("Path Consistency", test_path_consistency),
        ("Verilator Compilation", test_verilator_compilation),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All hex file path integration tests PASSED!")
        print("The AxE project now has consistent, portable hex file path management.")
        return True
    else:
        print("💥 Some tests FAILED!")
        print("Check the failures above and fix the issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)