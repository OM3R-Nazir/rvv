from rvv.base import BaseRVV

class MULADD(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## Same Width
    ##
    
    def vmacc_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', 'uuu', masked)
        vvd[mask] = ((vs1 * vs2) + vvd)[mask]
        self._post_op()
    
    def vmacc_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'uuu', masked)
        vvd[mask] = ((rs1 * vs2) + vvd)[mask]
        self._post_op()
    
    def vnmsac_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', 'uuu', masked)
        vvd[mask] = (-(vs1 * vs2) + vvd)[mask]
        self._post_op()
    
    def vnmsac_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'uuu', masked)
        vvd[mask] = (-(rs1 * vs2) + vvd)[mask]
        self._post_op()
        
    def vmadd_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', 'uuu', masked)
        vvd[mask] = ((vvd * vs1) + vs2)[mask]
        self._post_op()
        
    def vmadd_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'uuu', masked)
        vvd[mask] = ((vvd * rs1) + vs2)[mask]
        self._post_op()
        
    def vnmsub_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', 'uuu', masked)
        vvd[mask] = (-(vvd * vs1) + vs2)[mask]
        self._post_op()
    
    def vnmsub_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'uuu', masked)
        vvd[mask] = (-(vvd * rs1) + vs2)[mask]
        self._post_op()
        
    ##
    ## Widening
    ##
    
    def vwmacc_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'wvv', 'sss', masked)
        vvd[mask] = ((self._sext(vs1) * self._sext(vs2)) + vvd)[mask]
        self._post_op()
        
    def vwmacc_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'sss', masked)
        vvd[mask] = ((self._sext(rs1) * self._sext(vs2)) + vvd)[mask]
        self._post_op()
    
    def vwmaccsu_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', 'ssu', masked)
        vvd[mask] = ((self._sext(vs1) * self._zext(vs2)) + vvd)[mask]
        self._post_op()
    
    def vwmaccsu_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'ssu', masked)
        vvd[mask] = ((self._sext(rs1) * self._zext(vs2)) + vvd)[mask]
        self._post_op()
        
    def vwmaccus_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'usu', masked)
        vvd[mask] = ((self._zext(rs1) * self._sext(vs2)) + vvd)[mask]
        self._post_op()
    
    def vwmaccu_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', 'uuu', masked)
        vvd[mask] = ((self._zext(vs1) * self._zext(vs2)) + vvd)[mask]
        self._post_op()
    
    def vwmaccu_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'uuu', masked)
        vvd[mask] = ((self._zext(rs1) * self._zext(vs2)) + vvd)[mask]
        self._post_op()