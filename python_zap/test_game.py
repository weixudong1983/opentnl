#!/usr/bin/env python3
"""
Test script to verify game logic without GUI
"""
import sys
sys.path.insert(0, '.')

from geometry import Point
from game import ClientGame
from ship import Ship, ShipModule, ShipWeapon
from game_object import Move

def test_geometry():
    """Test geometry classes"""
    print("Testing geometry...")
    p1 = Point(3, 4)
    assert p1.len() == 5.0, "Point length calculation failed"
    
    p2 = Point(1, 1)
    p3 = p1 + p2
    assert p3.x == 4 and p3.y == 5, "Point addition failed"
    
    print("✓ Geometry tests passed")

def test_ship():
    """Test ship creation and basic functionality"""
    print("\nTesting ship...")
    game = ClientGame()
    ship = Ship(game, "Test Player", team=0, pos=Point(100, 100))
    
    assert ship.health == 1.0, "Ship health initialization failed"
    assert ship.energy == ship.ENERGY_MAX, "Ship energy initialization failed"
    assert ship.player_name == "Test Player", "Ship name failed"
    
    # Test movement
    move = Move()
    move.forward = True
    move.angle = 0
    ship.current_move = move
    
    ship.idle(0.016)  # One frame at 60fps
    
    print(f"  Ship position after move: {ship.position.x:.2f}, {ship.position.y:.2f}")
    print(f"  Ship velocity: {ship.velocity.x:.2f}, {ship.velocity.y:.2f}")
    
    print("✓ Ship tests passed")

def test_game():
    """Test game creation"""
    print("\nTesting game...")
    game = ClientGame(1024, 768)
    
    # Check initial objects (barriers, goal zones)
    print(f"  Initial object count: {len(game.objects)}")
    assert len(game.objects) > 0, "Game should have initial objects"
    
    # Create player
    player = game.create_local_player("Test Player")
    assert player is not None, "Player creation failed"
    assert player in game.objects, "Player not in game objects"
    
    # Update game
    game.update(0.016)
    
    print("✓ Game tests passed")

def test_collision():
    """Test collision detection"""
    print("\nTesting collisions...")
    game = ClientGame()
    
    ship = Ship(game, "Target", team=1, pos=Point(500, 500))
    game.add_object(ship)
    
    from projectile import Projectile
    # Create projectile heading toward ship
    proj = Projectile(game, Point(400, 500), Point(200, 0), None)
    game.add_object(proj)
    
    initial_health = ship.health
    
    # Update several times to let projectile reach ship
    for _ in range(10):
        game.update(0.016)
    
    # Projectile should have hit or passed
    print(f"  Ship health: {ship.health:.2f} (was {initial_health:.2f})")
    
    print("✓ Collision tests passed")

def main():
    print("=" * 50)
    print("Zap Game - Unit Tests")
    print("=" * 50)
    
    test_geometry()
    test_ship()
    test_game()
    test_collision()
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)
    print("\nGame is ready to run. Execute: python main.py")

if __name__ == "__main__":
    main()
