from rvv.base import BaseRVV
import numpy as np

class COMPARE(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## Equality
    ##    
    
    def vmseq_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', False, masked)
        vmvd_um = self.bools_to_vm((vop1 == vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmseq_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', False, masked)
        vmvd_um = self.bools_to_vm((vop1 == xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsne_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', False, masked)
        vmvd_um = self.bools_to_vm((vop1 != vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsne_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', False, masked)
        vmvd_um = self.bools_to_vm((vop1 != xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
    
    ##
    ## Signed Comparison
    ##
    
    def vmslt_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', True, masked)
        vmvd_um = self.bools_to_vm((vop1 < vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmslt_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', True, masked)
        vmvd_um = self.bools_to_vm((vop1 < xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)    
    
    def vmsle_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', True, masked)
        vmvd_um = self.bools_to_vm((vop1 <= vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsle_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', True, masked)
        vmvd_um = self.bools_to_vm((vop1 <= xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
    
    def vmsgt_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', True, masked)
        vmvd_um = self.bools_to_vm((vop1 > vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsgt_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', True, masked)
        vmvd_um = self.bools_to_vm((vop1 > xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)    
    
    def vmsge_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', True, masked)
        vmvd_um = self.bools_to_vm((vop1 >= vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsge_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', True, masked)
        vmvd_um = self.bools_to_vm((vop1 >= xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)    
    
    ##
    ## Unsigned Comparison
    ##
    
    def vmsltu_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', False, masked)
        vmvd_um = self.bools_to_vm((vop1 < vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsltu_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', False, masked)
        vmvd_um = self.bools_to_vm((vop1 < xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)    
    
    def vmsleu_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', False, masked)
        vmvd_um = self.bools_to_vm((vop1 <= vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsleu_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', False, masked)
        vmvd_um = self.bools_to_vm((vop1 <= xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
    
    def vmsgtu_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', False, masked)
        vmvd_um = self.bools_to_vm((vop1 > vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsgtu_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', False, masked)
        vmvd_um = self.bools_to_vm((vop1 > xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)    
    
    def vmsgeu_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', False, masked)
        vmvd_um = self.bools_to_vm((vop1 >= vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmsgeu_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'mvx', False, masked)
        vmvd_um = self.bools_to_vm((vop1 >= xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)       