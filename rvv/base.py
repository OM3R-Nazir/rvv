import numpy as np
from rvv.utils.sew import SEWC
import inspect

class BaseRVV:
    
    def __init__(self, VLEN: int = 2048, debug = False, debug_vb_as_v = False) -> None:
        self.VLEN : int = VLEN
        self.VLENB : int = VLEN // 8
        self.VRF : np.ndarray = np.zeros(self.VLENB * 32, dtype=np.uint8)
        self.SEW : SEWC = None
        self.LMUL : int = None
        self.VL : int = None
        self.VLMAX : int = None
        self._valid_sews : list[int] = [8, 16, 32, 64]
        self._valid_lmuls : list[int] = [1, 2, 4, 8]
        
        self._init_vec_regs()
        self.debug = debug
        self.debug_vb_as_v = debug_vb_as_v
        
    def _init_vec_regs(self):
        self.vsetvli(0, 8, 1)
        
        for i in range(32):
            v = self.vec(i)
            for k in range(self.VL):
                v[k] = k
    
    def _initer(self, optype, op, signed):
        if optype == 'v': return self.vec(op, signed)
        elif optype == 'w': return self.vecw(op, signed)
        elif optype == 'x': return self.scalar(op, signed)
        elif optype == 'm': return self.vecm(op)
        else: raise ValueError(f"Invalid Operand Type {optype}")
    
    def _init_ops_uni(self, vd, op1, optypes, signed, masked):
        self._debug_operation()
        if type(signed) == bool: signed = 'ss' if signed else 'uu'    
            
        tvd = self._initer(optypes[0], vd, signed)
        top1 = self._initer(optypes[1], op1, signed)
        
        ops = [vd, op1]
        vector_ops = [ops[i] for i in range(2) if optypes[i] != 'x']
        
        if masked:
            if 0 in vector_ops:
                raise ValueError("Invalid Vector Register Number 0 for Masked Operation")
            mask = self.vm_to_bools(self.vecm(0))
        else:
            mask = np.ones(self.VL, dtype=np.bool_)
        
        self._debug_val(top1, 1, optypes[1], 'op1')
        self._debug_mask(mask, masked)
        
        return tvd, top1, mask
    
    def _init_ops(self, vd, op1, op2, optypes, signed, masked):
        self._debug_operation()
        if type(signed) == bool: signed = 'sss' if signed else 'uuu'    
            
        tvd = self._initer(optypes[0], vd, signed[0])
        top1 = self._initer(optypes[1], op1, signed[1])
        top2 = self._initer(optypes[2], op2, signed[2])
        
        ops = [vd, op1, op2]
        vector_ops = [ops[i] for i in range(3) if optypes[i] != 'x']
        
        if masked:
            if 0 in vector_ops:
                raise ValueError("Invalid Vector Register Number 0 for Masked Operation")
            mask = self.vm_to_bools(self.vecm(0))
        else:
            mask = np.ones(self.VL, dtype=np.bool_)
        
        self._debug_val(top1, 1, optypes[1], 'op1')
        self._debug_val(top2, 2, optypes[2], 'op2')
        self._debug_mask(mask, masked)
        
        return tvd, top1, top2, mask

        
    def _init_ops_tri(self, vd, op1, op2, op3, optypes, signed, masked):
        self._debug_operation()
        if type(signed) == bool: signed = 'ssss' if signed else 'uuuu'    
            
        tvd = self._initer(optypes[0], vd, signed[0])
        top1 = self._initer(optypes[1], op1, signed[1])
        top2 = self._initer(optypes[2], op2, signed[2])
        top3 = self._initer(optypes[3], op3, signed[3])
        
        ops = [vd, op1, op2, op3]
        vector_ops = [ops[i] for i in range(3) if optypes[i] != 'x']
        
        if masked:
            if 0 in vector_ops:
                raise ValueError("Invalid Vector Register Number 0 for Masked Operation")
            mask = self.vm_to_bools(self.vecm(0))
        else:
            mask = np.ones(self.VL, dtype=np.bool_)
        
        self._debug_val(top1, 1, optypes[1], 'op1')
        self._debug_val(top2, 2, optypes[2], 'op2')
        self._debug_val(top3, 3, optypes[3], 'op3')
        self._debug_mask(mask, masked)
        
        return tvd, top1, top2,top3, mask
    
    def _init_ops_ext(self, vd, op1, optype, signed, masked):
        self._debug_operation()
           
        if optype == 'vf2':
            if self.SEW.SEW < 16: raise ValueError("EXT_VF2 requires SEW >= 16")
            op1_sew = self.SEW.get_lower_sew()
        elif optype == 'vf4':
            if self.SEW.SEW < 32: raise ValueError("EXT_VF4 requires SEW >= 32")
            op1_sew = self.SEW.get_lower_sew().get_lower_sew()
        elif optype == 'vf8':
            if self.SEW.SEW < 64: raise ValueError("EXT_VF8 requires SEW = 64")
            op1_sew = self.SEW.get_lower_sew().get_lower_sew().get_lower_sew()
            
        tvd = self.vec(vd, signed)
        top1 = self.vec(op1, signed)
        
        if signed:
            top1 = top1.view(op1_sew.idtype)
        else:
            top1 = top1.view(op1_sew.udtype)
        
        top1 = top1[:self.VL]
        
        ops = [vd, op1]
        vector_ops = [ops[i] for i in range(2) if optype[i] != 'x']
        
        if masked:
            if 0 in vector_ops:
                raise ValueError("Invalid Vector Register Number 0 for Masked Operation")
            mask = self.vm_to_bools(self.vecm(0))
        else:
            mask = np.ones(self.VL, dtype=np.bool_)
        
        self._debug_val(top1, 1, 'v', 'op1')
        self._debug_mask(mask, masked)
        
        return tvd, top1, mask
    
    def _debug_val(self, val, val_num, val_type, op_type):
        if self.debug:
            if val_type == 'x':
                print(f"{val_type + op_type:>5}   {val_num:02}: ", val)
            elif val_type == 'm':
                val_type = 'vm'
                if not self.debug_vb_as_v: val = self.vm_to_bools(val).view(np.uint8)
                print(f"{val_type + op_type:>5} {val_type:>2}{val_num:02}: ", val)
            elif val_type == 'v' or val_type == 'w':
                print(f"{val_type + op_type:>5} {val_type:>2}{val_num:02}: ", val)
            else:
                raise ValueError(f"Invalid Value Type {val_type}")
            
    def _debug_vd(self, vec, vec_num):
        if self.debug:
            self._debug_val(vec, vec_num, 'v', 'd')
                
    def _debug_vmd(self, vec, vec_num):
        if self.debug:
            self._debug_val(vec, vec_num, 'm', 'd')
    
    def _debug_mask(self, mask, masked):
        if self.debug and masked:
            if self.debug_vb_as_v: mask = self.bools_to_vm(mask)
            print(f"vmask  vm0:  {mask.view(np.uint8)}")
    
    def _debug_operation(self):
        if self.debug:
            print(f"\n Operation: {inspect.currentframe().f_back.f_back.f_code.co_name}")
            print(f"{'='*30}")
    
    def _debug_print(self, *args):
        if self.debug:
            print(*args)
    
    def _iclip(self, num):
        return np.clip(num, self.SEW.imin, self.SEW.imax)    
    
    def _uclip(self, num):
        return np.clip(num, self.SEW.umin, self.SEW.umax)    
    
    def _sext(self, num):
        return self.WSEW.idtype(self.SEW.idtype(num))
    
    def _zext(self, num):
        return self.WSEW.udtype(self.SEW.udtype(num)) 

    def bools_to_vm(self, bool_array):
        if len(bool_array) != self.VL:
            raise ValueError(f"Invalid Length of Mask {len(bool_array)} for VL {self.VL}")
        
        if len(bool_array) % 8 != 0:
            bool_array = np.pad(bool_array, (0, 8 - len(bool_array) % 8))
            
        reversed_bool_array = np.zeros_like(bool_array)
        for i in range(0, len(bool_array), 8):
            for j in range(8):
                reversed_bool_array[i+j] = bool_array[i+7-j]
                
        vbool = np.packbits(reversed_bool_array).view(np.uint8)
        return vbool
        
    def vm_to_bools(self, vbool):
        vbool = vbool.view(np.uint8)
        
        reversed_bool_array = np.unpackbits(vbool)
        bool_array = np.zeros_like(reversed_bool_array)
        for i in range(0, len(reversed_bool_array), 8):
            for j in range(8):
                bool_array[i+j] = reversed_bool_array[i+7-j]

        bool_array = bool_array[:self.VL].view(np.bool_)
        
        return bool_array
    
    def vm_masked(self, vmd, vms, mask):
        vmdb = self.vm_to_bools(vmd)
        vmb = self.vm_to_bools(vms)
        vmdb[mask] = vmb[mask]
        vmd[:] = self.bools_to_vm(vmdb)
        return vmd
        
    def vec(self, vi, signed=False):
        
        if vi % self.LMUL != 0:
            raise ValueError(f"Invalid Vector Register Number {vi} for LMUL {self.LMUL}")
        
        if type(signed) == str:
            signed = True if signed == 's' else False
        
        start = vi * self.VLENB
        end = start + self.VL * self.SEW.SEW // 8
        
        viewtype = self.SEW.idtype if signed else self.SEW.udtype
        
        return self.VRF[start:end].view(viewtype)
    
    def vecw(self, vi, signed=False):
        LMUL = self.LMUL + 1
        SEW = self.SEW.get_higher_sew()

        if vi % LMUL != 0:
            raise ValueError(f"Invalid Vector Register Number {vi} for LMUL {LMUL}")
        
        if type(signed) == str:
            signed = True if signed == 's' else False
            
        start = vi * self.VLENB
        end = start + self.VL * SEW.SEW // 8
        
        viewtype = SEW.idtype if signed else SEW.udtype
        
        return self.VRF[start:end].view(viewtype)
    
    def vecm(self, vi):
        start = vi * self.VLENB
        end = start + int(np.ceil(self.VL / 8))
        return self.VRF[start:end].view(np.uint8)
    
    def scalar(self, xi, signed=False):
        if type(signed) == str:
            signed = True if signed == 's' else False
        viewtype = self.SEW.idtype if signed else self.SEW.udtype
        return viewtype(xi)
    
    def vsetvli(self, avl, e, m) -> None:
        
        if e not in self._valid_sews:
            raise ValueError(f"Invalid SEW value {e}")
        if m not in self._valid_lmuls:
            raise ValueError(f"Invaid LMUL value {m}")
        
        self.SEW = SEWC(e)
        self.LMUL = m
        self.VLMAX = self.VLEN * self.LMUL // self.SEW.SEW
        
        if avl == 0: avl = self.VLMAX
        self.VL = min([self.VLMAX, avl]) 
          
        return self.VL
    
    def vle(self, vd, inp : np.ndarray):
        if type(inp) == list:
            self._debug_print(f"Warning: vle({vd}): List Input for vle is not recommended. Use np.array instead.")
            self._debug_print("Converting List to np.array of dtype", self.SEW.idtype)
            inp = np.array(inp, dtype=self.SEW.idtype)
        if inp.itemsize != self.SEW.SEW // 8:
            self._debug_print(f"Warning: vle({vd}): Input SEW {inp.itemsize*8} does not match Set SEW {self.SEW.SEW}.")
        inp = inp.view(self.SEW.udtype)
        if inp.size > self.VL:
            self._debug_print(f"Warning: vle({vd}): Input Size {inp.size} exceeds VL {self.VL}.")
        if inp.size < self.VL:
            raise ValueError(f"vle({vd}): Input Size {inp.size} is less than VL {self.VL}.")
        
        vvd = self.vec(vd)
        vvd[:] = inp[:self.VL]

    def vse(self, vd, out : np.ndarray):
        vvd = self.vec(vd)
        out[:vvd.size] = vvd
    
    def vlm(self, vd, inp : np.ndarray):
        vvd = self.vecm(vd)
        vvd[:] = np.array(inp).view(np.uint8)[:int(np.ceil(self.VL/8))]

    def vsm(self, vd, out : np.ndarray):
        vvd = self.vecm(vd)
        out[:vvd.size] = vvd[:]

    @property
    def WSEW(self):
        return self.SEW.get_higher_sew()
    
    @WSEW.setter
    def WSEW(self, sew):
        pass

    @property
    def NSEW(self):
        return self.SEW.get_lower_sew()
    
    @NSEW.setter
    def NSEW(self, sew):
        pass
    