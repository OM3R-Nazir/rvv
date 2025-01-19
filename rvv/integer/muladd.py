from rvv.base import BaseRVV

class MULADD(BaseRVV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    ##
    ## Same Width
    ##
    
    def vmacc_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', False, masked)
        vvd[mask] = ((vs1 * vs2) + vvd)[mask]
        self._debug_vd(vvd, vd)
    
    def vmacc_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', False, masked)
        vvd[mask] = ((rs1 * vs2) + vvd)[mask]
        self._debug_vd(vvd, vd)
    
    def vnmsac_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', False, masked)
        vvd[mask] = (-(vs1 * vs2) + vvd)[mask]
        self._debug_vd(vvd, vd)
    
    def vnmsac_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', False, masked)
        vvd[mask] = (-(rs1 * vs2) + vvd)[mask]
        self._debug_vd(vvd, vd)
        
    def vmadd_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', False, masked)
        vvd[mask] = ((vvd * vs1) + vs2)[mask]
        self._debug_vd(vvd, vd)
        
    def vmadd_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', False, masked)
        vvd[mask] = ((vvd * rs1) + vs2)[mask]
        self._debug_vd(vvd, vd)
        
    def vnmsub_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', False, masked)
        vvd[mask] = (-(vvd * vs1) + vs2)[mask]
        self._debug_vd(vvd, vd)
    
    def vnmsub_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', False, masked)
        vvd[mask] = (-(vvd * rs1) + vs2)[mask]
        self._debug_vd(vvd, vd)
        
    ##
    ## Widening
    ##
    
    def vwmacc_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'wvv', True, masked)
        vvd[mask] = ((self._sext(vs1) * self._sext(vs2)) + vvd)[mask]
        self._debug_vd(vvd, vd)
        
    def vwmacc_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', True, masked)
        vvd[mask] = ((self._sext(rs1) * self._sext(vs2)) + vvd)[mask]
        self._debug_vd(vvd, vd)
    
    def vwmaccsu_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', 'ssu', masked)
        vvd[mask] = ((self._sext(vs1) * self._zext(vs2)) + vvd)[mask]
        self._debug_vd(vvd, vd)
    
    def vwmaccsu_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'ssu', masked)
        vvd[mask] = ((self._sext(rs1) * self._zext(vs2)) + vvd)[mask]
        self._debug_vd(vvd, vd)
        
    def vwmaccus_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', 'usu', masked)
        vvd[mask] = ((self._zext(rs1) * self._sext(vs2)) + vvd)[mask]
        self._debug_vd(vvd, vd)
    
    def vwmaccu_vv(self, vd, vs1, vs2, masked):
        vvd, vs1, vs2, mask = self._init_ops(vd, vs1, vs2, 'vvv', False, masked)
        vvd[mask] = ((self._zext(vs1) * self._zext(vs2)) + vvd)[mask]
        self._debug_vd(vvd, vd)
    
    def vwmaccu_vx(self, vd, rs1, vs2, masked):
        vvd, rs1, vs2, mask = self._init_ops(vd, rs1, vs2, 'vxv', False, masked)
        vvd[mask] = ((self._zext(rs1) * self._zext(vs2)) + vvd)[mask]
        self._debug_vd(vvd, vd)