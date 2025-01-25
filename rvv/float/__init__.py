
from rvv.float.fopsbasic import FOpsBasic
from rvv.float.fcompare import FCompare
from rvv.float.fwiden import FWiden
from rvv.float.fmuladd import FMulAdd

class RVVFloat(FOpsBasic, FCompare, FWiden, FMulAdd):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)