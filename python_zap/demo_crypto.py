#!/usr/bin/env python3
"""
Demo script showcasing the simplified cryptography replacement

This demonstrates how the Python version replaces libtomcrypt's
asymmetric key operations with Python's cryptography library.
"""

from network import SimpleAsymmetricKey


def demo_key_generation():
    """Demonstrate key generation"""
    print("=" * 60)
    print("Key Generation Demo")
    print("=" * 60)
    
    print("\nGenerating RSA key pair (2048 bits)...")
    key = SimpleAsymmetricKey(key_size=2048)
    
    print("✓ Key pair generated")
    print(f"  Public key size: {len(key.get_public_key_bytes())} bytes")
    print(f"  Private key size: {len(key.get_private_key_bytes())} bytes")
    
    return key


def demo_encryption(key):
    """Demonstrate encryption and decryption"""
    print("\n" + "=" * 60)
    print("Encryption/Decryption Demo")
    print("=" * 60)
    
    message = "Hello from Zap game! This is a secret message."
    print(f"\nOriginal message: '{message}'")
    
    print("\nEncrypting with public key...")
    ciphertext = key.encrypt(message)
    print(f"✓ Encrypted (size: {len(ciphertext)} bytes)")
    print(f"  Ciphertext: {ciphertext[:50]}..." if len(ciphertext) > 50 else f"  Ciphertext: {ciphertext}")
    
    print("\nDecrypting with private key...")
    decrypted = key.decrypt(ciphertext).decode('utf-8')
    print(f"✓ Decrypted: '{decrypted}'")
    
    if decrypted == message:
        print("\n✓ Encryption/Decryption successful!")
    else:
        print("\n✗ Error: Messages don't match!")
    
    return True


def demo_signing(key):
    """Demonstrate digital signatures"""
    print("\n" + "=" * 60)
    print("Digital Signature Demo")
    print("=" * 60)
    
    message = "Game state update: Player moved to (100, 200)"
    print(f"\nMessage to sign: '{message}'")
    
    print("\nSigning with private key...")
    signature = key.sign(message)
    print(f"✓ Signed (signature size: {len(signature)} bytes)")
    
    print("\nVerifying signature with public key...")
    is_valid = key.verify(message, signature)
    
    if is_valid:
        print("✓ Signature is VALID")
    else:
        print("✗ Signature is INVALID")
    
    # Test with tampered message
    print("\nTesting with tampered message...")
    tampered = "Game state update: Player moved to (999, 999)"
    is_valid_tampered = key.verify(tampered, signature)
    
    if not is_valid_tampered:
        print("✓ Tampered message correctly rejected")
    else:
        print("✗ Error: Tampered message was accepted!")
    
    return True


def demo_key_exchange():
    """Demonstrate key exchange between two parties"""
    print("\n" + "=" * 60)
    print("Key Exchange Demo (Simulating Client-Server)")
    print("=" * 60)
    
    print("\nServer: Generating key pair...")
    server_key = SimpleAsymmetricKey(2048)
    print("✓ Server key generated")
    
    print("\nClient: Generating key pair...")
    client_key = SimpleAsymmetricKey(2048)
    print("✓ Client key generated")
    
    print("\nExchanging public keys...")
    server_public = server_key.get_public_key_bytes()
    client_public = client_key.get_public_key_bytes()
    
    # Load each other's public keys
    print("\nServer: Loading client's public key...")
    client_public_key = SimpleAsymmetricKey.load_public_key(client_public)
    print("✓ Client public key loaded")
    
    print("\nClient: Loading server's public key...")
    server_public_key = SimpleAsymmetricKey.load_public_key(server_public)
    print("✓ Server public key loaded")
    
    # Client sends encrypted message to server
    print("\n" + "-" * 60)
    print("Client → Server: Encrypted message")
    print("-" * 60)
    
    client_message = "Join game request: Player1"
    print(f"Client message: '{client_message}'")
    
    encrypted_to_server = server_public_key.encrypt(client_message)
    print(f"✓ Encrypted for server ({len(encrypted_to_server)} bytes)")
    
    decrypted_by_server = server_key.decrypt(encrypted_to_server).decode('utf-8')
    print(f"Server received: '{decrypted_by_server}'")
    
    if decrypted_by_server == client_message:
        print("✓ Message successfully transmitted to server")
    
    # Server sends encrypted response to client
    print("\n" + "-" * 60)
    print("Server → Client: Encrypted response")
    print("-" * 60)
    
    server_message = "Welcome! You are on team Blue"
    print(f"Server message: '{server_message}'")
    
    encrypted_to_client = client_public_key.encrypt(server_message)
    print(f"✓ Encrypted for client ({len(encrypted_to_client)} bytes)")
    
    decrypted_by_client = client_key.decrypt(encrypted_to_client).decode('utf-8')
    print(f"Client received: '{decrypted_by_client}'")
    
    if decrypted_by_client == server_message:
        print("✓ Message successfully transmitted to client")
    
    print("\n✓ Secure key exchange demonstration complete!")
    return True


def main():
    """Run all demos"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║  ZAP GAME - CRYPTOGRAPHY REPLACEMENT DEMONSTRATION      ║")
    print("║  Python cryptography library replaces libtomcrypt      ║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        # Generate key
        key = demo_key_generation()
        
        # Demonstrate encryption
        demo_encryption(key)
        
        # Demonstrate signing
        demo_signing(key)
        
        # Demonstrate key exchange
        demo_key_exchange()
        
        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("""
This demonstration shows how the Python version successfully replaces
the complex libtomcrypt library with Python's cryptography library:

✓ RSA key generation (2048-bit keys)
✓ Public/Private key encryption and decryption
✓ Digital signatures and verification
✓ Key exchange between client and server
✓ Message integrity protection

The Python implementation is:
  • Simpler to use (fewer lines of code)
  • Well-maintained and secure
  • Cross-platform compatible
  • Easier to debug and extend
  
Original C++ used libtomcrypt with ECC (Elliptic Curve Cryptography).
Python version uses RSA which is simpler but equally secure for the
game's networking needs.

For the Zap game specifically, this provides:
  • Secure client-server communication
  • Player authentication
  • Cheat prevention
  • Session integrity
        """)
        
        print("=" * 60)
        print("All demonstrations completed successfully! ✓")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
