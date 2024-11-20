import binascii
plaintext1 = "attack at dawn"
plaintext2 = "attack at dusk"
ciphertext_hex = "09e1c5f70a65ac519458e7e53f36"

# Convert plaintext messages to bytes
plaintext1_bytes = plaintext1.encode('ascii')
plaintext2_bytes = plaintext2.encode('ascii')
print(f"Plaintext '{plaintext1}' in bytes:", plaintext1_bytes)
print(f"Plaintext '{plaintext2}' in bytes:", plaintext2_bytes)

ciphertext_bytes = binascii.unhexlify(ciphertext_hex)

# Derive key by XORing plaintext1 with ciphertext
key = bytes([p ^ c for p, c in zip(plaintext1_bytes, ciphertext_bytes)])
print("Derived Key:", binascii.hexlify(key))

# XOR plaintext2 with the derived key to get the new ciphertext
new_ciphertext = bytes([p ^ k for p, k in zip(plaintext2_bytes, key)])
print("New Ciphertext (Hex):", binascii.hexlify(new_ciphertext).decode())
