from rvv.base import BaseRVV
import numpy as np

class Initialize(BaseRVV):
    
    def vmv_v_x(self, vd, xsrc):
        vd, xsrc, _ = self._init_ops_uni(vd, xsrc, 'vx', 'uu', False)
        vd[:] = xsrc
        self._post_op()
    
    def vfmv_v_f(self, vd, fsrc):
        vd, fsrc, _ = self._init_ops_uni(vd, fsrc, 'vf', 'ff', False)
        vd[:] = fsrc
        self._post_op()
    
    def viota_m(self, vd, vmask, masked = False):
        vd, vmask, mask = self._init_ops_uni(vd, vmask, 'vm', 'uu', masked)
        vmask = self.vm_to_bools(vmask)
        vd[mask] = np.cumsum(vmask[mask])
        self._post_op()
    
    def vid_v(self, vd, masked = False):
        vd, mask = self._init_ops_zero(vd, 'v', 'u', masked)
        vd[mask] = np.arange(self.VL)[mask]
        self._post_op()
    
    def vfmv_s_f(self, vd, fsrc):
        vd, fsrc, _ = self._init_ops_uni(vd, fsrc, 'vf', 'ff', False)
        vd[0] = fsrc
        self._post_op()
    
    def vmv_s_x(self, vd, xsrc):
        vd, xsrc, _ = self._init_ops_uni(vd, xsrc, 'vx', 'uu', False)
        vd[0] = xsrc
        self._post_op()
        