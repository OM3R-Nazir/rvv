from rvv.base import BaseRVV

class ADD(BaseRVV):
    def __init__(self, VLEN, debug):
        super().__init__(VLEN, debug)
    
    def vadd_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_vv(vd, op1, op2)
        vvd[:] = vop1[:] + vop2[:]
        self._debug_vec(vvd, vd)
        
    def vadd_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_vx(vd, op1, op2)
        vvd[:] = vop1[:] + xop2
        self._debug_vec(vvd, vd)

    def vsadd_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_vv(vd, op1, op2)

        for i in range(self.VL):
            vvd[i] = self._iclip(int(vop1[i]) + int(vop2[i]))
            
        self._debug_vec(vvd, vd)

    def vsadd_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_vx(vd, op1, op2)
        
        for i in range(self.VL):
            vvd[i] = self._iclip(int(vop1[i]) + int(xop2))
        
        self._debug_vec(vvd, vd)

    def vsaddu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_vv(vd, op1, op2)

        for i in range(self.VL):
            vvd[i] = self._uclip(int(vop1[i]) + int(vop2[i]))
            
        self._debug_vec(vvd, vd)

    def vsaddu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_vx(vd, op1, op2)
        
        for i in range(self.VL):
            vvd[i] = self._uclip(int(vop1[i]) + int(xop2))
        
        self._debug_vec(vvd, vd)

    def vwadd_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_w_vv(vd, op1, op2)
        vvd[:] = self._sext(vop1) + self._sext(vop2)
        self._debug_vec(vvd, vd)

    def vwadd_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_w_vx(vd, op1, op2)
        vvd[:] = self._sext(vop1) + self._sext(xop2)
        self._debug_vec(vvd, vd)

    def vwadd_wv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_w_wv(vd, op1, op2)
        vvd[:] = vop1 + self._sext(vop2)
        self._debug_vec(vvd, vd)

    def vwadd_wx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_w_wx(vd, op1, op2)
        vvd[:] = vop1 + self._sext(xop2)
        self._debug_vec(vvd, vd)        

    def vwaddu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_w_vv(vd, op1, op2)
        vvd[:] = self._zext(vop1) + self._zext(vop2)
        self._debug_vec(vvd, vd)

    def vwaddu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_w_vx(vd, op1, op2)
        vvd[:] = self._zext(vop1) + self._zext(xop2)
        self._debug_vec(vvd, vd)

    def vwaddu_wv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_w_wv(vd, op1, op2)
        vvd[:] = vop1 + self._zext(vop2)
        self._debug_vec(vvd, vd)

    def vwaddu_wx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_w_wx(vd, op1, op2)
        vvd[:] = vop1 + self._zext(xop2)
        self._debug_vec(vvd, vd)