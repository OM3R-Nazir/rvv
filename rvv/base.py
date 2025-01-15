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
            mask = self._get_mask()
        else:
            mask = np.ones(self.VL, dtype=np.bool_)
        
        if self.debug:
            if optypes[1] == 'x':
                print(f"xop1    : ", top1)
            else:
                print(f"vop1 v{op1:02}: ", top1)
            if optypes[2] == 'x':
                print(f"xop2    : ", top1)
            else:
                print(f"vop2 v{op1:02}: ", top2)
            if masked:
                print(f"mask    : ", mask.view(np.uint8))
        
        return tvd, top1, top2, mask
        
    def _debug_vd(self, vec, vec_num):
        if self.debug:
            print(f"vd   v{vec_num:02}: ", vec)
    
    def _iclip(self, num):
        return np.clip(num, self.SEW.imin, self.SEW.imax)    
    
    def _uclip(self, num):
        return np.clip(num, self.SEW.umin, self.SEW.umax)    
    
    def _sext(self, num):
        return self.WSEW.idtype(self.SEW.idtype(num))
    
    def _zext(self, num):
        return self.WSEW.udtype(self.SEW.udtype(num)) 
    
    def _get_mask(self):
        v0 = self.VRF[:self.VLENB].view(np.uint8)
        reverse_mask = v0 % 255 == 0
        v0[reverse_mask] = v0[reverse_mask] - 255
        mask = np.unpackbits(v0)[:self.VL].view(np.bool_)
        return mask

    
    def vec(self, vi, signed=False):
        
        if vi % self.LMUL != 0:
            raise ValueError(f"Invalid Vector Register Number {vi} for LMUL {self.LMUL}")
        
        if type(signed) == str:
            signed = True if signed == 's' else False
        
        start = vi * self.VLENB
        end = vi * self.VLENB + self.VL * self.SEW.SEW // 8
        
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
        end = vi * self.VLENB + self.VL * SEW.SEW // 8
        
        viewtype = SEW.idtype if signed else SEW.udtype
        
        return self.VRF[start:end].view(viewtype)
    
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
    