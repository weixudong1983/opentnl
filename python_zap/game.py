"""
Main game class and game loop
"""
import pygame
import time
from geometry import Point
from game_object import GameObject, Move
from ship import Ship
from barrier import Barrier, GoalZone
from projectile import Projectile


class Game:
    """Main game class"""
    
    def __init__(self, width=1024, height=768):
        self.width = width
        self.height = height
        self.objects = []
        self.players = []
        self.current_time = 0
        self.game_type = None
        self.camera_offset = Point(0, 0)
        
        # Initialize game objects
        self.init_game()
    
    def init_game(self):
        """Initialize game world"""
        # Create some barriers (arena walls)
        # Outer walls
        self.add_object(Barrier(self, Point(50, 50), Point(950, 50), 10))  # Top
        self.add_object(Barrier(self, Point(950, 50), Point(950, 700), 10))  # Right
        self.add_object(Barrier(self, Point(950, 700), Point(50, 700), 10))  # Bottom
        self.add_object(Barrier(self, Point(50, 700), Point(50, 50), 10))  # Left
        
        # Some internal barriers
        self.add_object(Barrier(self, Point(300, 200), Point(300, 400), 8))
        self.add_object(Barrier(self, Point(700, 200), Point(700, 400), 8))
        self.add_object(Barrier(self, Point(400, 350), Point(600, 350), 8))
        
        # Create goal zones for CTF-style gameplay
        self.add_object(GoalZone(self, Point(150, 150), 60, team=0))  # Blue team
        self.add_object(GoalZone(self, Point(850, 550), 60, team=1))  # Red team
    
    def add_object(self, obj):
        """Add object to game"""
        self.objects.append(obj)
    
    def remove_object(self, obj):
        """Remove object from game"""
        if obj in self.objects:
            self.objects.remove(obj)
    
    def create_player(self, player_name="Player", team=-1):
        """Create a new player ship"""
        # Random spawn position (simplified)
        import random
        pos = Point(
            random.randint(100, self.width - 100),
            random.randint(100, self.height - 100)
        )
        
        ship = Ship(self, player_name, team, pos)
        self.add_object(ship)
        self.players.append(ship)
        return ship
    
    def update(self, time_delta):
        """Update all game objects"""
        self.current_time += time_delta
        
        # Update all objects
        for obj in self.objects[:]:  # Copy list to allow modification
            obj.idle(time_delta)
        
        # Check collisions
        self.check_collisions()
        
        # Remove deleted objects
        self.objects = [obj for obj in self.objects if not obj.is_deleted()]
    
    def check_collisions(self):
        """Check for collisions between objects"""
        # Ships vs projectiles
        ships = [obj for obj in self.objects if isinstance(obj, Ship)]
        projectiles = [obj for obj in self.objects if isinstance(obj, Projectile)]
        barriers = [obj for obj in self.objects if isinstance(obj, Barrier)]
        
        for proj in projectiles:
            # Check ship collisions
            for ship in ships:
                if ship.has_exploded:
                    continue
                
                dist = (proj.position - ship.position).len()
                if dist < Ship.COLLISION_RADIUS + Projectile.COLLISION_RADIUS:
                    proj.collide_with_ship(ship)
            
            # Check barrier collisions
            for barrier in barriers:
                if barrier.extent.contains(proj.position):
                    proj.collide_with_barrier(barrier)
        
        # Ships vs barriers (prevent movement through walls)
        for ship in ships:
            if ship.has_exploded:
                continue
            
            for barrier in barriers:
                if barrier.collides_with_point(ship.position, Ship.COLLISION_RADIUS):
                    # Push ship out of barrier (simplified)
                    # More complex would calculate collision normal
                    ship.velocity = ship.velocity * -0.5
    
    def render(self, screen):
        """Render all game objects"""
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Render all objects
        for obj in self.objects:
            obj.render(screen, self.camera_offset)
    
    def get_local_player(self):
        """Get the local player's ship"""
        if self.players:
            return self.players[0]
        return None


class ClientGame(Game):
    """Client-side game"""
    
    def __init__(self, width=1024, height=768):
        super().__init__(width, height)
        self.local_player = None
    
    def create_local_player(self, player_name="Player"):
        """Create local player"""
        self.local_player = self.create_player(player_name, team=0)
        return self.local_player
    
    def update_camera(self):
        """Update camera to follow player"""
        if self.local_player and not self.local_player.has_exploded:
            # Center camera on player
            target_x = self.local_player.position.x - self.width / 2
            target_y = self.local_player.position.y - self.height / 2
            
            # Smooth camera movement
            self.camera_offset.x += (target_x - self.camera_offset.x) * 0.1
            self.camera_offset.y += (target_y - self.camera_offset.y) * 0.1


class ServerGame(Game):
    """Server-side game"""
    
    def __init__(self, width=1024, height=768):
        super().__init__(width, height)
        self.server = None
