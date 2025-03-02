# RVV

RVV is a Python module that simulates the behavior of the RISC-V Vector Extension. It provides a framework for most of the RISCV-V Base Vector Extension assembly instructions along with few extra instruction mentioned below. 

## Additional Features

- **Vector Register Operations**  
  Load (`vle`, `vlm`) and store (`vse`, `vsm`) vector registers from/to NumPy arrays.  
  Retrieve vector registers using `get_vector_reg` with more options like LMUL, VL and viewtype.

- **Vector Mask Handling**
  Convert boolean arrays to vector mask registers (`bools_to_vm`) and vice versa (`vm_to_bools`), ensuring the first mask corresponds to the first element, the second to the second, etc.

- **Scalar and Floating-Point Register Operations**  
  Load and store operations for scalar registers (`lb`, `lh`, `lw`, `ld`, etc.) and floating-point registers (`flh`, `flw`, `flf`) are provided to emulate RISC-V behavior. Store operations returns the value of the registers. Float store operations are a bit inaccurate as they tend to do conversion. Additional unsigned scalar stors (`sbu`, `shu`, `swu` and `sdu`) were added to return unsigned values of registers.

- **Debugging Options**  
  Enable debugging for detailed internal state tracing via the `debug` flag
  Enable `debug_vm_as_v` flag to debug mask registers as simple uint8 registers. Note that mask are stored in Little Endian.

## Additional Notes

- **Vector Initialization**  
  All vector arrays are initialized with values from 0 to VLEN in bytes.

- **Vector Memory Options**  
  Vector Memory operations (`vle8`, `vse8`, etc.) work a little different. Contrary to asm, where only pointer is required, insturctions in this library require you to pass in a numpy array as memory, and offset in bytes.

- **Extensions**  
  You can add extensions from `rvv.extensions`. Right now only ZVFH extension is implemented. In example below, it is shown how to add an extension to base class.

## Requirements

- Python 3.7 or higher
- [NumPy](https://numpy.org/)

## Usage

Below is a simple example demonstrating how to create a `RVV` object, configure vector length settings, and perform vector load/store operations:

```python
import numpy as np
from rvv import RVV

# Importing Extension
from rvv.extensions import ZVFH

# Create a RVV object with a vector length of 2048 bits and debugging enabled
rvv = RVV(VLEN=2048, debug=True)

# Enabling Extension
rvv = ZVFH(rvv).rvv

# Set the vector length configuration for 32-bit elements with LMUL=1
rvv.vsetvli(avl=4, e=32, m=1)  # avl=0 defaults to the maximum VL

# Load a vector register with a NumPy array
vector_data = np.array([1, 2, 3, 4], dtype=np.int32)
rvv.vle(1, vector_data)

# Initializing memory and loading another vector register from it
memory = np.arange(100, dtype=np.int32)
rvv.vle32(2, memory, 10)

# Convert a boolean array to a vector mask and back
bool_mask = np.array([True, False, True, True], dtype=bool)
vmask = rvv.bools_to_vm(bool_mask)

# Load Mask
rvv.vlm(0, vmask)

# Perform RVV operations
rvv.vadd(3, 2, 1)

# Store and print the contents of a vector register
stored_vector = rvv.vse(3)
print("Vector Register 2:", stored_vector)
```

## Documentation

### Class: `RVV`

#### Initialization
- **Parameters:**
  - `VLEN` (int, optional): Vector Length in bits (default: 2048).
  - `debug` (bool, optional): Enable debugging mode (default: False).
  - `debug_vb_as_v` (bool, optional): Debug vector boolean register as vector uint8 (default: False).

- **Attributes:**
  - `VLEN`: Vector Length in bits.
  - `VLENB`: Vector Length in bytes.
  - `LMUL`: Vector Length Multiplier.
  - `VL`: Vector Length register.
  - `VLMAX`: Maximum Vector Length.
  - `SEW`: Standard Element Width.
  - `debug`: Debugging mode flag.
  - `debug_vb_as_v`: Flag to debug vector boolean registers.

#### Methods

- **Vector Configuration**
  - `vsetvli(avl, e, m)`:  
    Sets the vector length configuration based on active vector length (`avl`), standard element width (`e`), and vector length multiplier (`m`).  
    Returns the effective vector length (VL).

- **All Base Extension Assembly instructions for RVV**

- **Vector Register Operations**
  - `vle(vd, inp)`:  
    Loads a vector register from a NumPy array. Supports conversion from lists and performs input size checks.
  - `vse(vd, out)`:  
    Stores a vector register into a NumPy array, or returns the vector if no output array is provided.
  - `get_vector_reg(vi, VL, LMUL, dtype)`:  
    Retrieves a vector register as a NumPy array view with the specified data type.

- **Mask Register Operations**
  - `vlm(vd, inp)`:  
    Loads a vector mask register from a NumPy array of `uint8` values.
  - `vsm(vd, out)`:  
    Stores a vector mask register into a NumPy array of `uint8` values.
  - `bools_to_vm(bool_array)`:  
    Converts a boolean array to a vector mask register. The boolean array is padded and reversed to match the RISC-V mask format, where the first mask corresponds to the first element.
  - `vm_to_bools(vbool)`:  
    Converts a vector mask register back into a standard boolean array, ensuring the first mask corresponds to the first element.

- **Scalar and Floating-Point Load/Store Operations**
  - **Scalar Loads:**  
    `lb`, `lbu`, `lh`, `lhu`, `lw`, `lwu`, `ld`  
    These methods load scalar values into the internal scalar register file (`_SRF`) with appropriate conversions.
  - **Scalar Stores:**  
    `sb`, `sbu`, `sh`, `shu`, `sw`, `swu`, `sd`, `sdu`  
    These methods return the stored scalar values from the register file.
  - **Floating-Point Loads/Stores:**  
    `flh`, `flw`, `flf` (for loading) and `fsh`, `fsw`, `fsd` (for storing)  
    These methods handle operations on the floating-point register file (`_FRF`).

## Contributing

Contributions are welcome! If you have suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
