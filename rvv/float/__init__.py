
from rvv.float.basicfops import BASICOPS
from rvv.float.fcompare import FCompare
from rvv.float.fwiden import FWiden

class RVVFloat(BASICOPS, FCompare, FWiden):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)