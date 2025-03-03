import numpy as np
from rvv.utils.sew import SEWC
import inspect
from enum import Enum

class BaseRVV:
    class VXRM(Enum):
        RNE = 0
        RTZ = 1
        RDN = 2
        RUP = 3

    def __init__(self, VLEN: int = 2048, debug = False, debug_vb_as_v = False) -> None:
        """
        Initialize a BaseRVV object with given parameters.

        Args:
            VLEN (int, optional): Vector Length in bits. Default is 2048.
            debug (bool, optional): Enable debugging mode. Default is False.
            debug_vb_as_v (bool, optional): Debug vector boolean register as vector uint8. Default is False.
        
        Attributes:
            VLEN (int): Vector Length in bits.
            VLENB (int): Vector Length in bytes.
            LMUL (float): Vector Length Multiplier.
            VL (int): Vector Length register.
            VLMAX (int): Maximum Vector Length.
            SEW (int): Standard Element Width.
            debug (bool): Debugging mode flag.
            debug_vb_as_v (bool): Debug vector boolean as vector flag.
        """

        self.VLEN : int = VLEN
        self.VLENB : int = VLEN // 8
        self.LMUL : float = None
        self.VL : int = None
        self.VLMAX : int = None
        self.SEW : int = None
        
        self._SEWC : SEWC = None
        
        self._valid_sews : list[int] = [8, 16, 32, 64]
        self._valid_lmuls : list[float] = [1/8, 1/4, 1/2, 1., 2., 4., 8.]
        self._valid_fsews : list[int] = [32, 64]
        
        self._extensions : list[str] = ["Base"]
        
        self._VRF : np.ndarray = np.zeros(self.VLENB * 32, dtype=np.uint8)
        self._SRF : list[np.uint64]  = [np.array([0], dtype=np.uint64)  for _ in range(32)]
        self._FRF : list[np.float64] = [np.array([0], dtype=np.float64) for _ in range(32)]
        
        self._init_vec_regs()
        self.debug = debug
        self.debug_vb_as_v = debug_vb_as_v
        
    def vsetvli(self, avl, e, m) -> None:
        """
        Set the vector length configuration based on active vector length (avl),
        standard element width (e), and vector length multiplier (m).

        Args:
            avl (int): Active vector length. If 0, it defaults to VLMAX.
            e (int): Standard element width. Must be one of the valid SEWs.
            m (float): Vector length multiplier. Must be one of the valid LMULs.

        Raises:
            ValueError: If `e` is not a valid SEW or `m` is not a valid LMUL.

        Returns:
            int: The effective vector length (VL) set by the function.
        """

        if e not in self._valid_sews:
            raise ValueError(f"Invalid SEW value {e}")
        if m not in self._valid_lmuls:
            raise ValueError(f"Invaid LMUL value {m}")
        
        self._SEWC = SEWC(e)
        self.SEW = self._SEWC.SEW
        self.LMUL = m
        self.VLMAX = self.VLEN * self.LMUL // self._SEWC.SEW
        
        if avl == 0: avl = self.VLMAX
        self.VL = min([self.VLMAX, avl]) 
          
        return self.VL
    
    def vle(self, vd, inp : np.ndarray):
        """
        Load a vector register from a numpy array.

        Args:
            vd (int): Destination vector register.
            inp (np.ndarray): Input numpy array.

        Raises:
            ValueError: If the input size is less than the current vector length (VL).

        Notes:
            If the input is a list, it is converted to a numpy array of the
            current SEW. If the input size exceeds the current VL, a warning
            is printed and the input is truncated. If the input size is less
            than the current VL, a ValueError is raised.

        Returns:
            None
        """
        
        if type(inp) == list:
            self._debug_print(f"Warning: vle({vd}): List Input for vle is not recommended. Use np.array instead.")
            self._debug_print("Converting List to np.array of dtype", self._SEWC.idtype)
            inp = np.array(inp, dtype=self._SEWC.idtype)
        if inp.itemsize != self._SEWC.SEW // 8:
            self._debug_print(f"Warning: vle({vd}): Input SEW {inp.itemsize*8} does not match Set SEW {self._SEWC.SEW}.")
        inp = inp.view(self._SEWC.udtype)
        if inp.size > self.VL:
            self._debug_print(f"Warning: vle({vd}): Input Size {inp.size} exceeds VL {self.VL}.")
        if inp.size < self.VL:
            raise ValueError(f"vle({vd}): Input Size {inp.size} is less than VL {self.VL}.")
        
        vvd = self._vec(vd)
        vvd[:] = inp[:self.VL]

    def vse(self, vd, out : np.ndarray = None):
        """
        Store a vector register to a numpy array.

        Args:
            vd (int): Source vector register.
            out (np.ndarray, optional): Output numpy array. If None, returns the stored vector.

        Returns:
            np.ndarray: The stored vector if out is None, otherwise None.
        """
        vvd = self._vec(vd)
        if out is None:
            return vvd
        out[:vvd.size] = vvd
    
    def vlm(self, vd, inp : np.ndarray):
        """
        Load a vector mask register from a numpy array of uint8 values.
        To load values of boolean type, convert boolean array to uint8 array using bools_to_vm() function.
        
        Args:
            vd (int): Destination vector register.
            inp (np.ndarray): Input numpy array of uint8 values.

        Returns:
            None
        """
        
        vvd = self._vecm(vd)
        vvd[:] = np.array(inp).view(np.uint8)[:int(np.ceil(self.VL/8))]

    def vsm(self, vd, out : np.ndarray):
        """
        Store a vector mask register to a numpy array of uint8 values.
        To get values of boolean type, convert return array to boolean array using vm_to_bools() function.
        
        Args:
            vd (int): Source vector register.
            out (np.ndarray): Output numpy array of uint8 values.

        Returns:
            None
        """
    
        vvd = self._vecm(vd)
        out[:vvd.size] = vvd[:]

    def lb(self, xi, value):
        self._SRF[xi] = np.uint64(np.int64(np.int8(value)))
    
    def lbu(self, xi, value):
        self._SRF[xi] = np.uint64(np.int64(np.uint8(value)))
    
    def lh(self, xi, value):
        self._SRF[xi] = np.uint64(np.int64(np.int16(value)))
    
    def lhu(self, xi, value):
        self._SRF[xi] = np.uint64(np.int64(np.uint16(value)))
        
    def lw(self, xi, value):
        self._SRF[xi] = np.uint64(np.int64(np.int32(value)))
    
    def lwu(self, xi, value):
        self._SRF[xi] = np.uint64(np.int64(np.uint32(value)))
        
    def ld(self, xi, value):
        self._SRF[xi] = np.uint64(value)
        
    def flh(self, fi, value):
        self._FRF[fi] = np.float16(value)
        
    def flw(self, fi, value):
        self._FRF[fi] = np.float32(value)
    
    def flf(self, fi, value):
        self._FRF[fi] = np.float64(value)

    def sb(self, xi):
        return np.int8(self._SRF[xi])
    
    def sbu(self, xi):
        return np.uint8(self._SRF[xi])
    
    def sh(self, xi):
        return np.int16(self._SRF[xi])
    
    def shu(self, xi):
        return np.uint16(self._SRF[xi])
    
    def sw(self, xi):
        return np.int32(self._SRF[xi])
    
    def swu(self, xi):
        return np.uint32(self._SRF[xi])
    
    def sd(self, xi):
        return np.int64(self._SRF[xi])
    
    def sdu(self, xi):
        return np.uint64(self._SRF[xi])
    
    def fsh(self, fi):
        return np.float16(self._FRF[fi])
        
    def fsw(self, fi):
        return np.float32(self._FRF[fi])
    
    def fsd(self, fi):
        return np.float64(self._FRF[fi])
        
    def get_vector_reg(self, vi : int, VL : int = None, LMUL : int = None, dtype : np.dtype = None):
        """
        Return a vector register as a numpy array.

        Parameters
        ----------
        vi : int
            Vector register index.
        VL : int, optional
            Vector length. Defaults to ``self.VL``.
        LMUL : int, optional
            Vector register group multiplier. Defaults to ``self.LMUL``.
        dtype : numpy.dtype, optional
            Data type of vector elements. Defaults to ``self._SEWC.idtype``.

        Returns
        -------
        numpy.ndarray
            A numpy array view of the vector register.

        Raises
        ------
        ValueError
            If the vector register index is not a multiple of ``LMUL``.
        """
        if LMUL is None: LMUL = self.LMUL
        if dtype is None: dtype = self._SEWC.idtype
        if VL is None: VL = self.VL
        SEWB = dtype.itemsize

        self._check_valid_lmul(vi, LMUL)
            
        start = vi * self.VLENB
        end = start + VL * SEWB

        return self._VRF[start:end].view(dtype)
    
    def bools_to_vm(self, bool_array):
        """
        Convert a boolean array to a vector mask register.

        The boolean array is padded and reversed to match the RISC-V vector mask
        register format. The returned vector mask is a numpy array of uint8 values.

        Args:
            bool_array (np.ndarray): A numpy array of boolean values.

        Returns:
            np.ndarray: A numpy array of uint8 values representing the vector mask.

        Raises:
            ValueError: If the length of the boolean array is not equal to ``self.VL``.
        """
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
        """
        Convert a vector mask register to a boolean array.

        The vector mask is reversed and padded to convert the RISC-V vector mask register 
        format into a standard boolean array, where the first mask corresponds to the first 
        element, the second to the second, and so on. The result is a NumPy array of boolean values.

        Args:
            vbool (np.ndarray): A numpy array of uint8 values representing the vector mask.

        Returns:
            np.ndarray: A numpy array of boolean values representing the vector mask.

        Raises:
            ValueError: If the length of the vector mask is not equal to ``self.VL``.
        """
        vbool = vbool.view(np.uint8)
        
        reversed_bool_array = np.unpackbits(vbool)
        bool_array = np.zeros_like(reversed_bool_array)
        for i in range(0, len(reversed_bool_array), 8):
            for j in range(8):
                bool_array[i+j] = reversed_bool_array[i+7-j]

        bool_array = bool_array[:self.VL].view(np.bool_)
        
        return bool_array
    
    def _init_vec_regs(self):
        """
        Initialize vector registers with values from 0 to VL-1.
        """
        self.vsetvli(0, 8, 1)
        
        for i in range(32):
            v = self._vec(i)
            for k in range(self.VL):
                v[k] = k
    
    def _initer(self, op, optype, viewtype):

        """
        Initialize an operand based on its type and view type.

        Parameters
        ----------
        op : int
            Operand index or identifier.
        optype : str
            Operand type, which can be one of the following:
            'v' for vector, 'w' for wide vector, 's' for scalar vector,
            'd' for double vector, 'x' for scalar register,
            'f' for floating-point register, 'm' for vector mask.
        viewtype : str
            View type for the operand, indicating how it should be interpreted.

        Returns
        -------
        np.ndarray or other types
            Initialized operand based on the type and view type.

        Raises
        ------
        ValueError
            If the operand type is invalid.
        """

        if optype == 'v': return self._vec(op, viewtype)
        elif optype == 'w': return self._vecw(op, viewtype)
        elif optype == 's': return self._vecs(op, viewtype)
        elif optype == 'd': return self._vecd(op, viewtype)
        elif optype == 'x': return self._sreg(op, viewtype)
        elif optype == 'f': return self._freg(op, viewtype)
        elif optype == 'm': return self._vecm(op)
        else: raise ValueError(f"Invalid Operand Type {optype}")
    
    def _get_mask(self, vops, masked):
        """
        Return a mask for a vector operation.

        Parameters
        ----------
        vops : list of int
            Vector register indices.
        masked : bool
            Whether the operation is masked.

        Returns
        -------
        numpy.ndarray
            A boolean mask of length ``self.VL``.

        Raises
        ------
        ValueError
            If the operation is masked and V0 is used as an operand.
        """
        if not masked:
            return np.ones(self.VL, dtype=np.bool_)
            
        if 0 in vops:
            raise ValueError("Cannot use V0 for as op in Masked Operation")
        
        return self.vm_to_bools(self._vecm(0))
    
    def _init_ops_generic(self, ops, optypes, viewtypes, masked):        
        """
        Initialize and prepare operands for a vector operation.

        This method initializes the operands based on their types and view types, 
        and applies a mask if the operation is masked. It performs debugging of 
        operand values and the mask, and sets a post-operation flag for additional 
        processing.

        Parameters
        ----------
        ops : list of int
            Indices or identifiers of the operands.
        optypes : list of str
            Types of the operands, which can be one of the following:
            'v' for vector, 'w' for wide vector, 's' for scalar vector,
            'd' for double vector, 'x' for scalar register,
            'f' for floating-point register, 'm' for vector mask.
        viewtypes : list of str
            View types for the operands, indicating how they should be interpreted.
        masked : bool
            Whether the operation is masked.

        Returns
        -------
        list
            A list of initialized operand values, with the mask appended as the 
            last element.
        """

        op_values = []
        for op, optype, viewtype in zip(ops, optypes, viewtypes):
            op_value = self._initer(op, optype, viewtype)
            op_values.append(op_value)
        
        # Debug all ops
        for i, (op_value, op, optype) in enumerate(list(zip(op_values, ops, optypes))):
            if i == 0:
                self._debug_val(optype, 'd', op_value, op)
                self._debug_print(f"{'-'*30}")
            else:  
                self._debug_val(optype, f'op{i}', op_value, op)
            
        vector_ops = [ops[i] for i in range(len(ops)) if optypes[i] != 'x']
        mask = self._get_mask(vector_ops, masked)
        
        # Debug Mask
        self._debug_mask(mask, masked)
        op_values.append(mask)
        
        # Post Operation Flag:
        self._pvd = {'optype': optypes[0], 'val': op_values[0], 'op' : ops[0], 'mask': mask}
        return op_values
    
    def _init_ops_zero(self, od, optypes, viewtypes, masked):
        """
        Initialize a single operand with zero inputs.

        Parameters
        ----------
        od : int
            Operand identifier.
        optypes : list of str
            Types of the operands.
        viewtypes : list of str
            View types for the operands, indicating how they should be interpreted.
        masked : bool
            Whether the operation is masked.

        Returns
        -------
        list
            A list containing the initialized operand value and the mask.
        """

        self._debug_operation()
        return self._init_ops_generic([od], optypes, viewtypes, masked)
    
    def _init_ops_uni(self, od, op1, optypes, viewtypes, masked):
        """
        Initialize two operands for a unary vector operation.

        This method initializes two operands, the destination operand and a single 
        source operand, for a unary vector operation. It also applies a mask if the 
        operation is masked and performs debugging operations.

        Parameters
        ----------
        od : int
            Destination operand identifier.
        op1 : int
            Source operand identifier.
        optypes : list of str
            Types of the operands, which can be one of the following:
            'v' for vector, 'w' for wide vector, 's' for scalar vector,
            'd' for double vector, 'x' for scalar register,
            'f' for floating-point register, 'm' for vector mask.
        viewtypes : list of str
            View types for the operands, indicating how they should be interpreted.
        masked : bool
            Whether the operation is masked.

        Returns
        -------
        list
            A list containing the initialized operand values and the mask.
        """

        self._debug_operation()
        return self._init_ops_generic([od, op1], optypes, viewtypes, masked)
    
    def _init_ops(self, od, op1, op2, optypes, viewtypes, masked):
        """
        Initialize three operands for a binary vector operation.

        This method initializes three operands, including a destination operand
        and two source operands, for a binary vector operation. It also applies 
        a mask if the operation is masked and performs debugging operations.

        Parameters
        ----------
        od : int
            Destination operand identifier.
        op1 : int
            First source operand identifier.
        op2 : int
            Second source operand identifier.
        optypes : list of str
            Types of the operands, which can be one of the following:
            'v' for vector, 'w' for wide vector, 's' for scalar vector,
            'd' for double vector, 'x' for scalar register,
            'f' for floating-point register, 'm' for vector mask.
        viewtypes : list of str
            View types for the operands, indicating how they should be interpreted.
        masked : bool
            Whether the operation is masked.

        Returns
        -------
        list
            A list containing the initialized operand values and the mask.
        """

        self._debug_operation()
        return self._init_ops_generic([od, op1, op2], optypes, viewtypes, masked)

    def _init_ops_tri(self, od, op1, op2, op3, optypes, viewtype, masked):
        """
        Initialize four operands for a ternary vector operation.

        This method initializes four operands, including a destination operand
        and three source operands, for a ternary vector operation. It also applies
        a mask if the operation is masked and performs debugging operations.

        Parameters
        ----------
        od : int
            Destination operand identifier.
        op1 : int
            First source operand identifier.
        op2 : int
            Second source operand identifier.
        op3 : int
            Third source operand identifier.
        optypes : list of str
            Types of the operands, which can be one of the following:
            'v' for vector, 'w' for wide vector, 's' for scalar vector,
            'd' for double vector, 'x' for scalar register,
            'f' for floating-point register, 'm' for vector mask.
        viewtype : str
            View type for the operands, indicating how they should be interpreted.
        masked : bool
            Whether the operation is masked.

        Returns
        -------
        list
            A list containing the initialized operand values and the mask.
        """
        self._debug_operation()
        return self._init_ops_generic([od, op1, op2, op3], optypes, viewtype, masked)
    
    def _init_ops_ext(self, vd, op1, optype, signed, masked):
        """
        Initialize operands for an extended vector operation.

        This method initializes two operands for an extended vector operation,
        taking into account the operand type to determine the required SEW
        (Standard Element Width) and applies appropriate view types based on
        whether the operation is signed or unsigned. It also applies a mask if
        the operation is masked and performs debugging operations.

        Parameters
        ----------
        vd : int
            Destination vector register identifier.
        op1 : int
            Source vector register identifier.
        optype : str
            Type of the operation, which can be 'vf2', 'vf4', or 'vf8'.
        signed : bool
            Whether the operation is signed.
        masked : bool
            Whether the operation is masked.

        Returns
        -------
        tuple
            A tuple containing the initialized destination vector, the modified
            source operand value, and the mask.
        
        Raises
        ------
        ValueError
            If the SEW requirement for the given optype is not met.
        """

        self._debug_operation()
           
        if optype == 'vf2':
            if self._SEWC.SEW < 16: raise ValueError("EXT_VF2 requires SEW >= 16")
            op1_sew = self._SEWC.get_lower_sew()
        elif optype == 'vf4':
            if self._SEWC.SEW < 32: raise ValueError("EXT_VF4 requires SEW >= 32")
            op1_sew = self._SEWC.get_lower_sew().get_lower_sew()
        elif optype == 'vf8':
            if self._SEWC.SEW < 64: raise ValueError("EXT_VF8 requires SEW = 64")
            op1_sew = self._SEWC.get_lower_sew().get_lower_sew().get_lower_sew()
        
        viewtype = 's' if signed else 'u'
        vvd = self._vec(vd, viewtype)
        op1_value = self._vec(op1, viewtype)
        
        if signed:
            op1_value = op1_value.view(op1_sew.idtype)
        else:
            op1_value = op1_value.view(op1_sew.udtype)
        
        op1_value = op1_value[:self.VL]
        
        ops = [vd, op1]
        vector_ops = [ops[i] for i in range(2) if optype[i] != 'x']
        
        mask = self._get_mask(vector_ops, masked)
        
        self._debug_val('v', 'd', vvd, vd)
        self._debug_print(f"{'-'*30}")
        self._debug_val('v', 'op1', op1_value, op1)
        self._debug_mask(mask, masked)
        
        # Post Operation VD:
        self._pvd = {'optype': 'v', 'val': vvd, 'op' : vd}
        
        return vvd, op1_value, mask
    
    def _post_op(self):
        """
        Print the post operation value of the destination vector register.
        
        Notes
        -----
        This function is only called if debug is enabled.
        """
        if self.debug:
            self._debug_val(self._pvd['optype'], 'd', self._pvd['val'], self._pvd['op'])
    
    def _debug_val(self, optype, opname, val, op=None):
        """
        Print the value of an operand/register.

        Parameters
        ----------
        optype : str
            Type of the operand/register.
        opname : str
            Name of the operand/register.
        val : int/float/bool
            Value of the operand/register.
        op : int, optional
            Index of the operand/register (default is None).

        Notes
        -----
        This function is only called if debug is enabled.
        """
        if self.debug:
            if optype in ['v','w','s','d','x','f']:
                print(f"{optype + opname:>5} {optype:>2}{op:02}: ", val)
            elif optype == 'm':
                optype = 'vm'
                if not self.debug_vb_as_v: val = self.vm_to_bools(val).view(np.uint8)
                print(f"{optype + opname:>5} {optype:>2}{op:02}: ", val)
            elif optype == '_':
                pass
            else:
                raise ValueError(f"Invalid Value Type {optype}")
    
    def _debug_mask(self, mask, masked):
        """
        Print the value of a mask register.

        Parameters
        ----------
        mask : numpy.ndarray
            Boolean mask array.
        masked : bool
            Whether the operation is masked.

        Notes
        -----
        This function is only called if debug is enabled.
        If debug_vb_as_v is True, the mask is converted from a boolean array to a vector mask.
        The mask is printed as a vector of uint8 values.
        """
        if self.debug and masked:
            if self.debug_vb_as_v: mask = self.bools_to_vm(mask)
            print(f"vmask  vm0:  {mask.view(np.uint8)}")
    
    def _debug_operation(self):
        """
        Print the name of the current operation.

        Notes
        -----
        This function is only called if debug is enabled.
        This function prints the name of the caller of the function that calls it.
        The operation name is obtained from the current frame using inspect.currentframe().
        The operation name is printed with a row of "=" characters above and below it.
        """
        if self.debug:
            print("\n")
            print(f"{'='*30}")
            print(f" Operation: {inspect.currentframe().f_back.f_back.f_code.co_name}")
            print(f"{'='*30}")
    
    def _debug_print(self, *args):
        """
        Print the given arguments if debugging is enabled.

        Parameters
        ----------
        *args
            Arguments to be printed.
        """
        if self.debug:
            print(*args)
    
    def _iclip(self, num):
        return np.clip(num, self._SEWC.imin, self._SEWC.imax)    
    
    def _uclip(self, num):
        return np.clip(num, self._SEWC.umin, self._SEWC.umax)    
    
    def _sext(self, num):
        return self._WSEW.idtype(self._SEWC.idtype(num))
    
    def _zext(self, num):
        return self._WSEW.udtype(self._SEWC.udtype(num)) 

    def _vm_masked(self, dest, src, mask):
        """Mask a destination vector register with a source vector register and a mask."""
        dest_bools = self.vm_to_bools(dest)
        src_bools = self.vm_to_bools(src)
        dest_bools[mask] = src_bools[mask]
        dest[:] = self.bools_to_vm(dest_bools)
        return dest
    
    def _get_viewtype(self, viewtype, SEW):
        """
        Return the numpy dtype corresponding to the given viewtype and SEW.

        Parameters
        ----------
        viewtype : str
            'u' for unsigned, 's' for signed, 'f' for floating-point.
        SEW : SEWC
            The Standard Element Width configuration.

        Returns
        -------
        numpy.dtype
            The numpy dtype corresponding to the given viewtype and SEW.

        Raises
        ------
        ValueError
            If the viewtype is not one of 'u', 's', or 'f', or if the SEW is not valid for the given viewtype.
        """
        if viewtype == 'u': return SEW.udtype
        elif viewtype == 's': return SEW.idtype
        elif viewtype == 'f': 
            if SEW.SEW not in self._valid_fsews: 
                raise ValueError(f"Invalid SEW {SEW.SEW} for dtype 'f'. Add ZVFH extension")
            return SEW.fdtype
        
        else: raise ValueError(f"Invalid Viewtype {viewtype}")
    
    def _check_valid_lmul(self, vi, lmul):
        if vi % self.LMUL != 0:
            raise ValueError(f"Invalid Vector Register Number {vi} for LMUL {lmul}")
        
    def _full_vec(self, vi, viewtype='u'):
        self._check_valid_lmul(vi, self.LMUL)
                
        start = vi * self.VLENB
        end = start + self.VLMAX * self._SEWC.SEW // 8
        viewtype = self._get_viewtype(viewtype, self._SEWC)
        
        return self._VRF[start:end].view(viewtype)
    
    def _vec(self, vi, viewtype='u'):
        self._check_valid_lmul(vi, self.LMUL)
                
        start = vi * self.VLENB
        end = start + self.VL * self._SEWC.SEW // 8
        viewtype = self._get_viewtype(viewtype, self._SEWC)
        
        return self._VRF[start:end].view(viewtype)
    
    def _vecw(self, vi, viewtype='u'):
        LMUL = self.LMUL*2
        SEWC = self._WSEW

        self._check_valid_lmul(vi, LMUL)
            
        start = vi * self.VLENB
        end = start + self.VL * SEWC.SEW // 8
        viewtype = self._get_viewtype(viewtype, SEWC)

        return self._VRF[start:end].view(viewtype)
    
    def _vecs(self, vi, viewtype='u'):
        LMUL = 1

        self._check_valid_lmul(vi, LMUL)
            
        start = vi * self.VLENB
        end = start + self.VL * self._SEWC.SEW // 8
        viewtype = self._get_viewtype(viewtype, self._SEWC)

        return self._VRF[start:end].view(viewtype)
    
    def _vecd(self, vi, viewtype='u'):
        LMUL = 1
        SEWC = self._WSEW

        self._check_valid_lmul(vi, LMUL)
            
        start = vi * self.VLENB
        end = start + self.VL * SEWC.SEW // 8
        viewtype = self._get_viewtype(viewtype, SEWC)

        return self._VRF[start:end].view(viewtype)
    
    def _vecm(self, vi):
        start = vi * self.VLENB
        end = start + int(np.ceil(self.VL / 8))
        return self._VRF[start:end].view(np.uint8)
    
    def _sreg(self, xi, viewtype='u'):
        if viewtype == 'x': return self._SRF[xi]
        viewtype = self._get_viewtype(viewtype, self._SEWC)
        return viewtype(self._SRF[xi])
    
    def _freg(self, xi, viewtype='f'):
        if viewtype == 'x': return self._FRF[xi]
        viewtype = self._get_viewtype(viewtype, self._SEWC)
        return viewtype(self._FRF[xi])
    
    def _vxrm_rounding(self, val, vxrm):
        if vxrm == self.VXRM.RNE:
            return int(np.round(val))
        elif vxrm == self.VXRM.RTZ:
            return int(np.trunc(val))
        elif vxrm == self.VXRM.RDN:
            return int(np.floor(val))
        elif vxrm == self.VXRM.RUP:
            return int(np.ceil(val))
    
    def _vxrm_right_shift(self, val, shift, vxrm):
        divider = 1 << shift
        val /= divider
        return self._vxrm_rounding(val, vxrm)
        
    @property
    def _WSEW(self):
        return self._SEWC.get_higher_sew()
    
    @_WSEW.setter
    def _WSEW(self, sew):
        pass

    @property
    def _NSEW(self):
        return self._SEWC.get_lower_sew()
    
    @_NSEW.setter
    def _NSEW(self, sew):
        pass
    