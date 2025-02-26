from rvv import RVV
import numpy as np

rvv = RVV(debug=True, debug_vb_as_v=False)

sew = 16
dtype = f"int{sew}"

v0 = np.array([1,1,1,0,1,0,1,0], dtype=np.bool_)
v1 = np.arange(20, dtype=dtype)
v1 *= 10
v2 = np.array([16, 10, 6, 4, 2, 8, 14, 12], dtype=dtype)
mem = np.zeros(1000, dtype=np.uint8)

rvv.vsetvli(avl=8, e=sew, m=1)
rvv.vlm_v(0, rvv.bools_to_vm(v0), 0)
rvv.vle(2, v2)
rvv.vloxei16_v(1, 2, v1, 0)
rvv.vsoxei16_v(1, 2, mem, 10)

# mem = mem.view(dtype)
for i, val in enumerate(mem):
    print(f" {i} : {val}")
    if i == 30:
        break
    
# rvv.vle(2,v2)
# rvv.li(3, 3)
# rvv.vsadd_vv(3,2,1)

