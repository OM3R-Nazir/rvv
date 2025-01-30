
from rvv.float.fopsbasic import FOpsBasic
from rvv.float.fcompare import FCompare
from rvv.float.fwiden import FWiden
from rvv.float.fmuladd import FMulAdd
from rvv.float.fmisc import FMisc

class RVVFloat(FOpsBasic, FCompare, FWiden, FMulAdd, FMisc):
    pass
