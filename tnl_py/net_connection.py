"""
NetConnection - Base class for network connections
"""
from .types import U32
from .net_base import NetBase
from .log import logprintf
from .bitstream import BitStream

class NetConnection:
    """
    Base class for all network connections.
    Manages connection state and packet transmission.
    """
    
    # Connection states
    NotConnected = 0
    AwaitingChallengeResponse = 1
    SendingPunchPackets = 2
    ComputingPuzzleSolution = 3
    AwaitingConnectResponse = 4
    Connected = 5
    TimedOut = 6
    Disconnected = 7
    
    # Termination reasons
    ReasonSelfDisconnect = 0
    ReasonRemoteDisconnect = 1
    ReasonTimedOut = 2
    ReasonError = 3
    
    def __init__(self):
        self.connection_state = self.NotConnected
        self.interface = None
        self.remote_address = None
        self.last_packet_send_time = 0
        self.last_packet_recv_time = 0
    
    def set_interface(self, interface):
        """Set the network interface for this connection"""
        self.interface = interface
    
    def get_interface(self):
        """Get the network interface"""
        return self.interface
    
    def connect(self, address):
        """Initiate a connection to the specified address"""
        self.remote_address = address
        self.connection_state = self.AwaitingConnectResponse
        self.send_connect_request()
    
    def send_connect_request(self):
        """Send connection request packet"""
        # Simplified - in real TNL this does challenge-response
        stream = BitStream()
        stream.write_bits(8, 1)  # Connect request packet type
        self.write_raw_packet(stream)
    
    def accept_connection(self):
        """Accept an incoming connection"""
        self.connection_state = self.Connected
        self.send_connect_accept()
        self.on_connection_established()
    
    def send_connect_accept(self):
        """Send connection accept packet"""
        stream = BitStream()
        stream.write_bits(8, 2)  # Connect accept packet type
        self.write_raw_packet(stream)
    
    def disconnect(self, reason_string=""):
        """Disconnect from remote host"""
        if self.connection_state == self.Connected:
            self.send_disconnect_packet(reason_string)
        
        self.connection_state = self.Disconnected
        self.on_connection_terminated(self.ReasonSelfDisconnect, reason_string)
    
    def send_disconnect_packet(self, reason):
        """Send disconnect packet"""
        stream = BitStream()
        stream.write_bits(8, 3)  # Disconnect packet type
        stream.write_string(reason)
        self.write_raw_packet(stream)
    
    def is_connected(self):
        """Check if connection is established"""
        return self.connection_state == self.Connected
    
    def check_packet_send(self):
        """Check if it's time to send a packet"""
        if not self.is_connected():
            return
        
        current_time = NetBase.get_current_time()
        # Send packet every 32ms (roughly 30Hz)
        if current_time - self.last_packet_send_time > 32:
            self.send_packet()
    
    def send_packet(self):
        """Send a data packet - override in subclasses"""
        pass
    
    def write_raw_packet(self, stream):
        """Write raw packet to network interface"""
        if self.interface and self.remote_address:
            self.interface.send_packet(self.remote_address, stream.get_buffer())
            self.last_packet_send_time = NetBase.get_current_time()
    
    def read_raw_packet(self, stream):
        """Read raw packet from network - override in subclasses"""
        self.last_packet_recv_time = NetBase.get_current_time()
    
    def is_data_to_transmit(self):
        """Check if there is data to transmit"""
        return True
    
    # Event handlers - override in subclasses
    
    def on_connect_terminated(self, reason, reason_string):
        """Called when connection attempt fails"""
        logprintf("Connection terminated: %s", reason_string)
    
    def on_connection_terminated(self, reason, reason_string):
        """Called when established connection is terminated"""
        logprintf("Connection terminated: %s", reason_string)
    
    def on_connection_established(self):
        """Called when connection is established"""
        logprintf("Connection established")
