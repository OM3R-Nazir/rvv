import numpy as np

class SEWC:
    
    def __init__(self, SEW):
        self.SEW = SEW
        
        if SEW == 8:
            self.idtype = np.int8
            self.udtype = np.uint8
        elif SEW == 16:
            self.idtype = np.int16
            self.udtype = np.uint16
            self.fdtype = np.float16
        elif SEW == 32:
            self.idtype = np.int32
            self.udtype = np.uint32
            self.fdtype = np.float32
        elif SEW == 64:
            self.idtype = np.int64
            self.udtype = np.uint64
            self.fdtype = np.float64

        self.imax = np.iinfo(self.idtype).max
        self.imin = np.iinfo(self.idtype).min
        self.umax = np.iinfo(self.udtype).max
        self.umin = 0

    def get_lower_sewc(self):
        if self.SEW == 8: raise ValueError("No SEW lower than 8")
        else: return SEWC(self.SEW//2)
        
    def get_higher_sewc(self):
        if self.SEW == 64: return ValueError("No SEW higher than 64")
        else: return SEWC(self.SEW*2)
