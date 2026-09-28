import pygame, sys
from settings import *
from support import setClick
from game import Game

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
title = pygame.display.set_caption("GunVenture")
Icon = pygame.image.load("pxArt.png")
pygame.display.set_icon(Icon)
clock = pygame.time.Clock()
game = Game(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                setClick(True)

    screen.fill(BG_COLOR)
    game.load()

    pygame.display.update()
    clock.tick(60)