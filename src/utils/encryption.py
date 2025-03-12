import os
import base64
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Get encryption key and salt from environment variables
# If not set, generate a secure random key and salt for development
# In production, these should be set as secure environment variables
SECRET_KEY = os.getenv("ENCRYPTION_KEY")
if not SECRET_KEY:
    # Generate a secure random key for development
    SECRET_KEY = secrets.token_hex(32)
    print("WARNING: Using a randomly generated encryption key. Set ENCRYPTION_KEY environment variable in production.")

SALT = os.getenv("ENCRYPTION_SALT")
if not SALT:
    # Generate a secure random salt for development
    SALT = secrets.token_hex(16)
    print("WARNING: Using a randomly generated salt. Set ENCRYPTION_SALT environment variable in production.")

SALT = SALT.encode()


def get_encryption_key():
    """Generate an encryption key from the secret key and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(SECRET_KEY.encode()))
    return key


def encrypt_value(value: str) -> str:
    """Encrypt a string value."""
    if not value:
        return value
    
    key = get_encryption_key()
    f = Fernet(key)
    encrypted_value = f.encrypt(value.encode())
    return encrypted_value.decode()


def decrypt_value(encrypted_value: str) -> str:
    """Decrypt an encrypted string value."""
    if not encrypted_value:
        return encrypted_value
    
    key = get_encryption_key()
    f = Fernet(key)
    try:
        decrypted_value = f.decrypt(encrypted_value.encode())
        return decrypted_value.decode()
    except Exception as e:
        # Log the error in production
        print(f"Error decrypting value: {e}")
        return "[Decryption Error]"