from rvv.base import BaseRVV
import numpy as np

class FoldMisc(BaseRVV):
    
    def vredand_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'uuu', masked)
        acc = scalar[0]
        for i in range(self.VL):
            if mask[i]:
                acc = acc & vector[i]
        vd[0] = acc
        self._post_op()
        
    def vredor_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'uuu', masked)
        acc = scalar[0]
        for i in range(self.VL):
            if mask[i]:
                acc = acc | vector[i]
        vd[0] = acc
        self._post_op()
    
    
    def vredxor_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'uuu', masked)
        acc = scalar[0]
        for i in range(self.VL):
            if mask[i]:
                acc = acc ^ vector[i]
        vd[0] = acc
        self._post_op()
    
    def vredmax_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'sss', masked)
        vd[0] = np.max([np.max(vector[mask]), scalar[0]])
        self._post_op()
        
    def vredmaxu_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'uuu', masked)
        vd[0] = np.max([np.max(vector[mask]), scalar[0]])
        self._post_op()
        
    def vredmin_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'sss', masked)
        vd[0] = np.min([np.min(vector[mask]), scalar[0]])
        self._post_op()
    
    def vredminu_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'uuu', masked)
        vd[0] = np.min([np.min(vector[mask]), scalar[0]])
        self._post_op()