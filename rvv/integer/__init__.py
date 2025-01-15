from rvv.integer.add import ADD
from rvv.integer.subtract import SUBTRACT
from rvv.integer.multiply import MULTIPLY

class RVVInteger(ADD, SUBTRACT, MULTIPLY):
    def __init__(self, VLEN=2048, debug=False):
        super().__init__(VLEN, debug)

