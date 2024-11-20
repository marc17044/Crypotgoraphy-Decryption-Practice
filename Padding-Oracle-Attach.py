import urllib
import sys
import binascii

TARGET = 'http://crypto-class.appspot.com/po?er='

class PaddingOracle:
    def query(self, q):
        target = TARGET + urllib.quote(q)  # Create query URL
        req = urllib.Request(target)  # Send HTTP request to server
        try:
            f = urllib.urlopen(req)  # Wait for response
        except urllib.HTTPError as e:
            print(f"We got: {e.code}")  # Print response code
            if e.code == 404:
                return True  # Good padding
            return False  # Bad padding

def decrypt_block(block, iv, oracle):
    """
    Decrypt a single block of ciphertext using the padding oracle.
    """
    block = binascii.unhexlify(block)  # Convert hex to binary
    iv = binascii.unhexlify(iv)  # Convert IV to binary
    decrypted = b""
    
    for i in range(16):  # For each byte of the block
        padding_value = 16 - i
        prefix = iv[:16 - i - 1]  # Starting point, before the modified byte
        suffix = decrypted[:i]  # Already decrypted part
        
        for guess in range(256):  # Try all possible byte values (0-255)
            modified_block = prefix + bytes([guess ^ padding_value]) + suffix
            modified_ciphertext = binascii.hexlify(modified_block)
            
            if oracle.query(modified_ciphertext):
                decrypted_byte = guess ^ padding_value
                decrypted = bytes([decrypted_byte]) + decrypted
                break
    
    return decrypted

def decrypt_ciphertext(ciphertext, oracle):
    """
    Decrypt the full ciphertext block by block.
    """
    blocks = [ciphertext[i:i+32] for i in range(0, len(ciphertext), 32)]
    decrypted_message = b""
    
    # The first block is the IV, so the next one starts the decryption
    for i in range(1, len(blocks)):
        block = blocks[i]
        iv = blocks[i - 1]  # The previous ciphertext block is the IV for the current block
        decrypted_message += decrypt_block(block, iv, oracle)

    return decrypted_message

if __name__ == "__main__":
    po = PaddingOracle()
    ciphertext = sys.argv[1]  # Pass the ciphertext from command line
    decrypted_message = decrypt_ciphertext(ciphertext, po)
    print("Decrypted Message:", decrypted_message.decode('utf-8'))
