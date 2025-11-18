#!/usr/bin/env python3
"""
TNLTest Visualizer - Python Version

This is a Python port of the TNL test visualizer using pygame.
It renders the game world with players and buildings.
"""

import sys
import time
import pygame
from test_game import TestGame, Position, Player
from tnl.address import Address
from tnl.log import logprintf

# Window dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

# Colors matching the original C++ implementation
COLOR_BACKGROUND = (255, 255, 0)  # Yellow (R=1.0, G=1.0, B=0.0)
COLOR_BUILDING = (255, 0, 0)  # Red
COLOR_PLAYER_OUTLINE = (0, 0, 0)  # Black
COLOR_AI_PLAYER = (0, 0, 255)  # Blue
COLOR_CLIENT_PLAYER = (127, 127, 255)  # Light blue (0.5, 0.5, 1.0)
COLOR_MY_PLAYER = (255, 255, 255)  # White
COLOR_SCOPE_CIRCLE = (127, 127, 127, 165)  # Gray with alpha (0.5, 0.5, 0.5, 0.65)


class TNLVisualizer:
    """Main visualizer class for TNL test application"""
    
    def __init__(self):
        """Initialize pygame and create window"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("TNLTest - Right Click for Menu")
        self.clock = pygame.time.Clock()
        
        # Game instances
        self.client_game = None
        self.server_game = None
        
        # Menu state
        self.show_menu = False
        self.menu_items = [
            "Restart as client",
            "Restart as server", 
            "Restart as client/server",
            "Restart as client pinging localhost"
        ]
        
        # Create initial client
        self.create_game_client(False)
    
    def create_game_client(self, ping_localhost=False):
        """Create a client game"""
        if self.client_game:
            del self.client_game
        if self.server_game:
            del self.server_game
        
        address = "localhost" if ping_localhost else "broadcast"
        bind_addr = Address(Address.IPProtocol, "0.0.0.0", 0)
        ping_addr = Address(Address.IPProtocol, address, 28999)
        
        self.client_game = TestGame(False, bind_addr, ping_addr)
        self.server_game = None
        
        logprintf("Started as client (pinging %s)", address)
    
    def create_game_server(self):
        """Create a server game"""
        if self.client_game:
            del self.client_game
        if self.server_game:
            del self.server_game
        
        bind_addr = Address(Address.IPProtocol, "0.0.0.0", 28999)
        
        self.client_game = None
        self.server_game = TestGame(True, bind_addr, None)
        
        logprintf("Started as server")
    
    def create_game_client_server(self):
        """Create both client and server in same process"""
        if self.client_game:
            del self.client_game
        if self.server_game:
            del self.server_game
        
        # Create server
        server_bind = Address(Address.IPProtocol, "0.0.0.0", 28999)
        self.server_game = TestGame(True, server_bind, None)
        
        # Create client
        client_bind = Address(Address.IPProtocol, "0.0.0.0", 0)
        ping_addr = Address(Address.IPProtocol, "localhost", 28999)
        self.client_game = TestGame(False, client_bind, ping_addr)
        
        logprintf("Started as client/server")
    
    def world_to_screen(self, x, y):
        """Convert world coordinates (0-1) to screen coordinates"""
        return (int(x * WINDOW_WIDTH), int(y * WINDOW_HEIGHT))
    
    def screen_to_world(self, x, y):
        """Convert screen coordinates to world coordinates (0-1)"""
        return (x / WINDOW_WIDTH, y / WINDOW_HEIGHT)
    
    def render_frame(self):
        """Render the current game state"""
        # Get the active game
        game = self.client_game if self.client_game else self.server_game
        if not game:
            return
        
        # Clear screen with yellow background
        self.screen.fill(COLOR_BACKGROUND)
        
        # Draw scope circle if we have a client player
        if game.client_player and game.client_player.get():
            player = game.client_player.get()
            center = self.world_to_screen(player.render_pos.x, player.render_pos.y)
            radius = int(0.25 * WINDOW_WIDTH)
            
            # Create a surface for alpha blending
            scope_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(scope_surface, COLOR_SCOPE_CIRCLE, center, radius)
            self.screen.blit(scope_surface, (0, 0))
        
        # Draw buildings
        for building in game.buildings:
            upper_left = self.world_to_screen(building.upper_left.x, building.upper_left.y)
            lower_right = self.world_to_screen(building.lower_right.x, building.lower_right.y)
            
            width = lower_right[0] - upper_left[0]
            height = lower_right[1] - upper_left[1]
            
            rect = pygame.Rect(upper_left[0], upper_left[1], width, height)
            pygame.draw.rect(self.screen, COLOR_BUILDING, rect)
        
        # Draw players
        for player in game.players:
            center = self.world_to_screen(player.render_pos.x, player.render_pos.y)
            
            # Draw black outline (slightly larger square)
            outline_size = int(0.012 * WINDOW_WIDTH)
            outline_rect = pygame.Rect(
                center[0] - outline_size,
                center[1] - outline_size,
                outline_size * 2,
                outline_size * 2
            )
            pygame.draw.rect(self.screen, COLOR_PLAYER_OUTLINE, outline_rect)
            
            # Draw colored inner square based on player type
            if player.my_player_type == Player.PlayerTypeAI or \
               player.my_player_type == Player.PlayerTypeAIDummy:
                color = COLOR_AI_PLAYER
            elif player.my_player_type == Player.PlayerTypeClient:
                color = COLOR_CLIENT_PLAYER
            else:  # PlayerTypeMyClient
                color = COLOR_MY_PLAYER
            
            inner_size = int(0.01 * WINDOW_WIDTH)
            inner_rect = pygame.Rect(
                center[0] - inner_size,
                center[1] - inner_size,
                inner_size * 2,
                inner_size * 2
            )
            pygame.draw.rect(self.screen, color, inner_rect)
        
        # Draw menu if showing
        if self.show_menu:
            self.draw_menu()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw the right-click menu"""
        menu_x = 50
        menu_y = 50
        menu_width = 300
        menu_height = len(self.menu_items) * 30 + 20
        
        # Draw menu background
        menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        menu_surface.fill((200, 200, 200, 230))
        pygame.draw.rect(menu_surface, (0, 0, 0), 
                        pygame.Rect(0, 0, menu_width, menu_height), 2)
        self.screen.blit(menu_surface, (menu_x, menu_y))
        
        # Draw menu items
        font = pygame.font.Font(None, 24)
        for i, item in enumerate(self.menu_items):
            text = font.render(item, True, (0, 0, 0))
            self.screen.blit(text, (menu_x + 10, menu_y + 10 + i * 30))
    
    def handle_mouse_click(self, pos, button):
        """Handle mouse clicks"""
        if button == 1:  # Left click
            # Move player to clicked position
            world_pos = self.screen_to_world(pos[0], pos[1])
            p = Position(world_pos[0], world_pos[1])
            
            if self.client_game:
                self.client_game.move_my_player_to(p)
            elif self.server_game:
                self.server_game.move_my_player_to(p)
        
        elif button == 3:  # Right click
            if self.show_menu:
                # Check if clicked on menu item
                menu_x = 50
                menu_y = 50
                if menu_x <= pos[0] <= menu_x + 300:
                    item_index = (pos[1] - menu_y - 10) // 30
                    if 0 <= item_index < len(self.menu_items):
                        self.execute_menu_action(item_index)
                self.show_menu = False
            else:
                self.show_menu = True
    
    def execute_menu_action(self, index):
        """Execute menu action"""
        if index == 0:  # Restart as client
            self.create_game_client(False)
        elif index == 1:  # Restart as server
            self.create_game_server()
        elif index == 2:  # Restart as client/server
            self.create_game_client_server()
        elif index == 3:  # Restart as client pinging localhost
            self.create_game_client(True)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos, event.button)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update game state
            if self.client_game:
                self.client_game.tick()
            if self.server_game:
                self.server_game.tick()
            
            # Render
            self.render_frame()
            
            # Cap at 60 FPS
            self.clock.tick(60)
        
        pygame.quit()


def main():
    """Main entry point"""
    try:
        visualizer = TNLVisualizer()
        visualizer.run()
    except Exception as e:
        logprintf("Error: %s", str(e))
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
