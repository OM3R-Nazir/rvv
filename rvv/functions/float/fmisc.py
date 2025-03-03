from rvv.base import BaseRVV
import numpy as np

class FMisc(BaseRVV):
    
    def vfmin_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = np.minimum(vop1, vop2)[mask]
        self._post_op()
    
    def vfmin_vf(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvf', 'fff', masked)
        vvd[mask] = np.minimum(vop1, xop2)[mask]
        self._post_op()
    
    def vfmax_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vvd[mask] = np.maximum(vop1, vop2)[mask]
        self._post_op()
    
    def vfmax_vf(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvf', 'fff', masked)
        vvd[mask] = np.maximum(vop1, xop2)[mask]
        self._post_op()
    
    def vfneg_v(self, vd, op1, masked=False):
        vvd, vop1, mask = self._init_ops_uni(vd, op1, None, 'vv', 'ff', masked)
        vvd[mask] = -vop1[mask]
        self._post_op()
    
    def vfabs_v(self, vd, op1, masked=False):
        vvd, vop1, mask = self._init_ops_uni(vd, op1, None, 'vv', 'ff', masked)
        vvd[mask] = np.abs(vop1)[mask]
        self._post_op()
    
    def vfclass_v(self, vd, op1, masked=False):
        vvd, vop1, mask = self._init_ops_uni(vd, op1, None, 'vv', 'uf', masked)
        vvd_um = np.zeros_like(vvd)
        # Classify each element and set the corresponding bits
        vvd_um |= (np.isneginf(vop1) << 0)  # Bit 0: Negative infinity
        vvd_um |= ((vop1 < 0) & np.isfinite(vop1) & ~np.isclose(vop1, 0) << 1)  # Bit 1: Negative normal
        vvd_um |= ((vop1 < 0) & ~np.isfinite(vop1) & ~np.isnan(vop1) << 2)  # Bit 2: Negative subnormal
        vvd_um |= ((vop1 == 0) & np.signbit(vop1) << 3)  # Bit 3: Negative zero
        vvd_um |= ((vop1 == 0) & ~np.signbit(vop1) << 4)  # Bit 4: Positive zero
        vvd_um |= ((vop1 > 0) & ~np.isfinite(vop1) & ~np.isnan(vop1) << 5)  # Bit 5: Positive subnormal
        vvd_um |= ((vop1 > 0) & np.isfinite(vop1) & ~np.isclose(vop1, 0) << 6)  # Bit 6: Positive normal
        vvd_um |= (np.isposinf(vop1) << 7)  # Bit 7: Positive infinity
        vvd_um |= ((np.isnan(vop1) & np.signbit(vop1)) << 8)  # Bit 8: Signaling NaN (approximated)
        vvd_um |= ((np.isnan(vop1) & ~np.signbit(vop1)) << 9)  # Bit 9: Quiet NaN (approximated)

        vvd[mask] = vvd_um[mask]
        
        self._post_op()
    
    def vfrec_v(self, vd, op1, masked=False):
        vvd, vop1, mask = self._init_ops_uni(vd, op1, None, 'vv', 'ff', masked)
        vvd[mask] = np.reciprocal(vop1)[mask]
        self._post_op()
    
    def vfrsqrt_v(self, vd, op1, masked=False):
        vvd, vop1, mask = self._init_ops_uni(vd, op1, None, 'vv', 'ff', masked)
        vvd[mask] = np.reciprocal(np.sqrt(vop1))[mask]
        self._post_op()
    
    def vfsqrt_v(self, vd, op1, masked=False):
        vvd, vop1, mask = self._init_ops_uni(vd, op1, None, 'vv', 'ff', masked)
        vvd[mask] = np.sqrt(vop1)[mask]
        self._post_op()
        