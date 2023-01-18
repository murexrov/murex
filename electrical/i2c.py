import board
from board import SCL, SDA
import busio

#pca9685
import adafruit_pca9685
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import adafruit_motor.servo
servo = adafruit_motor.servo.Servo(servo_channel)

i2c_bus = busio.I2C(SCL, SDA)

pca = PCA9685(i2c_bus)
pca.frequency = 50

for i in range(16):
    kit.servo[i].set_pulse_width(1500)

