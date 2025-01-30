from rvv.base import BaseRVV
import numpy as np

class MISC(BaseRVV):
    
    ##
    ## MIN
    ##
    
    def vmin_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        vvd[mask] = np.minimum(vop1, vop2)[mask]
        self._post_op()

    def vmin_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        vvd[mask] = np.minimum(vop1, xop2)[mask]
        self._post_op()
    
    def vminu_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vvd[mask] = np.minimum(vop1, vop2)[mask]
        self._post_op()
    
    def vminu_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = np.minimum(vop1, xop2)[mask]
        self._post_op()
    
    ##
    ## MAX
    ##
    
    def vmax_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        vvd[mask] = np.maximum(vop1, vop2)[mask]
        self._post_op()
        
    def vmax_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        vvd[mask] = np.maximum(vop1, xop2)[mask]
        self._post_op()
        
    def vmaxu_vv(self, vd, op1, op2, masked):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vvd[mask] = np.maximum(vop1, vop2)[mask]
        self._post_op()
    
    def vmaxu_vx(self, vd, op1, op2, masked):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = np.maximum(vop1, xop2)[mask]
        self._post_op()
    
    ##
    ## Negate
    ##
    
    def vneg_v(self, vd, op1, masked):
        vvd, vop1, mask = self._init_ops_uni(vd, op1, 'vv', 'ss', masked)
        vvd[mask] = -vop1[mask]
        self._post_op()

    ##
    ## Zero Extend
    ##
    
    def vzext_vf2(self, vd, op1, masked):
        vvd, vop1, mask = self._init_ops_ext(vd, op1, 'vf2', False, masked)
        vvd[mask] = self.SEW.udtype(vop1[mask])
        self._post_op()
    
    def vzext_vf4(self, vd, op1, masked):
        vvd, vop1, mask = self._init_ops_ext(vd, op1, 'vf4', False, masked)
        vvd[mask] = self.SEW.udtype(vop1[mask])
        self._post_op()
    
    def vzext_vf8(self, vd, op1, masked):
        vvd, vop1, mask = self._init_ops_ext(vd, op1, 'vf8', False, masked)
        vvd[mask] = self.SEW.udtype(vop1[mask])
        self._post_op()
    
    ##
    ## Sign Extend
    ##
    
    def vsext_vf2(self, vd, op1, masked):
        vvd, vop1, mask = self._init_ops_ext(vd, op1, 'vf2', True, masked)
        vvd[mask] = self.SEW.dtype(vop1[mask])
        self._post_op()
    
    def vsext_vf4(self, vd, op1, masked):
        vvd, vop1, mask = self._init_ops_ext(vd, op1, 'vf4', True, masked)
        vvd[mask] = self.SEW.dtype(vop1[mask])
        self._post_op()
    
    def vsext_vf8(self, vd, op1, masked):
        vvd, vop1, mask = self._init_ops_ext(vd, op1, 'vf8', True, masked)
        vvd[mask] = self.SEW.dtype(vop1[mask])
        self._post_op()
        