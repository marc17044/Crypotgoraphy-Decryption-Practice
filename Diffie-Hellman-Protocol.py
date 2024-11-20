import random

# Function to calculate (base^exp) % mod using the efficient method of exponentiation
def mod_exp(base, exp, mod):
    result = 1
    base = base % mod  # Ensure base is within mod
    while exp > 0:
        if exp % 2 == 1:  # If exp is odd, multiply the base with result
            result = (result * base) % mod
        exp = exp // 2  # Divide exp by 2
        base = (base * base) % mod  # Square the base
    return result

# Step 1: Public parameters (p and g)
p = 23  # A small prime number for simplicity
g = 5   # A primitive root modulo p

# Step 2: Alice's private key (a) and public key (A)
a = random.randint(1, p-1)  # Alice's private key (random)
A = mod_exp(g, a, p)         # Alice's public key (g^a mod p)

# Step 3: Bob's private key (b) and public key (B)
b = random.randint(1, p-1)  # Bob's private key (random)
B = mod_exp(g, b, p)         # Bob's public key (g^b mod p)

# Step 4: Alice and Bob exchange public keys
print(f"Alice's public key (A): {A}")
print(f"Bob's public key (B): {B}")

# Step 5: Alice computes the shared secret
shared_secret_alice = mod_exp(B, a, p)
print(f"Alice's computed shared secret: {shared_secret_alice}")

# Step 6: Bob computes the shared secret
shared_secret_bob = mod_exp(A, b, p)
print(f"Bob's computed shared secret: {shared_secret_bob}")

# Step 7: Verify if the shared secrets match
if shared_secret_alice == shared_secret_bob:
    print("The shared secret is the same for both Alice and Bob!")
else:
    print("The shared secret does not match.")
