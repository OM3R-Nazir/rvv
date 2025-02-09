from rvv.base import BaseRVV
import numpy as np

class Permutation(BaseRVV):
    
    def vrgather_vv(self, vd, vop1, vindex, masked = False):
        vd, vop1, vindex, mask = self._init_ops(vd, vop1, vindex, 'vvv', 'uuu', masked)
        vd[mask] = vop1[vindex][mask]
        self._post_op()
    
    def vrgatherei16_vv(self, vd, vop1, vindex, masked = False):
        vd, vop1, vindex, mask = self._init_ops(vd, vop1, vindex, 'vvv', 'uuu', masked)
        vindex_ei16 = vindex.view(np.uint16)[:vindex.size]
        vd[mask] = vop1[vindex_ei16][mask]
        self._post_op()
    
    def vrgather_vx(self, vd, vop1, index, masked = False):
        vd, vop1, index, mask = self._init_ops(vd, vop1, index, 'vvx', 'uux', masked)
        vd[mask] = vop1[index][mask]
        self._post_op()
    
    def vfslide1down_vf(self, vd, vop1, value, masked = False):
        vd, vop1, value, mask = self._init_ops(vd, vop1, value, 'vvf', 'fff', masked)
        vd[mask] = np.concatenate((vop1[1:], [value]))[mask]
        self._post_op()
    
    def vslide1down_vx(self, vd, vop1, value, masked = False):
        vd, vop1, value, mask = self._init_ops(vd, vop1, value, 'vvx', 'uuu', masked)
        vd[mask] = np.concatenate((vop1[1:], [value]))[mask]
        self._post_op()
    
    def vslidedown_vx(self, vd, vop1, offset, masked = False):
        vd, offset, mask = self._init_ops_uni(vd, offset, 'vx', 'uu', masked)
        vop1 = self.full_vec(vop1, viewtype='u')
        offset = min(offset, self.VL)
        
        vop1 = vop1[offset:]
        vop1 = np.concatenate((vop1, np.zeros(self.VLMAX - offset, dtype=self.SEW.udtype)))
        vop1 = vop1[:self.VL]
        
        vd[mask] = vop1[mask]
        self._post_op()
    
    def vfslide1up_vf(self, vd, vop1, value, masked = False):
        vd, vop1, value, mask = self._init_ops(vd, vop1, value, 'vvf', 'fff', masked)
        vd[mask] = np.concatenate(([value], vop1[:-1]))[mask]
        self._post_op()
    
    def vslide1up_vx(self, vd, vop1, value, masked = False):
        vd, vop1, value, mask = self._init_ops(vd, vop1, value, 'vvx', 'uuu', masked)
        vd[mask] = np.concatenate(([value], vop1[:-1]))[mask]
        self._post_op()
    
    def vslideup_vx(self, vd, vop1, offset, masked = False):
        vd, vop1, offset, mask = self._init_ops(vd, vop1, offset, 'vvx', 'uuu', masked)
        offset = min(offset, self.VL)
        vd[offset:][mask[offset:]] = vop1[:self.VL - offset][mask[offset:]]
        self._post_op()

    def vcompress_vm(self, vd, vsrc, vmask, masked = False):
        vd, vsrc, vmask, mask = self._init_ops(vd, vsrc, vmask, 'vvm', 'uuu', masked)
        vmask = self.vm_to_bools(vmask)
        comp_size = sum(vmask)
        vd[:comp_size][mask[:comp_size]] = vsrc[vmask][mask[:comp_size]]
        self._post_op()
    
    def vmerge_vvm(self, vd, vop1, vop2, vmask):
        vd, vop1, vop2, vmask, _ = self._init_ops_tri(vd, vop1, vop2, vmask, 'vvvm', 'uuuu', False)
        vmask = self.vm_to_bools(vmask)
        vd[vmask] = vop2[vmask]
        vd[~vmask] = vop1[~vmask]
        self._post_op()
    
    def vmerge_vxm(self, vd, vop1, xop2, vmask):
        vd, vop1, xop2, vmask, _ = self._init_ops_tri(vd, vop1, xop2, vmask, 'vvxm', 'uuuu', False)
        vmask = self.vm_to_bools(vmask)
        vd[vmask] = xop2
        vd[~vmask] = vop1[~vmask]
        self._post_op()
    
    def vfmerge_vfm(self, vd, vop1, fop2, vmask):
        vd, vop1, fop2, vmask, _ = self._init_ops_tri(vd, vop1, fop2, vmask, 'vvfm', 'uuuu', False)
        vmask = self.vm_to_bools(vmask)
        vd[vmask] = fop2
        vd[~vmask] = vop1[~vmask]
        self._post_op()
    
    def vmv_v_v(self, vd, vsrc):
        vd, vsrc, _ = self._init_ops_uni(vd, vsrc, 'vv', 'uu', False)
        vd[:] = vsrc
        self._post_op()

    def vmv_x_s(self, xd, xsrc): 
        xd, xsrc, _ = self._init_ops_uni(xd, xsrc, 'xs', 'ux', False)
        xd[:] = xsrc[0]
        self._post_op()
        
    def vfmv_f_s(self, fd, fsrc):
        fd, fsrc, _ = self._init_ops_uni(fd, fsrc, 'fs', 'xf', False)
        fd[:] = fsrc[0]
        self._post_op()