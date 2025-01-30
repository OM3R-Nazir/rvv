from rvv.base import BaseRVV

class ADD(BaseRVV):
    
    ##
    ## Same Width
    ##
    
    def vadd_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        vvd[mask] = (vop1 + vop2)[mask]
        self._post_op()
        
    def vadd_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        vvd[mask] = (vop1 + xop2)[mask]
        self._post_op()
        
    ##
    ## Saturating
    ##

    def vsadd_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)

        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(int(vop1[i]) + int(vop2[i]))
            
        self._post_op()

    def vsadd_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(int(vop1[i]) + int(xop2))
        
        self._post_op()

    def vsaddu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)

        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._uclip(int(vop1[i]) + int(vop2[i]))
            
        self._post_op()

    def vsaddu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._uclip(int(vop1[i]) + int(xop2))
        
        self._post_op()

    ##
    ## Widening
    ##

    def vwadd_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wvv', 'sss', masked)
        vvd[mask] = (self._sext(vop1) + self._sext(vop2))[mask]
        self._post_op()

    def vwadd_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wvx', 'sss', masked)
        vvd[mask] = (self._sext(vop1) + self._sext(xop2))[mask]
        self._post_op()

    def vwadd_wv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wwv', 'sss', masked)
        vvd[mask] = vop1 + self._sext(vop2)
        self._post_op()

    def vwadd_wx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wwx', 'sss', masked)
        vvd[mask] = (vop1 + self._sext(xop2))[mask]
        self._post_op()        

    def vwaddu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wvv', 'uuu', masked)
        vvd[mask] = (self._zext(vop1) + self._zext(vop2))[mask]
        self._post_op()

    def vwaddu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wvx', 'uuu', masked)
        vvd[mask] = (self._zext(vop1) + self._zext(xop2))[mask]
        self._post_op()

    def vwaddu_wv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'wwv', 'uuu', masked)
        vvd[mask] = vop1 + self._zext(vop2)
        self._post_op()

    def vwaddu_wx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'wwx', 'uuu', masked)
        vvd[mask] = (vop1 + self._zext(xop2))[mask]
        self._post_op()