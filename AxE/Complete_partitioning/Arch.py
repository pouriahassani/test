
from defines import *

class Arch:
    
    def __init__(self,i,mw, Int_Type,Float_Type):
        self.i = i
        self.name = "I" + str(Int_Type) + "_F" + str(Float_Type)
        self.power = mw
        self.Int_Type  = Int_Type
        self.Float_Type  = Float_Type

        
    

