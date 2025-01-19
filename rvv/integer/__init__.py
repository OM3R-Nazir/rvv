from rvv.integer.add import ADD
from rvv.integer.subtract import SUBTRACT
from rvv.integer.multiply import MULTIPLY
from rvv.integer.compare import COMPARE
from rvv.integer.carry import CARRY
from rvv.integer.muladd import MULADD

class RVVInteger(ADD, SUBTRACT, MULTIPLY, COMPARE, CARRY, MULADD):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

