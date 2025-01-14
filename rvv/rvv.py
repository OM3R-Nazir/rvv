# In Saturation Instructions, pythonic int type is being used. 
# Main reason being numpy does not support np.int128, so handling
# saturation for int64 type is not possible in pure numpy


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

    def get_lower_sew(self):
        if self.SEW == 8: raise ValueError("No SEW lower than 8")
        elif self.SEW == 16: return SEWC(8)
        elif self.SEW == 32: return SEWC(16)
        elif self.SEW == 64: return SEWC(32)
        
    def get_higher_sew(self):
        if self.SEW == 8: return SEWC(16)
        elif self.SEW == 16: return SEWC(32)
        elif self.SEW == 32: return SEWC(64)
        elif self.SEW == 64: raise ValueError("No SEW higher than 64")

class RVV:
    
    def __init__(self, VLEN: int = 2048, debug = False) -> None:
        self.VLEN : int = VLEN
        self.VLENB : int = VLEN // 8
        self.VRF : np.ndarray = np.zeros(self.VLENB * 32, dtype=np.uint8)
        self.SEW : SEWC = None
        self.WSEW : SEWC = None
        self.LMUL : int = None
        self.VL : int = None
        self.VLMAX : int = None
        
        self.__valid_sews : list[int] = [8, 16, 32, 64]
        self.__valid_lmuls : list[int] = [1, 2, 4, 8]
        
        self.__init_vec_regs()
        self.debug = debug
        
    def __init_vec_regs(self):
        self.vsetvli(0, 8, 1)
        
        for i in range(32):
            v = self.vec(i)
            for k in range(self.VL):
                v[k] = k
    
    def __init_vv(self, vd, op1, op2):
        vvd = self.vec(vd)
        vop1 = self.vec(op1)
        vop2 = self.vec(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"vop2 v{op2:02}: ", vop2)
        
        return vvd, vop1, vop2
    
    def __init_vx(self, vd, op1, op2):
        vvd = self.vec(vd)
        vop1 = self.vec(op1)
        xop2 = self.sca(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", xop2)
        
        return vvd, vop1, xop2
    
    def __init_w_vv(self, vd, op1, op2):
        vvd = self.vecw(vd)
        vop1 = self.vec(op1)
        vop2 = self.vec(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", vop2)
    
        return vvd, vop1, vop2
    
    def __init_w_vx(self, vd, op1, op2):

        vvd = self.vecw(vd)
        vop1 = self.vec(op1)
        xop2 = self.sca(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", xop2)
    
        return vvd, vop1, xop2
    
    def __init_w_wv(self, vd, op1, op2):
        vvd = self.vecw(vd)
        vop1 = self.vecw(op1)
        vop2 = self.vec(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", vop2)
    
        return vvd, vop1, vop2
    
    def __init_w_wx(self, vd, op1, op2):

        vvd = self.vecw(vd)
        vop1 = self.vecw(op1)
        xop2 = self.sca(op2)
        
        if self.debug:
            print(f"vop1 v{op1:02}: ", vop1)
            print(f"xop2    : ", xop2)
    
        return vvd, vop1, xop2
        
    def __debug_vec(self, vec, vec_num):
        if self.debug:
            print(f"vd   v{vec_num:02}: ", vec)
    
    def __iclip(self, num):
        return np.clip(num, self.SEW.imin, self.SEW.imax)    
    
    def __uclip(self, num):
        return np.clip(num, self.SEW.umin, self.SEW.umax)    
    
    def __sext(self, num):
        return self.WSEW.idtype(self.SEW.idtype(num))
    
    def __zext(self, num):
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
        
        if SEW not in self.__valid_sews:
            raise ValueError(f"Invalid SEW value {SEW}")
        if LMUL not in self.__valid_lmuls:
            raise ValueError(f"Invaid LMUL value {LMUL}")
        
        self.SEW = SEWC(SEW)
        self.WSEW = self.SEW.get_higher_sew()
        self.LMUL = LMUL
        self.VLMAX = self.VLEN * self.LMUL // self.SEW.SEW
        
        if AVL == 0: AVL = self.VLMAX
        self.VL = min([self.VLMAX, AVL]) 
          
        return self.VL
    
    def vle(self, vd, inp : np.ndarray):
        vvd = self.vec(vd)
        vvd[:] = np.array(inp).view(self.SEW.udtype)
        
    
    ######################################################################################
    #                                    Integer                                         #
    ######################################################################################
    
    ####
    ####  ADD
    ####    
    
    def vadd_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_vv(vd, op1, op2)
        vvd[:] = vop1[:] + vop2[:]
        self.__debug_vec(vvd, vd)
        
    def vadd_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_vx(vd, op1, op2)
        vvd[:] = vop1[:] + xop2
        self.__debug_vec(vvd, vd)
    
    def vsadd_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_vv(vd, op1, op2)

        for i in range(self.VL):
            vvd[i] = self.__iclip(int(vop1[i]) + int(vop2[i]))
            
        self.__debug_vec(vvd, vd)
    
    def vsadd_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_vx(vd, op1, op2)
        
        for i in range(self.VL):
            vvd[i] = self.__iclip(int(vop1[i]) + int(xop2))
        
        self.__debug_vec(vvd, vd)
    
    def vsaddu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_vv(vd, op1, op2)

        for i in range(self.VL):
            vvd[i] = self.__uclip(int(vop1[i]) + int(vop2[i]))
            
        self.__debug_vec(vvd, vd)
    
    def vsaddu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_vx(vd, op1, op2)
        
        for i in range(self.VL):
            vvd[i] = self.__uclip(int(vop1[i]) + int(xop2))
        
        self.__debug_vec(vvd, vd)
    
    def vwadd_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_w_vv(vd, op1, op2)
        vvd[:] = self.__sext(vop1) + self.__sext(vop2)
        self.__debug_vec(vvd, vd)
    
    def vwadd_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_w_vx(vd, op1, op2)
        vvd[:] = self.__sext(vop1) + self.__sext(xop2)
        self.__debug_vec(vvd, vd)
    
    def vwadd_wv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_w_wv(vd, op1, op2)
        vvd[:] = vop1 + self.__sext(vop2)
        self.__debug_vec(vvd, vd)
    
    def vwadd_wx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_w_wx(vd, op1, op2)
        vvd[:] = vop1 + self.__sext(xop2)
        self.__debug_vec(vvd, vd)        
    
    def vwaddu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_w_vv(vd, op1, op2)
        vvd[:] = self.__zext(vop1) + self.__zext(vop2)
        self.__debug_vec(vvd, vd)
    
    def vwaddu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_w_vx(vd, op1, op2)
        vvd[:] = self.__zext(vop1) + self.__zext(xop2)
        self.__debug_vec(vvd, vd)
    
    def vwaddu_wv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_w_wv(vd, op1, op2)
        vvd[:] = vop1 + self.__zext(vop2)
        self.__debug_vec(vvd, vd)
    
    def vwaddu_wx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_w_wx(vd, op1, op2)
        vvd[:] = vop1 + self.__zext(xop2)
        self.__debug_vec(vvd, vd)
                   
    ####
    ####  SUB
    ####    
    
    def vsub_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_vx(vd, op1, op2)
        vvd[:] = vop1[:] - vop2[:]
        self.__debug_vec(vvd, vd)
        
    def vsub_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_vx(vd, op1, op2)
        vvd[:] = vop1[:] - xop2
        self.__debug_vec(vvd, vd)    
    
    def vrsub_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_vx(vd, op1, op2)
        vvd[:] = xop2 - vop1[:]
        self.__debug_vec(vvd, vd)    

    def vssub_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_vv(vd, op1, op2)
        for i in range(self.VL):
            vvd[i] = self.__iclip(int(vop1[i]) - int(vop2[i]))
        self.__debug_vec(vvd, vd)

    def vssub_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_vx(vd, op1, op2)
        for i in range(self.VL):
            vvd[i] = self.__iclip(int(vop1[i]) - int(xop2))
        self.__debug_vec(vvd, vd)

    def vssubu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_vv(vd, op1, op2)
        for i in range(self.VL):
            vvd[i] = self.__uclip(int(vop1[i]) - int(vop2[i]))
        self.__debug_vec(vvd, vd)

    def vssubu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_vx(vd, op1, op2)
        for i in range(self.VL):
            vvd[i] = self.__uclip(int(vop1[i]) - int(xop2))
        self.__debug_vec(vvd, vd)

    def vwsub_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_w_vv(vd, op1, op2)
        vvd[:] = self.__sext(vop1) - self.__sext(vop2)
        self.__debug_vec(vvd, vd)

    def vwsub_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_w_vx(vd, op1, op2)
        vvd[:] = self.__sext(vop1) - self.__sext(xop2)
        self.__debug_vec(vvd, vd)

    def vwsub_wv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_w_wv(vd, op1, op2)
        vvd[:] = vop1 - self.__sext(vop2)
        self.__debug_vec(vvd, vd)

    def vwsub_wx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_w_wx(vd, op1, op2)
        vvd[:] = vop1 - self.__sext(xop2)
        self.__debug_vec(vvd, vd)

    def vwsubu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_w_vv(vd, op1, op2)
        vvd[:] = self.__zext(vop1) - self.__zext(vop2)
        self.__debug_vec(vvd, vd)

    def vwsubu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_w_vx(vd, op1, op2)
        vvd[:] = self.__zext(vop1) - self.__zext(xop2)
        self.__debug_vec(vvd, vd)

    def vwsubu_wv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_w_wv(vd, op1, op2)
        vvd[:] = vop1 - self.__zext(vop2)
        self.__debug_vec(vvd, vd)

    def vwsubu_wx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_w_wx(vd, op1, op2)
        vvd[:] = vop1 - self.__zext(xop2)
        self.__debug_vec(vvd, vd)

    ####
    ####  MUL
    ####    

    def vmul_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self.__init_vx(vd, op1, op2)
        vvd[:] = vop1[:] * vop2[:]
        self.__debug_vec(vvd, vd)
        
    def vmul_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self.__init_vx(vd, op1, op2)
        vvd[:] = vop1[:] * xop2
        self.__debug_vec(vvd, vd)     