
import os
import subprocess

from defines import *
from func_files import *
from constant import *

class System:
    
    path_base = PATH_SYSS
    
    name = ""
    
    # --------------------------------------------------------------------------
    # _ _ I N I T _ _
    # --------------------------------------------------------------------------
    
    def __init__( self, name ):
        
        self.name = name
        
    
    # --------------------------------------------------------------------------
    # G E T _ P A T H _ D I R
    # --------------------------------------------------------------------------
    
    def get_path_dir( self ):
        
        return self.path_base  + self.name + "/"
    
    # DEPRECATED
    
    def get_dir_path( self ):
        
        return self.get_path_dir()
    
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    
    def clean( self ):
        
        # Ensure consistent VERILATOR_ROOT handling by unsetting it before make
        clean_env = os.environ.copy()
        if 'VERILATOR_ROOT' in clean_env:
            del clean_env['VERILATOR_ROOT']
        
        # Use subprocess.run with explicit environment to avoid VERILATOR_ROOT conflicts
        print(f"🧹 Cleaning system: {self.name}")
        result = subprocess.run(
            ["make", "-C", self.get_dir_path(), "clean"],
            env=clean_env,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Clean failed: {result.stderr}")
        
    
    # --------------------------------------------------------------------------
    # 
    # --------------------------------------------------------------------------
    
    def compl( self ):
        
        # Ensure consistent VERILATOR_ROOT handling by unsetting it before make
        clean_env = os.environ.copy()
        if 'VERILATOR_ROOT' in clean_env:
            del clean_env['VERILATOR_ROOT']
        
        # Use subprocess.run with explicit environment to avoid VERILATOR_ROOT conflicts
        print(f"🔨 Compiling system: {self.name}")
        result = subprocess.run(
            ["make", "-C", self.get_dir_path()],
            env=clean_env,
            text=True
        )
        
        if result.returncode != 0:
            print(f"Compile failed: {result.stderr}")
            return False
        
        return True
        
    
    def set_memory_file( self ):
        
        pass
    
    # --------------------------------------------------------------------------
    # G E T _ D E F I N E
    # --------------------------------------------------------------------------
    
    def get_define( self, define_file, var ):
        
        return get_constant( self.get_dir_path() + define_file + ".vh", var )
    
    # --------------------------------------------------------------------------
    # S E T _ D E F I N E
    # --------------------------------------------------------------------------
    
    def set_define( self, define_file, var, val ):
        
        set_constant( self.get_dir_path() + define_file + ".vh", var, val )
    
