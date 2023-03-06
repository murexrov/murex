import asyncio
import json
import random
import threading
import time
import websockets
import os

CONNECTIONS = set()

n = 0

async def register(websocket):
    CONNECTIONS.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        CONNECTIONS.remove(websocket)

async def echo():
    global n
    while True:
        websockets.broadcast(CONNECTIONS, str(n))
        await asyncio.sleep(1)

async def main():
    async with websockets.serve(register, "localhost", 5678):
        await echo()


def infiniteloop2():
    global n
    n = 0
    while True:
        print(n)
        n += 1
        time.sleep(1)

thread1 = threading.Thread(target=asyncio.run, args=(main(),))
thread1.start()

thread2 = threading.Thread(target=infiniteloop2)
thread2.start()

thread1.join()
thread2.join()

camera_servo_angle = 0

neopixel_r, neopixel_g, neopixel_b = 255, 255, 255

thruster_fr = None
thruster_fl = None
thruster_br = None
thruster_bl = None
thruster_v1 = None
thruster_v2 = None
bldc_0 = None
bldc_1 = None
bldc_2 = None
bldc_3 = None
bme680_temperature = None
bme680_gas = None
bme680_humidity = None
bme680_pressure = None
bme680_altitude = None


output_dictionary = {
    "thruster": {
        "fr": thruster_fr,
        "fl": thruster_fl,
        "br": thruster_br,
        "bl": thruster_bl,
        "v1": thruster_v1,
        "v2": thruster_v2,
    },
    "arm": {
        "bldc_0": bldc_0,
        "bldc_1": bldc_1,
        "bldc_2": bldc_2,
        "bldc_3": bldc_3,
    },
    "bme680": {
        "temperature": bme680_temperature,
        "gas": bme680_gas,
        "humidity": bme680_humidity,
        "pressure": bme680_pressure,
        "altitude": bme680_altitude,
    },
    "joystick": {
        "joystick_left": "",
        "joystick_right": "",
        "button_y": "",
        "button_x": "",
        "button_b": "",
        "button_a": "",
        "button_joystick_left": "",
        "button_joystick_right": "",
        "button_menu": "",
        "button_window": "",
        "button_xbox_logo": "",
        "d_pad": "",
        "trigger_right": "",
        "trigger_left": "",
        "bumper_right": "",
        "bumper_left": "",
    },
    "neopixel": {
        "red": neopixel_r,
        "green": neopixel_g,
        "blue": neopixel_b,
    },
    "camera_angle": camera_servo_angle,
}
