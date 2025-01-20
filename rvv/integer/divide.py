from rvv.base import BaseRVV

class DIVIDE(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## Divide Signed
    ##
    
    def vdiv_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        vvd[mask] = vop1[mask] // vop2[mask]
        self._debug_vd(vvd, vd)
    
    def vdiv_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        vvd[mask] = vop1[mask] // xop2
        self._debug_vd(vvd, vd)
    
    ##
    ## Divide Unsigned
    ##
    
    def vdivu_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vvd[mask] = vop1[mask] // vop2[mask]
        self._debug_vd(vvd, vd)
    
    def vdivu_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = vop1[mask] // xop2
        self._debug_vd(vvd, vd)
    
    ##
    ## Remainder Signed
    ##
    
    def vrem_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        vvd[mask] = vop1[mask] % vop2[mask]
        self._debug_vd(vvd, vd)
    
    def vrem_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        vvd[mask] = vop1[mask] % xop2
        self._debug_vd(vvd, vd)
        
    ##
    ## Remainder Unsigned
    ##
    
    def vremu_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vvd[mask] = vop1[mask] % vop2[mask]
        self._debug_vd(vvd, vd)
        
    def vremu_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = vop1[mask] % xop2
        self._debug_vd(vvd, vd)