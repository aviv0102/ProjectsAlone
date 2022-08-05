import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_ip = '127.0.0.1'
dest_port = 55555
s.connect((dest_ip, dest_port))
msg = ''
for i in range(15000):
    msg += 'A'
    
s.send(msg)
data = s.recv(4096)
print "Server sent: ", data

s.close()
