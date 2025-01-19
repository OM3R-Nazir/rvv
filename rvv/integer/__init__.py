from rvv.integer.add import ADD
from rvv.integer.subtract import SUBTRACT
from rvv.integer.multiply import MULTIPLY
from rvv.integer.divide import DIVIDE
from rvv.integer.compare import COMPARE
from rvv.integer.carry import CARRY
from rvv.integer.muladd import MULADD
from rvv.integer.misc import MISC

class RVVInteger(ADD, SUBTRACT, MULTIPLY, DIVIDE, COMPARE, CARRY, MULADD, MISC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

