"""
Network Address representation
"""
import socket
import struct

class Address:
    """
    Network address class supporting IPv4 UDP addresses
    """
    
    # Protocol types
    IPProtocol = 0
    
    # Special address constants
    Any = "0.0.0.0"
    Broadcast = "255.255.255.255"
    
    def __init__(self, protocol=None, host="0.0.0.0", port=0):
        """
        Create a network address
        
        Args:
            protocol: Protocol type (currently only IP is supported)
            host: IP address string or 'broadcast' for broadcast address
            port: Port number
        """
        self.protocol = protocol if protocol is not None else self.IPProtocol
        
        if isinstance(host, str):
            if host.lower() == "any":
                self.host = "0.0.0.0"
            elif host.lower() == "broadcast":
                self.host = "255.255.255.255"
            else:
                self.host = host
        else:
            self.host = host
        
        self.port = port
    
    @classmethod
    def from_string(cls, addr_string):
        """
        Parse address from string format: "IP:host:port" or "IP:broadcast:port"
        
        Example: "IP:192.168.1.1:28999" or "IP:broadcast:28999"
        """
        parts = addr_string.split(':')
        if len(parts) < 3:
            return cls()
        
        protocol = cls.IPProtocol  # parts[0] would be "IP"
        host = parts[1]
        port = int(parts[2])
        
        return cls(protocol, host, port)
    
    def to_tuple(self):
        """Convert to (host, port) tuple for socket operations"""
        return (self.host, self.port)
    
    def is_broadcast(self):
        """Check if this is a broadcast address"""
        return self.host == "255.255.255.255" or self.host == "<broadcast>"
    
    def __eq__(self, other):
        """Check if two addresses are equal"""
        if not isinstance(other, Address):
            return False
        return self.host == other.host and self.port == other.port
    
    def __hash__(self):
        """Hash for use in dictionaries"""
        return hash((self.host, self.port))
    
    def __str__(self):
        """String representation"""
        return f"IP:{self.host}:{self.port}"
    
    def __repr__(self):
        """Debug representation"""
        return f"Address(host='{self.host}', port={self.port})"
