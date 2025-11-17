"""
Barrier class - walls and obstacles
"""
import pygame
from geometry import Point, Rect
from game_object import GameObject, GameObjectType


class Barrier(GameObject):
    """Static wall/barrier"""
    
    def __init__(self, game=None, start=Point(), end=Point(), width=10):
        super().__init__(game)
        self.object_type_mask = GameObjectType.BARRIER
        self.start = start.copy()
        self.end = end.copy()
        self.width = width
        self.update_extent()
    
    def update_extent(self):
        """Update bounding box"""
        half_width = self.width / 2
        self.extent.min = Point(
            min(self.start.x, self.end.x) - half_width,
            min(self.start.y, self.end.y) - half_width
        )
        self.extent.max = Point(
            max(self.start.x, self.end.x) + half_width,
            max(self.start.y, self.end.y) + half_width
        )
    
    def collides_with_point(self, point, radius=0):
        """Check if point (with radius) collides with barrier"""
        # Simple line segment collision
        # This is simplified - more accurate would use distance to line segment
        return self.extent.contains(point)
    
    def render(self, screen, camera_offset=Point()):
        """Render barrier"""
        start_screen = (self.start - camera_offset).to_tuple()
        end_screen = (self.end - camera_offset).to_tuple()
        
        color = (150, 150, 150)  # Gray
        pygame.draw.line(screen, color, start_screen, end_screen, self.width)
        pygame.draw.line(screen, (255, 255, 255), start_screen, end_screen, 2)


class GoalZone(GameObject):
    """Goal zone for game types like CTF"""
    
    def __init__(self, game=None, center=Point(), radius=50, team=-1):
        super().__init__(game)
        self.object_type_mask = GameObjectType.ITEM  # Or create GOAL_ZONE type
        self.position = center.copy()
        self.radius = radius
        self.team = team
        self.update_extent()
    
    def update_extent(self):
        """Update bounding box"""
        self.extent.min = Point(
            self.position.x - self.radius,
            self.position.y - self.radius
        )
        self.extent.max = Point(
            self.position.x + self.radius,
            self.position.y + self.radius
        )
    
    def contains_point(self, point):
        """Check if point is inside goal zone"""
        dist = (point - self.position).len()
        return dist <= self.radius
    
    def render(self, screen, camera_offset=Point()):
        """Render goal zone"""
        screen_pos = (self.position - camera_offset).to_tuple()
        
        # Color based on team
        if self.team == 0:
            color = (50, 50, 150)  # Blue
        elif self.team == 1:
            color = (150, 50, 50)  # Red
        else:
            color = (50, 150, 50)  # Green
        
        # Draw circle
        pygame.draw.circle(screen, color, screen_pos, int(self.radius))
        pygame.draw.circle(screen, (255, 255, 255), screen_pos, int(self.radius), 2)
