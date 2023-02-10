import cv2 as cv
import numpy as np

pic = None
def position(event,x,y,flag,param):
    if event == cv.EVENT_LBUTTONDOWN:
        dot_list.append((x,y))
        show_screenshot()

def nothing(x):
    pass

def show_screenshot():
    global pic
    annotations = np.zeros_like(pic, np.uint8)
    for i in range(len(dot_list)):
        cv.circle(annotations,dot_list[i],5,(r,r,r),-1)
    pic = cv.addWeighted(pic,1,annotations,1,0)
    cv.imshow('screenshot', pic)

#Change this to a parser that converts byte strings to frames (cv2 np.array form)
#Not done - need to change some naming stuff
in_frame = (np.frombuffer(bytes, np.uint8).reshape([cv.get(3), cv.get(4), 3]))
vid = cv.VideoCapture(1)

cv.namedWindow('frame')
cv.namedWindow('screenshot')
cv.setMouseCallback('screenshot',position)
cv.createTrackbar('R','frame',100,255,nothing) 
dot_list = []

while(True):
    r = cv.getTrackbarPos('R','frame')
    ret,frame = vid.read()
    cv.imshow('frame', frame)

    #Take Screenshot
    if cv.waitKey(1) & 0xFF == ord('s'):
        pic = frame
        show_screenshot()

    #Clear Previous Annotation
    if cv.waitKey(1) & 0xFF == ord('z'):
        if len(dot_list)!=0:
            dot_list.pop()
        show_screenshot()

    #Clear ALL Annotations
    if cv.waitKey(1) & 0xFF == ord('c'):
        dot_list = []
        show_screenshot()

    #Quit Program
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv.destroyAllWindows()
