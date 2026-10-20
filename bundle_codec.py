"""AppWorld encryption functions, Apache-2.0; see LICENSES/Apache-2.0.txt.
Excerpt from commit 42b5bcf3cd334fee33f0c37c02070a9f5807add5. Public key material below is a
reproducibility packaging key, not an account credential or access restriction.
"""
import hashlib
PASSWORD = "tool-recovery-artifacts-v1.0.0-public-bundle"
SALT = hashlib.sha256(b"tool-recovery-artifacts-public-replication").digest()[:16]

def encryption_key(password: str, salt: bytes) -> bytes:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


def encrypt_bytes(data: bytes, password: str, salt: bytes) -> bytes:
    import secrets

    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.decrepit.ciphers.modes import CFB
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

    key = encryption_key(password, salt)
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(key), CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return iv + encrypted_data


def decrypt_bytes(data: bytes, password: str, salt: bytes) -> bytes:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.decrepit.ciphers.modes import CFB
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

    key = encryption_key(password, salt)
    iv = data[:16]
    encrypted_data = data[16:]
    cipher = Cipher(algorithms.AES(key), CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data



