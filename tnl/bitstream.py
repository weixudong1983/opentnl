"""
BitStream - Bit-level stream interface for network data
"""
import struct
from .types import *

class BitStream:
    """
    BitStream provides bit-level reading and writing to a byte buffer.
    This is a simplified version focusing on the most common operations.
    """
    
    def __init__(self, buffer=None, max_size=1500):
        if buffer is None:
            self.buffer = bytearray(max_size)
            self.max_size = max_size
            self.max_read_bit_num = max_size * 8
        else:
            self.buffer = bytearray(buffer)
            self.max_size = len(buffer)
            self.max_read_bit_num = len(buffer) * 8
        
        self.bit_num = 0
        self.max_write_bit_num = self.max_size * 8
        self.error = False
    
    def reset(self):
        """Reset the stream to the beginning"""
        self.bit_num = 0
        self.error = False
    
    def get_bit_position(self):
        """Get current bit position"""
        return self.bit_num
    
    def set_bit_position(self, pos):
        """Set current bit position"""
        self.bit_num = pos
    
    def get_byte_position(self):
        """Get current byte position"""
        return (self.bit_num + 7) // 8
    
    def write_flag(self, flag):
        """Write a single bit flag"""
        return self.write_bits(1, 1 if flag else 0)
    
    def read_flag(self):
        """Read a single bit flag"""
        return self.read_bits(1) != 0
    
    def write_bits(self, bit_count, value):
        """Write specified number of bits"""
        if self.bit_num + bit_count > self.max_write_bit_num:
            self.error = True
            return False
        
        for i in range(bit_count):
            bit = (value >> (bit_count - 1 - i)) & 1
            byte_pos = self.bit_num // 8
            bit_pos = 7 - (self.bit_num % 8)
            
            if bit:
                self.buffer[byte_pos] |= (1 << bit_pos)
            else:
                self.buffer[byte_pos] &= ~(1 << bit_pos)
            
            self.bit_num += 1
        
        return True
    
    def read_bits(self, bit_count):
        """Read specified number of bits"""
        if self.bit_num + bit_count > self.max_read_bit_num:
            self.error = True
            return 0
        
        value = 0
        for i in range(bit_count):
            byte_pos = self.bit_num // 8
            bit_pos = 7 - (self.bit_num % 8)
            bit = (self.buffer[byte_pos] >> bit_pos) & 1
            value = (value << 1) | bit
            self.bit_num += 1
        
        return value
    
    def write(self, value):
        """Write a value (integer or float)"""
        if isinstance(value, float):
            return self.write_float32(value)
        elif isinstance(value, int):
            return self.write_int32(value)
        return False
    
    def read(self, value_type=None):
        """Read a value"""
        if value_type == float or value_type == F32:
            return self.read_float32()
        elif value_type == int or value_type == S32:
            return self.read_int32()
        return None
    
    def write_int32(self, value):
        """Write a 32-bit signed integer"""
        # Align to byte boundary
        if self.bit_num % 8 != 0:
            self.bit_num = ((self.bit_num + 7) // 8) * 8
        
        byte_pos = self.bit_num // 8
        if byte_pos + 4 > len(self.buffer):
            self.error = True
            return False
        
        struct.pack_into('>i', self.buffer, byte_pos, value)
        self.bit_num += 32
        return True
    
    def read_int32(self):
        """Read a 32-bit signed integer"""
        # Align to byte boundary
        if self.bit_num % 8 != 0:
            self.bit_num = ((self.bit_num + 7) // 8) * 8
        
        byte_pos = self.bit_num // 8
        if byte_pos + 4 > len(self.buffer):
            self.error = True
            return 0
        
        value = struct.unpack_from('>i', self.buffer, byte_pos)[0]
        self.bit_num += 32
        return value
    
    def write_float32(self, value):
        """Write a 32-bit float"""
        # Align to byte boundary
        if self.bit_num % 8 != 0:
            self.bit_num = ((self.bit_num + 7) // 8) * 8
        
        byte_pos = self.bit_num // 8
        if byte_pos + 4 > len(self.buffer):
            self.error = True
            return False
        
        struct.pack_into('>f', self.buffer, byte_pos, value)
        self.bit_num += 32
        return True
    
    def read_float32(self):
        """Read a 32-bit float"""
        # Align to byte boundary
        if self.bit_num % 8 != 0:
            self.bit_num = ((self.bit_num + 7) // 8) * 8
        
        byte_pos = self.bit_num // 8
        if byte_pos + 4 > len(self.buffer):
            self.error = True
            return 0.0
        
        value = struct.unpack_from('>f', self.buffer, byte_pos)[0]
        self.bit_num += 32
        return value
    
    def write_float(self, value, bit_count):
        """Write a compressed float (0.0 to 1.0) using specified bits"""
        if value < 0.0:
            value = 0.0
        elif value > 1.0:
            value = 1.0
        
        max_val = (1 << bit_count) - 1
        int_val = int(value * max_val + 0.5)
        return self.write_bits(bit_count, int_val)
    
    def read_float(self, bit_count):
        """Read a compressed float using specified bits"""
        max_val = (1 << bit_count) - 1
        int_val = self.read_bits(bit_count)
        return float(int_val) / float(max_val)
    
    def write_string(self, string):
        """Write a null-terminated string"""
        if string is None:
            string = ""
        
        encoded = string.encode('utf-8')
        for byte in encoded:
            if not self.write_bits(8, byte):
                return False
        return self.write_bits(8, 0)  # null terminator
    
    def read_string(self):
        """Read a null-terminated string"""
        chars = []
        while True:
            byte = self.read_bits(8)
            if byte == 0 or self.error:
                break
            chars.append(byte)
        
        return bytes(chars).decode('utf-8', errors='ignore')
    
    def get_buffer(self):
        """Get the underlying buffer"""
        byte_size = (self.bit_num + 7) // 8
        return bytes(self.buffer[:byte_size])
    
    def set_max_sizes(self, max_read, max_write):
        """Set maximum read and write sizes in bytes"""
        self.max_read_bit_num = max_read * 8
        self.max_write_bit_num = max_write * 8
    
    def has_error(self):
        """Check if an error occurred"""
        return self.error
