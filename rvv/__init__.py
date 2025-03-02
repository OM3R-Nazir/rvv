from rvv.functions.integer import RVVInteger
from rvv.functions.float import RVVFloat
from rvv.functions.fold import RVVFold
from rvv.functions.mask import RVVMask
from rvv.functions.bitwise import RVVBitwise
from rvv.functions.memory import RVVMemory
from rvv.functions.permutation import RVVPermutation
from rvv.functions.initialize import RVVInitialize
from rvv.functions.conversion import RVVConversion
from rvv.functions.fixedpoint import RVVFixed


class RVV(RVVInteger, RVVFloat, RVVFold, RVVMask, RVVBitwise, RVVMemory,
          RVVPermutation, RVVInitialize, RVVConversion, RVVFixed):
    def __init__(self, VLEN: int = 2048, debug = False, debug_vb_as_v = False):
        super().__init__(VLEN, debug, debug_vb_as_v)

__all__ = ['RVV']