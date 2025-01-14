from rvv.base import BaseRVV

class MULTIPLY(BaseRVV):
    def __init__(self, VLEN=2048, debug=False):
        super().__init__(VLEN, debug)
    
    def vmul_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_vx(vd, op1, op2)
        vvd[:] = vop1[:] * vop2[:]
        self._debug_vec(vvd, vd)
        
    def vmul_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_vx(vd, op1, op2)
        vvd[:] = vop1[:] * xop2
        self._debug_vec(vvd, vd)     