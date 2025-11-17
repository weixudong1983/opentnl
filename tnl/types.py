"""
TNL Basic Types and Constants
"""
import struct

# Basic type aliases
U8 = int  # 0-255
U16 = int  # 0-65535
U32 = int  # 0-4294967295
S8 = int  # -128 to 127
S16 = int  # -32768 to 32767
S32 = int  # -2147483648 to 2147483647
F32 = float
F64 = float

# Constants
FloatOne = 1.0
FloatHalf = 0.5
FloatZero = 0.0
FloatPi = 3.14159265358979323846

U8_MAX = 255
U16_MAX = 65535
U32_MAX = 4294967295

class Point3F:
    """3D point representation"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = F32(x)
        self.y = F32(y)
        self.z = F32(z)

def write_u32_to_buffer(value, buffer, offset=0):
    """Write U32 to buffer in network byte order (big endian)"""
    struct.pack_into('>I', buffer, offset, value & 0xFFFFFFFF)

def read_u32_from_buffer(buffer, offset=0):
    """Read U32 from buffer in network byte order (big endian)"""
    return struct.unpack_from('>I', buffer, offset)[0]

def write_u16_to_buffer(value, buffer, offset=0):
    """Write U16 to buffer in network byte order (big endian)"""
    struct.pack_into('>H', buffer, offset, value & 0xFFFF)

def read_u16_from_buffer(buffer, offset=0):
    """Read U16 from buffer in network byte order (big endian)"""
    return struct.unpack_from('>H', buffer, offset)[0]

def get_next_pow2(value):
    """Get next power of 2 greater than or equal to value"""
    value -= 1
    value |= value >> 1
    value |= value >> 2
    value |= value >> 4
    value |= value >> 8
    value |= value >> 16
    return value + 1
