from rvv.memory.loadstore import LoadStore
from rvv.memory.indexed import Indexed
from rvv.memory.segmented import Segmented

class RVVMemory(LoadStore, Indexed, Segmented):
    pass