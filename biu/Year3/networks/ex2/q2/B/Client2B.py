import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_ip = '127.0.0.1'
dest_port = 12469
s.connect((dest_ip, dest_port))
msg='A'
s.send(msg)
time.sleep(0.1)
s.send(msg)
time.sleep(2)
for i in range(11):
    s.send(msg)
    time.sleep(0.1)
    s.send(msg)
    time.sleep(2)

s.send("check")
data = s.recv(9096)
print "Server sent: ", data


s.close()
