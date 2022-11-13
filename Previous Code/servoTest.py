from gpiozero import Servo
from numpy import interp
import time
from inputs import get_gamepad

servo = Servo(26)
pwm = -1

def map(x):
	return (interp(x, [-32767,32768], [-1,1]))

while 1:
	events = get_gamepad()
	for event in events:
		if event.code == "ABS_HAT0Y":
			time.sleep(0.01)
			value = event.state
			print(value, pwm)
			if value == 1:
				pwm -= 0.1
			elif value == -1:
				pwm += 0.1
			pwm = round(pwm, 1)
			if (pwm <= -1.0 or pwm >= 1.0):
				print("no")
				if (pwm <= -1.0):
					pwm = -1.0
				elif (pwm >= 1.0):
					pwm = 1.0
				break
			else:
				servo.value = pwm