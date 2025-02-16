from rvv.integer import RVVInteger
from rvv.float import RVVFloat
from rvv.fold import RVVFold
from rvv.mask import RVVMask
from rvv.bitwise import RVVBitwise
from rvv.permutation import RVVPermutation
from rvv.initialize import RVVInitialize
from rvv.conversion import RVVConversion
from rvv.fixed import RVVFixed


class RVV(RVVInteger, RVVFloat, RVVFold, RVVMask, RVVBitwise, RVVPermutation, RVVInitialize, RVVConversion, RVVFixed):
    def __init__(self, VLEN: int = 2048, debug = False, debug_vb_as_v = False):
        super().__init__(VLEN, debug, debug_vb_as_v)

__all__ = ['RVV']