"""
Main entry point for Zap game
"""
import pygame
import sys
import math
from game import ClientGame
from game_object import Move
from geometry import Point


class ZapGame:
    """Main game application"""
    
    def __init__(self):
        pygame.init()
        
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Zap - Python Version")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create game
        self.game = ClientGame(self.width, self.height)
        self.player = self.game.create_local_player("Player 1")
        
        # Current move state
        self.current_move = Move()
        
        # Font for UI
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
    
    def handle_input(self):
        """Handle keyboard and mouse input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_1:
                    self.player.select_weapon(0)
                elif event.key == pygame.K_2:
                    self.player.select_weapon(1)
                elif event.key == pygame.K_3:
                    self.player.select_weapon(2)
                elif event.key == pygame.K_TAB:
                    self.player.select_weapon()
        
        # Get current key states
        keys = pygame.key.get_pressed()
        
        # Movement
        self.current_move.forward = keys[pygame.K_w] or keys[pygame.K_UP]
        self.current_move.backward = keys[pygame.K_s] or keys[pygame.K_DOWN]
        self.current_move.left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        self.current_move.right = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        
        # Weapons
        self.current_move.fire = keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]
        
        # Modules
        self.current_move.activate_module_1 = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]  # Boost
        self.current_move.activate_module_2 = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]  # Shield
        
        # Mouse aiming
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.player and not self.player.has_exploded:
            # Calculate angle from player to mouse
            player_screen_x = self.player.position.x - self.game.camera_offset.x
            player_screen_y = self.player.position.y - self.game.camera_offset.y
            
            dx = mouse_x - player_screen_x
            dy = mouse_y - player_screen_y
            self.current_move.angle = math.atan2(dy, dx)
        
        # Update player's current move
        if self.player:
            self.player.current_move = self.current_move
            
            # Update module states based on input
            from ship import ShipModule
            if len(self.player.modules) > 0:
                module = self.player.modules[0]
                self.player.module_active[module] = self.current_move.activate_module_1
            if len(self.player.modules) > 1:
                module = self.player.modules[1]
                self.player.module_active[module] = self.current_move.activate_module_2
    
    def update(self, time_delta):
        """Update game state"""
        if self.player and not self.player.has_exploded:
            self.game.update(time_delta)
            self.game.update_camera()
    
    def render(self):
        """Render game"""
        self.game.render(self.screen)
        
        # Render UI
        self.render_ui()
        
        pygame.display.flip()
    
    def render_ui(self):
        """Render user interface"""
        if not self.player:
            return
        
        # Health bar
        health_width = 200
        health_height = 20
        health_x = 10
        health_y = self.height - 30
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), 
                        (health_x, health_y, health_width, health_height))
        
        # Health fill
        if self.player.health > 0:
            fill_width = int(health_width * self.player.health)
            color = (0, 255, 0) if self.player.health > 0.5 else (255, 255, 0) if self.player.health > 0.25 else (255, 0, 0)
            pygame.draw.rect(self.screen, color,
                           (health_x, health_y, fill_width, health_height))
        
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (health_x, health_y, health_width, health_height), 2)
        
        # Health text
        health_text = self.font.render(f"Health: {int(self.player.health * 100)}%", True, (255, 255, 255))
        self.screen.blit(health_text, (health_x + health_width + 10, health_y))
        
        # Energy bar
        energy_x = 10
        energy_y = self.height - 60
        energy_max_width = 200
        
        pygame.draw.rect(self.screen, (50, 50, 50),
                        (energy_x, energy_y, energy_max_width, health_height))
        
        if self.player.energy > 0:
            energy_fill = int(energy_max_width * (self.player.energy / self.player.ENERGY_MAX))
            color = (100, 100, 255)
            pygame.draw.rect(self.screen, color,
                           (energy_x, energy_y, energy_fill, health_height))
        
        pygame.draw.rect(self.screen, (255, 255, 255),
                        (energy_x, energy_y, energy_max_width, health_height), 2)
        
        energy_text = self.font.render(f"Energy: {int(self.player.energy / 1000)}k", True, (255, 255, 255))
        self.screen.blit(energy_text, (energy_x + energy_max_width + 10, energy_y))
        
        # Active weapon
        from ship import ShipWeapon
        weapon_names = {
            ShipWeapon.NONE: "None",
            ShipWeapon.PHASER: "Phaser",
            ShipWeapon.BOUNCER: "Bouncer",
            ShipWeapon.TRIPLE: "Triple"
        }
        
        active_weapon = self.player.weapons[self.player.active_weapon] if self.player.active_weapon < len(self.player.weapons) else ShipWeapon.NONE
        weapon_name = weapon_names.get(active_weapon, "Unknown")
        weapon_text = self.font.render(f"Weapon: {weapon_name} ({self.player.active_weapon + 1})", True, (255, 255, 255))
        self.screen.blit(weapon_text, (10, 10))
        
        # Controls help
        help_y = 40
        help_texts = [
            "Controls:",
            "WASD/Arrows: Move",
            "Mouse: Aim",
            "Space/Click: Fire",
            "1/2/3 or Tab: Switch Weapon",
            "Shift: Boost",
            "Ctrl: Shield",
            "ESC: Quit"
        ]
        
        for i, text in enumerate(help_texts):
            help_surface = self.font.render(text, True, (200, 200, 200))
            self.screen.blit(help_surface, (10, help_y + i * 25))
        
        # Game over
        if self.player.has_exploded:
            game_over_text = self.large_font.render("SHIP DESTROYED", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(game_over_text, text_rect)
    
    def run(self):
        """Main game loop"""
        last_time = pygame.time.get_ticks()
        
        while self.running:
            current_time = pygame.time.get_ticks()
            time_delta = (current_time - last_time) / 1000.0  # Convert to seconds
            last_time = current_time
            
            # Cap time delta to prevent huge jumps
            time_delta = min(time_delta, 0.1)
            
            self.handle_input()
            self.update(time_delta)
            self.render()
            
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = ZapGame()
    game.run()


if __name__ == "__main__":
    main()
