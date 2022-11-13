import pigpio
pi = pigpio.pi()
pi.set_servo_pulsewidth(26, 1500)
