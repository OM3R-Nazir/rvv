from rvv import RVV
import numpy as np

rvv = RVV()

v1 = np.array([2]*8, dtype=np.int8)
v0 = np.array([3], dtype=np.int8)
rvv.vsetvli(1, 8, 1)
rvv.vle(0, v0)

rvv.vsetvli(8, 8, 1)
rvv.vle(1, v1)
rvv.vle(2, v1)
rvv.vmul_vv(3, 1, 2, True)

print(rvv.vec(3))