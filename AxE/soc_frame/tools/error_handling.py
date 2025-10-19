#!/usr/bin/env python3
"""
AxE Error Handling Utilities

Provides colorful, informative error messages that tell users exactly
what's wrong and how to fix it. No more silent fallbacks!
"""

import sys
import os
from pathlib import Path

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def print_error(title, message, solution=None, exit_code=1):
    """
    Print a colorful, informative error message and exit
    
    Args:
        title: Short error title
        message: Detailed error description
        solution: Optional solution steps
        exit_code: Exit code (default 1)
    """
    print(f"\n{Colors.RED}{Colors.BOLD}❌ ERROR: {title}{Colors.RESET}")
    print(f"{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"{Colors.WHITE}{message}{Colors.RESET}")
    
    if solution:
        print(f"\n{Colors.CYAN}{Colors.BOLD}💡 SOLUTION:{Colors.RESET}")
        print(f"{Colors.CYAN}{solution}{Colors.RESET}")
    
    print(f"{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    sys.exit(exit_code)

def print_warning(title, message, suggestion=None):
    """
    Print a colorful warning message (doesn't exit)
    
    Args:
        title: Short warning title
        message: Detailed warning description  
        suggestion: Optional suggestion
    """
    print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  WARNING: {title}{Colors.RESET}")
    print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"{Colors.WHITE}{message}{Colors.RESET}")
    
    if suggestion:
        print(f"\n{Colors.CYAN}{Colors.BOLD}💡 SUGGESTION:{Colors.RESET}")
        print(f"{Colors.CYAN}{suggestion}{Colors.RESET}")
    
    print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

def print_success(title, message):
    """
    Print a colorful success message
    
    Args:
        title: Short success title
        message: Detailed success description
    """
    print(f"\n{Colors.GREEN}{Colors.BOLD}✅ SUCCESS: {title}{Colors.RESET}")
    print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
    print(f"{Colors.WHITE}{message}{Colors.RESET}")
    print(f"{Colors.GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")

def axe_root_not_found_error():
    """Standard error for when AXE_ROOT cannot be found"""
    cwd = Path.cwd()
    
    print_error(
        title="AxE Project Root Not Found",
        message=f"""Cannot locate the AxE project root directory.

Current working directory: {cwd}
Environment variable AXE_ROOT: {os.environ.get('AXE_ROOT', 'NOT SET')}

The AxE project structure requires these directories:
  • CLAUDE.md (project marker file)
  • soc_frame/ (SoC framework directory)
  • soc_frame/tools/ (tools directory)

None of these were found in the current directory tree.""",
        solution=f"""1. Navigate to the AxE project directory:
   cd /path/to/axe/project

2. OR set the AXE_ROOT environment variable:
   export AXE_ROOT=/path/to/axe/project

3. OR run from within the AxE project directory structure

Example:
   export AXE_ROOT=/home/axe/workspace
   cd /home/axe/workspace/soc_frame/tools
   python3 your_script.py"""
    )

def missing_file_error(file_path, file_type="file"):
    """Standard error for missing files"""
    
    print_error(
        title=f"Required {file_type.title()} Not Found",
        message=f"""Cannot find required {file_type}: {file_path}

File exists: {Path(file_path).exists()}
Parent directory exists: {Path(file_path).parent.exists()}
Parent directory contents: {list(Path(file_path).parent.iterdir()) if Path(file_path).parent.exists() else 'N/A'}

This {file_type} is required for AxE operation.""",
        solution=f"""1. Check if the file path is correct:
   ls -la {file_path}

2. If the file should exist, check file permissions:
   chmod 644 {file_path}

3. If using hex files, ensure they are generated:
   cd soc_frame/systems/your_system
   make compile

4. Check the AxE project structure is complete:
   export AXE_ROOT=/path/to/axe/project
   python3 -c "from soc_frame.tools.axe_paths import validate_axe_environment; validate_axe_environment()" """
    )

def import_error(module_name, import_path=""):
    """Standard error for import failures"""
    
    print_error(
        title=f"Import Failed: {module_name}",
        message=f"""Cannot import required module: {module_name}

Python path: {sys.path}
Current working directory: {Path.cwd()}
Import attempted from: {import_path or 'default path'}

This module is required for AxE operation.""",
        solution=f"""1. Ensure you're running from the AxE project directory:
   cd /path/to/axe/project

2. Set up the Python path correctly:
   export PYTHONPATH=/path/to/axe/project/soc_frame/tools:$PYTHONPATH

3. OR add the tools directory to your Python path:
   import sys
   sys.path.insert(0, '/path/to/axe/project/soc_frame/tools')

4. Check if the module file exists:
   ls -la soc_frame/tools/{module_name}.py

Example:
   export AXE_ROOT=/home/axe/workspace
   export PYTHONPATH=/home/axe/workspace/soc_frame/tools:$PYTHONPATH
   python3 your_script.py"""
    )

def config_not_found_error(config_name, searched_paths):
    """Standard error for configuration file not found"""
    
    searched_list = '\n   '.join(str(p) for p in searched_paths)
    
    print_error(
        title=f"Configuration File Not Found: {config_name}",
        message=f"""Cannot find configuration file: {config_name}

Searched locations:
   {searched_list}

This configuration file is required for AxE operation.""",
        solution=f"""1. Create the configuration file in the tools directory:
   cp example_config.conf soc_frame/tools/{config_name}

2. OR check if the file exists with a different name:
   ls -la soc_frame/tools/*.conf

3. OR specify the full path to your configuration:
   python3 your_script.py --config /path/to/{config_name}

4. Check available configuration files:
   find . -name "*.conf" -type f"""
    )

def environment_validation_error(missing_paths):
    """Standard error for environment validation failure"""
    
    missing_list = '\n   '.join(f"{name}: {path}" for name, path in missing_paths.items())
    
    print_error(
        title="AxE Environment Validation Failed",
        message=f"""The AxE environment is not properly set up.

Missing critical paths:
   {missing_list}

These directories/files are required for AxE operation.""",
        solution=f"""1. Ensure you're in the correct AxE project directory:
   cd /path/to/axe/project
   ls -la  # Should show CLAUDE.md, soc_frame/, etc.

2. Set the AXE_ROOT environment variable:
   export AXE_ROOT=/path/to/axe/project

3. Run the environment test:
   python3 test_hex_paths.py

4. For a complete setup, run:
   ./setup-development.sh  # If available

Example:
   export AXE_ROOT=/home/axe/workspace
   cd /home/axe/workspace
   python3 test_hex_paths.py"""
    )

if __name__ == "__main__":
    """Test the error handling utilities"""
    
    print("Testing AxE Error Handling Utilities")
    print("=" * 50)
    
    # Test different error types
    print_success("Test Suite", "Error handling utilities loaded successfully")
    
    print_warning("Test Warning", "This is a test warning message", 
                 "This is what you should do to fix it")
    
    # Uncomment to test error (will exit):
    # print_error("Test Error", "This is a test error message", 
    #            "This is how you fix it")