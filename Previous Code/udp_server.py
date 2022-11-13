import socket
import sys

ip = "192.168.100.1"
port = int(1234)

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port
server_address = (ip, port)
s.bind(server_address)

while True:
    print("now listening")
    data, address = s.recvfrom(4096)
    received = data.decode('utf-8')
    print("Server received: ", received)
    send_data = "received" + received
    s.sendto(send_data.encode('utf-8'), address)
    print("Server sent : ", send_data)