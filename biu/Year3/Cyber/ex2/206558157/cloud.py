
'''''
	name: Aviv Shisman
	id:   206558157
'''''

# imports:
from Crypto import Random
from Crypto.Util import Counter
import Crypto.Cipher.AES as AES



'''
the cloud stores your content encrypted.
you can add variables and methods to this class as you want.	
'''
class Cloud:

    ''''
    Encrypt the content of 'filename' and store its ciphertext at self.ciphertext
    '''''
    def __init__(self, filename, key=Random.get_random_bytes(32), nonce=Random.get_random_bytes(8)):

        # getting encryption parameters
        self.key = key
        self.nonce = nonce
        countf = Counter.new(64, nonce,initial_value=1)

        # reading file
        with open(filename, mode='rb') as file:
            self.pt = file.read()

        # encrypt and save
        crypto = AES.new(key, AES.MODE_CTR, counter=countf)
        self.ciphertext = crypto.encrypt(self.pt)


	"""
	Returns the length of the plaintext/ciphertext 
	"""
    def Length(self):
        return len(self.ciphertext)

    """
    Returns one byte at 'position' from current self.ciphertext
    """
    def Read(self, position=0):
        return self.ciphertext[position]

    """
    Replace the byte in 'position' from self.ciphertext with the encryption of 'newbyte'.
    Return the previous byte from self.ciphertext 
    
    Remember that you should encrypt 'newbyte' under the appropriate key (it depends on the position).
    """
    def Write(self, position=0, newbyte='\x33'):
        old = self.ciphertext[position]
        pt = list(self.pt)
        pt[position] = newbyte
        self.pt = ''.join(pt)
        countf = Counter.new(64, self.nonce , initial_value = 1)
        crypto = AES.new(self.key, AES.MODE_CTR, counter=countf)
        ct = crypto.encrypt(self.pt)
        self.ciphertext = ct

        return old

