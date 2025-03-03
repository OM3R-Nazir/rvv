from rvv.base import BaseRVV

class DIVIDE(BaseRVV):
    
    ##
    ## Divide Signed
    ##
    
    def vdiv_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        vvd[mask] = vop1[mask] // vop2[mask]
        self._post_op()
    
    def vdiv_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        vvd[mask] = vop1[mask] // xop2
        self._post_op()
    
    ##
    ## Divide Unsigned
    ##
    
    def vdivu_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vvd[mask] = vop1[mask] // vop2[mask]
        self._post_op()
    
    def vdivu_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = vop1[mask] // xop2
        self._post_op()
    
    ##
    ## Remainder Signed
    ##
    
    def vrem_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        vvd[mask] = vop1[mask] % vop2[mask]
        self._post_op()
    
    def vrem_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        vvd[mask] = vop1[mask] % xop2
        self._post_op()
        
    ##
    ## Remainder Unsigned
    ##
    
    def vremu_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vvd[mask] = vop1[mask] % vop2[mask]
        self._post_op()
        
    def vremu_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = vop1[mask] % xop2
        self._post_op()