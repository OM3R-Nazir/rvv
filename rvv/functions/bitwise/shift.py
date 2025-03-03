from rvv.base import BaseRVV

class Shift(BaseRVV):

    def vsll_vv(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvv', 'ssu', masked)
        vd[mask] = (op1 << op2)[mask]
        self._post_op()
    
    def vsll_vx(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvx', 'ssu', masked)
        vd[mask] = (op1 << op2)[mask]
        self._post_op()

    def vsra_vv(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvv', 'ssu', masked)
        vd[mask] = (op1 >> op2)[mask]
        self._post_op()
    
    def vsra_vx(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvx', 'ssu', masked)
        vd[mask] = (op1 >> op2)[mask]
        self._post_op()
    
    def vsra_wv(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vwv', 'ssu', masked)
        vd[mask] = (self._SEWC.idtype(op1 >> self._WSEWC.udtype(op2)))[mask]
        self._post_op()
    
    def vsra_wx(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vwx', 'ssu', masked)
        vd[mask] = (self._SEWC.idtype(op1 >> self._WSEWC.udtype(op2)))[mask]
        self._post_op()
    
    def vsrl_vv(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vd[mask] = (op1 >> op2)[mask]
        self._post_op()
    
    def vsrl_vx(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vd[mask] = (op1 >> op2)[mask]
        self._post_op()
    
    def vsrl_wv(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vwv', 'uuu', masked)
        vd[mask] = (self._SEWC.udtype(op1 >> self._WSEWC.udtype(op2)))[mask]
        self._post_op()
    
    def vsrl_wx(self, vd, op1, op2, masked=False):
        vd, op1, op2, mask = self._init_ops(vd, op1, op2, 'vwx', 'uuu', masked)
        vd[mask] = (self._SEWC.udtype(op1 >> self._WSEWC.udtype(op2)))[mask]
        self._post_op()
    
    