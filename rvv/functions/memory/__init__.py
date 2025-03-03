from rvv.functions.memory.loadstore import LoadStore
from rvv.functions.memory.indexed import Indexed
from rvv.functions.memory.segmented import Segmented

class RVVMemory(LoadStore, Indexed, Segmented):
    pass