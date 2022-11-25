import socket
import threading

ip = "192.168.100.1"
port = int(1234)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((ip, port))

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode('utf-8'))
        except:
            pass

t = threading.Thread(target = receive)
t.start()

while True:
    message = input()
    client.sendto(message.encode('utf-8'), (ip, port))