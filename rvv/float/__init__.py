
from rvv.float.basicfops import BASICOPS
from rvv.float.fcompare import FCompare

class RVVFloat(BASICOPS, FCompare):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)