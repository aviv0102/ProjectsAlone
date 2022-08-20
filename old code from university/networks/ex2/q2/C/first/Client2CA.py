from socket import socket,AF_INET,SOCK_DGRAM

s = socket(AF_INET, SOCK_DGRAM)
dest_ip = '127.0.0.1'
dest_port = 54321
msg = ''
for i in range(15000):
    msg += 'A'

print "sent"
s.sendto(msg,(dest_ip,dest_port))
data,sender_info=s.recvfrom(2048)
print "Server sent: ", data

s.close()
