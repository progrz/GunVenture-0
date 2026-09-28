import pygame
from support import draw_text

class UI:
    def __init__(self, surface):
        self.display_surface = surface
        
        self.lives_indicator = pygame.image.load('Assets/head.png').convert_alpha()

        self.ammo_indicator = pygame.image.load('Assets/Bullets/1.png').convert_alpha()
        self.ammo_indicator = pygame.transform.rotate(self.ammo_indicator, 90)

    def show_lives(self):
        self.display_surface.blit(self.lives_indicator, (20,20))
        draw_text(str(self.lives_number), 40, 80, 20)

    def show_ammo(self):
        self.display_surface.blit(self.ammo_indicator, (35,70))
        draw_text(str(self.ammo_number), 40, 80, 70)

    def set_ammo(self, ammo):
        self.ammo_number = ammo

    def set_lives(self, lives):
        self.lives_number = lives