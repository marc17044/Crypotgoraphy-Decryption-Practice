from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

# Given key and ciphertext in hexadecimal
crt_key_hex = "36f18357be4dbd77f050515c73fcf9f2"
crt_ciphertext_hex = "770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451"

# Convert hex key and ciphertext to bytes
bin_crt_key = binascii.unhexlify(crt_key_hex)
bin_crt_ciphertext = binascii.unhexlify(crt_ciphertext_hex)

# Extract the first 16 bytes of the ciphertext as the nonce (IV for CTR mode)
nonce = bin_crt_ciphertext[:16]
actual_ciphertext = bin_crt_ciphertext[16:]

# Set up the AES cipher in CTR mode using the given key and nonce
cipher = Cipher(algorithms.AES(bin_crt_key), modes.CTR(nonce), backend=default_backend())
decryptor = cipher.decryptor()

# Decrypt the ciphertext
plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
print("Decrypted text:", plaintext.decode())
