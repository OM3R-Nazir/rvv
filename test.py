from rvv import RVV
import numpy as np

rvv = RVV()

v1 = np.array([2**40]*10, dtype=np.int64)

rvv.vsetvli(10, 64, 1)
rvv.vle(1, v1)
rvv.vle(2, v1)
rvv.vmulh_vv(3, 1, 2)

print(rvv.vec(3))