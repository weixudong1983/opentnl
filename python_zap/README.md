# Zap Game - Python Version

This is a simplified Python reimplementation of the Zap multiplayer vector graphics space game from OpenTNL.

## Requirements

- Python 3.8 or higher
- pygame
- cryptography (for simplified asymmetric key replacement)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Controls

- **Arrow Keys**: Move ship
- **Space**: Fire weapon
- **S**: Activate shield
- **B**: Activate boost
- **ESC**: Quit

## Features

This simplified version includes:
- Ship movement and physics
- Basic weapons and projectiles
- Barriers and obstacles
- Simple networking support
- Basic game types (CTF, etc.)

## Differences from C++ Version

- Simplified networking using Python sockets instead of TNL
- Pygame graphics instead of OpenGL/GLUT
- Simplified crypto using Python's cryptography library instead of libtomcrypt
- Streamlined game logic focusing on core gameplay
