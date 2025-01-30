from rvv.base import BaseRVV
import numpy as np

class MMisc(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def vfirst_m(self, xd, op1, masked = False):
        xd, op1, mask = self._init_ops_uni(xd, op1, 'xm', 'xu', masked)
        xd[:] = np.argmax(self.vm_to_bools(op1) & mask) if np.any(op1) else -1 
        self._post_op()
    
    def vcpop_m(self, xd, op1, masked = False):
        xd, op1, mask = self._init_ops_uni(xd, op1, 'xm', 'xu', masked)
        xd[:] = np.count_nonzero(self.vm_to_bools(op1) & mask)
        self._post_op()
    
    def vmsbf_m(self, vd, op1, masked = False):
        vd, op1, mask = self._init_ops_uni(vd, op1, 'mm', 'uu', masked)
        
        vd_bools = self.vm_to_bools(vd)
        op_bools = self.vm_to_bools(op1)
        acc = True
        for i in range(self.VL):
            if mask[i]:
                if op_bools[i]: acc = False
                vd_bools[i] = acc        
        vd[:] = self.bools_to_vm(vd_bools)
        
        self._post_op()
    
    def vmsif_m(self, vd, op1, masked = False):
        vd, op1, mask = self._init_ops_uni(vd, op1, 'mm', 'uu', masked)
        
        vd_bools = self.vm_to_bools(vd)
        op_bools = self.vm_to_bools(op1)
        acc = True
        for i in range(self.VL):
            if mask[i]:
                vd_bools[i] = acc        
                if op_bools[i]: acc = False
        vd[:] = self.bools_to_vm(vd_bools)
        
        self._post_op()
        
    def vmsof_m(self, vd, op1, masked = False):
        vd, op1, mask = self._init_ops_uni(vd, op1, 'mm', 'uu', masked)
        
        vd_bools = self.vm_to_bools(vd)
        op_bools = self.vm_to_bools(op1)
        acc = True
        for i in range(self.VL):
            if mask[i]:
                vd_bools[i] = acc and op_bools[i]
                if op_bools[i]: acc = False
        vd[:] = self.bools_to_vm(vd_bools)
        
        self._post_op()
    
    def vmmv_m(self, vd, op1):
        vd, op1, _ = self._init_ops_uni(vd, op1, 'mm', 'uu', False)
        vd[:] = op1
        self._post_op()
    
    def vmset_m(self, vd):
        vd, _ = self._init_ops_zero(vd, 'm', 'u', False)
        vd[:] = 255
        self._post_op()
    
    def vmclr_m(self, vd):
        vd, _ = self._init_ops_zero(vd, 'm', 'u', False)
        vd[:] = 0
        self._post_op()