from rvv import RVV
import numpy as np

rvv = RVV()

v1 = np.array(range(10), dtype=np.uint8)

rvv.vsetvli(10, 8, 1)
rvv.vle(1, v1)
rvv.vle(2, v1)
rvv.vadd_vv(3, 1, 2)
rvv.vsub_vv(3, 3, 1)

print(rvv.vec(3))