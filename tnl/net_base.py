"""
NetBase - Base networking utilities
"""
import socket
import time
from .types import U32

class NetBase:
    """Base networking utilities and timing"""
    
    _start_time = None
    
    @staticmethod
    def init():
        """Initialize networking"""
        NetBase._start_time = time.time()
    
    @staticmethod
    def get_current_time():
        """Get current time in milliseconds since init"""
        if NetBase._start_time is None:
            NetBase.init()
        return U32((time.time() - NetBase._start_time) * 1000)
    
    @staticmethod
    def sleep(milliseconds):
        """Sleep for specified milliseconds"""
        time.sleep(milliseconds / 1000.0)

# Initialize on module import
NetBase.init()
