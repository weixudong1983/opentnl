#!/usr/bin/env python3
"""
TNLTest Client - Python Version

This is a Python port of the TNL test client.
It connects to a server and displays player/building information.
"""

import sys
import time
from test_game import TestGame, Position
from tnl.address import Address
from tnl.log import logprintf

def main():
    """Main client function"""
    # Parse command line arguments
    server_host = "localhost"
    server_port = 28999
    
    if len(sys.argv) >= 2:
        server_host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            server_port = int(sys.argv[2])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [server_host] [server_port]")
            return 1
    
    logprintf("=" * 60)
    logprintf("TNLTest Client - Python Version")
    logprintf("=" * 60)
    logprintf("Connecting to %s:%d...", server_host, server_port)
    
    # Create bind address (use any available port)
    bind_address = Address(Address.IPProtocol, "0.0.0.0", 0)
    
    # Create ping/server address
    ping_address = Address(Address.IPProtocol, server_host, server_port)
    
    # Create game (client mode)
    game = TestGame(False, bind_address, ping_address)
    
    logprintf("Client started. Looking for server...")
    logprintf("Press Ctrl+C to quit")
    
    last_status_time = 0
    
    try:
        # Main client loop
        while True:
            game.tick()
            
            # Print periodic status
            current_time = time.time()
            if current_time - last_status_time > 5.0:
                last_status_time = current_time
                
                if game.my_net_interface.connection_to_server:
                    conn = game.my_net_interface.connection_to_server
                    if conn.is_connected():
                        logprintf("Connected: %d players, %d buildings in game",
                                 len(game.players), len(game.buildings))
                    else:
                        logprintf("Connecting...")
                else:
                    logprintf("Searching for server...")
            
            time.sleep(0.01)  # ~100Hz update rate
    
    except KeyboardInterrupt:
        logprintf("\nClient shutting down...")
        return 0

if __name__ == "__main__":
    sys.exit(main())
