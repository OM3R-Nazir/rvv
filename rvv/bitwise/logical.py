from rvv.base import BaseRVV

class Logical(BaseRVV):
    
    def vand_vv(self, vd, op1, op2, masked = False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vd[mask] = (op1 & op2)[mask]
        self._post_op()
    
    def vand_vx(self, vd, op1, op2, masked = False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vd[mask] = (op1 & op2)[mask]
        self._post_op()
    
    def vor_vv(self, vd, op1, op2, masked = False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vd[mask] = (op1 | op2)[mask]
        self._post_op()
    
    def vor_vx(self, vd, op1, op2, masked = False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vd[mask] = (op1 | op2)[mask]
        self._post_op()
    
    def vxor_vv(self, vd, op1, op2, masked = False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vd[mask] = (op1 ^ op2)[mask]
        self._post_op()
    
    def vxor_vx(self, vd, op1, op2, masked = False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vd[mask] = (op1 ^ op2)[mask]
        self._post_op()
    
    def vnot_v(self, vd, op1, masked = False):
        vd, op1, mask = self._init_ops_uni(vd, op1, 'vv', 'uu', masked)
        vd[mask] = ~op1[mask]
        self._post_op()

            