from rvv.base import BaseRVV

class CARRY(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## ADD
    ##
    
    def vadc_vvm(self, vd, op1, op2, carryin):
        vvd, vop1, vop2, carryin, mask = self._init_ops_tri(vd, op1, op2, carryin, 'vvvm', 'uuuu', False)
        vvd[:] = vop1 + vop2 + self.vm_to_bools(carryin)
        self._post_op()
    
    def vadc_vxm(self, vd, op1, op2, carryin):
        vvd, vop1, xop2, carryin, mask = self._init_ops_tri(vd, op1, op2, carryin, 'vvxm', 'uuuu', False)
        vvd[:] = vop1 + xop2 + self.vm_to_bools(carryin)
        self._post_op()
        
    ##
    ## ADD Carry Out
    ##
    
    def vmadc_vv(self, vmd, op1, op2):
        vmvd, vop1, vop2, mask = self._init_ops(vmd, op1, op2, 'mvv', 'uuu', False)
        vmvd_b = self.vm_to_bools(vmvd)
        for i in range(self.VL):
            vmvd_b[i] = (int(vop1[i]) + int(vop2[i])) > self.SEW.umax
        vmvd[:] = self.bools_to_vm(vmvd_b)
        self._post_op()
    
    def vmadc_vx(self, vmd, op1, op2):
        vmvd, vop1, xop2, mask = self._init_ops(vmd, op1, op2, 'mvx', 'uuu', False)
        vmvd_b = self.vm_to_bools(vmvd)
        for i in range(self.VL):
            vmvd_b[i] = (int(vop1[i]) + int(xop2)) > self.SEW.umax
        vmvd[:] = self.bools_to_vm(vmvd_b)
        self._post_op()
    
    def vmadc_vvm(self, vmd, op1, op2, carryin):
        vmvd, vop1, vop2, carryin, mask = self._init_ops_tri(vmd, op1, op2, carryin, 'mvvm', 'uuuu', False)
        vmvd_b = self.vm_to_bools(vmvd)
        carryin = self.vm_to_bools(carryin)
        for i in range(self.VL):
            vmvd_b[i] = (int(vop1[i]) + int(vop2[i]) + carryin[i]) > self.SEW.umax
        vmvd[:] = self.bools_to_vm(vmvd_b)
        self._post_op()
    
    def vmadc_vxm(self, vmd, op1, op2, carryin):
        vmvd, vop1, xop2, carryin, mask = self._init_ops_tri(vmd, op1, op2, carryin, 'mvxm', 'uuuu', False)
        vmvd_b = self.vm_to_bools(vmvd)
        carryin = self.vm_to_bools(carryin)
        for i in range(self.VL):
            vmvd_b[i] = (int(vop1[i]) + int(xop2) + carryin[i]) > self.SEW.umax
        vmvd[:] = self.bools_to_vm(vmvd_b)
        self._post_op()
        
    ##
    ## Subtract
    ##
    
    def vsbc_vvm(self, vd, op1, op2, borrowin):
        vvd, vop1, vop2, borrowin, mask = self._init_ops_tri(vd, op1, op2, borrowin, 'vvvm', 'uuuu', False)
        vvd[:] = vop1 - vop2 - self.vm_to_bools(borrowin)
        self._post_op()
        
    def vsbc_vxm(self, vd, op1, op2, borrowin):
        vvd, vop1, xop2, borrowin, mask = self._init_ops_tri(vd, op1, op2, borrowin, 'vvxm', 'uuuu', False)
        vvd[:] = vop1 - xop2 - self.vm_to_bools(borrowin)
        self._post_op()
    
    ##
    ## Subtract Borrow Out
    ##
    
    def vmsbc_vv(self, vmd, op1, op2):
        vmvd, vop1, vop2, mask = self._init_ops(vmd, op1, op2, 'mvv', 'uuu', False)
        vmvd_b = self.vm_to_bools(vmvd)
        for i in range(self.VL):
            vmvd_b[i] = (int(vop1[i]) - int(vop2[i])) < 0
        vmvd[:] = self.bools_to_vm(vmvd_b)
        self._post_op()
        
    def vmsbc_vx(self, vmd, op1, op2):
        vmvd, vop1, xop2, mask = self._init_ops(vmd, op1, op2, 'mvx', 'uuu', False)
        vmvd_b = self.vm_to_bools(vmvd)
        for i in range(self.VL):
            vmvd_b[i] = (int(vop1[i]) - int(xop2)) < 0
        vmvd[:] = self.bools_to_vm(vmvd_b)
        self._post_op()
        
    def vmsbc_vvm(self, vmd, op1, op2, borrowin):
        vmvd, vop1, vop2, borrowin, mask = self._init_ops_tri(vmd, op1, op2, borrowin, 'mvvm', 'uuuu', False)
        vmvd_b = self.vm_to_bools(vmvd)
        borrowin = self.vm_to_bools(borrowin)
        for i in range(self.VL):
            vmvd_b[i] = (int(vop1[i]) - int(vop2[i]) - borrowin[i]) < 0
        vmvd[:] = self.bools_to_vm(vmvd_b)
        self._post_op()
    
    def vmsbc_vxm(self, vmd, op1, op2, borrowin):
        vmvd, vop1, xop2, borrowin, mask = self._init_ops_tri(vmd, op1, op2, borrowin, 'mvxm', 'uuuu', False)
        vmvd_b = self.vm_to_bools(vmvd)
        borrowin = self.vm_to_bools(borrowin)
        for i in range(self.VL):
            vmvd_b[i] = (int(vop1[i]) - int(xop2) - borrowin[i]) < 0
        vmvd[:] = self.bools_to_vm(vmvd_b)
        self._post_op()