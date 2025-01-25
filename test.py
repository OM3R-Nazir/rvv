from rvv import RVV
import numpy as np

rvv = RVV(debug=True, debug_vb_as_v=False)

v1 = np.array([4,6,4,3,3,3,3,3], dtype=np.uint8)
v2 = np.array([2,3,1,2,3,3,3,3], dtype=np.int8)
v0 = np.array([1,0,1,0,1,0,0,0], dtype=np.bool_)

rvv.vsetvli(avl=8, e=8, m=1)
rvv.vlm(0, rvv.bools_to_vm(v0))
rvv.vle(1,v1)
rvv.vle(2,v2)
rvv.vsetvli(avl=8, e=8, m=1)
rvv.li(3, 15)
rvv.vadd_vx(3,1,3)