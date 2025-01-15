from rvv.base import BaseRVV

class SUBTRACT(BaseRVV):
    def __init__(self, VLEN, debug):
        super().__init__(VLEN, debug)
    
    def vsub_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'vvv', False)
        vvd[:] = vop1[:] - vop2[:]
        self._debug_vd(vvd, vd)
        
    def vsub_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'vvx', False)
        vvd[:] = vop1[:] - xop2
        self._debug_vd(vvd, vd)    
    
    def vrsub_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'vvx', False)
        vvd[:] = xop2 - vop1[:]
        self._debug_vd(vvd, vd)    

    def vssub_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'vvv', True)
        for i in range(self.VL):
            vvd[i] = self._iclip(int(vop1[i]) - int(vop2[i]))
        self._debug_vd(vvd, vd)

    def vssub_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'vvx', True)
        for i in range(self.VL):
            vvd[i] = self._iclip(int(vop1[i]) - int(xop2))
        self._debug_vd(vvd, vd)

    def vssubu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'vvv', False)
        for i in range(self.VL):
            vvd[i] = self._uclip(int(vop1[i]) - int(vop2[i]))
        self._debug_vd(vvd, vd)

    def vssubu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'vvx', False)
        for i in range(self.VL):
            vvd[i] = self._uclip(int(vop1[i]) - int(xop2))
        self._debug_vd(vvd, vd)

    def vwsub_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'wvv', True)
        vvd[:] = self._sext(vop1) - self._sext(vop2)
        self._debug_vd(vvd, vd)

    def vwsub_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'wvx', True)
        vvd[:] = self._sext(vop1) - self._sext(xop2)
        self._debug_vd(vvd, vd)

    def vwsub_wv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'wwv', True)
        vvd[:] = vop1 - self._sext(vop2)
        self._debug_vd(vvd, vd)

    def vwsub_wx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'wwx', True)
        vvd[:] = vop1 - self._sext(xop2)
        self._debug_vd(vvd, vd)

    def vwsubu_vv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'wvv', False)
        vvd[:] = self._zext(vop1) - self._zext(vop2)
        self._debug_vd(vvd, vd)

    def vwsubu_vx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'wvx', False)
        vvd[:] = self._zext(vop1) - self._zext(xop2)
        self._debug_vd(vvd, vd)

    def vwsubu_wv(self, vd, op1, op2):
        vvd, vop1, vop2 = self._init_ops(vd, op1, op2, 'wwv', False)
        vvd[:] = vop1 - self._zext(vop2)
        self._debug_vd(vvd, vd)

    def vwsubu_wx(self, vd, op1, op2):
        vvd, vop1, xop2 = self._init_ops(vd, op1, op2, 'wwx', False)
        vvd[:] = vop1 - self._zext(xop2)
        self._debug_vd(vvd, vd)