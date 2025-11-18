# TNL Visualizer - Graphical Test Application

This is a Python implementation of the TNLTest graphical application, providing visual feedback for the network object replication system.

## Features

- **Real-time Visualization** - See players and buildings in a 400x400 window
- **Interactive Controls** - Click to move your player, right-click for menu
- **Multiple Modes** - Run as client, server, or both
- **Color-coded Objects** - Different colors for different player types

## Colors (matching original C++ implementation)

- **Background**: Yellow
- **Buildings**: Red rectangles (always visible to all clients)
- **Players**:
  - AI Players: Blue
  - Other Clients: Light Blue
  - Your Player: White
  - Black outline on all players
- **Scope Circle**: Gray semi-transparent circle showing visibility range

## Requirements

```bash
pip install pygame
```

Or install all requirements:
```bash
pip install -r ../requirements.txt
```

## Running the Visualizer

```bash
cd test
python3 visualizer.py
```

## Controls

### Mouse
- **Left Click**: Move your player to the clicked position
- **Right Click**: Open/close menu

### Menu Options
1. **Restart as client** - Connect to server on LAN broadcast
2. **Restart as server** - Start dedicated server
3. **Restart as client/server** - Run both in same process
4. **Restart as client pinging localhost** - Connect to local server

### Keyboard
- **ESC**: Quit application

## How It Works

The visualizer renders the game state at 60 FPS:

1. **Client Mode**: Shows objects ghosted from the server
   - Only sees buildings (always in scope)
   - Only sees nearby players (within scope radius)
   - Shows semi-transparent scope circle around your player

2. **Server Mode**: Shows all objects in the world
   - 50 random buildings
   - 15 AI-controlled players moving randomly
   - Your player (if you click to move)

3. **Client/Server Mode**: Runs both simultaneously
   - Server creates the world
   - Client connects via localhost
   - Best for testing locally

## Architecture

The visualizer uses pygame for rendering:
- World coordinates: 0.0 to 1.0 (normalized)
- Screen coordinates: 0 to 400 pixels
- Coordinate conversion handles mapping between spaces

Player sizes:
- Outline: 0.012 world units (4.8 pixels at 400x400)
- Inner: 0.01 world units (4 pixels)

Scope radius: 0.25 world units (100 pixels)

## Screenshot

![TNL Visualizer](https://github.com/user-attachments/assets/56837ade-b26e-43f7-adfd-604dcec4eaaf)

*Yellow background with red buildings and a blue AI player visible*

## Differences from C++ Version

- Uses pygame instead of OpenGL/GLUT
- Simplified menu system (right-click instead of dedicated menu button)
- Same colors, sizes, and behavior as original
- Python-based for easier modification and cross-platform compatibility

## Performance

- Runs at 60 FPS
- Network updates at ~30 Hz
- Handles 50+ buildings and 15+ players smoothly

## Troubleshooting

### "No module named 'pygame'"
Install pygame: `pip install pygame`

### "No available video device"
You're in a headless environment. The visualizer needs a display.
Use the console-based client/server instead:
```bash
python3 server.py  # In one terminal
python3 client.py  # In another terminal
```

### Players not moving
- In client mode: Make sure a server is running
- Check that connection is established (see console output)
- Try client/server mode for local testing
