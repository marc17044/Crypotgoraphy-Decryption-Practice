import hashlib

def calculate_h0(file_path):
    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Read the entire file into memory
        file_data = f.read()
        
    # Split the file into 1KB (1024-byte) blocks
    block_size = 1024
    blocks = [file_data[i:i + block_size] for i in range(0, len(file_data), block_size)]
    
    # Initialize the hash for the final block
    current_hash = b""
    
    # Iterate over the blocks in reverse order
    for block in reversed(blocks):
        # Append the current hash to the block (if not empty)
        block += current_hash
        # Compute the SHA-256 hash of the augmented block
        current_hash = hashlib.sha256(block).digest()
    
    # Return the final hash (h0) as a hex-encoded string
    return current_hash.hex()

# Example usage:
# Replace 'video_file_path' with the actual path to the video file.
video_file_path = "C:/Users/Marc/Downloads/6.2.birthday.mp4_download"
h0 = calculate_h0(video_file_path)
print(f"Calculated h0: {h0}")

video_file_path = "C:/Users/Marc/Downloads/6.1.intro.mp4_download"
h0 = calculate_h0(video_file_path)
print(f"Calculated final: {h0}")
