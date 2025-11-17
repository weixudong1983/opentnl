"""
Ship class - the player's controllable object
"""
import math
import pygame
from geometry import Point, Color
from game_object import MoveObject, GameObjectType, DamageInfo


# Ship modules (equipment)
class ShipModule:
    NONE = 0
    BOOST = 1
    SHIELD = 2
    REPAIR = 3
    SENSOR = 4
    CLOAK = 5
    ENGINEER = 6


# Ship weapons
class ShipWeapon:
    NONE = 0
    PHASER = 1
    BOUNCER = 2
    TRIPLE = 3
    BURST = 4
    MINE = 5


class Ship(MoveObject):
    """Player ship"""
    
    # Constants
    MAX_VELOCITY = 450.0  # points per second
    ACCELERATION = 2500.0
    BOOST_MAX_VELOCITY = 700.0
    BOOST_ACCELERATION = 5000.0
    REPAIR_RADIUS = 65
    COLLISION_RADIUS = 24
    VISIBILITY_RADIUS = 30
    ENERGY_MAX = 100000
    ENERGY_RECHARGE_RATE = 6000
    ENERGY_BOOST_DRAIN = 15000
    ENERGY_SHIELD_DRAIN = 27000
    ENERGY_REPAIR_DRAIN = 15000
    ENERGY_SENSOR_DRAIN = 8000
    ENERGY_CLOAK_DRAIN = 8000
    WEAPON_FIRE_DELAY = 250  # milliseconds
    
    def __init__(self, game=None, player_name="Player", team=-1, pos=Point(0, 0)):
        super().__init__(game)
        self.object_type_mask = GameObjectType.SHIP
        self.player_name = player_name
        self.team = team
        self.position = pos.copy()
        self.actual_pos = pos.copy()
        
        # Ship state
        self.health = 1.0  # 0.0 to 1.0
        self.energy = self.ENERGY_MAX
        self.mass = 1.0
        self.has_exploded = False
        self.cooldown = False
        
        # Weapons and modules
        self.modules = [ShipModule.BOOST, ShipModule.SHIELD]
        self.module_active = {
            ShipModule.BOOST: False,
            ShipModule.SHIELD: False,
            ShipModule.REPAIR: False,
            ShipModule.SENSOR: False,
            ShipModule.CLOAK: False,
            ShipModule.ENGINEER: False
        }
        
        self.weapons = [ShipWeapon.PHASER, ShipWeapon.BOUNCER, ShipWeapon.TRIPLE]
        self.active_weapon = 0
        
        # Timers
        self.fire_timer = 0
        self.warp_in_timer = 0
        self.sensor_zoom_timer = 0
        self.weapon_fire_decloak_timer = 0
        self.cloak_timer = 0
        
        # Visual
        self.trail_points = []
        self.mounted_items = []
        self.repair_targets = []
    
    def is_shield_active(self):
        return self.module_active.get(ShipModule.SHIELD, False)
    
    def is_boost_active(self):
        return self.module_active.get(ShipModule.BOOST, False)
    
    def is_cloak_active(self):
        return self.module_active.get(ShipModule.CLOAK, False)
    
    def is_sensor_active(self):
        return self.module_active.get(ShipModule.SENSOR, False)
    
    def is_repair_active(self):
        return self.module_active.get(ShipModule.REPAIR, False)
    
    def is_destroyed(self):
        return self.has_exploded
    
    def set_loadout(self, module1, module2, weapon1, weapon2, weapon3):
        """Set ship loadout"""
        self.modules = [module1, module2]
        self.weapons = [weapon1, weapon2, weapon3]
        self.active_weapon = 0
    
    def select_weapon(self, index=None):
        """Select weapon by index, or cycle to next"""
        if index is not None:
            self.active_weapon = max(0, min(len(self.weapons) - 1, index))
        else:
            self.active_weapon = (self.active_weapon + 1) % len(self.weapons)
    
    def process_move(self, time_delta):
        """Process ship movement based on current move"""
        if self.has_exploded or not self.current_move:
            return
        
        # Determine max velocity and acceleration
        max_vel = self.MAX_VELOCITY
        accel = self.ACCELERATION
        
        if self.is_boost_active() and self.energy > 0:
            max_vel = self.BOOST_MAX_VELOCITY
            accel = self.BOOST_ACCELERATION
        
        # Calculate movement direction from input
        move_dir = Point()
        if self.current_move.forward:
            move_dir.y -= 1
        if self.current_move.backward:
            move_dir.y += 1
        if self.current_move.left:
            move_dir.x -= 1
        if self.current_move.right:
            move_dir.x += 1
        
        # Normalize and scale by acceleration
        if move_dir.len() > 0:
            move_dir.normalize(accel * time_delta)
            self.velocity += move_dir
        
        # Apply drag/friction
        if move_dir.len() == 0:
            friction = 0.95
            self.velocity *= friction
        
        # Limit velocity
        vel_len = self.velocity.len()
        if vel_len > max_vel:
            self.velocity.normalize(max_vel)
        
        # Update position
        self.position += self.velocity * time_delta
        self.actual_pos = self.position.copy()
        
        # Update angle from move input
        if hasattr(self.current_move, 'angle'):
            self.angle = self.current_move.angle
    
    def process_weapon_fire(self):
        """Process weapon firing"""
        if not self.current_move or not self.current_move.fire:
            return
        
        if self.fire_timer > 0:
            return
        
        # Fire weapon based on active weapon type
        weapon = self.weapons[self.active_weapon] if self.active_weapon < len(self.weapons) else ShipWeapon.NONE
        
        if weapon == ShipWeapon.PHASER:
            self.fire_phaser()
        elif weapon == ShipWeapon.BOUNCER:
            self.fire_bouncer()
        elif weapon == ShipWeapon.TRIPLE:
            self.fire_triple()
        
        self.fire_timer = self.WEAPON_FIRE_DELAY
    
    def fire_phaser(self):
        """Fire a phaser projectile"""
        if self.game:
            from projectile import Projectile
            aim = Point(math.cos(self.angle), math.sin(self.angle))
            proj = Projectile(self.game, self.position, aim * 600, self)
            self.game.add_object(proj)
    
    def fire_bouncer(self):
        """Fire a bouncer projectile"""
        # Similar to phaser but bounces off walls
        if self.game:
            from projectile import Projectile
            aim = Point(math.cos(self.angle), math.sin(self.angle))
            proj = Projectile(self.game, self.position, aim * 500, self, bounces=True)
            self.game.add_object(proj)
    
    def fire_triple(self):
        """Fire three projectiles"""
        if self.game:
            from projectile import Projectile
            aim = Point(math.cos(self.angle), math.sin(self.angle))
            spread = 0.15  # radians
            
            for offset in [-spread, 0, spread]:
                angle = self.angle + offset
                dir_vec = Point(math.cos(angle), math.sin(angle))
                proj = Projectile(self.game, self.position, dir_vec * 600, self)
                self.game.add_object(proj)
    
    def process_energy(self, time_delta):
        """Update energy based on active modules"""
        # Recharge energy
        if not self.cooldown:
            self.energy = min(self.ENERGY_MAX, self.energy + self.ENERGY_RECHARGE_RATE * time_delta)
        
        # Drain energy from active modules
        if self.is_boost_active():
            self.energy -= self.ENERGY_BOOST_DRAIN * time_delta
        if self.is_shield_active():
            self.energy -= self.ENERGY_SHIELD_DRAIN * time_delta
        if self.is_repair_active():
            self.energy -= self.ENERGY_REPAIR_DRAIN * time_delta
        if self.is_sensor_active():
            self.energy -= self.ENERGY_SENSOR_DRAIN * time_delta
        if self.is_cloak_active():
            self.energy -= self.ENERGY_CLOAK_DRAIN * time_delta
        
        # Deactivate modules if out of energy
        if self.energy <= 0:
            self.energy = 0
            self.cooldown = True
            for module in self.module_active:
                self.module_active[module] = False
        
        # Exit cooldown when energy is recharged enough
        if self.cooldown and self.energy > 15000:
            self.cooldown = False
    
    def idle(self, time_delta):
        """Update ship each frame"""
        if self.has_exploded:
            return
        
        # Update timers
        self.fire_timer = max(0, self.fire_timer - time_delta * 1000)
        
        # Process movement
        self.process_move(time_delta)
        
        # Process energy
        self.process_energy(time_delta)
        
        # Process weapon fire
        self.process_weapon_fire()
        
        # Update extent
        self.update_extent()
    
    def update_extent(self):
        """Update bounding box"""
        radius = self.COLLISION_RADIUS
        self.extent.min = Point(self.position.x - radius, self.position.y - radius)
        self.extent.max = Point(self.position.x + radius, self.position.y + radius)
    
    def damage_object(self, damage_info):
        """Take damage"""
        if self.has_exploded:
            return
        
        # Shield absorbs damage
        if self.is_shield_active():
            self.energy -= 20000
            if self.energy < 0:
                self.energy = 0
                self.module_active[ShipModule.SHIELD] = False
                self.health -= damage_info.damage_amount * 0.5
        else:
            self.health -= damage_info.damage_amount
        
        if self.health <= 0:
            self.kill()
    
    def kill(self):
        """Destroy ship"""
        self.has_exploded = True
        self.health = 0
        # Emit explosion effect here if needed
    
    def render(self, screen, camera_offset=Point()):
        """Render ship"""
        if self.has_exploded:
            return
        
        # Calculate screen position
        screen_pos = (self.position - camera_offset).to_tuple()
        
        # Draw ship as triangle
        size = 15
        angle_rad = self.angle
        
        # Ship points (triangle pointing right)
        points = [
            Point(size, 0),
            Point(-size/2, size/2),
            Point(-size/2, -size/2)
        ]
        
        # Rotate and translate
        rotated = []
        for p in points:
            rx = p.x * math.cos(angle_rad) - p.y * math.sin(angle_rad)
            ry = p.x * math.sin(angle_rad) + p.y * math.cos(angle_rad)
            rotated.append((
                int(screen_pos[0] + rx),
                int(screen_pos[1] + ry)
            ))
        
        # Color based on team
        if self.team == 0:
            color = (100, 100, 255)  # Blue
        elif self.team == 1:
            color = (255, 100, 100)  # Red
        else:
            color = (100, 255, 100)  # Green
        
        # Draw shield if active
        if self.is_shield_active():
            pygame.draw.circle(screen, (150, 150, 255), screen_pos, 25, 2)
        
        # Draw ship
        pygame.draw.polygon(screen, color, rotated)
        pygame.draw.polygon(screen, (255, 255, 255), rotated, 2)
