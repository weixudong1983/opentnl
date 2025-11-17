"""
NetInterface - Network interface for sending/receiving packets
"""
import socket
import select
from .address import Address
from .net_base import NetBase
from .bitstream import BitStream
from .log import logprintf

class NetInterface:
    """
    NetInterface manages UDP socket communication and connection management.
    """
    
    def __init__(self):
        self.socket = None
        self.bind_address = None
        self.connections = []
        self.allow_connections = True
    
    def bind(self, address):
        """
        Bind to a network address.
        
        Args:
            address: Address to bind to
        
        Returns:
            True if successful
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Enable broadcast if needed
            if address.is_broadcast():
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            self.socket.bind(address.to_tuple())
            self.socket.setblocking(False)
            
            self.bind_address = address
            logprintf("NetInterface bound to %s", address)
            return True
            
        except Exception as e:
            logprintf("Failed to bind: %s", str(e))
            return False
    
    def set_allow_connections(self, allow):
        """Set whether to allow incoming connections"""
        self.allow_connections = allow
    
    def add_connection(self, connection):
        """Add a connection to be managed"""
        if connection not in self.connections:
            self.connections.append(connection)
            connection.set_interface(self)
    
    def remove_connection(self, connection):
        """Remove a connection"""
        if connection in self.connections:
            self.connections.remove(connection)
    
    def find_connection(self, address):
        """Find a connection by address"""
        for conn in self.connections:
            if conn.remote_address == address:
                return conn
        return None
    
    def send_packet(self, address, data):
        """
        Send a packet to the specified address.
        
        Args:
            address: Destination address
            data: Packet data (bytes)
        """
        if not self.socket:
            return
        
        try:
            if address.is_broadcast():
                # For broadcast, send to broadcast address
                self.socket.sendto(data, ("<broadcast>", address.port))
            else:
                self.socket.sendto(data, address.to_tuple())
        except Exception as e:
            logprintf("Send error: %s", str(e))
    
    def check_incoming_packets(self):
        """Check for and process incoming packets"""
        if not self.socket:
            return
        
        try:
            # Use select to check for readable data with timeout
            readable, _, _ = select.select([self.socket], [], [], 0)
            
            if readable:
                data, addr = self.socket.recvfrom(1500)
                if data:
                    self.process_packet(Address(Address.IPProtocol, addr[0], addr[1]), data)
                    
        except socket.error:
            pass  # No data available
    
    def process_packet(self, address, data):
        """
        Process an incoming packet.
        
        Args:
            address: Source address
            data: Packet data
        """
        # Find existing connection
        connection = self.find_connection(address)
        
        stream = BitStream(data)
        stream.set_max_sizes(len(data), len(data))
        
        # If no connection exists, check if this is a connection request
        if not connection:
            packet_type = stream.read_bits(8)
            stream.set_bit_position(0)  # Reset for connection to read
            
            if packet_type == 1 and self.allow_connections:  # Connect request
                # Handle connect request - subclasses should override
                self.handle_connect_request(address, stream)
            else:
                # Handle info packets - subclasses can override
                self.handle_info_packet(address, packet_type, stream)
        else:
            # Pass to existing connection
            connection.read_raw_packet(stream)
    
    def handle_connect_request(self, address, stream):
        """
        Handle incoming connection request.
        Override in subclasses to create appropriate connection type.
        """
        logprintf("Connection request from %s (no handler)", address)
    
    def handle_info_packet(self, address, packet_type, stream):
        """
        Handle info packets (pings, etc).
        Override in subclasses.
        """
        pass
    
    def process_connections(self):
        """Process all active connections"""
        # Remove disconnected connections
        self.connections = [c for c in self.connections 
                           if c.connection_state not in 
                           [c.Disconnected, c.TimedOut]]
        
        # Process each connection
        for connection in self.connections:
            connection.check_packet_send()
    
    def tick(self):
        """
        Main tick function - call regularly.
        Checks for incoming packets and processes connections.
        """
        self.check_incoming_packets()
        self.process_connections()
    
    def shutdown(self):
        """Shutdown the network interface"""
        if self.socket:
            self.socket.close()
            self.socket = None
