from rvv.base import BaseRVV

class Conversion(BaseRVV):
    
    def vwcvt_x_x_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'wv', 'ss', masked)
        vd[mask] = self._sext(vsrc)
        self._post_op()
    
    def vwcvtu_x_x_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'wv', 'uu', masked)
        vd[mask] = self._zext(vsrc)
        self._post_op()
    
    def vncvt_x_x_w(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vw', 'ss', masked)
        vd[mask] = self.SEW.idtype(vsrc)
        self._post_op()
    
    def vncvtu_x_x_w(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vw', 'uu', masked)
        vd[mask] = self.SEW.udtype(vsrc)
        self._post_op()
    
    def vfwcvt_f_f_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vw', 'ff', masked)
        vd[mask] = self.SEW.fdtype(vsrc)
        self._post_op()
        
    def vfncvt_f_f_w(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'wv', 'ff', masked)
        vd[mask] = self.WSEW.fdtype(vsrc)
        self._post_op()
        
    def vfcvt_f_x_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vv', 'fs', masked)
        vd[mask] = self.SEW.fdtype(vsrc)
        self._post_op()
    
    def vfcvt_f_xu_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vv', 'fu', masked)
        vd[mask] = self.SEW.fdtype(vsrc)
        self._post_op()
    
    def vfncvt_f_x_w(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vw', 'fs', masked)
        vd[mask] = self.SEW.fdtype(vsrc)
        self._post_op()
    
    def vfncvt_f_xu_w(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vw', 'fu', masked)
        vd[mask] = self.SEW.fdtype(vsrc)
        self._post_op()
    
    def vfwcvt_f_x_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'wv', 'fs', masked)
        vd[mask] = self.WSEW.fdtype(vsrc)
        self._post_op()
    
    def vfwcvt_f_xu_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'wv', 'fu', masked)
        vd[mask] = self.WSEW.fdtype(vsrc)
        self._post_op()
        
    def vfcvt_x_f_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vv', 'sf', masked)
        vd[mask] = self.SEW.idtype(vsrc)
        self._post_op()
        
    def vfcvt_xu_f_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vv', 'uf', masked)
        vd[mask] = self.SEW.udtype(vsrc)
        self._post_op()
    
    def vfncvt_x_f_w(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vw', 'sf', masked)
        vd[mask] = self.SEW.idtype(vsrc)
        self._post_op()
    
    def vfncvt_xu_f_w(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'vw', 'uf', masked)
        vd[mask] = self.SEW.udtype(vsrc)
        self._post_op()
    
    def vfwcvt_x_f_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'wv', 'sf', masked)
        vd[mask] = self.WSEW.idtype(vsrc)
        self._post_op()
    
    def vfwcvt_xu_f_v(self, vd, vsrc, masked):
        vd, vsrc, mask = self._init_ops_uni(vd, vsrc, 'wv', 'uf', masked)
        vd[mask] = self.WSEW.udtype(vsrc)
        self._post_op()
        