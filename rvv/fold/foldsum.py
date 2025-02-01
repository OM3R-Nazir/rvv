from rvv.base import BaseRVV

class FoldSum(BaseRVV): 
    
    def vredsum_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'uuu', masked)
        vd[0] = scalar[0] + vector[mask].sum()
        self._post_op()
    
    def vfredosum_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'fff', masked)
        vd[0] = scalar[0] + vector[mask].sum()
        self._post_op()
    
    def vfredusum_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'svs', 'fff', masked)
        
        def process(items):
            if len(items) == 1:
                return items[0]
            mid = len(items) // 2
            resA = process(items[:mid])
            resB = process(items[mid:])
            return resA + resB
        
        all_items = [scalar[0]] + list(vector[mask])
        
        vd[0] = process(all_items)
        self._post_op()
    
    def vwredsum_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'dvd', 'uuu', masked)
        vd[0] = scalar[0] + vector[mask].sum()
        self._post_op()
    
    def vwfredosum_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'dvd', 'fff', masked)
        vd[0] = scalar[0] + vector[mask].sum()
        self._post_op()
    
    def vwfredusum_vs(self, vd, vector, scalar, masked=False):
        vd, vector, scalar, mask = self._init_ops(vd, vector, scalar, 'dvd', 'fff', masked)
        
        def process(items):
            if len(items) == 1:
                return items[0]
            mid = len(items) // 2
            resA = process(items[:mid])
            resB = process(items[mid:])
            return resA + resB
        
        all_items = [scalar[0]] + list(vector[mask])
        
        vd[0] = process(all_items)
        self._post_op()