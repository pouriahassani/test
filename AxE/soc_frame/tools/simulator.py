
import os
import subprocess

import logging
import logging.handlers

from system import *
from memory import *

from software_program import *
from software_controller import *

class Simulator:
    
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    
    def __init__( self ):
        
        pass
        
    
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    
    def run( self, sys, what, args=None, prnt=False ):
        
        logging.debug( "run" )
        
        # check args
        
        assert( isinstance(sys, System) )
        
        if args is None: args = []
        
        # Modern path resolution using axe_paths module
        try:
            from axe_paths import AXE_PATHS
            call = [ str(AXE_PATHS.get_system_executable(sys.name)) ]
        except ImportError as e:
            # NO SILENT FALLBACKS - Show clear error and exit
            from error_handling import print_error
            from pathlib import Path
            
            print_error(
                title="Cannot Find System Executable",
                message=f"""Failed to locate system executable for: {sys.name}

Import error: {e}
Current working directory: {Path.cwd()}

The simulator requires the axe_paths module to locate system executables.""",
                solution=f"""1. Ensure you're in the AxE project directory:
   cd /path/to/axe/project

2. Set up the environment:
   export AXE_ROOT=/path/to/axe/project
   export PYTHONPATH=/path/to/axe/project/soc_frame/tools:$PYTHONPATH

3. Build the system executable:
   cd soc_frame/systems/{sys.name}
   make compile

4. Test the path resolution:
   python3 -c "from axe_paths import AXE_PATHS; print(AXE_PATHS.get_system_executable('{sys.name}'))" """
            )
        call.extend( args )
        
        #~ print( str( call ) )
        
        # create the necessary hex file and copy it to a place where the
        # memory can find it.
        
        # if   isinstance( what, Program ):
            
        #     self.set_hex( what.get_path_hex() )
            
        # elif isinstance( what, Memory ):
            
        #     # TODO pack mem file
        #     pass
            
            
        # elif isinstance( what, str ): # str would be a path to a hex file
            
        #     self.set_hex( what )
            
        
        # if the output should be printed or returned
        print(call)  
        if prnt:
            # Create a clean environment for subprocess calls
            clean_env = os.environ.copy()
            clean_env['OMP_NUM_THREADS'] = '4'
            
            # Remove VERILATOR_ROOT to avoid conflicts with system verilator
            if 'VERILATOR_ROOT' in clean_env:
                del clean_env['VERILATOR_ROOT']
            
            # Use subprocess.run instead of os.system for better environment control
            result = subprocess.run(call, env=clean_env, capture_output=False)
            if result.returncode != 0:
                print(f"Simulation failed with return code: {result.returncode}")
            
        else:
            # Clean environment for subprocess calls
            clean_env = os.environ.copy()
            if 'VERILATOR_ROOT' in clean_env:
                del clean_env['VERILATOR_ROOT']
            
            proc = subprocess.run( call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=clean_env )
            
            stdout = proc.stdout.decode("utf-8")
            stderr = proc.stderr.decode("utf-8")
            print(proc.returncode, proc.stderr)
            stdout_l = stdout.split("\n")
            del stdout_l[-1]
            return stdout_l
            
        
    
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    
    def run_prog( self, sys, prg     , args=None ): return self.run( sys, prg     , args )
    def run_mem(  self, sys, mem     , args=None ): return self.run( sys, mem     , args )
    def run_hex(  self, sys, hex_path, args=None ): return self.run( sys, hex_path, args )
    
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    
    def set_hex( self, src ):
        
        logging.debug( "set_hex" )
        
        # Modern path resolution using axe_paths module
        try:
            from axe_paths import AXE_PATHS
            dst = str(AXE_PATHS.get_memory_hex_path())
        except ImportError as e:
            # NO SILENT FALLBACKS - Show clear error and exit
            from error_handling import print_error
            from pathlib import Path
            
            print_error(
                title="Cannot Find Memory Hex File Path",
                message=f"""Failed to locate memory hex file destination path.

Import error: {e}
Source hex file: {src}
Current working directory: {Path.cwd()}

The simulator requires the axe_paths module to locate the memory hex file.""",
                solution=f"""1. Ensure you're in the AxE project directory:
   cd /path/to/axe/project

2. Set up the environment:
   export AXE_ROOT=/path/to/axe/project
   export PYTHONPATH=/path/to/axe/project/soc_frame/tools:$PYTHONPATH

3. Check the memory hex file path:
   python3 -c "from axe_paths import get_memory_hex_path; print(get_memory_hex_path())"

4. Ensure the hex file exists:
   ls -la /path/to/axe/project/test.hex"""
            )
        
        logging.debug( "src: " + src )
        logging.debug( "dst: " + dst )
        
        # Resolve paths to check if they're the same file
        src_resolved = os.path.abspath(src)
        dst_resolved = os.path.abspath(dst)
        
        if src_resolved == dst_resolved:
            logging.debug( "Source and destination are the same file, skipping copy" )
            return
        
        # if os.path.isfile( dst ):
        #     os.system( "rm " + dst )
        
        # os.system( "touch " + src )
        # os.system( "cp " + dst + " " + src )
        
    
