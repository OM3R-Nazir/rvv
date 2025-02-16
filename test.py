from rvv import RVV
import numpy as np

rvv = RVV(debug=True, debug_vb_as_v=False)

sew = 8
dtype = f"int{sew}"

v0 = np.array([1,1,1,0,1,0,1,0], dtype=np.bool_)
v1 = np.arange(8, dtype=dtype)
v2 = np.array([15, 0, 127, 0, 0, 0, 0, 2], dtype=dtype)

rvv.vsetvli(avl=8, e=sew, m=1)
rvv.vlm(0, rvv.bools_to_vm(v0))
rvv.vle(1,v1)
rvv.vle(2,v2)
rvv.li(3, 3)
rvv.vsadd_vv(3,2,1)
