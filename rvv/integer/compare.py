from rvv.base import BaseRVV
import numpy as np

class COMPARE(BaseRVV):
    def __init__(self, VLEN=2048, debug=False):
        super().__init__(VLEN, debug)
        
    def vmseq_vv(self, vd, op1, op2, masked=False):
        vmvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'bvv', False, masked)
        vmvd_um = self.bools_to_vb((vop1 == vop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)
        
    def vmseq_vx(self, vd, op1, op2, masked=False):
        vmvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'bvx', False, masked)
        vmvd_um = self.bools_to_vb((vop1 == xop2))
        self.vm_masked(vmvd, vmvd_um, mask)
        self._debug_vmd(vmvd, vd)