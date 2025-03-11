import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# In production, this should be a secure environment variable
# For development, we'll use a fixed key
SECRET_KEY = os.getenv("ENCRYPTION_KEY", "this-is-a-development-key-do-not-use-in-production")
SALT = os.getenv("ENCRYPTION_SALT", "development-salt").encode()


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