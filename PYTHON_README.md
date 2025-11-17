# TNL Python Implementation

This is a Python implementation of the Torque Network Library (TNL) and its test application.

## Overview

The TNL library has been rewritten in Python, focusing on the core networking features needed for the test application. The implementation includes:

- **tnl_py/** - Python TNL library
  - BitStream for bit-level serialization
  - NetObject for network-replicated objects
  - GhostConnection for object replication
  - NetInterface for UDP networking
  - Supporting utilities (Random, Log, Address, etc.)

- **test_py/** - Test application
  - TestGame: Main game class
  - Player: Networked player objects
  - Building: Static building objects
  - server.py: Dedicated server
  - client.py: Client application

## Changes from C++ Version

1. **No libtomcrypt dependency**: Asymmetric encryption has been removed for simplicity. The basic networking functionality works without it.

2. **Simplified architecture**: 
   - Removed complex features not needed for basic testing
   - Focused on core object replication and networking
   - Uses Python's built-in libraries only

3. **Python idioms**: 
   - Classes instead of structs
   - Properties instead of getter/setters where appropriate
   - Standard Python networking (socket module)

## Running the Tests

### Start the Server

```bash
cd test_py
python3 server.py [port]
```

Default port is 28999 if not specified.

### Start a Client

```bash
cd test_py
python3 client.py [server_host] [server_port]
```

Default is localhost:28999 if not specified.

### Example

Terminal 1 (Server):
```bash
cd test_py
python3 server.py
```

Terminal 2 (Client):
```bash
cd test_py
python3 client.py localhost
```

You should see output like:
```
[HH:MM:SS] TNLTest Client - Python Version
[HH:MM:SS] Connecting to localhost:28999...
[HH:MM:SS] Client: Ping response from IP:127.0.0.1:28999, connecting...
[HH:MM:SS] Connection established
[HH:MM:SS] Connected: X players, 50 buildings in game
```

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

## Architecture

The Python implementation follows the same basic architecture as the C++ version:

1. **Server** creates a world with Buildings and AI Players
2. **Client** connects to server and receives ghost (replicated) objects
3. **GhostConnection** handles automatic object synchronization
4. Objects use **pack_update/unpack_update** for state serialization
5. **Scope queries** determine which objects are visible to each client

## Key Classes

- `NetObject`: Base class for all networked objects
- `GhostConnection`: Connection that supports object ghosting
- `NetInterface`: UDP socket manager
- `BitStream`: Bit-level data serialization
- `Player`: Example networked object (moves around the world)
- `Building`: Example scope-always object (visible to all clients)

## How It Works

1. **Server Side**:
   - Creates 50 random buildings (ScopeAlways objects)
   - Creates 15 AI-controlled players
   - When a client connects, creates a Player for that client
   - Performs scope queries to determine which objects to replicate
   - Sends ghost updates ~30 times per second

2. **Client Side**:
   - Pings the server to discover it
   - Connects to the server
   - Receives ghost objects and their state updates
   - Displays periodic status showing number of players and buildings

3. **Object Replication (Ghosting)**:
   - Server calls `object_in_scope()` for objects visible to each client
   - Objects are assigned ghost IDs
   - Initial ghost creation sends class name and full state
   - Subsequent updates only send changed states
   - BitStream compresses data (e.g., positions use 12 bits instead of 32)

## Testing

Run the test programs as described above. The client should successfully connect and receive:
- 50 buildings (always in scope)
- 1-3 players (the client's player plus any AI players in scope)

## Limitations

This is a simplified implementation focusing on core functionality:

- No RPC (Remote Procedure Call) events (stub implementation only)
- No encryption or connection security
- Simplified packet structure
- No adaptive communication
- No packet loss handling or reliability guarantees
- Limited error handling

These features could be added incrementally as needed.

## Future Enhancements

Potential additions:
- Complete RPC implementation
- Basic encryption using Python's cryptography library
- Connection security (simple token-based authentication)
- Packet loss detection and retransmission
- Compression for larger object counts
- GUI client using pygame or tkinter
- Performance optimizations
