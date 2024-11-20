


def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a


# Example usage
print(gcd(378, 210)) # Output: 5
print(gcd(42, 112)) # Output: 14
print(gcd(1512, 444)) # Output: 12



def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1  
    return gcd, x, y
# Example usage
gcd, x, y = extended_gcd(35, 15)
print(f"GCD: {gcd}, x: {x}, y: {y}") # Output: GCD: 5, x: 1, y: -2








