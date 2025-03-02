from rvv.base import BaseRVV

class Logical(BaseRVV):
    def vmand_mm(self, vd, op1, op2):
        vd, op1, op2, _ = self._init_ops(vd, op1, op2, 'mmm', 'uuu', False)
        vd[:] = op1 & op2
        self._post_op()
    
    def vmandn_mm(self, vd, op1, op2):
        vd, op1, op2, _ = self._init_ops(vd, op1, op2, 'mmm', 'uuu', False)
        vd[:] = op1 & ~op2
        self._post_op()
    
    def vmnand_mm(self, vd, op1, op2):
        vd, op1, op2, _ = self._init_ops(vd, op1, op2, 'mmm', 'uuu', False)
        vd[:] = ~(op1 & op2)
        self._post_op()
    
    def vmnor_mm(self, vd, op1, op2):
        vd, op1, op2, _ = self._init_ops(vd, op1, op2, 'mmm', 'uuu', False)
        vd[:] = ~(op1 | op2)
        self._post_op()
    
    def vmnot_m(self, vd, op1):
        vd, op1, _ = self._init_ops_uni(vd, op1, 'mm', 'uuu', False)
        vd[:] = ~op1
        self._post_op()
    
    def vmor_mm(self, vd, op1, op2):
        vd, op1, op2, _ = self._init_ops(vd, op1, op2, 'mmm', 'uuu', False)
        vd[:] = op1 | op2
        self._post_op()
    
    def vmorn_mm(self, vd, op1, op2):
        vd, op1, op2, _ = self._init_ops(vd, op1, op2, 'mmm', 'uuu', False)
        vd[:] = op1 | ~op2
        self._post_op()
    
    def vmxnor_mm(self, vd, op1, op2):
        vd, op1, op2, _ = self._init_ops(vd, op1, op2, 'mmm', 'uuu', False)
        vd[:] = ~(op1 ^ op2)
        self._post_op()
    
    def vmxor_mm(self, vd, op1, op2):
        vd, op1, op2, _ = self._init_ops(vd, op1, op2, 'mmm', 'uuu', False)
        vd[:] = op1 ^ op2
        self._post_op()
    