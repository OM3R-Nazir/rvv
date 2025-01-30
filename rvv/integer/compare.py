from rvv.base import BaseRVV

class COMPARE(BaseRVV):
    
    ##
    ## Equality
    ##    
    
    def vmseq_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 == vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmseq_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 == xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsne_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 != vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsne_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 != xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    ##
    ## Signed Comparison
    ##
    
    def vmslt_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'sss', masked)
        vmvd_um = self.bools_to_vm((vop1 < vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmslt_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'sss', masked)
        vmvd_um = self.bools_to_vm((vop1 < xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()    
    
    def vmsle_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'sss', masked)
        vmvd_um = self.bools_to_vm((vop1 <= vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsle_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'sss', masked)
        vmvd_um = self.bools_to_vm((vop1 <= xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmsgt_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'sss', masked)
        vmvd_um = self.bools_to_vm((vop1 > vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsgt_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'sss', masked)
        vmvd_um = self.bools_to_vm((vop1 > xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()    
    
    def vmsge_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'sss', masked)
        vmvd_um = self.bools_to_vm((vop1 >= vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsge_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'sss', masked)
        vmvd_um = self.bools_to_vm((vop1 >= xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()    
    
    ##
    ## Unsigned Comparison
    ##
    
    def vmsltu_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 < vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsltu_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 < xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()    
    
    def vmsleu_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 <= vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsleu_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 <= xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
    
    def vmsgtu_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 > vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsgtu_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 > xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()    
    
    def vmsgeu_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 >= vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()
        
    def vmsgeu_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', 'uuu', masked)
        vmvd_um = self.bools_to_vm((vop1 >= xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._post_op()       