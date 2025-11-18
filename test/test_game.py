"""
TNLTest - Test game classes in Python

This is a Python port of the TNL test application, demonstrating
networked object replication.
"""

import sys
import os

# Add parent directory to path to import tnl
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tnl import *
from tnl.types import *
from tnl.bitstream import BitStream
from tnl.net_object import NetObject, SafePtr
from tnl.ghost_connection import GhostConnection
from tnl.net_interface import NetInterface
from tnl.random import Random
from tnl.log import logprintf

class Position:
    """Position structure for game objects"""
    def __init__(self, x=0.0, y=0.0):
        self.x = F32(x)
        self.y = F32(y)

class Player(NetObject):
    """
    Player object that can move around and replicate across the network.
    """
    
    # Player types
    PlayerTypeAI = 0
    PlayerTypeAIDummy = 1
    PlayerTypeClient = 2
    PlayerTypeMyClient = 3
    
    # Mask bits
    InitialMask = 1 << 0
    PositionMask = 1 << 1
    
    def __init__(self, player_type=None):
        super().__init__()
        
        if player_type is None:
            player_type = self.PlayerTypeClient
        
        # Position state
        self.start_pos = Position(Random.read_f(), Random.read_f())
        self.end_pos = Position(self.start_pos.x, self.start_pos.y)
        self.render_pos = Position(self.start_pos.x, self.start_pos.y)
        self.t = 1.0
        self.t_delta = 0.0
        
        self.my_player_type = player_type
        self.game = None
        
        # Mark as ghostable
        self.net_flags = NetObject.Ghostable
    
    def add_to_game(self, game):
        """Add this player to a game"""
        game.players.append(self)
        self.game = game
        
        if self.my_player_type == self.PlayerTypeMyClient:
            game.client_player = SafePtr(self)
    
    def perform_scope_query(self, connection):
        """Determine which objects are in scope"""
        if not self.game:
            return
        
        # All buildings are always in scope
        for building in self.game.buildings:
            connection.object_in_scope(building)
        
        # Players within radius 0.25 are in scope
        for player in self.game.players:
            dx = player.render_pos.x - self.render_pos.x
            dy = player.render_pos.y - self.render_pos.y
            dist_squared = dx * dx + dy * dy
            
            if dist_squared < 0.0625:  # 0.25^2
                connection.object_in_scope(player)
    
    def pack_update(self, connection, update_mask, stream):
        """Pack object state for network transmission"""
        # Initial state
        if stream.write_flag(update_mask & self.InitialMask):
            if stream.write_flag(self.my_player_type != self.PlayerTypeAI):
                stream.write_flag(connection.get_scope_object() == self)
        
        # Position state
        if stream.write_flag(update_mask & self.PositionMask):
            stream.write_float(self.start_pos.x, 12)
            stream.write_float(self.start_pos.y, 12)
            stream.write_float(self.end_pos.x, 12)
            stream.write_float(self.end_pos.y, 12)
            stream.write_float32(self.t)
            stream.write_float32(self.t_delta)
        
        return 0  # All updated
    
    def unpack_update(self, connection, stream):
        """Unpack object state from network"""
        # Initial state
        if stream.read_flag():
            if stream.read_flag():
                if stream.read_flag():
                    self.my_player_type = self.PlayerTypeMyClient
                else:
                    self.my_player_type = self.PlayerTypeClient
            else:
                self.my_player_type = self.PlayerTypeAIDummy
        
        # Position state
        if stream.read_flag():
            self.start_pos.x = stream.read_float(12)
            self.start_pos.y = stream.read_float(12)
            self.end_pos.x = stream.read_float(12)
            self.end_pos.y = stream.read_float(12)
            self.t = stream.read_float32()
            self.t_delta = stream.read_float32()
            self.update(0)
    
    def server_set_position(self, start_pos, end_pos, t, t_delta):
        """Update position on server"""
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.t = t
        self.t_delta = t_delta
        
        # Mark state as changed
        self.set_mask_bits(self.PositionMask)
    
    def update(self, time_delta):
        """Update player movement"""
        self.t += self.t_delta * time_delta
        
        if self.t >= 1.0:
            self.t = 1.0
            self.t_delta = 0.0
            self.render_pos.x = self.end_pos.x
            self.render_pos.y = self.end_pos.y
            
            # AI players pick new random destination
            if self.my_player_type == self.PlayerTypeAI:
                self.start_pos.x = self.render_pos.x
                self.start_pos.y = self.render_pos.y
                self.t = 0.0
                self.end_pos.x = Random.read_f()
                self.end_pos.y = Random.read_f()
                self.t_delta = 0.2 + Random.read_f() * 0.1
                self.set_mask_bits(self.PositionMask)
        
        self.render_pos.x = self.start_pos.x + (self.end_pos.x - self.start_pos.x) * self.t
        self.render_pos.y = self.start_pos.y + (self.end_pos.y - self.start_pos.y) * self.t
    
    def on_ghost_add(self, connection):
        """Called when ghost is added on client"""
        test_interface = connection.get_interface()
        if hasattr(test_interface, 'game'):
            self.add_to_game(test_interface.game)
        return True
    
    def on_ghost_available(self, connection):
        """Called when ghost becomes available on a client"""
        logprintf("Player ghost available at (%g, %g)", 
                 self.render_pos.x, self.render_pos.y)

# Register the Player class
NetObject.register_class("Player", Player)


class Building(NetObject):
    """
    Static building object that is always in scope.
    """
    
    InitialMask = 1 << 0
    
    def __init__(self):
        super().__init__()
        
        self.game = None
        
        # Random position and size
        self.upper_left = Position(Random.read_f() * 0.9, Random.read_f() * 0.9)
        self.lower_right = Position(
            self.upper_left.x + Random.read_f() * 0.1,
            self.upper_left.y + Random.read_f() * 0.1
        )
        
        # Mark as ghostable and scope always
        self.net_flags = NetObject.Ghostable | NetObject.ScopeAlways
    
    def add_to_game(self, game):
        """Add building to game"""
        game.buildings.append(self)
        self.game = game
    
    def pack_update(self, connection, update_mask, stream):
        """Pack building state"""
        if stream.write_flag(update_mask & self.InitialMask):
            stream.write_float(self.upper_left.x, 12)
            stream.write_float(self.upper_left.y, 12)
            stream.write_float(self.lower_right.x, 12)
            stream.write_float(self.lower_right.y, 12)
        
        return 0
    
    def unpack_update(self, connection, stream):
        """Unpack building state"""
        if stream.read_flag():
            self.upper_left.x = stream.read_float(12)
            self.upper_left.y = stream.read_float(12)
            self.lower_right.x = stream.read_float(12)
            self.lower_right.y = stream.read_float(12)
    
    def on_ghost_add(self, connection):
        """Called when ghost is added on client"""
        test_interface = connection.get_interface()
        if hasattr(test_interface, 'game'):
            self.add_to_game(test_interface.game)
        return True

# Register the Building class
NetObject.register_class("Building", Building)


class TestConnection(GhostConnection):
    """
    Test connection class for TNLTest.
    """
    
    def __init__(self):
        super().__init__()
        self.my_player = SafePtr()
    
    def on_connection_established(self):
        """Called when connection is established"""
        super().on_connection_established()
        
        # Activate ghosting
        self.activate_ghosting()
        
        # Server creates a player for this client
        if self.is_server:
            player = Player(Player.PlayerTypeClient)
            test_interface = self.get_interface()
            if hasattr(test_interface, 'game'):
                player.add_to_game(test_interface.game)
            
            self.my_player.set(player)
            self.set_scope_object(player)
            
            logprintf("Server: Created player for client")
    
    def on_connection_terminated(self, reason, reason_string):
        """Called when connection is terminated"""
        super().on_connection_terminated(reason, reason_string)
        
        # Notify interface if this is a client
        if not self.is_server:
            test_interface = self.get_interface()
            if hasattr(test_interface, 'connection_to_server'):
                test_interface.connection_to_server = None
                test_interface.pinging_servers = True
    
    def is_data_to_transmit(self):
        """Always have data to transmit in simulation"""
        return True


class TestNetInterface(NetInterface):
    """
    Network interface for TNLTest with server pinging support.
    """
    
    PingDelayTime = 2000  # milliseconds
    GamePingRequest = 100
    GamePingResponse = 101
    
    def __init__(self, game, is_server, bind_address, ping_address=None):
        super().__init__()
        
        self.game = game
        self.is_server = is_server
        self.pinging_servers = not is_server
        self.last_ping_time = 0
        self.ping_address = ping_address
        self.connection_to_server = None
        
        # Bind to address
        self.bind(bind_address)
        
        if is_server:
            self.set_allow_connections(True)
    
    def handle_connect_request(self, address, stream):
        """Handle incoming connection request"""
        if not self.is_server:
            return
        
        logprintf("Server: Connection request from %s", address)
        
        # Create new connection
        connection = TestConnection()
        connection.set_is_server(True)
        connection.remote_address = address
        
        self.add_connection(connection)
        connection.accept_connection()
    
    def handle_info_packet(self, address, packet_type, stream):
        """Handle ping packets"""
        if packet_type == self.GamePingRequest:
            # Server responds to ping
            if self.is_server:
                logprintf("Server: Ping request from %s", address)
                response_stream = BitStream()
                response_stream.write_bits(8, self.GamePingResponse)
                self.send_packet(address, response_stream.get_buffer())
        
        elif packet_type == self.GamePingResponse:
            # Client received ping response
            if not self.is_server and self.pinging_servers:
                logprintf("Client: Ping response from %s, connecting...", address)
                self.pinging_servers = False
                
                # Connect to server
                connection = TestConnection()
                connection.set_is_server(False)
                self.add_connection(connection)
                connection.connect(address)
                self.connection_to_server = connection
    
    def send_ping(self):
        """Send ping request to find servers"""
        if self.ping_address:
            stream = BitStream()
            stream.write_bits(8, self.GamePingRequest)
            self.send_packet(self.ping_address, stream.get_buffer())
    
    def tick(self):
        """Tick the network interface"""
        super().tick()
        
        # Send pings if looking for servers
        if self.pinging_servers and self.ping_address:
            current_time = NetBase.get_current_time()
            if current_time - self.last_ping_time > self.PingDelayTime:
                self.send_ping()
                self.last_ping_time = current_time


class TestGame:
    """
    Main game class managing players and buildings.
    """
    
    def __init__(self, is_server, bind_address, ping_address=None):
        self.is_server = is_server
        self.players = []
        self.buildings = []
        self.last_time = NetBase.get_current_time()
        self.server_player = SafePtr()
        self.client_player = SafePtr()
        
        # Create network interface
        self.my_net_interface = TestNetInterface(
            self, is_server, bind_address, ping_address
        )
        
        # Server creates world
        if is_server:
            logprintf("Server: Creating game world...")
            
            # Create buildings
            for i in range(50):
                building = Building()
                building.add_to_game(self)
            
            # Create AI players
            for i in range(15):
                player = Player(Player.PlayerTypeAI)
                player.add_to_game(self)
            
            logprintf("Server: Created %d buildings and %d AI players",
                     len(self.buildings), len(self.players))
    
    def tick(self):
        """Main game tick"""
        current_time = NetBase.get_current_time()
        time_delta = (current_time - self.last_time) / 1000.0
        self.last_time = current_time
        
        # Update all players
        for player in self.players:
            player.update(time_delta)
        
        # Tick network
        self.my_net_interface.tick()
    
    def move_my_player_to(self, new_position):
        """Move the player controlled by this client"""
        # This would send RPC to server in full implementation
        logprintf("Moving player to (%g, %g)", new_position.x, new_position.y)
