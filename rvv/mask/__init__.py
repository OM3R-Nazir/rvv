from rvv.mask.logical import Logical
from rvv.mask.mmisc import MMisc

class RVVMask(Logical, MMisc):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)