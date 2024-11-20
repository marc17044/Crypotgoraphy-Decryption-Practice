import hmac
import hashlib

def generate_mac(key, message):
    """
    Generates an HMAC for a given message and secret key.
    
    :param key: The secret key (bytes).
    :param message: The message to be authenticated (bytes).
    :return: The HMAC (Message Authentication Code) for the message.
    """
    return hmac.new(key, message, hashlib.sha256).hexdigest()

def verify_mac(key, message, mac):
    """
    Verifies the HMAC for a given message and secret key.
    
    :param key: The secret key (bytes).
    :param message: The message to be verified (bytes).
    :param mac: The expected HMAC to compare against.
    :return: True if the MAC is valid, False otherwise.
    """
    generated_mac = generate_mac(key, message)
    return hmac.compare_digest(generated_mac, mac)

# Example usage

# Secret key (should be kept safe and confidential)
secret_key = b"supersecretkey"

# Original message
original_message = b"Hello, this is a secure message!"

# Generate MAC
mac = generate_mac(secret_key, original_message)
print(f"Generated MAC: {mac}")

# Verify the MAC (should return True if the message is intact)
is_valid = verify_mac(secret_key, original_message, mac)
print(f"MAC verification result: {is_valid}")

# Simulate a tampered message
tampered_message = b"Hello, this is a tampered message!"

# Verify the MAC with the tampered message (should return False)
is_valid_tampered = verify_mac(secret_key, tampered_message, mac)
print(f"MAC verification result for tampered message: {is_valid_tampered}")
