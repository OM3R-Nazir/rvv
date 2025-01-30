from rvv import RVV
import numpy as np

rvv = RVV(debug=True, debug_vb_as_v=False)

# v1 = np.array([4.2,6,4.3,3,3,3,3,3], dtype=np.float32)
# v2 = np.array([2.3,3,1,2.1,3,3,3,3], dtype=np.float32)
v0 = np.array([1,1,1,0,1,0,1,0], dtype=np.bool_)
v1 = np.array([0,1,1,0,1,0,0,0], dtype=np.bool_)
v2 = np.array([1,0,1,0,1,1,1,0], dtype=np.bool_)

rvv.vsetvli(avl=7, e=8, m=1)
rvv.vlm(0, rvv.bools_to_vm(v0[:7]))
rvv.vlm(1, rvv.bools_to_vm(v1[:7]))
rvv.vlm(2, rvv.bools_to_vm(v2[:7]))
rvv.vmandn_mm(3,1,2)
rvv.vnot_v(3,1)
# rvv.vsetvli(avl=8, e=32, m=1)
# rvv.vle(1,v1)
# rvv.vle(2,v2)
# rvv.flw(3, 3.3)
# rvv.vfadd_vf(4,1,3)