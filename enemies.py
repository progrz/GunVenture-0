from support import import_folder
from settings import TILE_SIZE
from random import randint
import os
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        # enemy
        self.import_sprite()
        self.frameIndex = 0
        self.frameSpeed = 0.15
        self.image = self.enemy_sprites['run'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        self.rect.y += TILE_SIZE - self.image.get_size()[1]
        self.speed = randint(3,5)

    def import_sprite(self):
        self.enemy_sprites = {'run': []}

        for enemy_state in self.enemy_sprites.keys():    
            path = f'Assets/Enemies/Enemy/{enemy_state}'
            self.enemy_sprites[enemy_state] = import_folder(path)
    
    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)
    
    def animate(self):
        self.frameIndex += self.frameSpeed
        animation = self.enemy_sprites['run']

        if self.frameIndex > len(animation):
            self.frameIndex = 0
        
        image = animation[int(self.frameIndex)]
        # if self.isFacingRight:
        self.image = image
        # else :
        #     flip_img = pygame.transform.flip(image, True, False)
        #     self.image = flip_img

    def reverse(self):
        self.speed *= -1

    def update(self):
        self.animate()
        self.move()
        self.reverse_image()