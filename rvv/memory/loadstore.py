from rvv.base import BaseRVV
import numpy as np

class LoadStore(BaseRVV):
    
    def __vle(self, sew, vd, np_memory, np_memory_offset, masked=False, bstride=None):
        self._debug_operation()
        vector = np.zeros(self.VL, np.uint8)
        np_memory = np_memory.view(np.uint8)
        
        sew_bytes = sew // 8
        bstride = sew_bytes if bstride is None else bstride
        
        min_memory_size = np_memory_offset + ((self.VL - 1) * bstride) + sew_bytes
        if min_memory_size > np_memory.size:
            raise ValueError("Size of np_memory is too small")
        
        if bstride == sew_bytes:
            vector = np_memory[np_memory_offset:np_memory_offset + (self.VL * sew_bytes)]
        else:
            for i in range(self.VL):
                start = np_memory_offset + i * bstride
                vector[i:i + sew_bytes] = np_memory[start:start + sew_bytes]
        
        
        vvd = self.vec(vd)
        vector = vector.view(f"uint{sew}")
        mask = self._get_mask([vd], masked)
        
        self._debug_val('v', 'd', vvd, vd)
        self._debug_print(f"{'-'*30}")
        
        vvd[mask] = vector[mask]
        
        self._debug_val('v', 'd', vvd, vd)
    

    
    def __vse(self, sew, vd, np_memory, np_memory_offset, masked=False, bstride=None):
        self._debug_operation()
        
        np_memory = np_memory.view(np.uint8)
        sew_bytes = sew // 8
        bstride = sew_bytes if bstride is None else bstride
        
        min_memory_size = np_memory_offset + ((self.VL - 1) * bstride) + sew_bytes
        if min_memory_size > np_memory.size:
            raise ValueError("Size of np_memory is too small")
        
        np_memory = np_memory.view(f"uint{sew}")
        vvd = self.vec(vd).view(f"uint{sew}")
        mask = self._get_mask([vd], masked)
        
        self._debug_val('v', 'd', vvd, vd)
        self._debug_print(f"{'-'*30}")
        
        if bstride == sew_bytes:
            start = np_memory_offset * sew_bytes
            end = start + self.VL * sew_bytes
            np_memory[start:end][mask] = vvd[mask]
            return
        
        for i in range(self.VL):
            start = np_memory_offset + i * bstride
            if mask[i]:
                np_memory[start:start + sew_bytes] = vvd[i]
        
        
    def vle8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vle(8, vd, np_memory, np_memory_offset, masked)

    def vle16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vle(16, vd, np_memory, np_memory_offset, masked)
    
    def vle32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vle(32, vd, np_memory, np_memory_offset, masked)
    
    def vle64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vle(64, vd, np_memory, np_memory_offset, masked)
    
    def vse8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vse(8, vd, np_memory, np_memory_offset, masked)
    
    def vse16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vse(16, vd, np_memory, np_memory_offset, masked)
    
    def vse32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vse(32, vd, np_memory, np_memory_offset, masked)
    
    def vse64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vse(64, vd, np_memory, np_memory_offset, masked)
    
    def vlse8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vle(8, vd, np_memory, np_memory_offset, masked, bstride)
    
    def vlse16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vle(16, vd, np_memory, np_memory_offset, masked, bstride)
    
    def vlse32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vle(32, vd, np_memory, np_memory_offset, masked, bstride)
    
    def vlse64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vle(64, vd, np_memory, np_memory_offset, masked, bstride)
        
    def vsse8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vse(8, vd, np_memory, np_memory_offset, masked, bstride)
    
    def vsse16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vse(16, vd, np_memory, np_memory_offset, masked, bstride)
    
    def vsse32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vse(32, vd, np_memory, np_memory_offset, masked, bstride)
    
    def vsse64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vse(64, vd, np_memory, np_memory_offset, masked, bstride)