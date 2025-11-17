"""
Projectile class - weapons fire
"""
import math
import pygame
from geometry import Point
from game_object import MoveObject, GameObjectType, DamageInfo


class Projectile(MoveObject):
    """Projectile fired from weapons"""
    
    COLLISION_RADIUS = 5
    LIFETIME = 2000  # milliseconds
    
    def __init__(self, game=None, pos=Point(), vel=Point(), source=None, bounces=False):
        super().__init__(game)
        self.object_type_mask = GameObjectType.PROJECTILE
        self.position = pos.copy()
        self.actual_pos = pos.copy()
        self.velocity = vel.copy()
        self.source = source
        self.bounces = bounces
        self.lifetime = self.LIFETIME
        self.team = source.team if source else -1
        self.damage_amount = 0.3
    
    def idle(self, time_delta):
        """Update projectile"""
        # Update position
        self.position += self.velocity * time_delta
        self.actual_pos = self.position.copy()
        
        # Update lifetime
        self.lifetime -= time_delta * 1000
        if self.lifetime <= 0:
            self.to_delete = True
        
        # Update extent
        self.update_extent()
    
    def update_extent(self):
        """Update bounding box"""
        radius = self.COLLISION_RADIUS
        self.extent.min = Point(self.position.x - radius, self.position.y - radius)
        self.extent.max = Point(self.position.x + radius, self.position.y + radius)
    
    def collide_with_ship(self, ship):
        """Handle collision with ship"""
        # Don't hit own ship
        if ship == self.source:
            return
        
        # Don't hit teammates
        if ship.team == self.team and self.team != -1:
            return
        
        # Create damage info
        damage = DamageInfo()
        damage.collision_point = self.position.copy()
        damage.impulse_vector = self.velocity.normalized(50)
        damage.damage_amount = self.damage_amount
        damage.damaging_object = self
        
        ship.damage_object(damage)
        self.to_delete = True
    
    def collide_with_barrier(self, barrier):
        """Handle collision with barrier"""
        if self.bounces:
            # Calculate bounce
            # Simple: reverse velocity on collision
            # More complex would calculate normal and reflect
            self.velocity = -self.velocity
        else:
            self.to_delete = True
    
    def render(self, screen, camera_offset=Point()):
        """Render projectile"""
        screen_pos = (self.position - camera_offset).to_tuple()
        
        # Draw as circle
        if self.bounces:
            color = (255, 255, 0)  # Yellow for bouncer
        else:
            color = (255, 100, 100)  # Red for normal
        
        pygame.draw.circle(screen, color, screen_pos, self.COLLISION_RADIUS)
        pygame.draw.circle(screen, (255, 255, 255), screen_pos, self.COLLISION_RADIUS, 1)
