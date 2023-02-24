import pigpio
from numpy import interp
import socket
import time

cw_pin = 7
fl_pin = 11
fr_pin = 13
bl_pin = 29
br_pin = 31
top_pin = 26
bottom_pin = 28
cam_pin = 8
arm_pin = 33
claw_pin = 35
grip_pin = 36
gnd_pin = 34
cam_pwm = 0

def reset():
    pi.set_servo_pulsewidth(fl_pin, 1500)
    pi.set_servo_pulsewidth(fr_pin, 1500)
    pi.set_servo_pulsewidth(bl_pin, 1500)
    pi.set_servo_pulsewidth(br_pin, 1500)
    pi.set_servo_pulsewidth(top_pin, 1500)
    pi.set_servo_pulsewidth(bottom_pin, 1500)
    pi.set_servo_pulsewidth(cam_pin, 1500)
    pi.set_servo_pulsewodth(arm_pin, 1500)
    pi.set_servo_pulsewidth(claw_pin, 1500)
    pi.set_servo_pulsewidth(grip_pin, 1500)
    
pi = pigpio.pi()
ip = "192.168.100.1"
port = int(1234)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
reset()
server.bind((ip, port))

def receive():
    message, addr = server.recvfrom(1024)
    received = message.decode('utf-8')
    server.sendto(message.encode('utf-8'), addr)
    return received
def gamepadMap(x):
    x = x.split()
    if x[0] == 'SYN_REPORT':
        return 'SYN_REPORT'
    return x
def mapX(x):
    return int(interp(x, [-32768, 32767], [1100, 1900]))
def mapY(x):
    return int(interp(x, [-32768, 32767], [1900, 1100]))
def mapLeftTrigger(x):
    return int(interp(x, [0, 1023], [1500, 1100]))
def mapRightTrigger(x):
    return int(interp(x, [0, 1023], [1500, 1900]))

try:
    while True:
        inp = gamepadMap(receive())
        if inp != 'SYN_REPORT':
            code = inp[0]
            state = inp[1]
            if code == 'ABS_HAT0Y':
                #camera pwm
                time.sleep(0.01)
                if state == 1:
                    cam_pwm -= 0.1
                elif state == -1:
                    cam_pwm += 0.1
                if cam_pwm <= -1.0:
                    cam_pwm = -1.0
                elif cam_pwm >= 1.0:
                    cam_pwm = 1.0
                else:
                    pi.set_servo_pulsewidth(cam_pwm)
            elif code == 'ABS_RY':
                time.sleep(0.01)
                
except KeyboardInterrupt:
    server.close()
    reset()