
from defines import *

class Prg:
    
    def __init__(self, i, name, ec, ac,exact_energy, approximate_energy,Int_pref, Float_pref ):
        
        self.i = i
        self.name = name
        self.exact_energy = exact_energy
        self.approximate_energy = approximate_energy
        self.Int_pref = Int_pref
        self.Float_pref = Float_pref
        
        self.c = []
        self.c.append( ec )
        self.c.append( ac )
        
        self.t = 0
        self.d = 0
        self.d_next = 0
        self.release = 0
        self.deadline = 0
        self.ready = False
        
        self.s = 0
        
    def get_c(self,i):
        return self.c[i]
    
    def pn( self ):
        
        return ( str(self.i) + " " + self.name[0:4] )
        
    
    def p( self ):
        
        return ( "prg" + self.pn() + "\tec: " + str(self.c[ARCH_EXACT]) + "\tac: " + str(self.c[ARCH_APPRX]) + "\tt: " + str(self.t) )
        
    
    def set_t( self, mult ):
        
        self.t = round( self.c[ARCH_EXACT] * mult, 2 )
        self.d = self.t 

    def set_deadline( self, mult ):
        self.deadline = round( self.c[0] * mult, 2 )
        
        
        
    
