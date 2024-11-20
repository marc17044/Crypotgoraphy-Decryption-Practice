import sys
import os
import urllib.request
import time
import binascii

# Padding oracle URL
class PaddingOracle(object):
    def __init__(self):
        self.targetURL = 'http://crypto-class.appspot.com/po?er='

    def query(self, q):
        target = self.targetURL + urllib.parse.quote(str(q))    # Create query URL
        req = urllib.request.Request(target)         # Send HTTP request to server
        try:
            f = urllib.request.urlopen(req)          # Wait for response
        except urllib.error.HTTPError as e:          
            return e.code == 404  # 404 indicates valid padding

class CharGuesser(object):
	def __init__(self):
		self.letterFrequencyOrder = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']
		self.firstLetterFrequencyOrder = ['T', 'A', 'S', 'H', 'W', 'I', 'O', 'B', 'M', 'F', 'C', 'L', 'D', 'P', 'N', 'E', 'G', 'R', 'Y', 'U', 'V', 'J', 'K', 'Q', 'Z', 'X']
		self.otherCharsOrder = [' ','0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', '!', '?', '&']
		self.commonBigramsOrder = ['th', 'en', 'ng', 'he', 'ed', 'of', 'in', 'to', 'al', 'er', 'it', 'de', 'an', 'ou', 'se', 're', 'ea', 'le', 'nd', 'hi', 'sa', 'at', 'is', 'si', 'on', 'or', 'ar', 'nt', 'ti', 've', 'ha', 'as', 'ra', 'es', 'te', 'ld', 'st', 'et', 'ur']
		self.charsUsed = []


	def guessPrecedingChar(self, currentChar=None):
		if(currentChar):
			# Check common bigrams
			for bigram in self.commonBigramsOrder:
				if bigram[1] == currentChar.lower():
					if not self.checkUsed(bigram[0]):
						return self.setUsed(bigram[0])
					if not self.checkUsed(bigram[0].upper()):
						return self.setUsed(bigram[0].upper())

		# Else check chars in order of probability
		for char in self.letterFrequencyOrder:
			if not self.checkUsed(char):
				return self.setUsed(char)

		# Else check uppercase chars in order of probability of first chars
		for char in self.firstLetterFrequencyOrder:
			if not self.checkUsed(char):
				return self.setUsed(char)

		# Else check common chars, puntcuation, numbers, etc
		for char in self.otherCharsOrder:
			if not self.checkUsed(char):
				return self.setUsed(char)
				
		# Else loop all ASCII from 0-255
		for char in map(lambda x: chr(x), range(0,256)):
			if not self.checkUsed(char):
				return self.setUsed(char)	
		
		# When all else fails?
		return None

	def checkUsed(self,char):
		return char in self.charsUsed

	def setUsed(self,char):
		self.charsUsed.append(char)
		return char


def main():
    cryptoText = bytes.fromhex("ccaf7c1f12cb3a23c4fa8233bd5ea696c974306f107a54b8cb83530c71afcadd5ffe8a666f845243098818e8c522fab8b4a954e5f299995aeb1976f45b5ffc40")
    blockSize = 16  # AES block size in bytes
    cryptoBlocks  = splitCount(cryptoText, blockSize)  # Split into 16-byte blocks
    messageBlocks = splitCount(bytes.fromhex("00" * blockSize * (len(cryptoBlocks) - 1)), blockSize)

    start_time = time.time()
    total_attempts = 0
    guessed_message = ""

    po = PaddingOracle()
    
    for blockNum in reversed(range(1, len(cryptoBlocks))):
        if blockNum >= len(messageBlocks):
            print(f"Error: blockNum {blockNum} is out of range for messageBlocks.")
            continue

        for position in reversed(range(0, blockSize)):
            paddingNum = blockSize - position
            cryptoSourceBlock = bytearray(cryptoBlocks[blockNum])

            for pl in range(1, paddingNum):
                plPos = position + pl
                if plPos < len(messageBlocks[blockNum]):
                    messageValue = messageBlocks[blockNum][plPos]
                    cryptoSourceBlock[plPos] ^= ord(str(messageValue)) ^ paddingNum

            charGuesser = CharGuesser()
            lastChar = None
            counter = 0

            while counter < 256:
                guess = charGuesser.guessPrecedingChar(lastChar)
                if guess is None:
                    break

                cryptoSourceBlock[position] ^= ord(guess) ^ paddingNum
                cryptoGuess = buildCryptoString(cryptoBlocks, blockNum, cryptoSourceBlock)  # Updated to use modified buildCryptoString
                total_attempts += 1

                elapsed_time = time.time() - start_time
                sys.stdout.flush()
                sys.stdout.write(f"\rElapsed Time: {elapsed_time:.2f} sec | Total Attempts: {total_attempts} | Current Ciphertext: {cryptoGuess}")
                

                if po.query(cryptoGuess):
                    messageBlocks[blockNum][position] = guess
                    guessed_message += guess
                    break

                counter += 1

    print("\nGuessed message:", guessed_message)

def splitCount(s, count):
    return [s[i:i + count] for i in range(0, len(s), count)]

def buildCryptoString(cryptoBlocks, blockNum, modifiedBlock):
    """Build the full ciphertext with the modified block inserted at blockNum."""
    modifiedCiphertext = b''.join(
        cryptoBlocks[:blockNum] + [modifiedBlock] + cryptoBlocks[blockNum + 1:]
    )
    return binascii.hexlify(modifiedCiphertext).decode('utf-8')

main()
