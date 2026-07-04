from cryptography.fernet import Fernet
from django.conf import settings

def _get_fernet():
    return Fernet(settings.PASSWORD_ENCRYPTION_KEY)

def encrypt_password(plain_password: str) -> str:
    """Encrypts a plaintext password and returns it as a string."""
    if not plain_password:
        return plain_password
    fernet = _get_fernet()
    encrypted_bytes = fernet.encrypt(plain_password.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_password(encrypted_password: str) -> str:
    """Decrypts an encrypted password string and returns the plaintext."""
    if not encrypted_password:
        return encrypted_password
    fernet = _get_fernet()
    try:
        decrypted_bytes = fernet.decrypt(encrypted_password.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except Exception:
        # If decryption fails (e.g., old plaintext password or corrupted data),
        # return None
        return None
