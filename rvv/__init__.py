from rvv.integer import RVVInteger

class RVV(RVVInteger):
    def __init__(self, VLEN=2048, debug=False):
        super().__init__(VLEN, debug)

__all__ = ['RVV']