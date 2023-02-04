# update rpi and python, install blinka:
# https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

# installations for rpi:
# 1. PCA9685 Driver: https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
# 2. BNO055 IMU: https://github.com/adafruit/Adafruit_CircuitPython_BNO055
# 3. BME680 Sensor: https://github.com/adafruit/Adafruit_CircuitPython_BME680

# run these commands after installations:
# sudo pip3 install adafruit-circuitpython-pca9685
# sudo pip3 install adafruit-circuitpython-servokit
# sudo pip3 install adafruit-circuitpython-bno055
# sudo pip3 install adafruit-circuitpython-bme680

import time
import board
from board import SCL, SDA
import busio

import adafruit_pca9685
from adafruit_pca9685 import PCA9685
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
import adafruit_motor.servo
import adafruit_bno055
import adafruit_bme680

# PCA9685 Driver
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

# Example: stop signals for all thrusters connected to pwm channels
for i in range(16):
    kit.servo[i].set_pulse_width(1500) # "i" refers to the channel on PCA9685

# BNO055 IMU
i2c = board.I2C(SCL, SDA)
bno055 = adafruit_bno055.BNO055_I2C(i2c)

last_val = 0xFFFF

def temperature():
    global last_val  # if using pylint disable global statement
    result = bno055.temperature
    if abs(result - last_val) == 128:
        result = bno055.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result

# example access of sensor values + units
print("Temperature: {} degrees C".format(bno055.temperature))
print("Accelerometer (m/s^2): {}".format(bno055.acceleration))
print("Magnetometer (microteslas): {}".format(bno055.magnetic))
print("Gyroscope (rad/sec): {}".format(bno055.gyro))
print("Euler angle: {}".format(bno055.euler))
print("Quaternion: {}".format(bno055.quaternion))
print("Linear acceleration (m/s^2): {}".format(bno055.linear_acceleration))
print("Gravity (m/s^2): {}".format(bno055.gravity))

#BME680 Temp, Humidity, Pressure Sensor
i2c = board.I2C(SCL, SDA)
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

#this temperature sensor is kinda goofy so it's good we have 2 temp sensors that we can use to cross check and calibrate
temperature_offset = -5

# example access of sensor values + units
print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
print("Gas: %d ohm" % bme680.gas)
print("Humidity: %0.1f %%" % bme680.relative_humidity)
print("Pressure: %0.3f hPa" % bme680.pressure)
print("Altitude = %0.2f meters" % bme680.altitude)
