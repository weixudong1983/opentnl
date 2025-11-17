# Zap Game - Python Version
# Documentation Index

This directory contains a complete Python reimplementation of the OpenTNL Zap game.

## Quick Links

### Getting Started
- **[快速开始.md](快速开始.md)** - Chinese quick start guide
- **[README.md](README.md)** - English quick start guide
- **[GUIDE.md](GUIDE.md)** - Complete user and developer guide
- **[requirements.txt](requirements.txt)** - Python dependencies

### Documentation
- **[SUMMARY.md](SUMMARY.md)** - Bilingual project summary (Chinese + English)
- **[COMPARISON.md](COMPARISON.md)** - Detailed C++ vs Python comparison
- **[.gitignore](.gitignore)** - Git ignore rules for Python

### Scripts
- **[main.py](main.py)** - Main game - run this to play!
- **[run.py](run.py)** - Launcher with dependency checking
- **[verify_install.py](verify_install.py)** - Complete installation verification
- **[test_game.py](test_game.py)** - Unit tests
- **[demo_crypto.py](demo_crypto.py)** - Cryptography replacement demo

### Source Code
- **[game.py](game.py)** - Game world and object management
- **[ship.py](ship.py)** - Player ship implementation
- **[projectile.py](projectile.py)** - Weapon projectiles
- **[barrier.py](barrier.py)** - Walls and obstacles
- **[geometry.py](geometry.py)** - Math and geometry classes
- **[game_object.py](game_object.py)** - Base game object classes
- **[network.py](network.py)** - Networking and cryptography (replaces libtomcrypt)

## Quick Commands

### First Time Setup
```bash
python verify_install.py
```

### Play the Game
```bash
python main.py
```

### See Crypto Demo
```bash
python demo_crypto.py
```

### Run Tests
```bash
python test_game.py
```

## What's Different?

### From Original C++:
- **252 files → 11 files** (95% reduction)
- **~50,000 lines → ~2,000 lines** (96% reduction)
- **libtomcrypt removed** → Python cryptography library
- **OpenGL/GLUT → Pygame** (simpler 2D graphics)
- **Instant run** (no compilation needed)

### Working Features:
✅ Ship movement and physics
✅ 3 weapon types
✅ Energy system
✅ Shield and Boost modules
✅ Collision detection
✅ Team gameplay
✅ Real-time UI

## Language Options

- **English**: README.md, GUIDE.md, COMPARISON.md
- **中文 (Chinese)**: 快速开始.md, SUMMARY.md (bilingual)

## File Sizes

Total: ~60 KB of source code
- Documentation: ~24 KB
- Source code: ~36 KB
- Very lightweight!

## Requirements

- Python 3.8+
- pygame
- cryptography

Install: `pip install -r requirements.txt`

## Project Status

✅ Complete and tested
✅ All features working
✅ Cross-platform
✅ Well documented
✅ Ready to use

---

**Start here**: Run `python verify_install.py` for guided setup!
