#!/usr/bin/env python3
"""
Test the new colorful error handling
"""

import sys
import os
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent / "soc_frame" / "tools"))

# Test 1: Test the error handling utilities directly
print("=== Testing Error Handling Utilities ===")
from error_handling import print_success, print_warning

print_success("Error Handling Test", "Error handling utilities are working correctly!")

print_warning("Test Warning", "This is a test warning", "This would be the suggested fix")

# Test 2: Test that successful imports work
print("\n=== Testing Successful Path Import ===")
os.environ['AXE_ROOT'] = '/home/axe/workspace'

try:
    from defines import PATH_PRGS
    print(f"✅ SUCCESS: PATH_PRGS = {PATH_PRGS}")
except Exception as e:
    print(f"❌ FAILED: {e}")

print("\n=== All Error Handling Tests Complete ===")