from rvv.base import BaseRVV

class MULTIPLY(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## Same Width
    ##
    
    def vmul_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = (vop1 * vop2)[mask]
        self._post_op()
        
    def vmul_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = (vop1 * xop2)[mask]
        self._post_op()
        
    ##
    ## High Same Width
    ##
        
    def vmulh_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.SEW.idtype(int(vop1[i]) * int(vop2[i]) >> self.SEW.SEW)
        self._post_op()
         
    def vmulh_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.SEW.idtype(int(vop1[i]) * int(xop2) >> self.SEW.SEW)
        self._post_op()
        
    def vmulhu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.SEW.udtype((int(vop1[i]) * int(vop2[i])) >> self.SEW.SEW)
        self._post_op()
        
    def vmulhu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.SEW.udtype((int(vop1[i]) * int(xop2)) >> self.SEW.SEW)
        self._post_op()
        
    def vmulhsu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'ssu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.SEW.idtype(int(vop1[i]) * int(vop2[i]) >> self.SEW.SEW)
        self._post_op()
        
    def vmulhsu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'ssu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.SEW.idtype(int(vop1[i]) * int(xop2) >> self.SEW.SEW)
        self._post_op()
    
    ##
    ## Widening
    ##
    
    def vwmul_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wvv', 'sss', masked)
        vvd[mask] = (self._sext(vop1) * self._sext(vop2))[mask]
        self._post_op()
        
    def vwmul_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wvx', 'sss', masked)
        vvd[mask] = (self._sext(vop1) * self._sext(xop2))[mask]
        self._post_op()
        
    def vwmulu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wvv', 'uuu', masked)
        vvd[mask] = (self._zext(vop1) * self._zext(vop2))[mask]
        self._post_op()
        
    def vwmulu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wvx', 'uuu', masked)
        vvd[mask] = (self._zext(vop1) * self._zext(xop2))[mask]
        self._post_op()
        
    def vwmulsu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wvv', 'ssu', masked)
        vvd[mask] = (self._sext(vop1) * self._zext(vop2))[mask]
        self._post_op()
        
    def vwmulsu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wvx', 'ssu', masked)
        vvd[mask] = (self._sext(vop1) * self._zext(xop2))[mask]
        self._post_op()