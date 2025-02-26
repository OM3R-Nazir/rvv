from rvv.base import BaseRVV
import numpy as np

class Indexed(BaseRVV):
    
    def __get_vindex(self, vi, sew):
        start = vi * self.VLENB
        end = start + self.VL * sew // 8
        return self.VRF[start:end].view(f"uint{sew}")
    
    def __vloxei(self, isew, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_operation()
        
        vvd = self.vec(vd)
        mask = self._get_mask([vd, vindex], masked)
        vvindex = self.__get_vindex(vindex, isew)
        
        self._debug_val('v', 'd', vvd, vd)
        self._debug_val('v', 'i', vvindex, vindex)
        self._debug_print(f"{'-'*30}")
        
        np_memory = np_memory.view(np.uint8)
        for i in range(self.VL):
            if mask[i]:
                ptr = vvindex[i] + np_memory_offset
                vvd[i] = np_memory[ptr:ptr + self.SEW.SEW // 8].view(self.SEW.udtype)[0]
        
        self._debug_val('v', 'd', vvd, vd)
    
    def __vsoxei(self, isew, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_operation()
        
        vvd = self.vec(vd)
        mask = self._get_mask([vd, vindex], masked)
        vvindex = self.__get_vindex(vindex, isew)
        
        self._debug_val('v', 'd', vvd, vd)
        self._debug_val('v', 'i', vvindex, vindex)
        self._debug_print(f"{'-'*30}")
        
        np_memory = np_memory.view(self.SEW.udtype)
        for i in range(self.VL):
            if mask[i]:
                ptr = (vvindex[i] + np_memory_offset) * 8 // self.SEW.SEW
                np_memory[ptr] = vvd[i]
        
    def vloxei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxei(8, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vloxei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxei(16, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vloxei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxei(32, vd, vindex, np_memory, np_memory_offset, masked)
        
    def vloxei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxei(64, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vluxei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print("Warning: vluxei8_v is not implemented yet, defaulting to vloxei8_v")
        self.__vloxei(8, vd, vindex, np_memory, np_memory_offset, masked)
        
    def vluxei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print("Warning: vluxei16_v is not implemented yet, defaulting to vloxei16_v")
        self.__vloxei(16, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vluxei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print("Warning: vluxei32_v is not implemented yet, defaulting to vloxei32_v")
        self.__vloxei(32, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vluxei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print("Warning: vluxei64_v is not implemented yet, defaulting to vloxei64_v")
        self.__vloxei(64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxei(8, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vsoxei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxei(16, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vsoxei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxei(32, vd, vindex, np_memory, np_memory_offset, masked)
        
    def vsoxei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxei(64, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vsuxei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print("Warning: vsuxei8_v is not implemented yet, defaulting to vsoxei8_v")
        self.__vsoxei(8, vd, vindex, np_memory, np_memory_offset, masked)
        
    def vsuxei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print("Warning: vsuxei16_v is not implemented yet, defaulting to vsoxei16_v")
        self.__vsoxei(16, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vsuxei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print("Warning: vsuxei32_v is not implemented yet, defaulting to vsoxei32_v")
        self.__vsoxei(32, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vsuxei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print("Warning: vsuxei64_v is not implemented yet, defaulting to vsoxei64_v")
        self.__vsoxei(64, vd, vindex, np_memory, np_memory_offset, masked)