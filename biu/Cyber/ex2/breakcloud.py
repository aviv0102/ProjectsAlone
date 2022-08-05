'''''
	name: Aviv Shisman
	id:   206558157
'''''



"""
what it does:
	receives 'cloud', an object of type Cloud.
	creates a file with the name 'plain.txt' that stores the current text that is encrypted in the cloud.

how?

	1. old_encrypted_byte = plaintext_byte XOR key (was encrypted in cloud)
	2. new_encrypted_byte = '\0' XOR key (will do it in stage 3)
	
	3. write the new encrypted byte instead of the old and get the old back with Write method
	4. write the old byte back to return to prev state + get the new byte
	
	5. dycrepted_byte = old XOR new => (plain_byte XOR key) XOR ('\0' XOR key) 
											=> '\0'' XOR plain_byte => plain_byte 
"""
def breakcloud(cloud):
	pt = ''
	for i in range(cloud.Length()):
		old = cloud.Write(i, '\0')	# stage 2,3
		new = cloud.Write(i,old)	# stage 4

		decrypted = chr(ord(old) ^ ord(new)) # stage 5
		pt += decrypted

	# write results!
	with open('plain.txt', 'w') as f:
		f.write(pt)

	return