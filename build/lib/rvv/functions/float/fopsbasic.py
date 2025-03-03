from rvv.base import BaseRVV

class FOpsBasic(BaseRVV):
        
    def vfadd_vv(self, vd, op1, op2, masked=False):
        vd, op1, op2, masked = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vd[masked] = (op1 + op2)[masked]
        self._post_op()
    
    def vfadd_vf(self, vd, op1, op2, masked=False):
        vd, op1, xop2, masked = self._init_ops(vd, op1, op2, 'vvf', 'fff', masked)
        vd[masked] = (op1 + xop2)[masked]
        self._post_op()
        
    def vfsub_vv(self, vd, op1, op2, masked=False):
        vd, op1, op2, masked = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vd[masked] = (op1 - op2)[masked]
        self._post_op()
        
    def vfsub_vf(self, vd, op1, op2, masked=False):
        vd, op1, xop2, masked = self._init_ops(vd, op1, op2, 'vvf', 'fff', masked)
        vd[masked] = (op1 - xop2)[masked]
        self._post_op()
    
    def vfrsub_vf(self, vd, op1, op2, masked=False):
        vd, op1, xop2, masked = self._init_ops(vd, op1, op2, 'vvf', 'fff', masked)
        vd[masked] = (xop2 - op1)[masked]
        self._post_op()
    
    def vfmul_vv(self, vd, op1, op2, masked=False):
        vd, op1, op2, masked = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vd[masked] = (op1 * op2)[masked]
        self._post_op()
    
    def vfmul_vf(self, vd, op1, op2, masked=False):
        vd, op1, xop2, masked = self._init_ops(vd, op1, op2, 'vvf', 'fff', masked)
        vd[masked] = (op1 * xop2)[masked]
        self._post_op()
    
    def vfdiv_vv(self, vd, op1, op2, masked=False):
        vd, op1, op2, masked = self._init_ops(vd, op1, op2, 'vvv', 'fff', masked)
        vd[masked] = (op1 / op2)[masked]
        self._post_op()
    
    def vfdiv_vf(self, vd, op1, op2, masked=False):
        vd, op1, xop2, masked = self._init_ops(vd, op1, op2, 'vvf', 'fff', masked)
        vd[masked] = (op1 / xop2)[masked]
        self._post_op()
    
    def vfrdiv_vf(self, vd, op1, op2, masked=False):
        vd, op1, xop2, masked = self._init_ops(vd, op1, op2, 'vvf', 'fff', masked)
        vd[masked] = (xop2 / op1)[masked]
        self._post_op()
        