import cv2, socket, pickle, struct
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.100.1'
port = 8061

cap = cv2.VideoCapture(0)
# rate = 100
# cap.set(3, int(16 * rate))
# cap.set(4, int(9 * rate))
# cap.set(5, 1)
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
# print(cap.get(3), cap.get(4))

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((host, port))
	s.listen()
	c, addr = s.accept()
	with c:
		print(f"Connected by {addr}")
		while True:
			try:
				ret, frame = cap.read()
				# frame = rescale_frame(frame, percent = 50)
				data = pickle.dumps(frame)
				message_size = struct.pack("=Q", len(data))
				c.sendall(message_size + data)
			except socket.error or KeyboardInterrupt:
				c.close
				break
cap.release()
