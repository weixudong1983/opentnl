# Zap Game - Python Implementation Guide

## Overview

This is a simplified Python reimplementation of the Zap multiplayer vector graphics space game from OpenTNL (Torque Network Library). The original C++ project contained 252 source files across multiple components. This Python version focuses on core gameplay and can be run standalone.

## Architecture

### File Structure

```
python_zap/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── main.py                   # Main entry point and game loop
├── game.py                   # Game class and game world management
├── geometry.py               # Point, Color, Rect classes
├── game_object.py           # Base GameObject and MoveObject classes
├── ship.py                   # Player ship implementation
├── projectile.py            # Projectile/weapons implementation
├── barrier.py               # Walls, obstacles, goal zones
├── network.py               # Simplified networking (replaces TNL)
└── test_game.py             # Unit tests
```

### Key Design Decisions

1. **Graphics**: Pygame instead of OpenGL/GLUT
   - Simpler 2D vector graphics
   - Cross-platform compatibility
   - Easy to extend

2. **Networking**: Python sockets instead of TNL
   - Simplified client-server architecture
   - Pickle-based serialization
   - Socket.IO could be added for web support

3. **Cryptography**: Python's `cryptography` library instead of libtomcrypt
   - RSA for asymmetric key operations
   - Much simpler API
   - Well-maintained standard library

4. **Physics**: Simplified but functional
   - Basic 2D vector physics
   - Collision detection
   - No complex swept ellipsoid (simplified to circle/rect)

## Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies

```bash
cd python_zap
pip install -r requirements.txt
```

This installs:
- `pygame` - for graphics and input
- `cryptography` - for simplified asymmetric key encryption

## Running the Game

### Single Player (Local)

```bash
cd python_zap
python main.py
```

### Running Tests

```bash
cd python_zap
python test_game.py
```

## Controls

| Key | Action |
|-----|--------|
| W / Up Arrow | Move Forward |
| S / Down Arrow | Move Backward |
| A / Left Arrow | Move Left |
| D / Right Arrow | Move Right |
| Mouse | Aim direction |
| Space / Left Click | Fire weapon |
| 1, 2, 3 | Select weapon |
| Tab | Cycle weapons |
| Shift | Activate Boost (Module 1) |
| Ctrl | Activate Shield (Module 2) |
| ESC | Quit |

## Gameplay

### Ship Systems

- **Health**: Displayed in bottom-left corner. When it reaches 0, ship is destroyed.
- **Energy**: Powers modules and weapons. Recharges automatically.
- **Weapons**:
  - Phaser: Standard rapid-fire projectile
  - Bouncer: Bounces off walls
  - Triple: Fires three projectiles in a spread
- **Modules**:
  - Boost: Increases speed (drains energy)
  - Shield: Absorbs damage (drains energy)

### Objective

Navigate the arena, avoid barriers, and practice combat mechanics. The game includes:
- Destructible barriers forming an arena
- Goal zones (blue and red teams)
- Multiple weapon types
- Energy management system

## Differences from Original C++

### Simplified Components

1. **No libtomcrypt**: Replaced with Python's `cryptography` library
   - Original used ECC (Elliptic Curve Cryptography)
   - Python version uses RSA for simplicity
   - Can be swapped for other algorithms easily

2. **Simplified Networking**: 
   - Original: Complex TNL ghost object system with delta compression
   - Python: Basic socket communication with pickle serialization
   - Suitable for LAN games, could be enhanced for internet play

3. **2D Graphics Only**:
   - Original: OpenGL with 3D perspective on 2D gameplay
   - Python: Pure 2D pygame rendering
   - Faster, simpler, more maintainable

4. **Removed Components**:
   - Voice chat codec (GSM, LPC10)
   - OpenAL audio (could add pygame.mixer)
   - Master server (could add separately)
   - Complex ghost object replication
   - Journaling/replay system

### Retained Core Features

✓ Ship physics and movement
✓ Weapons and projectiles
✓ Barriers and collision detection
✓ Energy system
✓ Module system (boost, shield, etc.)
✓ Multiple weapon types
✓ Team-based gameplay structure
✓ Game object hierarchy
✓ Basic networking structure

## Extending the Game

### Adding New Weapons

1. Add weapon type to `ship.py`:
```python
class ShipWeapon:
    NEW_WEAPON = 7
```

2. Implement firing logic in Ship class:
```python
def fire_new_weapon(self):
    # Create projectile or effect
    pass
```

3. Add to weapon fire processing:
```python
elif weapon == ShipWeapon.NEW_WEAPON:
    self.fire_new_weapon()
```

### Adding New Game Objects

1. Create new class inheriting from `GameObject` or `MoveObject`
2. Implement required methods: `idle()`, `render()`, `update_extent()`
3. Add to game in `game.py`

### Adding Multiplayer

The `network.py` module provides basic client-server infrastructure:

1. Server:
```python
from network import NetworkServer
server = NetworkServer(port=28000)
server.start()
```

2. Client:
```python
from network import NetworkConnection
conn = NetworkConnection('localhost', 28000)
conn.connect()
```

3. Game state synchronization would need to be implemented

## Performance

- Targets 60 FPS
- Handles 100+ game objects comfortably
- Lightweight compared to original C++ version
- Can run on modest hardware (no 3D graphics required)

## Future Enhancements

Potential additions to make it more feature-complete:

1. **Sound Effects**: Use pygame.mixer for weapons, explosions
2. **Music**: Background music system
3. **AI Bots**: Computer-controlled ships
4. **Game Types**: CTF, King of the Hill, Soccer
5. **Level Editor**: Create custom maps
6. **Multiplayer**: Full client-server implementation
7. **Particle Effects**: Explosions, trails, sparks
8. **Power-ups**: Health, energy, weapon pickups
9. **HUD**: Radar, minimap, scores
10. **Menu System**: Start screen, options

## Troubleshooting

### "No module named 'pygame'"
Run: `pip install pygame`

### "No module named 'cryptography'"
Run: `pip install cryptography`

### Game runs slowly
- Reduce number of particles/effects
- Lower FPS target in main.py
- Disable vsync

### Display issues
Make sure pygame is properly installed and your system supports SDL2.

## License

This is a reimplementation based on OpenTNL's Zap game.
Original Copyright (C) 2004 GarageGames.com, Inc.

The original was licensed under GPL v2. This Python version maintains GPL v2 compatibility.

## Credits

- Original OpenTNL and Zap: GarageGames
- Python reimplementation: Created as a simplified learning/demonstration version
- Pygame: pygame.org community
- Python Cryptography: PyCA community
