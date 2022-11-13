import socket
import sys
from inputs import get_gamepad

ip = "192.168.100.1"
port = int(1234)

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("connection established to rpi")
# Let's send data through UDP protocol
while True:
    events = get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)
        send_data = str(str(event.code) + " " + str(event.state))
    s.sendto(send_data.encode('utf-8'), (ip, port))
    print("Client Sent : ", send_data)
    data, address = s.recvfrom(4096)
    print("Client received : ", data.decode('utf-8'))
# close the socket
s.close()