# Quick Start Guide - Python TNL

## Installation

No installation needed! Uses only Python standard library.

**Requirements:** Python 3.7 or higher

## Running the Tests

### 1. Start the Server

```bash
cd test
python3 server.py
```

You should see:
```
[HH:MM:SS] TNLTest Dedicated Server - Python Version
[HH:MM:SS] Starting server on port 28999...
[HH:MM:SS] Server: Created 50 buildings and 15 AI players
[HH:MM:SS] Server ready. Waiting for clients...
```

### 2. Start a Client (in another terminal)

```bash
cd test
python3 client.py localhost
```

You should see:
```
[HH:MM:SS] TNLTest Client - Python Version
[HH:MM:SS] Connecting to localhost:28999...
[HH:MM:SS] Client: Ping response from IP:127.0.0.1:28999, connecting...
[HH:MM:SS] Connection established
[HH:MM:SS] Connected: X players, 50 buildings in game
```

### 3. Multiple Clients

You can start multiple clients. Each will connect and receive its own player.

```bash
# Terminal 3
cd test
python3 client.py localhost

# Terminal 4
cd test
python3 client.py localhost
```

## Custom Ports

### Server:
```bash
python3 server.py 30000
```

### Client:
```bash
python3 client.py localhost 30000
```

## What You'll See

- **Server**: Creates a world with 50 random buildings and 15 AI-controlled players
- **Client**: Connects, receives buildings (always visible) and nearby players (within radius)
- Objects update automatically as AI players move around

## Troubleshooting

### "Connection refused" or "No route to host"
- Make sure the server is running
- Check firewall settings
- Try using IP address instead of 'localhost'

### "Module not found"
- Make sure you're in the `test` directory
- Make sure `tnl` directory exists in parent directory
- Try: `cd /path/to/opentnl/test && python3 server.py`

### No output from client
- Wait a few seconds for connection
- Check that server and client ports match
- Look for error messages

## Next Steps

Read the full documentation:
- **PYTHON_README.md** - Detailed overview
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **test/test_game.py** - Example of how to use TNL classes

Enjoy your Python TNL implementation! 🎉
