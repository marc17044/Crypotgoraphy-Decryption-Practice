# Question 1
# An attacker intercepts the following ciphertext (hex encoded): 

#    20814804c1767293b99f1d9cab3bc3e7 ac1e37bfb15599e5f40eef805488281d 

# He knows that the plaintext is the ASCII encoding of the message "Pay Bob 100$" (excluding the quotes). 
# He also knows that the cipher used is CBC encryption with a random IV using AES as the underlying block cipher. 
# Show that the attacker can change the ciphertext so that it will decrypt to "Pay Bob 500$". What is the resulting ciphertext (hex encoded)? 
# This shows that CBC provides no integrity.

import sys

def main():
	# input
	cypherText = "20814804c1767293b99f1d9cab3bc3e7 ac1e37bfb15599e5f40eef805488281d".split(' ')
	
	# set the CBC parts. The first part is the IV
	cypherTextIV = bytes.fromhex(cypherText[0])
	cypherTextC0 = bytes.fromhex(cypherText[1])
	
	# define plaintexts
	plainText = "Pay Bob 100$"
	plainTextTarget = "Pay Bob 500$"

	# define paddings
	paddingNum1 = 16 - (len(plainText) % 16)
	padding1 = plainText + chr(paddingNum1) * paddingNum1

	paddingNum2 = 16 - (len(plainTextTarget) % 16)
	padding2 = plainTextTarget + chr(paddingNum2) * paddingNum2

	# XOR the plaintext to determine the value to XOR with
	xorredPlainText = strxor(padding1, padding2)

	# Since the decryption of c[0] is XORed with IV to retrieve the plaintext, xor the IV with the desired mutation
	newIV = strxor(xorredPlainText, cypherTextIV)

	# new CBC 
	print("New CBC\n", newIV.hex(), cypherText[1])

	# Output:
	# New CBC
	# 20814804c1767293bd9f1d9cab3bc3e7 ac1e37bfb15599e5f40eef805488281d


# xor two strings of different lengths
def strxor(a, b):     
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])


main()