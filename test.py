from rvv import RVV
import numpy as np

rvv = RVV(debug=True)

v1 = np.array([2,3,4,3,3,3,3,3], dtype=np.int8)
v2 = np.array([3,3,1,3,3,3,3,3], dtype=np.int8)


rvv.vsetvli(8, 8, 1)
rvv.vle(1,v1)
rvv.vle(2,v2)
rvv.vmseq_vv(3,1,2)