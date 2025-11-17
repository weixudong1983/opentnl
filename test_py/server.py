#!/usr/bin/env python3
"""
TNLTest Dedicated Server - Python Version

This is a Python port of the TNL test dedicated server.
It creates a game world with buildings and AI players,
and allows clients to connect.
"""

import sys
import time
from test_game import TestGame, Position
from tnl_py.address import Address
from tnl_py.log import logprintf

def main():
    """Main server function"""
    # Parse command line arguments
    port = 28999
    if len(sys.argv) >= 2:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [port]")
            return 1
    
    logprintf("=" * 60)
    logprintf("TNLTest Dedicated Server - Python Version")
    logprintf("=" * 60)
    logprintf("Starting server on port %d...", port)
    
    # Create bind address (listen on all interfaces)
    bind_address = Address(Address.IPProtocol, "0.0.0.0", port)
    
    # Note: We pass 'True' as first parameter to indicate this is a server
    # The second parameter should be False (not is_server)
    game = TestGame(True, bind_address, None)
    
    logprintf("Server ready. Waiting for clients...")
    logprintf("Press Ctrl+C to stop")
    
    try:
        # Main server loop
        while True:
            game.tick()
            time.sleep(0.01)  # ~100Hz update rate
    
    except KeyboardInterrupt:
        logprintf("\nServer shutting down...")
        return 0

if __name__ == "__main__":
    sys.exit(main())
