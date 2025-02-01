from rvv.integer import RVVInteger
from rvv.float import RVVFloat
from rvv.fold import RVVFold
from rvv.mask import RVVMask
from rvv.bitwise import RVVBitwise

class RVV(RVVInteger, RVVFloat, RVVFold, RVVMask, RVVBitwise):
    def __init__(self, VLEN: int = 2048, debug = False, debug_vb_as_v = False):
        super().__init__(VLEN, debug, debug_vb_as_v)

__all__ = ['RVV']