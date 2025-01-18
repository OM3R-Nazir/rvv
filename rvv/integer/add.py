from rvv.base import BaseRVV

class ADD(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## Same Width
    ##
    
    def vadd_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', False, masked)
        vvd[mask] = (vop1 + vop2)[mask]
        self._debug_vd(vvd, vd)
        
    def vadd_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', False, masked)
        vvd[mask] = (vop1 + xop2)[mask]
        self._debug_vd(vvd, vd)
        
    ##
    ## Saturating
    ##

    def vsadd_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', True, masked)

        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(int(vop1[i]) + int(vop2[i]))
            
        self._debug_vd(vvd, vd)

    def vsadd_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', True, masked)
        
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(int(vop1[i]) + int(xop2))
        
        self._debug_vd(vvd, vd)

    def vsaddu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', False, masked)

        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._uclip(int(vop1[i]) + int(vop2[i]))
            
        self._debug_vd(vvd, vd)

    def vsaddu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', False, masked)
        
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._uclip(int(vop1[i]) + int(xop2))
        
        self._debug_vd(vvd, vd)

    ##
    ## Widening
    ##

    def vwadd_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wvv', True, masked)
        vvd[mask] = (self._sext(vop1) + self._sext(vop2))[mask]
        self._debug_vd(vvd, vd)

    def vwadd_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wvx', True, masked)
        vvd[mask] = (self._sext(vop1) + self._sext(xop2))[mask]
        self._debug_vd(vvd, vd)

    def vwadd_wv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wwv', True, masked)
        vvd[mask] = vop1 + self._sext(vop2)
        self._debug_vd(vvd, vd)

    def vwadd_wx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wwx', True, masked)
        vvd[mask] = (vop1 + self._sext(xop2))[mask]
        self._debug_vd(vvd, vd)        

    def vwaddu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wvv', False, masked)
        vvd[mask] = (self._zext(vop1) + self._zext(vop2))[mask]
        self._debug_vd(vvd, vd)

    def vwaddu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wvx', False, masked)
        vvd[mask] = (self._zext(vop1) + self._zext(xop2))[mask]
        self._debug_vd(vvd, vd)

    def vwaddu_wv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wwv', False, masked)
        vvd[mask] = vop1 + self._zext(vop2)
        self._debug_vd(vvd, vd)

    def vwaddu_wx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wwx', False, masked)
        vvd[mask] = (vop1 + self._zext(xop2))[mask]
        self._debug_vd(vvd, vd)