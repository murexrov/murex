import os
import time
import busio
import board
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import adafruit_bme680
import neopixel
import socket
import sys

ip = "192.168.100.1"
port = int(6666)

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
print("connection established to rpi")

i2c, pca, thrusters = None
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
thrusters = [servo.Servo(pca.channels[i] for i in range(5))]
pca.frequency = 50

# @TODO: verify which channels are which motor/thruster
arm_bldcs = [servo.Servo(pca.channels[i] for i in range(6, 9))]

bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
bme680.sea_level_pressure = 1013.25
bme680_temperature_offset = -5

pixel_pin = board.D18
num_pixels = 1
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

# @TODO: verify thresholds for camera servo
camera_servo_angle = 0
camera_servo = servo.Servo(pca.channels[10])

# Thruster Fraction Range: -1 (-max [1100]), 0 (neutral [1500]), 1 (max [1900])
def set_thrusters(a, b, c, d, e, f):
    speeds = [a, b, c, d, e, f]
    for i in range(5):

        if speeds[i] <= -1:
            speeds[i] = -1
        elif speeds[i] >= 1:
            speeds[i] = 1

        # SPEED/2 + 0.5 is used to translate fraction from -1 <-> 1
        fractional_speed = (speeds[i] / 2) + 0.5
        thrusters[i].fraction(fractional_speed)

# Initialize thrusters by setting to neutral (1500), then waiting for 7 seconds
def init_thrusters():
    for i in range(5):
        thrusters[i].set_pulse_width_range(1100, 1900)
        thrusters[i].fraction(0.5)

    time.sleep(7)

def gamepad_stream_in():
    data, address = s.recvfrom(4096)
    received = data.decode('utf-8')
    send_data = "received: " + received
    s.sendto(send_data.encode('utf-8'), address)
    return(received)

def gamepad_map(x):
    x = x.split()
    if (x[0] == 'SYN_REPORT'):
        return ('SYN_REPORT')
    else:
        return (x)

def gamepad_map_joystick(x):
    return int(interp(x, [-32768,32767], [-1,1]))

def gamepad_map_trigger(x):
    return int(interp(x, [0, 1023], [-1,1]))

def end():

    pca.deinit()
    s.close()
    camera_servo.angle(0)

    # running it again makes sure the motors stop
    init_thrusters()

def log_bme680(bme680, bme680_temperature_offset):
    print("\nTemperature: %0.1f C" % (bme680.temperature + bme680_temperature_offset))
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)

def set_left_joystick_position(gamepad_map_joystick, gamepad_hid_code, game_state, joystick_position_left):
    if (gamepad_hid_code == "ABS_Y"):
        interpolated_game_state = gamepad_map_joystick(game_state)
        joystick_position_left = [joystick_position_left[0], interpolated_game_state]

    if (gamepad_hid_code == "ABS_X"):
        interpolated_game_state = gamepad_map_joystick(game_state)
        joystick_position_left = [interpolated_game_state, joystick_position_left[1]]
    return joystick_position_left

def set_right_joystick_position(gamepad_map_joystick, gamepad_hid_code, game_state, joystick_position_right):
    if (gamepad_hid_code == "ABS_RY"):
        interpolated_game_state = gamepad_map_joystick(game_state)
        joystick_position_right = [joystick_position_right[0], interpolated_game_state]

    if (gamepad_hid_code == "ABS_RX"):
        interpolated_game_state = gamepad_map_joystick(game_state)
        joystick_position_right = [interpolated_game_state, joystick_position_right[1]]
    return joystick_position_right

def get_gamepad_input(gamepad_stream_in, gamepad_map):
    print(gamepad_map(gamepad_stream_in))
    gamepad_stream = gamepad_map(gamepad_stream_in)
    gamepad_hid_code = str(gamepad_stream[0])
    game_state = int(gamepad_stream[1])
    return gamepad_hid_code,game_state

def set_turning(joystick_position_right):
    if (joystick_position_right[0] > 0.2 or joystick_position_right[0] < -0.2):
        if (joystick_position_right[0] > 0):
            turn_right = joystick_position_right[0]
            turn_left = 0

        elif (joystick_position_right[0] < 0):
            turn_left = joystick_position_right[0]
            turn_right = 0
    return turn_right,turn_left

def rotate_camera(camera_servo_angle, camera_servo, gamepad_hid_code, game_state):
    if (gamepad_hid_code == "ABS_HAT0Y"):
        # time.sleep(0.01) # is this line necessary?
        if (game_state == 1):
            camera_servo_angle += 15

        elif(game_state == -1):
            camera_servo_angle -= 15

        if (not camera_servo_angle <= 180 and not camera_servo_angle >= 0):
            camera_servo.angle(camera_servo_angle)

if __name__ == "__main__":
    try:
        os.system("ffmpeg -f v4l2 -i /dev/video0 -c:v h264_v4l2m2m -b:v 125000 -fflags nobuffer -flags low_delay -preset ultrafast -tune zerolatency -probesize 32 -num_output_buffers 32 -num_capture_buffers 16 -analyzeduration 0 -f mpegts udp://192.168.100.52:1234")

        print("begin video streaming")

        init_thrusters()

        joystick_position_left = [0, 0]
        joystick_position_right = [0, 0]

        # MAIN LOOP

        while True:

            log_bme680(bme680, bme680_temperature_offset)

            gamepad_hid_code, game_state = get_gamepad_input(gamepad_stream_in, gamepad_map)

            set_left_joystick_position(gamepad_hid_code, game_state, joystick_position_left)
            set_right_joystick_position(gamepad_hid_code, game_state, joystick_position_right)

            # Aidan's Thrust Vectoring Formula
            turn_right, turn_left = set_turning(joystick_position_right)

            thruster_fr = ((-joystick_position_left[1] + joystick_position_left[0]) / (2 ** 0.5)) + turn_left
            thruster_fl = ((joystick_position_left[1] + joystick_position_left[0]) / (2 ** 0.5)) + turn_right
            thruster_br = ((joystick_position_left[1] + joystick_position_left[0]) / (2 ** 0.5)) + -turn_left
            thruster_bl = ((-joystick_position_left[1] + joystick_position_left[0]) / (2 ** 0.5)) + -turn_right
            thruster_v1 = joystick_position_right[1]
            thruster_v2 = joystick_position_right[1]

            set_thrusters(thruster_fl, thruster_fr, thruster_bl, thruster_br, thruster_v1, thruster_v2)

            # @TODO: experimental support for arm motors
            # arm_bldcs[0] = claw
            # arm_bldcs[1] = servo
            # arm_bldcs[2] = turning 1
            # arm_bldcs[3] = turning 2

            rotate_camera(camera_servo_angle, camera_servo, gamepad_hid_code, game_state)

            # @TODO: host webserver with telemetry/diagnostic data?
            # @TODO: better debugging/logging potential

            # Change color of Neopixel
            pixels.fill((255, 255, 255))

    except KeyboardInterrupt:
        end()
        print("Program Ended")
