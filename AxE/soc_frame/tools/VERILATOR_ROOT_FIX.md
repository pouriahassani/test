# VERILATOR_ROOT Environment Variable Fix

## Problem
The Python build system was experiencing inconsistent VERILATOR_ROOT environment variable handling, causing conflicts when calling the build system through Python scripts. This led to verilator complaining about inconsistent VERILATOR_ROOT paths.

## Root Cause
1. **Environment Variable Inheritance**: When Python scripts called `os.system("make ...")`, the VERILATOR_ROOT environment variable was being passed through inconsistently
2. **Conflicting Paths**: The system had both a custom verilator installation (at `/home/axe/verilator`) and a system-installed verilator (at `/usr/share/verilator`)
3. **Makefile Logic**: The Makefile logic handles empty VERILATOR_ROOT by defaulting to system verilator, but conflicts arise when the variable is set but points to an incompatible version

## Solution
Modified the Python build system to ensure consistent VERILATOR_ROOT handling:

### Files Modified:
1. **`system.py`**:
   - `clean()` method: Now uses `subprocess.run` with a cleaned environment
   - `compl()` method: Now uses `subprocess.run` with a cleaned environment
   - Both methods unset VERILATOR_ROOT before calling make

2. **`software.py`**:
   - `clean()` method: Now uses `subprocess.run` with a cleaned environment
   - `compl()` method: Now uses `subprocess.run` with a cleaned environment
   - Both methods unset VERILATOR_ROOT before calling make

3. **`simulator.py`**:
   - `run()` method: Now uses `subprocess.run` with a cleaned environment
   - Unsets VERILATOR_ROOT before executing simulation binaries

### Key Changes:
1. **Environment Cleaning**: All subprocess calls now explicitly remove VERILATOR_ROOT from the environment
2. **Subprocess Usage**: Replaced `os.system()` calls with `subprocess.run()` for better control
3. **Error Handling**: Added proper error handling and return codes
4. **Consistency**: All build-related Python functions now handle environment variables consistently

## How It Works
1. When Python scripts need to call make or verilator:
   - Copy the current environment
   - Remove VERILATOR_ROOT from the copied environment
   - Use subprocess.run with the cleaned environment
   - Let the Makefile logic handle verilator detection using system paths

2. This approach ensures:
   - No conflicts between different verilator installations
   - Consistent behavior across all Python build scripts
   - Proper fallback to system-installed verilator

## Testing
A test script `test_verilator_env.py` was created to validate the environment handling:
- Tests current environment state
- Validates verilator command works with clean environment
- Confirms make command availability
- Verifies the fix resolves VERILATOR_ROOT conflicts

## Usage
The fix is transparent to users. The existing Python build scripts (`system.py`, `software.py`, `simulator.py`) will now handle VERILATOR_ROOT consistently without requiring any changes to user code.

## Benefits
1. **Eliminates VERILATOR_ROOT conflicts**: No more inconsistent path errors
2. **Robust build system**: Better error handling and return codes
3. **Consistent behavior**: All Python build scripts now work the same way
4. **Maintainable**: Clear separation between Python environment and build environment
5. **Backwards compatible**: Existing code continues to work without modification