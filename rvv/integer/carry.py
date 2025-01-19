from rvv.base import BaseRVV
import numpy as np

class CARRY(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## ADD
    ##
    
    def vadc_vvm(self, vd, op1, op2, carryin):
        vvd, vop1, vop2, carryin, mask = self._init_ops_tri(vd, op1, op2, carryin, 'vvvb', False, False)
        vvd[:] = vop1 + vop2 + self.vb_to_bools(carryin)
        self._debug_vd(vvd, vd)
    
    def vadc_vxm(self, vd, op1, op2, carryin):
        vvd, vop1, xop2, carryin, mask = self._init_ops_tri(vd, op1, op2, carryin, 'vvxb', False, False)
        vvd[:] = vop1 + xop2 + self.vb_to_bools(carryin)
        self._debug_vd(vvd, vd)
        
    ##
    ## ADD Carry Out
    ##
    
    def vmadc_vv(self, vbd, op1, op2):
        vvbd, vop1, vop2, mask = self._init_ops(vbd, op1, op2, 'bvv', False, False)
        vvbd_b = self.vb_to_bools(vvbd)
        for i in range(self.VL):
            vvbd_b[i] = (int(vop1[i]) + int(vop2[i])) > self.SEW.umax
        vvbd[:] = self.bools_to_vb(vvbd_b)
        self._debug_vbd(vvbd, vbd)
    
    def vmadc_vx(self, vbd, op1, op2):
        vvbd, vop1, xop2, mask = self._init_ops(vbd, op1, op2, 'bvx', False, False)
        vvbd_b = self.vb_to_bools(vvbd)
        for i in range(self.VL):
            vvbd_b[i] = (int(vop1[i]) + int(xop2)) > self.SEW.umax
        vvbd[:] = self.bools_to_vb(vvbd_b)
        self._debug_vbd(vvbd, vbd)
    
    def vmadc_vvm(self, vbd, op1, op2, carryin):
        vvbd, vop1, vop2, carryin, mask = self._init_ops_tri(vbd, op1, op2, carryin, 'bvvb', False, False)
        vvbd_b = self.vb_to_bools(vvbd)
        carryin = self.vb_to_bools(carryin)
        for i in range(self.VL):
            vvbd_b[i] = (int(vop1[i]) + int(vop2[i]) + carryin[i]) > self.SEW.umax
        vvbd[:] = self.bools_to_vb(vvbd_b)
        self._debug_vbd(vvbd, vbd)
    
    def vmadc_vxm(self, vbd, op1, op2, carryin):
        vvbd, vop1, xop2, carryin, mask = self._init_ops_tri(vbd, op1, op2, carryin, 'bvxb', False, False)
        vvbd_b = self.vb_to_bools(vvbd)
        carryin = self.vb_to_bools(carryin)
        for i in range(self.VL):
            vvbd_b[i] = (int(vop1[i]) + int(xop2) + carryin[i]) > self.SEW.umax
        vvbd[:] = self.bools_to_vb(vvbd_b)
        self._debug_vbd(vvbd, vbd)