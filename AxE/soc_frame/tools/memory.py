
import json

from func_files import *
from func_addr import *

from software_program import *

class Memory:
    
    # the memory object has a dict, that holds all the programs/tasks.
    # 
    # {
    #     "task1" :                         <- the name of the program/task
    #     {
    #         "arch_32_i" :                 <- the architecture
    #         {
    #             "sp"  : 12                <- the stack pointer
    #             "hex" : [...]             <- array of all instructions
    #         }
    #     }
    # }
    
    prgs = {}
    
    # --------------------------------------------------------------------------
    # __init__
    # --------------------------------------------------------------------------
    
    def __init__( self, memory_file_path = None ):
        
        if ( memory_file_path != None ):
            self.load( memory_file_path )
        
    
    # --------------------------------------------------------------------------
    # load
    # --------------------------------------------------------------------------
    
    def load( self, memory_file_path ):
        
        self.prgs = read_dict_from_json( memory_file_path )
        
    
    # --------------------------------------------------------------------------
    # save
    # --------------------------------------------------------------------------
    
    def save( self, memory_file_path ):
        
        write_dict_to_json( self.prgs, memory_file_path )
        
    
    # --------------------------------------------------------------------------
    # include
    # --------------------------------------------------------------------------
    
    # including (adding) a prog to the memory
    
    def include( self, prg, sp ):
        
        self.prgs[ prg.name ] = {}
        self.prgs[ prg.name ][ prg.arch ] = {}
        
        self.prgs[ prg.name ][ prg.arch ][ "sp" ] = sp
        self.prgs[ prg.name ][ prg.arch ][ "hex" ] = prg.read()
    
    # --------------------------------------------------------------------------
    # info
    # --------------------------------------------------------------------------
    
    # MIGHT NOT WORK
    
    # print some debug info
    
    def info( self ):
        
        print( "-------------------------------------------------------- info" )
        print( "" )
        
        prgs_lst = self.get_prgs_lst()
        
        for prg in prgs_lst:
            
            print( "--- " + prg + " ---" )
            print( "arch \t\t size \t\t sp" )
            
            for arch in self.prgs[prg]:
                
                size = len(self.prgs[prg][arch]["hex"])
                sp = self.prgs[prg][arch]["sp"]
                
                print( arch + "\t\t" + str(size) + "\t\t" + sp )
                
            
            print( "" )
        
        print( "---------------------------------------------------- info end" )
        
    
    # --------------------------------------------------------------------------
    # get_prgs_lst
    # --------------------------------------------------------------------------
    
    # this is a list of programs stored in this object
    
    def get_prgs_lst( self ):
        
        prg_list = []
        
        for prg in self.prgs:
            
            prg_list.append( prg )
            
        
        prg_list.sort()
        
        return prg_list
        
    
    # --------------------------------------------------------------------------
    # pack_prgs
    # --------------------------------------------------------------------------
    
    # here the memory usage of every prg is analyzed and the stack pointer set
    # accordingly, instead of guessing or distributing them equally. this allows
    # the memory file to become smaller which can be important if the system
    # should run on a board.
    
    # after running this method all the prgs stored in the dict have a stack
    # pointer set that is not wasting any memory.
    
    def pack_prgs( self, sim, prgs_lst, arch_dict ):
        
        # Load stack pointer from generated memory configuration
        try:
            with open('/home/axe/workspace/soc_frame/generated/memory_vars.mk', 'r') as f:
                for line in f:
                    if line.startswith('STACK_POINTER'):
                        sp = line.split('=')[1].strip()
                        break
                else:
                    # Fallback if configuration not found
                    sp = "0x00F00000"  # Use our YAML config default
        except FileNotFoundError:
            # Throw an error if the file is not found
            from error_handling import print_error
            print_error(
                title="Memory Configuration Error",
                message="The memory configuration file '../generated/memory_vars.mk' was not found.",
            )
            exit(1)

        
        # we iterate over every prg and for each prg every arch
        
        for prg_name in prgs_lst:
            
            self.prgs[ prg_name ] = {}
            
            for arch, sys in arch_dict.items():
                
                self.prgs[ prg_name ][ arch ] = {}
                
                # here we are using software objects. this means, that the
                # program is read from the filesystem and not the dict of
                # the memory object!
                
                prg = Program( prg_name, arch )
                
                # Use stack pointer from memory configuration system
                # prg.clean()
                # prg.compl( sp )
                
                # a simulation is run with an arg that outputs the memory usage
                
                # memory_usage = sim.run( sys, prg, [MEM_PACKER_OUTPUT_MEMORY] )
                
                # sp = prg.get_stack_pointer( memory_usage )
                
                # the program has to be compiled again using the new stack
                # pointer. this is the program that is then read and stored in
                # the dict of the memory.
                
                prg.clean()
                
                # Try compilation with current memory layout, adjust if it fails
                compilation_success = prg.compl( sp )
                if not compilation_success:
                    print("⚠️  Compilation failed - adjusting memory layout...")
                    exit(1)
                    import subprocess
                    subprocess.run(['python3', '/home/axe/workspace/soc_frame/tools/simple_memory_adjuster.py'])
                    print("🔄 Retrying compilation with adjusted memory...")
                    prg.clean()
                    compilation_success = prg.compl( sp )
                    if not compilation_success:
                        raise Exception("Compilation failed even after memory adjustment")
                
                self.prgs[ prg_name ][ arch ][ "sp" ] = sp
                self.prgs[ prg_name ][ arch ][ "hex" ] = prg.read()
            
        
    
    # --------------------------------------------------------------------------
    # pack
    # --------------------------------------------------------------------------
    
    # here the actual memory file is created. the result is a .hex file where
    # all the instructions of all the prgs are included.
    
    def pack( self, arch_lst, dst, first = "" ):
        
        filler = "00000000"
        
        # Create a dictionary to store program addresses
        prg_addresses = {}
        
        prgs_lst = self.get_prgs_lst()
        
        # Calculate program addresses based on the new scheme
        # Controller is first, then user programs at node memory spaces
        for i, prg in enumerate(prgs_lst):
            if prg == first:  # Controller program
                prg_addresses[prg] = 0  # Controller starts at address 0
            else:
                # User programs start at (program_index) * AXI_OFFSET_STEP (0x01000000)
                # Find the program index (excluding controller)
                user_prgs = [p for p in prgs_lst if p != first]
                if prg in user_prgs:
                    prg_index = user_prgs.index(prg)
                    prg_addresses[prg] = (prg_index + 1) * 0x01000000  # 16MB * (index + 1)
        
        # Find the maximum address to determine memory size needed
        max_addr = 0
        for prg in prgs_lst:
            for arch in arch_lst:
                try:
                    prg_hex = self.prgs[ prg ][ arch ][ "hex" ]
                    prg_start_addr = prg_addresses.get(prg, 0)
                    prg_start = prg_start_addr // 4  # Convert address to index directly
                    prg_end = prg_start + len(prg_hex) + addr_to_index(self.prgs[prg][arch]["sp"]) - len(prg_hex)
                    max_addr = max(max_addr, prg_end)
                except KeyError:
                    continue
        
        # Create sparse memory array
        mem = [filler] * max_addr
        
        # Place programs at their assigned addresses
        for prg in prgs_lst:
            for arch in arch_lst:
                try:
                    prg_hex = self.prgs[ prg ][ arch ][ "hex" ]
                    prg_start_addr = prg_addresses.get(prg, 0)
                    prg_start_index = prg_start_addr // 4  # Convert address to index directly
                    
                    # Place program instructions
                    for j, instruction in enumerate(prg_hex):
                        mem[prg_start_index + j] = instruction
                    
                    # Fill gap to stack pointer
                    missing = addr_to_index(self.prgs[prg][arch]["sp"]) - len(prg_hex)
                    # Gap is already filled with filler, so no need to extend
                    
                    print(f"Placed {prg} at address {hex(prg_addresses.get(prg, 0))} (index {prg_start_index})")
                    
                except KeyError:
                    continue
                
            
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
                Target hex file: {dst}
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
        mem_f = open( dst, "w" )
        
        for i,l in enumerate( mem ):
            
            mem_f.write( l + "\n" )
            #~ mem_f.write( str(i) + ": " + l + "\n" )
            
        
        mem_f.close()
        
    
