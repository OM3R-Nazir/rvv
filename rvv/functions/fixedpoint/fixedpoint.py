from rvv.base import BaseRVV

class FixedPoint(BaseRVV):
    
    ##
    ## Saturating Addition
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
    ## Saturating Subtraction    
    ##    

    def vssub_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(int(vop1[i]) - int(vop2[i]))
        self._post_op()

    def vssub_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(int(vop1[i]) - int(xop2))
        self._post_op()

    def vssubu_vv(self, vd, op1, op2, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._uclip(int(vop1[i]) - int(vop2[i]))
        self._post_op()

    def vssubu_vx(self, vd, op1, op2, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._uclip(int(vop1[i]) - int(xop2))
        self._post_op()
    
    ##
    ## Averaging addition
    ##
    
    def vaadd_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_rounding(int(vop1[i]) + int(vop2[i]), vxrm)
        self._post_op()
    
    def vaadd_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_rounding(int(vop1[i]) + int(xop2), vxrm)
        self._post_op()
    
    def vaaddu_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_rounding(int(vop1[i]) + int(vop2[i]), vxrm)
        self._post_op()
    
    def vaaddu_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_rounding(int(vop1[i]) + int(xop2), vxrm)
        self._post_op()
        
    ##
    ## Averaging subtraction
    ##
    
    def vasub_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_rounding(int(vop1[i]) - int(vop2[i]), vxrm)
        self._post_op()
    
    def vasub_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_rounding(int(vop1[i]) - int(xop2), vxrm)
        self._post_op()
        
    def vasubu_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_rounding(int(vop1[i]) - int(vop2[i]), vxrm)
        self._post_op()
        
    def vasubu_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_rounding(int(vop1[i]) - int(xop2), vxrm)
        self._post_op()
    
    ##
    ## Fractional Rounding and Saturating Multiplication
    ##
    
    def vsmul_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(self.vxrm_right_shift(int(vop1[i]) * int(vop2[i]), self.SEWC.SEW, vxrm))
                
        self._post_op()
    
    def vsmul_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(self.vxrm_right_shift(int(vop1[i]) * int(xop2), self.SEWC.SEW, vxrm))
        self._post_op()
    
    ##
    ## Clipping and Narrowing
    ##
    
    def vnclip_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(self.vxrm_right_shift(int(vop1[i]), (self.SEWC.SEW - 1) & int(vop2[i]), vxrm))
        self._post_op()
    
    def vnclip_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(self.vxrm_right_shift(int(vop1[i]), (self.SEWC.SEW - 1) & int(xop2), vxrm))
        self._post_op()
    
    def vnclipu_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(self.vxrm_right_shift(int(vop1[i]), (self.SEWC.SEW - 1) & int(vop2[i]), vxrm))
        self._post_op()
    
    def vnclipu_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self._iclip(self.vxrm_right_shift(int(vop1[i]), (self.SEWC.SEW - 1) & int(xop2), vxrm))
        self._post_op()
    
    ##
    ## Right Shift
    ##
    
    def vssra_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_right_shift(int(vop1[i]), int(vop2[i]), vxrm)
        self._post_op()
    
    def vssra_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'sss', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_right_shift(int(vop1[i]), int(xop2), vxrm)
        self._post_op()
        
    def vssrl_vv(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, vop2, mask = self._init_ops(vd, op1, op2, 'vvv', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_right_shift(int(vop1[i]), int(vop2[i]), vxrm)
        self._post_op()
    
    def vssrl_vx(self, vd, op1, op2, vxrm, masked=False):
        vvd, vop1, xop2, mask = self._init_ops(vd, op1, op2, 'vvx', 'uuu', masked)
        for i in range(self.VL):
            if mask[i]:
                vvd[i] = self.vxrm_right_shift(int(vop1[i]), int(xop2), vxrm)
        self._post_op()
    