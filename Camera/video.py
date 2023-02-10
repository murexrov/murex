import cv2
import numpy as np

vc = cv2.VideoCapture(1)
frame_width = int(vc.get(3))
frame_height = int(vc.get(4))
#fourcc = cv2.VideoWriter_fourcc(*'h264')
#out = cv2.VideoWriter("test.mp4", fourcc, 10, (frame_width, frame_height))
if not vc.isOpened():
    print("Error")
while vc.isOpened():
    ret, frame = vc.read()
    if ret:
        #cv2.imshow('Frame', frame)
        #out.write(frame)
        img_str = cv2.imencode('.jpg', frame)[1].tobytes()
        #print(img_str)
        if cv2.waitKey(25) & 0xFF == ord('q'):
           break
    else:
        break
    image = np.asarray(bytearray(img_str), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imshow('Image', image)
vc.release()
#out.release()
cv2.destroyAllWindows()
