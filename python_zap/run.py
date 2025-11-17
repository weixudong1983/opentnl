#!/usr/bin/env python3
"""
Zap Game Launcher
Checks dependencies and runs the game
"""
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    
    missing = []
    
    try:
        import pygame
        print("✓ pygame installed")
    except ImportError:
        missing.append("pygame")
        print("✗ pygame not found")
    
    try:
        import cryptography
        print("✓ cryptography installed")
    except ImportError:
        missing.append("cryptography")
        print("✗ cryptography not found")
    
    if missing:
        print("\nMissing dependencies:", ", ".join(missing))
        print("\nInstalling dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        print("\nDependencies installed!")
    else:
        print("\nAll dependencies satisfied!")
    
    return True

def main():
    print("=" * 60)
    print("  Zap Game - Python Version")
    print("  Simplified OpenTNL Reimplementation")
    print("=" * 60)
    print()
    
    try:
        if check_dependencies():
            print("\nStarting game...")
            print()
            import main as game_main
            game_main.main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
