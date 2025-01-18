import numpy as np
from rvv.utils.sew import SEWC

class BaseRVV:
    
    def __init__(self, VLEN: int = 2048, debug = False) -> None:
        self.VLEN : int = VLEN
        self.VLENB : int = VLEN // 8
        self.VRF : np.ndarray = np.zeros(self.VLENB * 32, dtype=np.uint8)
        self.SEW : SEWC = None
        self.WSEW : SEWC = None
        self.LMUL : int = None
        self.VL : int = None
        self.VLMAX : int = None
        
        self._valid_sews : list[int] = [8, 16, 32, 64]
        self._valid_lmuls : list[int] = [1, 2, 4, 8]
        
        self._init_vec_regs()
        self.debug = debug
        
    def _init_vec_regs(self):
        self.vsetvli(0, 8, 1)
        
        for i in range(32):
            v = self.vec(i)
            for k in range(self.VL):
                v[k] = k
    
    def _initer(self, optype, op, signed):
        if optype == 'v': return self.vec(op, signed)
        elif optype == 'w': return self.vecw(op, signed)
        elif optype == 'x': return self.scalar(op, signed)
        elif optype == 'm': return self.vecm(op)
        
    def _init_ops(self, vd, op1, op2, optypes, signed, masked):
        
        if type(signed) == bool: signed = 'sss' if signed else 'uuu'    
            
        tvd = self._initer(optypes[0], vd, signed[0])
        top1 = self._initer(optypes[1], op1, signed[1])
        top2 = self._initer(optypes[2], op2, signed[2])
        
        ops = [vd, op1, op2]
        vector_ops = [ops[i] for i in range(3) if optypes[i] != 'x']
        
        if masked:
            if 0 in vector_ops:
                raise ValueError("Invalid Vector Register Number 0 for Masked Operation")
            mask = self.mask_to_bools(self.vecm(0))
        else:
            mask = np.ones(self.VL, dtype=np.bool_)
        
        if self.debug:
            self._debug_val(top1, 1, optypes[1], 'op1')
            self._debug_val(top2, 2, optypes[2], 'op2')
            if masked:
                print(f'{"mask":<10}',mask)
        return tvd, top1, top2, mask
        
    def _debug_val(self, val, val_num, val_type, op_type):
        if self.debug:
            if val_type == 'x':
                print(f"{val_type + op_type:>5}   {val_num:02}: ", val)
            elif val_type == 'm':
                val_type = 'vm'
                print(f"{val_type + op_type:>5} {val_type:>2}{val_num:02}: ", self.mask_to_bools(val).view(np.uint8))
            else:
                print(f"{val_type + op_type:>5} {val_type:>2}{val_num:02}: ", val)

    def _debug_vd(self, vec, vec_num, mask_debug=False):
        if self.debug:
            if mask_debug:
                self._debug_val(vec, vec_num, 'm', 'd')
            else:
                self._debug_val(vec, vec_num, 'v', 'd')
    
    def _iclip(self, num):
        return np.clip(num, self.SEW.imin, self.SEW.imax)    
    
    def _uclip(self, num):
        return np.clip(num, self.SEW.umin, self.SEW.umax)    
    
    def _sext(self, num):
        return self.WSEW.idtype(self.SEW.idtype(num))
    
    def _zext(self, num):
        return self.WSEW.udtype(self.SEW.udtype(num)) 

    def bools_to_mask(self, bool_array):
        if len(bool_array) != self.VL:
            raise ValueError(f"Invalid Length of Mask {len(bool_array)} for VL {self.VL}")
        
        if len(bool_array) % 8 != 0:
            bool_array = np.pad(bool_array, (0, 8 - len(bool_array) % 8))
            
        reversed_bool_array = np.zeros_like(bool_array)
        for i in range(0, len(bool_array), 8):
            for j in range(8):
                reversed_bool_array[i+j] = bool_array[i+7-j]
                
        mask = np.packbits(reversed_bool_array).view(np.uint8)
        return mask
        
    def mask_to_bools(self, mask):
        mask = mask.view(np.uint8)
        
        reversed_bool_array = np.unpackbits(mask)
        bool_array = np.zeros_like(reversed_bool_array)
        for i in range(0, len(reversed_bool_array), 8):
            for j in range(8):
                bool_array[i+j] = reversed_bool_array[i+7-j]

        bool_array = bool_array[:self.VL].view(np.bool_)
        
        return bool_array
    
    def vec(self, vi, signed=False):
        
        if vi % self.LMUL != 0:
            raise ValueError(f"Invalid Vector Register Number {vi} for LMUL {self.LMUL}")
        
        if type(signed) == str:
            signed = True if signed == 's' else False
        
        start = vi * self.VLENB
        end = start + self.VL * self.SEW.SEW // 8
        
        viewtype = self.SEW.idtype if signed else self.SEW.udtype
        
        return self.VRF[start:end].view(viewtype)
    
    def vecw(self, vi, signed=False):
        LMUL = self.LMUL + 1
        SEW = self.SEW.get_higher_sew()

        if vi % LMUL != 0:
            raise ValueError(f"Invalid Vector Register Number {vi} for LMUL {LMUL}")
        
        if type(signed) == str:
            signed = True if signed == 's' else False
            
        start = vi * self.VLENB
        end = start + self.VL * SEW.SEW // 8
        
        viewtype = SEW.idtype if signed else SEW.udtype
        
        return self.VRF[start:end].view(viewtype)
    
    def vecm(self, vi):
        start = vi * self.VLENB
        end = start + int(np.ceil(self.VL / 8))
        return self.VRF[start:end].view(np.uint8)
    
    def scalar(self, xi, signed=False):
        viewtype = self.SEW.idtype if signed else self.SEW.udtype
        return viewtype(xi)
    
    def vsetvli(self, AVL, SEW, LMUL) -> None:
        
        if SEW not in self._valid_sews:
            raise ValueError(f"Invalid SEW value {SEW}")
        if LMUL not in self._valid_lmuls:
            raise ValueError(f"Invaid LMUL value {LMUL}")
        
        self.SEW = SEWC(SEW)
        self.LMUL = LMUL
        self.VLMAX = self.VLEN * self.LMUL // self.SEW.SEW
        
        if AVL == 0: AVL = self.VLMAX
        self.VL = min([self.VLMAX, AVL]) 
          
        return self.VL
    
    def vle(self, vd, inp : np.ndarray):
        vvd = self.vec(vd)
        vvd[:] = np.array(inp).view(self.SEW.udtype)

    def vse(self, vd, out : np.ndarray):
        vvd = self.vec(vd)
        out[:vvd.size] = vvd
    
    def vlm(self, vd, inp : np.ndarray):
        vvd = self.vecm(vd)
        vvd[:] = np.array(inp).view(np.uint8)[:int(np.ceil(self.VL/8))]

    def vsm(self, vd, out : np.ndarray):
        vvd = self.vecm(vd)
        out[:vvd.size] = vvd[:]

    @property
    def WSEW(self):
        return self.SEW.get_higher_sew()
    
    @WSEW.setter
    def WSEW(self, sew):
        pass

    @property
    def NSEW(self):
        return self.SEW.get_lower_sew()
    
    @NSEW.setter
    def NSEW(self, sew):
        pass
    