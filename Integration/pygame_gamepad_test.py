import pygame

pygame.joystick.init()

xbox = pygame.joystick

while True:
    print(xbox.Joystick(0).get_axis(0))