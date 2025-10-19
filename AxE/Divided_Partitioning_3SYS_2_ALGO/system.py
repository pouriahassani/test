
from defines import *

from Node import *

class system:
    
    def __init__( self, name = None, node_archs = []):
        
        self.name = name
        self.nodes = []
        self.prgs = []
        self.CHARGING_INITIAL = 0
        self.CHARGING_RATE = 0
        self.SSE = {"MIN_SSE":0,"MIN_SST":0,"NP":0}
        self.SST = {"MIN_SSE":0,"MIN_SST":0,"NP":0}
        
        if len(node_archs) > 0:
            for node_arch in node_archs:
                self.create_add_node( node_arch )
    
        
    
    def reset( self ):
        self.prgs = []
        for node in self.nodes:
            node.reset()
        
    
    def create_add_node( self, arch ):
        
        ni_next = len( self.nodes )
        
        self.nodes.append( Node( ni_next, (str(ni_next) + arch.name), arch ) )
        
    
