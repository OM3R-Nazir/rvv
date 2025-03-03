from rvv.base import BaseRVV

class FCompare(BaseRVV):
        
    def vmfeq_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 == vop2))
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfeq_vf(self, vd, op1, op2, masked=False):
        vmvd, vop1, fop2, mask = self._init_ops(vd, op1, op2, 'mvf', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 == fop2))    
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfne_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 != vop2))
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfne_vf(self, vd, op1, op2, masked=False):
        vmvd, vop1, fop2, mask = self._init_ops(vd, op1, op2, 'mvf', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 != fop2))    
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmflt_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 < vop2))
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmflt_vf(self, vd, op1, op2, masked=False):
        vmvd, vop1, fop2, mask = self._init_ops(vd, op1, op2, 'mvf', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 < fop2))    
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfle_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 <= vop2))
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfle_vf(self, vd, op1, op2, masked=False):
        vmvd, vop1, fop2, mask = self._init_ops(vd, op1, op2, 'mvf', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 <= fop2))    
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfgt_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 > vop2))
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfgt_vf(self, vd, op1, op2, masked=False):
        vmvd, vop1, fop2, mask = self._init_ops(vd, op1, op2, 'mvf', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 > fop2))    
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfge_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 >= vop2))
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmfge_vf(self, vd, op1, op2, masked=False):
        vmvd, vop1, fop2, mask = self._init_ops(vd, op1, op2, 'mvf', 'fff', masked)
        vmvd_um = self.bools_to_vm((vop1 >= fop2))    
        self._vm_masked(vmvd, vmvd_um, mask)
        self._post_op()