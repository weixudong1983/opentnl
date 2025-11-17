"""
Simplified networking module
Replaces libtomcrypt asymmetric keys with Python's cryptography library
"""
import socket
import json
import pickle
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


class SimpleAsymmetricKey:
    """
    Simplified replacement for libtomcrypt asymmetric keys
    Uses RSA from Python's cryptography library
    """
    
    def __init__(self, key_size=2048):
        """Generate a new key pair"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def get_public_key_bytes(self):
        """Export public key as bytes"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    
    def get_private_key_bytes(self):
        """Export private key as bytes"""
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    
    @staticmethod
    def load_public_key(key_bytes):
        """Load public key from bytes"""
        key = SimpleAsymmetricKey.__new__(SimpleAsymmetricKey)
        key.public_key = serialization.load_pem_public_key(
            key_bytes,
            backend=default_backend()
        )
        key.private_key = None
        return key
    
    @staticmethod
    def load_private_key(key_bytes):
        """Load private key from bytes"""
        key = SimpleAsymmetricKey.__new__(SimpleAsymmetricKey)
        key.private_key = serialization.load_pem_private_key(
            key_bytes,
            password=None,
            backend=default_backend()
        )
        key.public_key = key.private_key.public_key()
        return key
    
    def encrypt(self, message):
        """Encrypt message with public key"""
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        return self.public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def decrypt(self, ciphertext):
        """Decrypt message with private key"""
        if self.private_key is None:
            raise ValueError("Cannot decrypt without private key")
        
        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    
    def sign(self, message):
        """Sign message with private key"""
        if self.private_key is None:
            raise ValueError("Cannot sign without private key")
        
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        return self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    
    def verify(self, message, signature):
        """Verify signature with public key"""
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        try:
            self.public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False


class NetworkConnection:
    """Simple network connection wrapper"""
    
    def __init__(self, host='localhost', port=28000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self):
        """Connect to server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.socket.setblocking(False)
            self.connected = True
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def send_data(self, data):
        """Send data (will be pickled)"""
        if not self.connected or not self.socket:
            return False
        
        try:
            serialized = pickle.dumps(data)
            # Send length prefix
            length = len(serialized)
            self.socket.sendall(length.to_bytes(4, 'big'))
            self.socket.sendall(serialized)
            return True
        except Exception as e:
            print(f"Send failed: {e}")
            return False
    
    def receive_data(self):
        """Receive data (will be unpickled)"""
        if not self.connected or not self.socket:
            return None
        
        try:
            # Read length prefix
            length_bytes = self.socket.recv(4)
            if not length_bytes:
                return None
            
            length = int.from_bytes(length_bytes, 'big')
            
            # Read data
            data = b''
            while len(data) < length:
                chunk = self.socket.recv(min(4096, length - len(data)))
                if not chunk:
                    return None
                data += chunk
            
            return pickle.loads(data)
        except BlockingIOError:
            return None
        except Exception as e:
            print(f"Receive failed: {e}")
            return None
    
    def close(self):
        """Close connection"""
        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False


class NetworkServer:
    """Simple network server"""
    
    def __init__(self, host='', port=28000):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = []
    
    def start(self):
        """Start server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.socket.setblocking(False)
            print(f"Server started on {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Server start failed: {e}")
            return False
    
    def accept_connections(self):
        """Accept new connections"""
        try:
            client_socket, address = self.socket.accept()
            client_socket.setblocking(False)
            self.clients.append((client_socket, address))
            print(f"Client connected from {address}")
            return True
        except BlockingIOError:
            return False
        except Exception as e:
            print(f"Accept failed: {e}")
            return False
    
    def broadcast(self, data):
        """Broadcast data to all clients"""
        serialized = pickle.dumps(data)
        length = len(serialized)
        
        disconnected = []
        for client_socket, address in self.clients:
            try:
                client_socket.sendall(length.to_bytes(4, 'big'))
                client_socket.sendall(serialized)
            except Exception:
                disconnected.append((client_socket, address))
        
        # Remove disconnected clients
        for client in disconnected:
            self.clients.remove(client)
            client[0].close()
    
    def stop(self):
        """Stop server"""
        for client_socket, _ in self.clients:
            client_socket.close()
        self.clients = []
        
        if self.socket:
            self.socket.close()
            self.socket = None
