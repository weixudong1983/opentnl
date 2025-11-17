"""
NetObject - Base class for all network-replicated objects
"""
from .types import U32
from .log import logprintf

class NetObject:
    """
    Base class for all objects that can be ghosted (replicated) across the network.
    This is a simplified version of the C++ TNL NetObject.
    """
    
    # Class-level registry
    _class_registry = {}
    _next_id = 1
    
    # Ghost flags
    Ghostable = 1 << 0
    ScopeAlways = 1 << 1
    
    def __init__(self):
        self.net_flags = 0
        self.mask_bits = 0
        self.ghost_id = 0
        self.server_id = NetObject._next_id
        NetObject._next_id += 1
        self.is_ghost = False
        self.scope_object = None
    
    @classmethod
    def register_class(cls, class_name, class_type=None):
        """Register a NetObject class for network creation"""
        if class_type is None:
            # Called as instance method from subclass
            NetObject._class_registry[class_name] = cls
        else:
            # Called with explicit class type
            NetObject._class_registry[class_name] = class_type
    
    @classmethod
    def create_by_name(cls, class_name):
        """Create a NetObject instance by class name"""
        if class_name in NetObject._class_registry:
            return NetObject._class_registry[class_name]()
        return None
    
    def get_class_name(self):
        """Get the class name for network serialization"""
        return self.__class__.__name__
    
    def set_mask_bits(self, mask):
        """Set mask bits to indicate state has changed"""
        self.mask_bits |= mask
    
    def clear_mask_bits(self, mask):
        """Clear specific mask bits"""
        self.mask_bits &= ~mask
    
    def pack_update(self, connection, update_mask, stream):
        """
        Pack object state update into stream.
        Override in subclasses to implement object-specific serialization.
        
        Args:
            connection: The GhostConnection sending the update
            update_mask: Bitmask of which states to update
            stream: BitStream to write data to
        
        Returns:
            Updated mask bits (usually 0 after successful update)
        """
        return 0
    
    def unpack_update(self, connection, stream):
        """
        Unpack object state update from stream.
        Override in subclasses to implement object-specific deserialization.
        
        Args:
            connection: The GhostConnection receiving the update
            stream: BitStream to read data from
        """
        pass
    
    def perform_scope_query(self, connection):
        """
        Determine which objects are in scope for this object.
        Called on the server for scope objects to determine what should be ghosted.
        
        Args:
            connection: The GhostConnection to perform scoping for
        """
        pass
    
    def on_ghost_add(self, connection):
        """
        Called on the client when a ghost is first added.
        
        Args:
            connection: The GhostConnection that added the ghost
        
        Returns:
            True if successful, False to terminate connection
        """
        return True
    
    def on_ghost_remove(self):
        """Called on the client when a ghost is removed"""
        pass
    
    def on_ghost_available(self, connection):
        """
        Called on the server when a ghost becomes available on a client.
        
        Args:
            connection: The GhostConnection where ghost is now available
        """
        pass

class SafePtr:
    """
    Safe pointer that handles object deletion gracefully.
    Similar to TNL::SafePtr in C++.
    """
    def __init__(self, obj=None):
        self._obj = obj
    
    def set(self, obj):
        """Set the pointer to a new object"""
        self._obj = obj
    
    def get(self):
        """Get the current object"""
        return self._obj
    
    def is_valid(self):
        """Check if the pointer is valid"""
        return self._obj is not None
    
    def __bool__(self):
        """Boolean conversion"""
        return self._obj is not None
    
    def __eq__(self, other):
        """Equality comparison"""
        if isinstance(other, SafePtr):
            return self._obj == other._obj
        return self._obj == other
