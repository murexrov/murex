import socket
import threading
import queue

messages = queue.Queue()

ip = "192.168.100.1"
port = int(1234)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((ip, port))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass
def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode('utf-8'))
            server.sendto(message, addr)

t1 = threading.Thread(target = receive)
t2 = threading.Thread(target = broadcast)

t1.start()
t2.start()