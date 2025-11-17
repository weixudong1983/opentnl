"""
Torque Network Library - Python Implementation
Copyright (C) 2004 GarageGames.com, Inc.
Python port 2024

This is a simplified Python implementation of the TNL library
focusing on core networking features for the test application.
"""

from .types import *
from .bitstream import BitStream
from .random import Random
from .address import Address
from .net_base import NetBase
from .net_object import NetObject
from .net_connection import NetConnection
from .ghost_connection import GhostConnection
from .net_interface import NetInterface
from .log import Log, LogConsumer

__version__ = "1.0.0"
__all__ = [
    'BitStream', 'Random', 'Address', 'NetBase', 
    'NetObject', 'NetConnection', 'GhostConnection', 
    'NetInterface', 'Log', 'LogConsumer'
]
