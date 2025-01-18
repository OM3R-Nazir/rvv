from rvv.base import BaseRVV
import numpy as np

class COMPARE(BaseRVV):
    def __init__(self, VLEN=2048, debug=False):
        super().__init__(VLEN, debug)
        
    def vmseq_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'mvv', False, masked)
        vvd = self.bools_to_mask((vop1 == vop2)[mask])
        self._debug_vd(vvd, vd, True)