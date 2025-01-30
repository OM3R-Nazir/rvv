from rvv.base import BaseRVV

class FMulAdd(BaseRVV):
    
    def vfmacc_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = ((vop1 * vop2) + vvd)[mask]
        self._post_op()
    
    def vfmacc_vf(self, vd, op1, op2, masked=False):
        vvd, fop1, vop2, mask = self._init_ops(vd, op1, op2, 'vxv', 'fff', masked)
        vvd[mask] = ((fop1 * vop2) + vvd)[mask]
        self._post_op()
    
    def vfnmacc_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = (-(vop1 * vop2) - vvd)[mask]
        self._post_op()
        
    def vfnmacc_vf(self, vd, op1, op2, masked=False):
        vvd, fop1, vop2, mask = self._init_ops(vd, op1, op2, 'vxv', 'fff', masked)
        vvd[mask] = (-(fop1 * vop2) - vvd)[mask]
        self._post_op()
    
    def vfmsac_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = ((vop1 * vop2) - vvd)[mask]
        self._post_op()
        
    def vfmsac_vf(self, vd, op1, op2, masked=False):
        vvd, fop1, vop2, mask = self._init_ops(vd, op1, op2, 'vxv', 'fff', masked)
        vvd[mask] = ((fop1 * vop2) - vvd)[mask]
        self._post_op()
    
    def vfnmsac_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = (-(vop1 * vop2) + vvd)[mask]
        self._post_op()
    
    def vfnmsac_vf(self, vd, op1, op2, masked=False):
        vvd, fop1, vop2, mask = self._init_ops(vd, op1, op2, 'vxv', 'fff', masked)
        vvd[mask] = (-(fop1 * vop2) + vvd)[mask]
        self._post_op()
    
    def vfmadd_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = ((vvd * vop1) + vop2)[mask]
        self._post_op()
    
    def vfmadd_vf(self, vd, op1, op2, masked=False):
        vvd, fop1, vop2, mask = self._init_ops(vd, op1, op2, 'vxv', 'fff', masked)
        vvd[mask] = ((vvd * fop1) + vop2)[mask]
        self._post_op()
    
    def vfnmadd_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = (-(vvd * vop1) - vop2)[mask]
        self._post_op()
    
    def vfnmadd_vf(self, vd, op1, op2, masked=False):
        vvd, fop1, vop2, mask = self._init_ops(vd, op1, op2, 'vxv', 'fff', masked)
        vvd[mask] = (-(vvd * fop1) - vop2)[mask]
        self._post_op()
    
    def vfmsub_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = ((vvd * vop1) - vop2)[mask]
        self._post_op()
    
    def vfmsub_vf(self, vd, op1, op2, masked=False):
        vvd, fop1, vop2, mask = self._init_ops(vd, op1, op2, 'vxv', 'fff', masked)
        vvd[mask] = ((vvd * fop1) - vop2)[mask]
        self._post_op()
    
    def vfnmsub_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = (-(vvd * vop1) + vop2)[mask]
        self._post_op()
    
    def vfnmsub_vf(self, vd, op1, op2, masked=False):
        vvd, fop1, vop2, mask = self._init_ops(vd, op1, op2, 'vxv', 'fff', masked)
        vvd[mask] = (-(vvd * fop1) + vop2)[mask]
        self._post_op()