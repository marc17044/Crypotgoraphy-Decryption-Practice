from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
import os

def generate_key():
    """Generates a random key for AES encryption"""
    return os.urandom(32)  # 256-bit key for AES-256

def encrypt(plaintext, key):
    """Encrypts plaintext using AES-GCM"""
    # Generate a random nonce (96 bits for AES-GCM)
    nonce = os.urandom(12)

    # Create an AES cipher object with GCM mode
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()

    # Perform padding to ensure the plaintext is a multiple of the block size (128 bits for AES)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode()) + padder.finalize()

    # Encrypt the data and generate the authentication tag
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext, nonce, encryptor.tag

def decrypt(ciphertext, key, nonce, tag):
    """Decrypts the ciphertext using AES-GCM and verifies authenticity"""
    # Create the AES cipher object for decryption
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data and remove padding
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()

    return plaintext.decode()

# Example usage
key = generate_key()  # Generate a random key
plaintext = "This is a secret message!"

# Encrypt the plaintext
ciphertext, nonce, tag = encrypt(plaintext, key)
print("Ciphertext:", ciphertext.hex())
print("Nonce:", nonce.hex())
print("Tag:", tag.hex())

# Decrypt the ciphertext
decrypted_message = decrypt(ciphertext, key, nonce, tag)
print("Decrypted Message:", decrypted_message)
