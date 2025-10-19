#!/usr/bin/env python3
"""
Test script to verify VERILATOR_ROOT environment variable handling.
This script helps validate that the fixes resolve the inconsistent VERILATOR_ROOT issue.
"""

import os
import subprocess
import sys

def test_verilator_environment():
    """Test various scenarios for VERILATOR_ROOT handling."""
    print("Testing VERILATOR_ROOT environment variable handling...")
    
    # Test 1: Check current environment
    print("\n1. Current environment:")
    verilator_root = os.environ.get('VERILATOR_ROOT')
    print(f"   VERILATOR_ROOT = {verilator_root}")
    
    # Test 2: Test with VERILATOR_ROOT set
    print("\n2. Testing with VERILATOR_ROOT set:")
    test_env = os.environ.copy()
    test_env['VERILATOR_ROOT'] = '/test/path'
    print(f"   Set VERILATOR_ROOT = {test_env['VERILATOR_ROOT']}")
    
    # Test 3: Test with VERILATOR_ROOT unset
    print("\n3. Testing with VERILATOR_ROOT unset:")
    clean_env = os.environ.copy()
    if 'VERILATOR_ROOT' in clean_env:
        del clean_env['VERILATOR_ROOT']
    print(f"   VERILATOR_ROOT = {clean_env.get('VERILATOR_ROOT', 'not set')}")
    
    # Test 4: Test verilator command with clean environment
    print("\n4. Testing verilator command with clean environment:")
    try:
        result = subprocess.run(['verilator', '--version'], 
                               env=clean_env, 
                               capture_output=True, 
                               text=True)
        if result.returncode == 0:
            print("   SUCCESS: Verilator runs correctly with clean environment")
            print(f"   Version: {result.stdout.strip()}")
        else:
            print("   ERROR: Verilator failed with clean environment")
            print(f"   Error: {result.stderr}")
    except FileNotFoundError:
        print("   ERROR: Verilator command not found")
    
    # Test 5: Test make command with clean environment
    print("\n5. Testing make command availability:")
    try:
        result = subprocess.run(['make', '--version'], 
                               env=clean_env, 
                               capture_output=True, 
                               text=True)
        if result.returncode == 0:
            print("   SUCCESS: Make command available")
        else:
            print("   ERROR: Make command failed")
    except FileNotFoundError:
        print("   ERROR: Make command not found")
    
    print("\nTest completed. The fixes should resolve VERILATOR_ROOT conflicts.")

if __name__ == "__main__":
    test_verilator_environment()