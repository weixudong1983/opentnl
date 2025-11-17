"""
Game object base classes and types
"""
from geometry import Point, Rect
from enum import IntFlag


class GameObjectType(IntFlag):
    """Object type flags (can be combined with bitwise OR)"""
    UNKNOWN = 1 << 0
    SHIP = 1 << 1
    BARRIER = 1 << 2
    MOVEABLE = 1 << 3
    PROJECTILE = 1 << 4
    ITEM = 1 << 5
    RESOURCE_ITEM = 1 << 6
    ENGINEERED = 1 << 7
    FORCE_FIELD = 1 << 8
    LOADOUT_ZONE = 1 << 9
    MINE = 1 << 10
    TEST_ITEM = 1 << 11
    FLAG = 1 << 12
    TURRET_TARGET = 1 << 13
    DELETED = 1 << 30
    COMMAND_MAP_VIS = 1 << 31


# Combined types
DAMAGEABLE_TYPES = (GameObjectType.SHIP | GameObjectType.MOVEABLE | 
                   GameObjectType.PROJECTILE | GameObjectType.ITEM | 
                   GameObjectType.RESOURCE_ITEM | GameObjectType.ENGINEERED | 
                   GameObjectType.MINE)

MOTION_TRIGGER_TYPES = (GameObjectType.SHIP | GameObjectType.RESOURCE_ITEM | 
                       GameObjectType.TEST_ITEM)


class DamageInfo:
    """Information about damage dealt"""
    
    def __init__(self):
        self.collision_point = Point()
        self.impulse_vector = Point()
        self.damage_amount = 0.0
        self.damage_type = 0
        self.damaging_object = None


class GameObject:
    """Base class for all game objects"""
    
    def __init__(self, game=None):
        self.game = game
        self.position = Point()
        self.velocity = Point()
        self.object_type_mask = GameObjectType.UNKNOWN
        self.team = -1
        self.extent = Rect()
        self.creation_time = 0
        self.in_database = False
        self.controlling_client = None
        self.owner = None
        self.disable_collision_count = 0
        self.to_delete = False
    
    def get_pos(self):
        """Get position"""
        return self.position
    
    def set_pos(self, pos):
        """Set position"""
        self.position = pos.copy()
        self.update_extent()
    
    def get_vel(self):
        """Get velocity"""
        return self.velocity
    
    def get_team(self):
        """Get team"""
        return self.team
    
    def set_team(self, team):
        """Set team"""
        self.team = team
    
    def get_object_type_mask(self):
        """Get object type mask"""
        return self.object_type_mask
    
    def update_extent(self):
        """Update bounding box - override in subclasses"""
        pass
    
    def idle(self, time_delta):
        """Update object - override in subclasses"""
        pass
    
    def render(self, screen, camera_offset=Point()):
        """Render object - override in subclasses"""
        pass
    
    def damage_object(self, damage_info):
        """Apply damage - override in subclasses"""
        pass
    
    def collide(self, other):
        """Handle collision with another object"""
        pass
    
    def is_deleted(self):
        """Check if object should be deleted"""
        return self.to_delete


class MoveObject(GameObject):
    """Base class for objects that can move"""
    
    def __init__(self, game=None):
        super().__init__(game)
        self.actual_pos = Point()
        self.actual_vel = Point()
        self.render_pos = Point()
        self.render_vel = Point()
        self.angle = 0.0
        self.angular_velocity = 0.0
        self.last_move = None
        self.current_move = None
    
    def get_actual_pos(self):
        """Get actual position"""
        return self.actual_pos
    
    def set_actual_pos(self, pos):
        """Set actual position"""
        self.actual_pos = pos.copy()
        self.position = pos.copy()
        self.update_extent()
    
    def get_render_pos(self):
        """Get render position for interpolation"""
        return self.render_pos
    
    def update_interpolation(self):
        """Update render position for smooth movement"""
        # Simple lerp
        self.render_pos = self.position.copy()
        self.render_vel = self.velocity.copy()
    
    def process_move(self, time_delta):
        """Process movement - override in subclasses"""
        pass


class Move:
    """Player input/movement state"""
    
    def __init__(self):
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        self.fire = False
        self.activate_module_1 = False
        self.activate_module_2 = False
        self.angle = 0.0  # Mouse/aim angle
