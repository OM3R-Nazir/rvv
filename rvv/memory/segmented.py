from rvv.base import BaseRVV
import numpy as np

class Segmented(BaseRVV):

    def __seg_check(self, seg, vd):
        if (self.LMUL * seg > 8):
            raise ValueError(f"Invalid LMUL ({self.LMUL}) for Seg {seg}!")
        
        if (vd > 32 - seg * self.LMUL):
            raise ValueError(f"Invalid Vd ({vd}) for Seg {seg} x LMUL {self.LMUL}!")
    
    def __get_vindex(self, vi, sew):
        start = vi * self.VLENB
        end = start + self.VL * sew // 8
        return self.VRF[start:end].view(f"uint{sew}")
    
    def __debug_vds(self, seg, vd):
        for i in range(seg):
            _vd = vd + i
            vvd = self.vec(_vd)
            self._debug_val('v', 'd', vvd, _vd)
    
    def __debug_pre(self, seg, vd, mask, masked):
        self.__debug_vds(seg, vd)
        self._debug_mask(mask, masked)
        self._debug_print(f"{'-'*30}")
    
    def __debug_pre_indexed(self, seg, vd, vindex, vvindex, mask, masked):
        self.__debug_vds(seg, vd)
        self._debug_val('v', 'i', vvindex, vindex)
        self._debug_mask(mask, masked)
        self._debug_print(f"{'-'*30}")

    def __vlseg(self, seg, sew, vd, np_memory, np_memory_offset, masked):
        self._debug_operation()
        self.__seg_check(seg, vd)
            
        dtype = f"uint{sew}"
        sew_bytes = sew // 8

        np_memory = np_memory.view(dtype)
        np_memory_offset = np_memory_offset // sew_bytes
        
        min_memory_size = np_memory_offset + self.VL * seg
        
        if min_memory_size > np_memory.size:
            raise ValueError("Size of np_memory is too small")
        
        vector = np.zeros(self.VL * seg, dtype)
        vector = np_memory[np_memory_offset:np_memory_offset + self.VL * seg]
                
        mask = self._get_mask([vd], masked)
        
        self.__debug_pre(seg, vd, mask, masked)

        for i in range(seg):
            _vd = vd + i
            vvd = self.vec(_vd)
            vvd[mask] = vector[i::seg][mask]
        
        self.__debug_vds(seg, vd)

    def __vsseg(self, seg, sew, vd, np_memory, np_memory_offset, masked):
        self._debug_operation()
        self.__seg_check(seg, vd)
            
        dtype = f"uint{sew}"
        sew_bytes = sew // 8

        np_memory = np_memory.view(dtype)
        np_memory_offset = np_memory_offset // sew_bytes
        
        min_memory_size = np_memory_offset + self.VL * seg
        
        if min_memory_size > np_memory.size:
            raise ValueError("Size of np_memory is too small")
        
        mask = self._get_mask([vd], masked).repeat(seg)
        vector = np.zeros(self.VL * seg, dtype)
        
        self.__debug_pre(seg, vd, mask, masked)
            
        self._debug_mask(mask, masked)
        self._debug_print(f"{'-'*30}")

        for i in range(seg):
            _vd = vd + i
            vvd = self.vec(_vd)
            vector[i::2] = vvd

        np_memory[np_memory_offset:np_memory_offset + self.VL * seg][mask] = vector[mask]
    
    
    def __vlsseg(self, seg, sew, vd, np_memory, np_memory_offset, bstride, masked):
        self._debug_operation()
        self.__seg_check(seg, vd)
            
        dtype = f"uint{sew}"
        sew_bytes = sew // 8
        
        if bstride % sew_bytes != 0:
            raise ValueError(f"Stride in bytes ({bstride} B) is not SEW byte({sew} b = {sew_bytes} B) aligned!")

        
        np_memory = np_memory.view(np.uint8)
        
        min_memory_size = np_memory_offset + seg * sew_bytes + ((self.VL - 1) * bstride)        
        if min_memory_size > np_memory.size:
            raise ValueError("Size of np_memory is too small")
        
        mask = self._get_mask([vd], masked)
        
        self.__debug_pre(seg, vd, mask, masked)
        
        vector = np.zeros(self.VL * seg, dtype)
        for i in range(self.VL):
            offset = bstride * i + np_memory_offset
            segment = np_memory[offset:offset + seg*sew_bytes].view(dtype)
            vector[i*seg:(i+1)*seg] = segment
        
        for i in range(seg):
            _vd = vd + i
            vvd = self.vec(_vd)
            vvd[mask] = vector[i::seg][mask]
                
        self.__debug_vds(seg, vd)
    
    def __vssseg(self, seg, sew, vd, np_memory, np_memory_offset, bstride, masked):
        self._debug_operation()
        self.__seg_check(seg, vd)
            
        dtype = f"uint{sew}"
        sew_bytes = sew // 8
        
        if bstride % sew_bytes != 0:
            raise ValueError(f"Stride in bytes ({bstride} B) is not SEW byte({sew} b = {sew_bytes} B) aligned!")

        
        np_memory = np_memory.view(np.uint8)
        
        min_memory_size = np_memory_offset + seg * sew_bytes + ((self.VL - 1) * bstride)        
        if min_memory_size > np_memory.size:
            raise ValueError("Size of np_memory is too small")
        
        mask = self._get_mask([vd], masked)
        vector = np.zeros(self.VL * seg, dtype)
        
        self.__debug_pre(seg, vd, mask, masked)
        
        for i in range(seg):
            _vd = vd + i
            vvd = self.vec(_vd)
            vector[i::2] = vvd

        for i in range(self.VL):
            if not mask[i]: continue
            offset = bstride * i + np_memory_offset
            np_memory[offset:offset + seg*sew_bytes] = vector[i*seg:(i+1)*seg].view(np.uint8)
    
    
    def __vloxseg(self, seg, isew, vd, vindex, np_memory, np_memory_offset, masked):
        self._debug_operation()
        
        mask = self._get_mask([vd, vindex], masked)
        vvindex = self.__get_vindex(vindex, isew)
        
        self.__debug_pre_indexed(seg, vd, vindex, vvindex, mask, masked)
        
        sew_bytes = self.SEWC.SEW // 8
        vector = np.zeros(self.VL * seg, self.SEWC.udtype)
        np_memory = np_memory.view(np.uint8)
        
        for i in range(self.VL):
            ptr = vvindex[i] + np_memory_offset
            vector[i * seg:(i + 1) * seg] = np_memory[ptr:ptr + sew_bytes*seg].view(self.SEWC.udtype)
            
        for i in range(seg):
            _vd = vd + i
            vvd = self.vec(_vd)
            vvd[mask] = vector[i::seg][mask]
        
        self.__debug_vds(seg, vd)
    
    def __vsoxseg(self, seg, isew, vd, vindex, np_memory, np_memory_offset, masked):
        self._debug_operation()
        
        mask = self._get_mask([vd, vindex], masked)
        vvindex = self.__get_vindex(vindex, isew)
        
        self.__debug_pre_indexed(seg, vd, vindex, vvindex, mask, masked)
        
        sew_bytes = self.SEWC.SEW // 8
        vector = np.zeros(self.VL * seg, self.SEWC.udtype)
        np_memory = np_memory.view(np.uint8)
        
        for i in range(seg):
            _vd = vd + i
            vvd = self.vec(_vd)
            vector[i::seg] = vvd
            
        for i in range(self.VL):
            if not mask[i]: continue
            ptr = vvindex[i] + np_memory_offset
            np_memory[ptr:ptr + sew_bytes*seg] = vector[i * seg:(i + 1) * seg].view(np.uint8)


    ######################################
    ######################################
    
    # VLSEG
    
    ######################################
    ######################################
    
    def vlseg2e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(2, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg2e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(2, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg2e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(2, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg2e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(2, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg3e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(3, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg3e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(3, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg3e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(3, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg3e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(3, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg4e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(4, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg4e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(4, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg4e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(4, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg4e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(4, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg5e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(5, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg5e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(5, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg5e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(5, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg5e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(5, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg6e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(6, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg6e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(6, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg6e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(6, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg6e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(6, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg7e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(7, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg7e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(7, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg7e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(7, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg7e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(7, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg8e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(8, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg8e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(8, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg8e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(8, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg8e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vlseg(8, 64, vd, np_memory, np_memory_offset, masked)


    ######################################
    ######################################
    
    # VSSEG
    
    ######################################
    ######################################
    
    def vsseg2e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(2, 8, vd, np_memory, np_memory_offset, masked)

    def vsseg2e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(2, 16, vd, np_memory, np_memory_offset, masked)

    def vsseg2e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(2, 32, vd, np_memory, np_memory_offset, masked)

    def vsseg2e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(2, 64, vd, np_memory, np_memory_offset, masked)

    def vsseg3e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(3, 8, vd, np_memory, np_memory_offset, masked)

    def vsseg3e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(3, 16, vd, np_memory, np_memory_offset, masked)

    def vsseg3e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(3, 32, vd, np_memory, np_memory_offset, masked)

    def vsseg3e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(3, 64, vd, np_memory, np_memory_offset, masked)

    def vsseg4e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(4, 8, vd, np_memory, np_memory_offset, masked)

    def vsseg4e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(4, 16, vd, np_memory, np_memory_offset, masked)

    def vsseg4e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(4, 32, vd, np_memory, np_memory_offset, masked)

    def vsseg4e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(4, 64, vd, np_memory, np_memory_offset, masked)

    def vsseg5e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(5, 8, vd, np_memory, np_memory_offset, masked)

    def vsseg5e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(5, 16, vd, np_memory, np_memory_offset, masked)

    def vsseg5e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(5, 32, vd, np_memory, np_memory_offset, masked)

    def vsseg5e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(5, 64, vd, np_memory, np_memory_offset, masked)

    def vsseg6e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(6, 8, vd, np_memory, np_memory_offset, masked)

    def vsseg6e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(6, 16, vd, np_memory, np_memory_offset, masked)

    def vsseg6e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(6, 32, vd, np_memory, np_memory_offset, masked)

    def vsseg6e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(6, 64, vd, np_memory, np_memory_offset, masked)

    def vsseg7e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(7, 8, vd, np_memory, np_memory_offset, masked)

    def vsseg7e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(7, 16, vd, np_memory, np_memory_offset, masked)

    def vsseg7e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(7, 32, vd, np_memory, np_memory_offset, masked)

    def vsseg7e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(7, 64, vd, np_memory, np_memory_offset, masked)

    def vsseg8e8_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(8, 8, vd, np_memory, np_memory_offset, masked)

    def vsseg8e16_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(8, 16, vd, np_memory, np_memory_offset, masked)

    def vsseg8e32_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(8, 32, vd, np_memory, np_memory_offset, masked)

    def vsseg8e64_v(self, vd, np_memory, np_memory_offset, masked=False):
        self.__vsseg(8, 64, vd, np_memory, np_memory_offset, masked)


    ######################################
    ######################################
    
    # VLSEG_FF
    
    ######################################
    ######################################

    def vlseg2e8ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg2e8ff_v is not implemented yet, defaulting to vlseg2e8_v")
        self.__vlseg(2, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg2e16ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg2e16ff_v is not implemented yet, defaulting to vlseg2e16_v")
        self.__vlseg(2, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg2e32ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg2e32ff_v is not implemented yet, defaulting to vlseg2e32_v")
        self.__vlseg(2, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg2e64ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg2e64ff_v is not implemented yet, defaulting to vlseg2e64_v")
        self.__vlseg(2, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg3e8ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg3e8ff_v is not implemented yet, defaulting to vlseg3e8_v")
        self.__vlseg(3, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg3e16ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg3e16ff_v is not implemented yet, defaulting to vlseg3e16_v")
        self.__vlseg(3, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg3e32ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg3e32ff_v is not implemented yet, defaulting to vlseg3e32_v")
        self.__vlseg(3, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg3e64ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg3e64ff_v is not implemented yet, defaulting to vlseg3e64_v")
        self.__vlseg(3, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg4e8ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg4e8ff_v is not implemented yet, defaulting to vlseg4e8_v")
        self.__vlseg(4, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg4e16ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg4e16ff_v is not implemented yet, defaulting to vlseg4e16_v")
        self.__vlseg(4, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg4e32ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg4e32ff_v is not implemented yet, defaulting to vlseg4e32_v")
        self.__vlseg(4, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg4e64ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg4e64ff_v is not implemented yet, defaulting to vlseg4e64_v")
        self.__vlseg(4, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg5e8ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg5e8ff_v is not implemented yet, defaulting to vlseg5e8_v")
        self.__vlseg(5, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg5e16ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg5e16ff_v is not implemented yet, defaulting to vlseg5e16_v")
        self.__vlseg(5, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg5e32ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg5e32ff_v is not implemented yet, defaulting to vlseg5e32_v")
        self.__vlseg(5, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg5e64ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg5e64ff_v is not implemented yet, defaulting to vlseg5e64_v")
        self.__vlseg(5, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg6e8ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg6e8ff_v is not implemented yet, defaulting to vlseg6e8_v")
        self.__vlseg(6, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg6e16ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg6e16ff_v is not implemented yet, defaulting to vlseg6e16_v")
        self.__vlseg(6, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg6e32ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg6e32ff_v is not implemented yet, defaulting to vlseg6e32_v")
        self.__vlseg(6, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg6e64ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg6e64ff_v is not implemented yet, defaulting to vlseg6e64_v")
        self.__vlseg(6, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg7e8ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg7e8ff_v is not implemented yet, defaulting to vlseg7e8_v")
        self.__vlseg(7, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg7e16ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg7e16ff_v is not implemented yet, defaulting to vlseg7e16_v")
        self.__vlseg(7, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg7e32ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg7e32ff_v is not implemented yet, defaulting to vlseg7e32_v")
        self.__vlseg(7, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg7e64ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg7e64ff_v is not implemented yet, defaulting to vlseg7e64_v")
        self.__vlseg(7, 64, vd, np_memory, np_memory_offset, masked)

    def vlseg8e8ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg8e8ff_v is not implemented yet, defaulting to vlseg8e8_v")
        self.__vlseg(8, 8, vd, np_memory, np_memory_offset, masked)

    def vlseg8e16ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg8e16ff_v is not implemented yet, defaulting to vlseg8e16_v")
        self.__vlseg(8, 16, vd, np_memory, np_memory_offset, masked)

    def vlseg8e32ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg8e32ff_v is not implemented yet, defaulting to vlseg8e32_v")
        self.__vlseg(8, 32, vd, np_memory, np_memory_offset, masked)

    def vlseg8e64ff_v(self, vd, np_memory, np_memory_offset, masked = False):
        self._debug_print(f"Warning: vlseg8e64ff_v is not implemented yet, defaulting to vlseg8e64_v")
        self.__vlseg(8, 64, vd, np_memory, np_memory_offset, masked)


    ######################################
    ######################################
    
    # VLSSEG
    
    ######################################
    ######################################
    
    def vlsseg2e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(2, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg2e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(2, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg2e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(2, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg2e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(2, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg3e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(3, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg3e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(3, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg3e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(3, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg3e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(3, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg4e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(4, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg4e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(4, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg4e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(4, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg4e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(4, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg5e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(5, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg5e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(5, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg5e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(5, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg5e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(5, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg6e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(6, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg6e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(6, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg6e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(6, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg6e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(6, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg7e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(7, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg7e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(7, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg7e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(7, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg7e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(7, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg8e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(8, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg8e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(8, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg8e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(8, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vlsseg8e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vlsseg(8, 64, vd, np_memory, np_memory_offset, bstride, masked)


    ######################################
    ######################################
    
    # VSSSEG
    
    ######################################
    ######################################
    
    def vssseg2e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(2, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg2e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(2, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg2e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(2, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg2e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(2, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg3e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(3, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg3e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(3, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg3e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(3, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg3e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(3, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg4e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(4, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg4e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(4, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg4e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(4, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg4e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(4, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg5e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(5, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg5e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(5, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg5e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(5, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg5e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(5, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg6e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(6, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg6e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(6, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg6e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(6, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg6e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(6, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg7e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(7, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg7e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(7, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg7e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(7, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg7e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(7, 64, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg8e8_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(8, 8, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg8e16_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(8, 16, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg8e32_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(8, 32, vd, np_memory, np_memory_offset, bstride, masked)

    def vssseg8e64_v(self, vd, np_memory, np_memory_offset, bstride, masked=False):
        self.__vssseg(8, 64, vd, np_memory, np_memory_offset, bstride, masked)


    ######################################
    ######################################
    
    # VLOXSEGEI
    
    ######################################
    ######################################
    
    def vloxseg2ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(2, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg2ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(2, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg2ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(2, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg2ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(2, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg3ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(3, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg3ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(3, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg3ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(3, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg3ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(3, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg4ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(4, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg4ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(4, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg4ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(4, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg4ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(4, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg5ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(5, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg5ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(5, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg5ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(5, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg5ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(5, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg6ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(6, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg6ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(6, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg6ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(6, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg6ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(6, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg7ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(7, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg7ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(7, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg7ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(7, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg7ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(7, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg8ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(8, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg8ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(8, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg8ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(8, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vloxseg8ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vloxseg(8, 64, vd, vindex, np_memory, np_memory_offset, masked)


    ######################################
    ######################################
    
    # VSOXSEG
    
    ######################################
    ######################################
    
    def vsoxseg2ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(2, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg2ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(2, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg2ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(2, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg2ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(2, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg3ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(3, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg3ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(3, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg3ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(3, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg3ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(3, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg4ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(4, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg4ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(4, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg4ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(4, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg4ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(4, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg5ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(5, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg5ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(5, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg5ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(5, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg5ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(5, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg6ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(6, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg6ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(6, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg6ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(6, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg6ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(6, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg7ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(7, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg7ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(7, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg7ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(7, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg7ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(7, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg8ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(8, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg8ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(8, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg8ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(8, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsoxseg8ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self.__vsoxseg(8, 64, vd, vindex, np_memory, np_memory_offset, masked)

    ######################################
    ######################################
    
    # VLUXSEGEI
    
    ######################################
    ######################################

    def vluxseg2ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg2ei8_v is not implemented yet, defaulting to vloxseg2ei8_v")
        self.__vloxseg(2, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg2ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg2ei16_v is not implemented yet, defaulting to vloxseg2ei16_v")
        self.__vloxseg(2, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg2ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg2ei32_v is not implemented yet, defaulting to vloxseg2ei32_v")
        self.__vloxseg(2, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg2ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg2ei64_v is not implemented yet, defaulting to vloxseg2ei64_v")
        self.__vloxseg(2, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg3ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg3ei8_v is not implemented yet, defaulting to vloxseg3ei8_v")
        self.__vloxseg(3, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg3ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg3ei16_v is not implemented yet, defaulting to vloxseg3ei16_v")
        self.__vloxseg(3, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg3ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg3ei32_v is not implemented yet, defaulting to vloxseg3ei32_v")
        self.__vloxseg(3, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg3ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg3ei64_v is not implemented yet, defaulting to vloxseg3ei64_v")
        self.__vloxseg(3, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg4ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg4ei8_v is not implemented yet, defaulting to vloxseg4ei8_v")
        self.__vloxseg(4, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg4ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg4ei16_v is not implemented yet, defaulting to vloxseg4ei16_v")
        self.__vloxseg(4, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg4ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg4ei32_v is not implemented yet, defaulting to vloxseg4ei32_v")
        self.__vloxseg(4, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg4ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg4ei64_v is not implemented yet, defaulting to vloxseg4ei64_v")
        self.__vloxseg(4, 64, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vluxseg4ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg4ei8_v is not implemented yet, defaulting to vloxseg4ei8_v")
        self.__vloxseg(4, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg4ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg4ei16_v is not implemented yet, defaulting to vloxseg4ei16_v")
        self.__vloxseg(4, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg4ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg4ei32_v is not implemented yet, defaulting to vloxseg4ei32_v")
        self.__vloxseg(4, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg4ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg4ei64_v is not implemented yet, defaulting to vloxseg4ei64_v")
        self.__vloxseg(4, 64, vd, vindex, np_memory, np_memory_offset, masked)
        
    def vluxseg5ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg5ei8_v is not implemented yet, defaulting to vloxseg5ei8_v")
        self.__vloxseg(5, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg5ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg5ei16_v is not implemented yet, defaulting to vloxseg5ei16_v")
        self.__vloxseg(5, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg5ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg5ei32_v is not implemented yet, defaulting to vloxseg5ei32_v")
        self.__vloxseg(5, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg5ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg5ei64_v is not implemented yet, defaulting to vloxseg5ei64_v")
        self.__vloxseg(5, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg6ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg6ei8_v is not implemented yet, defaulting to vloxseg6ei8_v")
        self.__vloxseg(6, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg6ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg6ei16_v is not implemented yet, defaulting to vloxseg6ei16_v")
        self.__vloxseg(6, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg6ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg6ei32_v is not implemented yet, defaulting to vloxseg6ei32_v")
        self.__vloxseg(6, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg6ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg6ei64_v is not implemented yet, defaulting to vloxseg6ei64_v")
        self.__vloxseg(6, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg7ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg7ei8_v is not implemented yet, defaulting to vloxseg7ei8_v")
        self.__vloxseg(7, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg7ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg7ei16_v is not implemented yet, defaulting to vloxseg7ei16_v")
        self.__vloxseg(7, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg7ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg7ei32_v is not implemented yet, defaulting to vloxseg7ei32_v")
        self.__vloxseg(7, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg7ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg7ei64_v is not implemented yet, defaulting to vloxseg7ei64_v")
        self.__vloxseg(7, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg8ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg8ei8_v is not implemented yet, defaulting to vloxseg8ei8_v")
        self.__vloxseg(8, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg8ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg8ei16_v is not implemented yet, defaulting to vloxseg8ei16_v")
        self.__vloxseg(8, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg8ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg8ei32_v is not implemented yet, defaulting to vloxseg8ei32_v")
        self.__vloxseg(8, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vluxseg8ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vluxseg8ei64_v is not implemented yet, defaulting to vloxseg8ei64_v")
        self.__vloxseg(8, 64, vd, vindex, np_memory, np_memory_offset, masked)

    ######################################
    ######################################
    
    # VSUXSEGEI
    
    ######################################
    ######################################

    def vsuxseg2ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg2ei8_v is not implemented yet, defaulting to vsoxseg2ei8_v")
        self.__vsoxseg(2, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg2ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg2ei16_v is not implemented yet, defaulting to vsoxseg2ei16_v")
        self.__vsoxseg(2, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg2ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg2ei32_v is not implemented yet, defaulting to vsoxseg2ei32_v")
        self.__vsoxseg(2, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg2ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg2ei64_v is not implemented yet, defaulting to vsoxseg2ei64_v")
        self.__vsoxseg(2, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg3ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg3ei8_v is not implemented yet, defaulting to vsoxseg3ei8_v")
        self.__vsoxseg(3, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg3ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg3ei16_v is not implemented yet, defaulting to vsoxseg3ei16_v")
        self.__vsoxseg(3, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg3ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg3ei32_v is not implemented yet, defaulting to vsoxseg3ei32_v")
        self.__vsoxseg(3, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg3ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg3ei64_v is not implemented yet, defaulting to vsoxseg3ei64_v")
        self.__vsoxseg(3, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg4ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg4ei8_v is not implemented yet, defaulting to vsoxseg4ei8_v")
        self.__vsoxseg(4, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg4ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg4ei16_v is not implemented yet, defaulting to vsoxseg4ei16_v")
        self.__vsoxseg(4, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg4ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg4ei32_v is not implemented yet, defaulting to vsoxseg4ei32_v")
        self.__vsoxseg(4, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg4ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg4ei64_v is not implemented yet, defaulting to vsoxseg4ei64_v")
        self.__vsoxseg(4, 64, vd, vindex, np_memory, np_memory_offset, masked)
    
    def vsuxseg4ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg4ei8_v is not implemented yet, defaulting to vsoxseg4ei8_v")
        self.__vsoxseg(4, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg4ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg4ei16_v is not implemented yet, defaulting to vsoxseg4ei16_v")
        self.__vsoxseg(4, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg4ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg4ei32_v is not implemented yet, defaulting to vsoxseg4ei32_v")
        self.__vsoxseg(4, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg4ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg4ei64_v is not implemented yet, defaulting to vsoxseg4ei64_v")
        self.__vsoxseg(4, 64, vd, vindex, np_memory, np_memory_offset, masked)
        
    def vsuxseg5ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg5ei8_v is not implemented yet, defaulting to vsoxseg5ei8_v")
        self.__vsoxseg(5, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg5ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg5ei16_v is not implemented yet, defaulting to vsoxseg5ei16_v")
        self.__vsoxseg(5, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg5ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg5ei32_v is not implemented yet, defaulting to vsoxseg5ei32_v")
        self.__vsoxseg(5, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg5ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg5ei64_v is not implemented yet, defaulting to vsoxseg5ei64_v")
        self.__vsoxseg(5, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg6ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg6ei8_v is not implemented yet, defaulting to vsoxseg6ei8_v")
        self.__vsoxseg(6, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg6ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg6ei16_v is not implemented yet, defaulting to vsoxseg6ei16_v")
        self.__vsoxseg(6, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg6ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg6ei32_v is not implemented yet, defaulting to vsoxseg6ei32_v")
        self.__vsoxseg(6, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg6ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg6ei64_v is not implemented yet, defaulting to vsoxseg6ei64_v")
        self.__vsoxseg(6, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg7ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg7ei8_v is not implemented yet, defaulting to vsoxseg7ei8_v")
        self.__vsoxseg(7, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg7ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg7ei16_v is not implemented yet, defaulting to vsoxseg7ei16_v")
        self.__vsoxseg(7, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg7ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg7ei32_v is not implemented yet, defaulting to vsoxseg7ei32_v")
        self.__vsoxseg(7, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg7ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg7ei64_v is not implemented yet, defaulting to vsoxseg7ei64_v")
        self.__vsoxseg(7, 64, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg8ei8_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg8ei8_v is not implemented yet, defaulting to vsoxseg8ei8_v")
        self.__vsoxseg(8, 8, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg8ei16_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg8ei16_v is not implemented yet, defaulting to vsoxseg8ei16_v")
        self.__vsoxseg(8, 16, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg8ei32_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg8ei32_v is not implemented yet, defaulting to vsoxseg8ei32_v")
        self.__vsoxseg(8, 32, vd, vindex, np_memory, np_memory_offset, masked)

    def vsuxseg8ei64_v(self, vd, vindex, np_memory, np_memory_offset, masked=False):
        self._debug_print(f"Warning: vsuxseg8ei64_v is not implemented yet, defaulting to vsoxseg8ei64_v")
        self.__vsoxseg(8, 64, vd, vindex, np_memory, np_memory_offset, masked)
