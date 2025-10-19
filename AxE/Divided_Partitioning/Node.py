
from defines import *

import math

class Node:
    
    def __init__(self, i, name, arch ):
        
        self.i = i
        self.name = name
        self.arch = arch
        
        self.prgs = []
        
    
    def reset( self ):
        self.prgs = []

        
    
