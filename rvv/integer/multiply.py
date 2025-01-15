from rvv.base import BaseRVV
import numpy as np

class MULTIPLY(BaseRVV):
    def __init__(self, VLEN=2048, debug=False):
        super().__init__(VLEN, debug)
    
    ##
    ## Same Width
    ##
    
    def vmul_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'vvx', False)
        vvd[:] = vop1[:] * vop2[:]
        self._debug_vd(vvd, vd)
        
    def vmul_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'vvx', False)
        vvd[:] = vop1[:] * xop2
        self._debug_vd(vvd, vd)
        
    ##
    ## High Same Width
    ##
        
    def vmulh_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'vvv', True)
        for i in range(self.VL):
            vvd[i] = self.SEW.idtype(int(vop1[i]) * int(vop2[i]) >> self.SEW.SEW)
        self._debug_vd(vvd, vd)
         
    def vmulh_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'vvx', True)
        for i in range(self.VL):
            vvd[i] = self.SEW.idtype(int(vop1[i]) * int(xop2) >> self.SEW.SEW)
        self._debug_vd(vvd, vd)
        
    def vmulhu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'vvv', False)
        for i in range(self.VL):
            vvd[i] = self.SEW.udtype((int(vop1[i]) * int(vop2[i])) >> self.SEW.SEW)
        self._debug_vd(vvd, vd)
        
    def vmulhu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'vvx', False)
        for i in range(self.VL):
            vvd[i] = self.SEW.udtype((int(vop1[i]) * int(xop2)) >> self.SEW.SEW)
        self._debug_vd(vvd, vd)
        
    def vmulhsu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'vvv', 'ssu')
        for i in range(self.VL):
            vvd[i] = self.SEW.idtype(int(vop1[i]) * int(vop2[i]) >> self.SEW.SEW)
        self._debug_vd(vvd, vd)
        
    def vmulhsu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'vvx', 'ssu')
        for i in range(self.VL):
            vvd[i] = self.SEW.idtype(int(vop1[i]) * int(xop2) >> self.SEW.SEW)
        self._debug_vd(vvd, vd)
    
    ##
    ## Widening
    ##
    
    def vwmul_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'wvv', True)
        vvd[:] = self._sext(vop1) * self._sext(vop2)
        self._debug_vd(vvd, vd)
        
    def vwmul_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'wvx', True)
        vvd[:] = self._sext(vop1) * self._sext(xop2)
        self._debug_vd(vvd, vd)
        
    def vwmulu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'wvv', False)
        vvd[:] = self._zext(vop1) * self._zext(vop2)
        self._debug_vd(vvd, vd)
        
    def vwmulu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'wvx', False)
        vvd[:] = self._zext(vop1) * self._zext(xop2)
        self._debug_vd(vvd, vd)
        
    def vwmulsu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'wvv', 'ssu')
        vvd[:] = self._sext(vop1) * self._zext(vop2)
        self._debug_vd(vvd, vd)
        
    def vwmulsu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'wvx', 'ssu')
        vvd[:] = self._sext(vop1) * self._zext(xop2)
        self._debug_vd(vvd, vd)