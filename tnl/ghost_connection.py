"""
GhostConnection - Connection that supports object ghosting (replication)
"""
from .net_connection import NetConnection
from .net_object import NetObject
from .bitstream import BitStream
from .log import logprintf

class GhostInfo:
    """Information about a ghosted object"""
    def __init__(self):
        self.obj = None
        self.ghost_id = 0
        self.update_mask = 0
        self.flags = 0
        self.initial_sent = False  # Track if initial state has been sent

class GhostConnection(NetConnection):
    """
    GhostConnection extends NetConnection to support object replication (ghosting).
    Objects on the server can be "ghosted" to clients, with automatic state updates.
    """
    
    def __init__(self):
        super().__init__()
        self.ghost_array = {}  # ghost_id -> GhostInfo
        self.local_ghosts = {}  # server_id -> GhostInfo
        self.next_ghost_id = 1
        self.scope_object = None
        self.ghosting_sequence = False
        self.ghosting = False
        self.is_server = False
    
    def set_is_server(self, is_server):
        """Set whether this is the server side of the connection"""
        self.is_server = is_server
    
    def set_scope_object(self, obj):
        """Set the object used for scoping queries"""
        self.scope_object = obj
        obj.scope_object = self
    
    def get_scope_object(self):
        """Get the scope object"""
        return self.scope_object
    
    def activate_ghosting(self):
        """Activate ghosting for this connection"""
        self.ghosting = True
        logprintf("Ghosting activated")
    
    def is_ghosting(self):
        """Check if ghosting is active"""
        return self.ghosting
    
    def object_in_scope(self, obj):
        """
        Mark an object as being in scope for this connection.
        Called during scope queries.
        """
        if not obj or not (obj.net_flags & NetObject.Ghostable):
            return
        
        server_id = obj.server_id
        
        # Check if already ghosted
        if server_id in self.local_ghosts:
            ghost_info = self.local_ghosts[server_id]
            # Update mask with current changes
            ghost_info.update_mask |= obj.mask_bits
        else:
            # Need to ghost this object
            ghost_info = GhostInfo()
            ghost_info.obj = obj
            ghost_info.ghost_id = self.next_ghost_id
            self.next_ghost_id += 1
            ghost_info.update_mask = 0xFFFFFFFF  # Send all state initially
            
            self.ghost_array[ghost_info.ghost_id] = ghost_info
            self.local_ghosts[server_id] = ghost_info
    
    def send_packet(self):
        """Send a packet with ghost updates"""
        if not self.is_connected() or not self.ghosting:
            return
        
        stream = BitStream()
        stream.write_bits(8, 10)  # Ghost update packet type
        
        self.write_packet(stream)
        self.write_raw_packet(stream)
    
    def write_packet(self, stream):
        """
        Write ghost updates into the packet stream.
        This is where object state synchronization happens.
        """
        if not self.is_server:
            return
        
        # Perform scope query if we have a scope object
        if self.scope_object:
            self.scope_object.perform_scope_query(self)
        
        # Write updates for all in-scope ghosts
        updates_written = 0
        max_updates = 50  # Limit updates per packet
        
        for ghost_info in list(self.ghost_array.values()):
            if updates_written >= max_updates:
                break
            
            obj = ghost_info.obj
            if not obj:
                continue
            
            # Check if object needs update
            update_mask = ghost_info.update_mask
            if update_mask == 0:
                continue
            
            # Write ghost update
            stream.write_flag(True)  # Has update
            stream.write_bits(16, ghost_info.ghost_id)
            
            # Check if this is initial ghost creation
            is_initial = not ghost_info.initial_sent
            
            # Write initial flag
            stream.write_flag(is_initial)
            
            if is_initial:
                # Write class name for creation
                stream.write_string(obj.get_class_name())
                ghost_info.initial_sent = True
            
            # Pack the object's state
            remaining_mask = obj.pack_update(self, update_mask, stream)
            
            # Clear the updated bits
            ghost_info.update_mask = remaining_mask
            obj.mask_bits &= remaining_mask
            
            updates_written += 1
            
            # Notify that ghost is available
            if is_initial:
                obj.on_ghost_available(self)
        
        # Write end marker
        stream.write_flag(False)
    
    def read_raw_packet(self, stream):
        """Read and process incoming packet"""
        super().read_raw_packet(stream)
        
        packet_type = stream.read_bits(8)
        
        if packet_type == 1:  # Connect request
            self.accept_connection()
        elif packet_type == 2:  # Connect accept
            self.connection_state = self.Connected
            self.on_connection_established()
        elif packet_type == 3:  # Disconnect
            reason = stream.read_string()
            self.on_connection_terminated(self.ReasonRemoteDisconnect, reason)
        elif packet_type == 10:  # Ghost update
            self.read_packet(stream)
    
    def read_packet(self, stream):
        """Read ghost updates from packet stream"""
        if self.is_server:
            return
        
        # Read ghost updates
        while stream.read_flag():  # Has update
            ghost_id = stream.read_bits(16)
            
            # Read initial flag
            is_initial = stream.read_flag()
            
            if is_initial:
                # New ghost - read class name and create
                class_name = stream.read_string()
                obj = NetObject.create_by_name(class_name)
                
                if obj:
                    obj.is_ghost = True
                    obj.ghost_id = ghost_id
                    
                    ghost_info = GhostInfo()
                    ghost_info.obj = obj
                    ghost_info.ghost_id = ghost_id
                    
                    self.ghost_array[ghost_id] = ghost_info
                    
                    # Unpack initial state
                    obj.unpack_update(self, stream)
                    
                    # Notify ghost was added
                    if not obj.on_ghost_add(self):
                        # Ghost add failed - should disconnect
                        self.disconnect("Ghost add failed")
                        return
                else:
                    logprintf("Failed to create ghost of type %s", class_name)
                    return
            else:
                # Existing ghost - update state
                if ghost_id in self.ghost_array:
                    ghost_info = self.ghost_array[ghost_id]
                    if ghost_info.obj:
                        ghost_info.obj.unpack_update(self, stream)
    
    def post_net_event(self, event):
        """Post a network event (RPC) - simplified stub"""
        # In full TNL this would queue events for transmission
        # For this simplified version, we'll just log
        logprintf("Net event posted: %s", event.__class__.__name__)
