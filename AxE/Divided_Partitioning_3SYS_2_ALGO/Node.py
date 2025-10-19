
from defines import *

import math

class Node:
    
    def __init__(self, i, name, arch ):
        
        self.i = i
        self.name = name
        self.arch = arch
        self.potential_sse = 0
        self.potential_sst = 0
        self.prgs = []
        
    
    def reset( self ):
        self.prgs = []
        self.potential_sse = 0
        self.potential_sst = 0

        
    
