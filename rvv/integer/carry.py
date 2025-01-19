from rvv.base import BaseRVV
import numpy as np

class CARRY(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## ADD
    ##
    
    def vadc_vvm(self, vd, op1, op2, carryin):
        vvd, vop1, vop2, carryin, mask = self._init_ops_tri(vd, op1, op2, carryin, 'vvvm', False, False)
        vvd[:] = vop1 + vop2 + self.vm_to_bools(carryin)
        self._debug_vd(vvd, vd)
    
    def vadc_vxm(self, vd, op1, op2, carryin):
        vvd, vop1, xop2, carryin, mask = self._init_ops_tri(vd, op1, op2, carryin, 'vvxm', False, False)
        vvd[:] = vop1 + xop2 + self.vm_to_bools(carryin)
        self._debug_vd(vvd, vd)
        
    ##
    ## ADD Carry Out
    ##
    
    def vmadc_vv(self, vmd, op1, op2):
        vvmd, vop1, vop2, mask = self._init_ops(vmd, op1, op2, 'mvv', False, False)
        vvmd_b = self.vm_to_bools(vvmd)
        for i in range(self.VL):
            vvmd_b[i] = (int(vop1[i]) + int(vop2[i])) > self.SEW.umax
        vvmd[:] = self.bools_to_vm(vvmd_b)
        self._debug_vmd(vvmd, vmd)
    
    def vmadc_vx(self, vmd, op1, op2):
        vvmd, vop1, xop2, mask = self._init_ops(vmd, op1, op2, 'mvx', False, False)
        vvmd_b = self.vm_to_bools(vvmd)
        for i in range(self.VL):
            vvmd_b[i] = (int(vop1[i]) + int(xop2)) > self.SEW.umax
        vvmd[:] = self.bools_to_vm(vvmd_b)
        self._debug_vmd(vvmd, vmd)
    
    def vmadc_vvm(self, vmd, op1, op2, carryin):
        vvmd, vop1, vop2, carryin, mask = self._init_ops_tri(vmd, op1, op2, carryin, 'mvvm', False, False)
        vvmd_b = self.vm_to_bools(vvmd)
        carryin = self.vm_to_bools(carryin)
        for i in range(self.VL):
            vvmd_b[i] = (int(vop1[i]) + int(vop2[i]) + carryin[i]) > self.SEW.umax
        vvmd[:] = self.bools_to_vm(vvmd_b)
        self._debug_vmd(vvmd, vmd)
    
    def vmadc_vxm(self, vmd, op1, op2, carryin):
        vvmd, vop1, xop2, carryin, mask = self._init_ops_tri(vmd, op1, op2, carryin, 'mvxm', False, False)
        vvmd_b = self.vm_to_bools(vvmd)
        carryin = self.vm_to_bools(carryin)
        for i in range(self.VL):
            vvmd_b[i] = (int(vop1[i]) + int(xop2) + carryin[i]) > self.SEW.umax
        vvmd[:] = self.bools_to_vm(vvmd_b)
        self._debug_vmd(vvmd, vmd)