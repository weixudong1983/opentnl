"""
Random number generator for TNL
"""
import random

class Random:
    """Random number utilities"""
    
    @staticmethod
    def read_f():
        """Return a random float between 0.0 and 1.0"""
        return random.random()
    
    @staticmethod
    def read_i(min_val=0, max_val=2147483647):
        """Return a random integer between min_val and max_val"""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def set_seed(seed):
        """Set the random seed"""
        random.seed(seed)
