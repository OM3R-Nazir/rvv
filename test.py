from rvv import RVV
import numpy as np
from rvv.extensions import ZVFH

rvv = RVV(debug=True, debug_vb_as_v=False)
rvv = ZVFH(rvv).rvv
sew = 16
dtype = f"float{sew}"

v0 = np.array([1,1,1,0,1,0,1,0], dtype=np.bool_)
v1 = np.arange(20, dtype=dtype)
v1 *= 10
v2 = np.array([16, 10, 6, 4, 2, 8, 14, 12], dtype=dtype)*4
mem_source = np.arange(100, dtype=dtype)
mem_dest = np.zeros(1000, dtype=np.uint8)

rvv.vsetvli(avl=8, e=sew, m=1)
rvv.vlm_v(0, rvv.bools_to_vm(v0), 0)
rvv.vle(3, v2)
rvv.vfadd_vf(3, 3, 3)
print(rvv.vec(3).view(dtype))

# rvv.vloxseg2ei16_v(1, 3, mem_source, 0)
# rvv.vsoxseg2ei16_v(1, 3, mem_dest, 0)

# mem_dest = mem_dest.view(dtype)
# for i in range(mem_dest.size // 10):
#     print(mem_dest[i*10 : i*10 + 10])
#     if i == 8: break
    
# rvv.vle(2,v2)
# rvv.li(3, 3)
# rvv.vsadd_vv(3,2,1)

