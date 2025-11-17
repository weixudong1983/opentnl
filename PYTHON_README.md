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

## Limitations

This is a simplified implementation focusing on core functionality:

- No RPC (Remote Procedure Call) events
- No encryption
- No connection security (certificates, puzzles, etc.)
- Simplified packet structure
- No adaptive communication
- No packet loss handling

These features could be added incrementally as needed.
