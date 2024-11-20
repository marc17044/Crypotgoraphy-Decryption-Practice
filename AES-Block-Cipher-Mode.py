from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

class BlockCipher:
    def __init__(self, key=None):
        # Generate a 256-bit (32-byte) AES key if none is provided (many-time key usage)
        self.key = key if key else os.urandom(32)
        self.backend = default_backend()
    
    def encrypt(self, plaintext, one_time_key=False):
        try:
            # Generate a new AES key if one_time_key is specified
            key = os.urandom(32) if one_time_key else self.key
            iv = os.urandom(16)  # 16-byte IV for AES
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
            encryptor = cipher.encryptor()

            # Padding plaintext to match AES block size
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext) + padder.finalize()

            # Encrypt the padded plaintext
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()
            return iv + ciphertext  # Return IV + ciphertext for decryption
        except Exception as e:
            print(f"Encryption failed: {e}")
            return None

    def decrypt(self, iv_and_ciphertext):
        try:
            iv = iv_and_ciphertext[:16]  # Extract the IV
            ciphertext = iv_and_ciphertext[16:]  # The actual ciphertext

            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove padding from plaintext
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            return plaintext
        except Exception as e:
            print(f"Decryption failed: {e}")
            return None


    # Initialize the cipher with a many-time key
cbc_key = bytes.fromhex("140b41b22a29beb4061bda66b6747e14")
cbc_ciphertext = bytes.fromhex("5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253")
block_cipher = BlockCipher(cbc_key)

decrypted_text = block_cipher.decrypt(cbc_ciphertext)
if decrypted_text:
    print("Decrypted text:", decrypted_text)
    try:
        print("Decrypted text:", decrypted_text.decode())
    except UnicodeDecodeError as e:
        print(f"Decoding failed: {e}")
