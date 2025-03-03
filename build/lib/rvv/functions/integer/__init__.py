from rvv.functions.integer.add import ADD
from rvv.functions.integer.subtract import SUBTRACT
from rvv.functions.integer.multiply import MULTIPLY
from rvv.functions.integer.divide import DIVIDE
from rvv.functions.integer.compare import COMPARE
from rvv.functions.integer.carry import CARRY
from rvv.functions.integer.muladd import MULADD
from rvv.functions.integer.misc import MISC

class RVVInteger(ADD, SUBTRACT, MULTIPLY, DIVIDE, COMPARE, CARRY, MULADD, MISC):
    pass


