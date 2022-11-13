import time
import pigpio
from numpy import interp
from gpiozero import Servo
import socket
import sys
# from inputs import get_gamepad
from gpiozero.pins.pigpio import PiGPIOFactory
factory = PiGPIOFactory()

FrontLeft = 26
FrontRight = 19
BackLeft = 13
BackRight = 6 #Problems
Top = 24
Bottom = 23

camServoPin = 22
armServoPin = 20
clawServoPin = 21
gripServoPin = 16
camServo = Servo(camServoPin,min_pulse_width=0.8/1000,max_pulse_width=2.2/1000,pin_factory=factory)
armServo = Servo(armServoPin,min_pulse_width=0.8/1000,max_pulse_width=2.2/1000,pin_factory=factory)
clawServo = Servo(clawServoPin,min_pulse_width=0.8/1000,max_pulse_width=2.2/1000,pin_factory=factory)
gripServo = Servo(gripServoPin,min_pulse_width=0.8/1000,max_pulse_width=2.2/1000,pin_factory=factory)
camServoPwm = 0
armServoPwm = 0
clawServoPwm = 0
gripServoPwm = 0
armSpeed=0.1
clawSpeed=0.1
gripState=0

ip = "192.168.100.1" # <- ip number
port = int(1234) # <- port number

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MODE = 0

# 0 = forward/backward, 1= left/right, 2 = turning

pi = pigpio.pi()

def stopSignal():
    pi.set_servo_pulsewidth(FrontLeft, 1500)
    pi.set_servo_pulsewidth(FrontRight, 1500)
    pi.set_servo_pulsewidth(BackLeft, 1500)
    pi.set_servo_pulsewidth(BackRight, 1500)
    pi.set_servo_pulsewidth(Top, 1500)
    pi.set_servo_pulsewidth(Bottom, 1500)
    

def init():
    print ("start init")
    stopSignal()
    print ("stop signal completed, waiting 7 seconds")
    # uncomment below if running normally
    time.sleep(7)
    print ("finished waiting, binding sockets")
    # Bind the socket to the port
    server_address = (ip, port)
    s.bind(server_address)
    print ("finished init, udp now up")

def udpStreamIn():
    data, address = s.recvfrom(4096)
    received = data.decode('utf-8')
    send_data = "received: " + received
    s.sendto(send_data.encode('utf-8'), address)
    return(received)

def debug_udp():
    print("now listening")
    data, address = s.recvfrom(4096)
    received = data.decode('utf-8')
    print("Server received: ", received)
    send_data = "received: " + received
    s.sendto(send_data.encode('utf-8'), address)
    print("Server sent : ", send_data)
    return(received)

def gamepadMap(x):
    x = x.split()
    if (x[0] == 'SYN_REPORT'):
        return ('SYN_REPORT')
    else:
        return (x)

def mapY(x):
    return int(interp(x, [-32768,32767], [1750,1250]))

def mapX(x):
    return int(interp(x, [-32768,32767], [1250,1750]))

def mapLeftTrigger(x):
    return int(interp(x, [0, 1023], [1500,1250]))

def mapRightTrigger(x):
    return int(interp(x, [0, 1023], [1500,1750]))


try:
    # print(gamepadMap(udpStreamIn()))
    init()
    while 1:
        # event = get_gamepad()
        streamIn = gamepadMap(udpStreamIn())
        if(streamIn != 'SYN_REPORT'):
            code = streamIn[0]
            state = int(streamIn[1])
            print(code, state)
            print(camServoPwm)
            value = state

            if(code == "ABS_HAT0Y"):
                time.sleep(0.01)
                if(value == 1):
                    camServoPwm -= 0.1
                elif(value == -1):
                    camServoPwm += 0.1
                camServoPwm = round(camServoPwm, 1)
                if (camServoPwm <= -1.0 or camServoPwm >= 1.0):
                    print("over servo limit")
                    if (camServoPwm <= -1.0):
                        camServoPwm = -1.0
                    elif (camServoPwm >= 1.0):
                        camServoPwm = 1.0
                else:
                    camServo.value = camServoPwm

            if(code == "ABS_RY"):
                time.sleep(0.01)
                if(mapY(value) > 1600):
                    armServoPwm -= armSpeed
                    print("arm down")
                elif(mapY(value) < 1400):
                    armServoPwm += armSpeed
                    print("arm up")
                if (armServoPwm <= -1.0 or armServoPwm >= 1.0):
                    print("over servo limit")
                    if (armServoPwm <= -1.0):
                        armServoPwm = -1.0
                    elif (armServoPwm >= 1.0):
                        armServoPwm = 1.0
                else:
                    armServo.value = armServoPwm

            if(code == "ABS_RX"):
                print("claw moving")
                time.sleep(0.01)
                if(mapY(value) > 1600):
                    clawServoPwm -= clawSpeed
                    print("claw down")
                elif(mapY(value) < 1400):
                    clawServoPwm += clawSpeed
                    print("claw up")
                if (clawServoPwm <= -1.0 or clawServoPwm >= 1.0):
                    print("over servo limit")
                    if (clawServoPwm <= -1.0):
                        clawServoPwm = -1.0
                    elif (clawServoPwm >= 1.0):
                        clawServoPwm = 1.0
                else:
                    clawServo.value = clawServoPwm

            if(code=="BTN_NORTH" and state==1):
                if(gripState):
                    gripServo.min()
                    gripState=0
                else:
                    gripServo.max()
                    gripState=1

            if(code == "BTN_SOUTH" and state == 1):
                print("mode switched")
                MODE = (MODE + 1) % 3
            elif (MODE == 0):
                if(code == "ABS_Y"):
                    print("move forward/backward")
                    pwmPulse = (mapY(int(state)))
                    print(pwmPulse)
                    if(pwmPulse<1550 and pwmPulse>1450):
                        pwmPulse=1500
                    pi.set_servo_pulsewidth(BackLeft, pwmPulse)
                    pi.set_servo_pulsewidth(BackRight, pwmPulse)
                    pi.set_servo_pulsewidth(FrontLeft, 3000-pwmPulse)
                    pi.set_servo_pulsewidth(FrontRight, 3000-pwmPulse)
            elif (MODE == 1):
                if(code == "ABS_X"):
                    print("move left/right")
                    pwmPulse = (mapX(int(state)))
                    if(pwmPulse<1550 and pwmPulse>1450):
                        pwmPulse=1500
                    pi.set_servo_pulsewidth(BackLeft, 3000-pwmPulse)
                    pi.set_servo_pulsewidth(BackRight, pwmPulse)
                    pi.set_servo_pulsewidth(FrontLeft, 3000-pwmPulse)
                    pi.set_servo_pulsewidth(FrontRight, pwmPulse)
            elif (MODE == 2):
                if(code == "ABS_X"):
                    print("turn counterclockwise/clockwise")
                    pwmPulse = (mapX(int(state)))
                    if(pwmPulse<1550 and pwmPulse>1450):
                        pwmPulse=1500
                    pi.set_servo_pulsewidth(BackLeft, pwmPulse)
                    pi.set_servo_pulsewidth(BackRight, 3000-pwmPulse)
                    pi.set_servo_pulsewidth(FrontLeft, 3000-pwmPulse)
                    pi.set_servo_pulsewidth(FrontRight, pwmPulse)
            else:
                pass

            if(code == "ABS_RZ"):
                print("move down!")
                pwmPulse = (mapLeftTrigger(int(state)))
                print(pwmPulse)
                if(pwmPulse>1450):
                    pwmPulse=1500
                pi.set_servo_pulsewidth(Top, pwmPulse)
                pi.set_servo_pulsewidth(Bottom, pwmPulse)

            if(code == "ABS_Z"):
                print("move up!")
                pwmPulse = (mapRightTrigger(int(state)))
                print(pwmPulse)
                if(pwmPulse<1550):
                    pwmPulse=1500
                pi.set_servo_pulsewidth(Top, pwmPulse)
                pi.set_servo_pulsewidth(Bottom, pwmPulse)
        else:
            pass

except KeyboardInterrupt:
    print("exited")
    s.close()
    print("closed udp")
    stopSignal()
    print("stop signal complete")
