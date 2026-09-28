import pygame, sys, math
from settings import *

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

CENTER = (300, 300) # x, y
RADIUS = 100 # r

satelliteCenter = (CENTER[0]+RADIUS, CENTER[1])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse = pygame.mouse.get_pos()
    vector = (mouse[0]-CENTER[0], mouse[1]-CENTER[1])
    distance = (vector[0]**2 + vector[1]**2)**0.5

    if distance > 0:
        scalar = RADIUS / distance
        satelliteCenter = (
        int(round( CENTER[0] + vector[0]*scalar )),
        int(round( CENTER[1] + vector[1]*scalar )) )

    screen.fill((152,206,231))
    pygame.draw.circle(screen, (71,153,192), CENTER, RADIUS)
    pygame.draw.circle(screen, (243,79,79), satelliteCenter, 16)

    pygame.display.update()
    clock.tick(60)