
from rvv.functions.float.fopsbasic import FOpsBasic
from rvv.functions.float.fcompare import FCompare
from rvv.functions.float.fwiden import FWiden
from rvv.functions.float.fmuladd import FMulAdd
from rvv.functions.float.fmisc import FMisc

class RVVFloat(FOpsBasic, FCompare, FWiden, FMulAdd, FMisc):
    pass
