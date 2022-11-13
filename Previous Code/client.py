import cv2,socket,pickle,struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = "192.168.100.1"
port = 8061
host = (ip, port)

data = b''
payload_size = struct.calcsize("L")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(host)
    while True:
        # data = s.recv(1024)
        while len(data) < payload_size:
            data += s.recv(4096)
        # print(data)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("=L", packed_msg_size)[0] ### CHANGED

        # Retrieve all data based on message size
        while len(data) < msg_size:
            data += s.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Extract frame
        frame = pickle.loads(frame_data)
        frame = cv2.flip(frame, 1)

        cv2.imshow('Live Feed', frame)
        cv2.waitKey(1)  

        if cv2.getWindowProperty('Live Feed', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()