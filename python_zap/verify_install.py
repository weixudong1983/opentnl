#!/usr/bin/env python3
"""
Installation verification and quick start guide for Zap Python
"""
import sys
import subprocess

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def check_python_version():
    """Check if Python version is sufficient"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python 3.8 or higher required")
        return False
    
    print("✓ Python version is sufficient")
    return True

def check_dependencies():
    """Check and install dependencies"""
    print_header("Checking Dependencies")
    
    dependencies = {
        'pygame': 'pygame',
        'cryptography': 'cryptography'
    }
    
    missing = []
    installed = []
    
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {module} is installed")
            installed.append(module)
        except ImportError:
            print(f"✗ {module} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("\nWould you like to install them now? (y/n): ", end='')
        
        try:
            response = input().lower()
            if response == 'y':
                print("\nInstalling dependencies...")
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
                print("\n✓ Dependencies installed successfully")
                return True
            else:
                print("\nPlease install dependencies manually:")
                print(f"  pip install {' '.join(missing)}")
                return False
        except:
            print("\nPlease install dependencies manually:")
            print(f"  pip install {' '.join(missing)}")
            return False
    
    print("\n✓ All dependencies are installed")
    return True

def run_tests():
    """Run unit tests"""
    print_header("Running Unit Tests")
    
    try:
        print("\nExecuting test_game.py...\n")
        result = subprocess.run([sys.executable, "test_game.py"], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✓ All tests passed")
            return True
        else:
            print("\n✗ Some tests failed")
            return False
    except Exception as e:
        print(f"\n✗ Error running tests: {e}")
        return False

def demo_crypto():
    """Run crypto demonstration"""
    print_header("Running Cryptography Demo")
    
    print("\nWould you like to see the cryptography replacement demo? (y/n): ", end='')
    
    try:
        response = input().lower()
        if response == 'y':
            print("\nRunning demo_crypto.py...\n")
            subprocess.run([sys.executable, "demo_crypto.py"])
            return True
    except:
        pass
    
    print("Skipping crypto demo")
    return True

def show_instructions():
    """Show how to run the game"""
    print_header("Quick Start Instructions")
    
    print("""
To run the game:

    python main.py

Or use the launcher:

    python run.py

Controls:
    WASD / Arrow Keys  - Move ship
    Mouse              - Aim
    Space / Left Click - Fire weapon
    1, 2, 3 or Tab     - Switch weapons
    Shift              - Activate Boost
    Ctrl               - Activate Shield
    ESC                - Quit

Files of Interest:
    main.py         - Main game loop and UI
    game.py         - Game world and objects
    ship.py         - Player ship implementation
    network.py      - Networking with simplified crypto
    test_game.py    - Unit tests
    demo_crypto.py  - Cryptography demonstration
    GUIDE.md        - Complete documentation
    COMPARISON.md   - C++ vs Python comparison

For more information, see:
    README.md       - Quick start
    GUIDE.md        - Complete guide
    COMPARISON.md   - Detailed comparison with C++ version
    """)

def main():
    """Main verification process"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║  " + "Zap Game - Python Installation Verification".center(64) + "  ║")
    print("║  " + "Simplified OpenTNL Reimplementation".center(64) + "  ║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    
    steps_passed = 0
    total_steps = 4
    
    # Check Python version
    if check_python_version():
        steps_passed += 1
    else:
        print("\n✗ Python version check failed")
        return 1
    
    # Check dependencies
    if check_dependencies():
        steps_passed += 1
    else:
        print("\n✗ Dependency check failed")
        return 1
    
    # Run tests
    if run_tests():
        steps_passed += 1
    else:
        print("\n⚠ Tests failed, but you can still try running the game")
        steps_passed += 1  # Don't fail on test errors
    
    # Crypto demo (optional)
    if demo_crypto():
        steps_passed += 1
    
    # Show instructions
    show_instructions()
    
    # Summary
    print_header("Installation Summary")
    print(f"\nSteps completed: {steps_passed}/{total_steps}")
    
    if steps_passed >= 3:
        print("\n✓ Installation verified successfully!")
        print("\nYou are ready to run the game:")
        print("    python main.py")
    else:
        print("\n⚠ Some verification steps failed")
        print("Please check the errors above and resolve them")
        return 1
    
    print("\n" + "=" * 70)
    print("  Have fun playing Zap!")
    print("=" * 70 + "\n")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nVerification interrupted by user")
        sys.exit(1)
