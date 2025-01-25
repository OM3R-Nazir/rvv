
from rvv.float.fopsbasic import FOpsBasic
from rvv.float.fcompare import FCompare
from rvv.float.fwiden import FWiden

class RVVFloat(FOpsBasic, FCompare, FWiden):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)