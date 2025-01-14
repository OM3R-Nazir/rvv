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
    
    def _init_vv(self, vd, op1, op2):
        vvd = self.vec(vd)
        vop1 = self.vec(op1)
        vop2 = self.vec(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"vop2 v{op2:02}: ", vop2)
        
        return vvd, vop1, vop2
    
    def _init_vx(self, vd, op1, op2):
        vvd = self.vec(vd)
        vop1 = self.vec(op1)
        xop2 = self.sca(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", xop2)
        
        return vvd, vop1, xop2
    
    def _init_w_vv(self, vd, op1, op2):
        vvd = self.vecw(vd)
        vop1 = self.vec(op1)
        vop2 = self.vec(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", vop2)
    
        return vvd, vop1, vop2
    
    def _init_w_vx(self, vd, op1, op2):

        vvd = self.vecw(vd)
        vop1 = self.vec(op1)
        xop2 = self.sca(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", xop2)
    
        return vvd, vop1, xop2
    
    def _init_w_wv(self, vd, op1, op2):
        vvd = self.vecw(vd)
        vop1 = self.vecw(op1)
        vop2 = self.vec(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", vop2)
    
        return vvd, vop1, vop2
    
    def _init_w_wx(self, vd, op1, op2):

        vvd = self.vecw(vd)
        vop1 = self.vecw(op1)
        xop2 = self.sca(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", xop2)
    
        return vvd, vop1, xop2
        
    def _debug_vec(self, vec, vec_num):
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
    
    def vec(self, vi):
        
        if vi % self.LMUL != 0:
            raise ValueError(f"Invalid Vector Register Number {vi} for LMUL {self.LMUL}")
        
        start = vi * self.VLENB
        end = vi * self.VLENB + self.VL * self.SEW.SEW // 8
        
        return self.VRF[start:end].view(self.SEW.udtype)
    
    def vecw(self, vi):
        LMUL = self.LMUL + 1
        SEW = self.SEW.get_higher_sew()

        if vi % LMUL != 0:
            raise ValueError(f"Invalid Vector Register Number {vi} for LMUL {LMUL}")
        
        start = vi * self.VLENB
        end = vi * self.VLENB + self.VL * SEW.SEW // 8
        
        return self.VRF[start:end].view(SEW.udtype)
    
    def sca(self, xi):
        return self.SEW.udtype(xi)
    
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