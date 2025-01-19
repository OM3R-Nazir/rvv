from rvv.integer.add import ADD
from rvv.integer.subtract import SUBTRACT
from rvv.integer.multiply import MULTIPLY
from rvv.integer.compare import COMPARE
from rvv.integer.carry import CARRY

class RVVInteger(ADD, SUBTRACT, MULTIPLY, COMPARE, CARRY):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

