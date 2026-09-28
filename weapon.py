import pygame
from support import import_folder

class Gun:
    pass
class Bullet(pygame.sprite.Sprite):
    def __init__(self, posX, posY, direction, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.import_sprite()
        self.speed = 20

        # bullet props
        # self.damage = damage
        self.bullet_duration = 1000
        self.bullet_fired = pygame.time.get_ticks()
        
        # bullet pos
        self.pos = pygame.math.Vector2(posX, posY)
        self.direction = direction

        if self.direction < 0:
            image = self.bullet_sprite[1]
            flip_img = pygame.transform.flip(image, True, False)
            image = flip_img
        else:
            image = self.bullet_sprite[1]
        
        self.image = image
        self.rect = self.image.get_rect(center = (self.pos))
    
    def update(self):
        self.rect.x += self.speed * self.direction

        current_ticks = pygame.time.get_ticks()
        if current_ticks - self.bullet_fired >= self.bullet_duration:
            self.kill()

    def import_sprite(self):
        path = f'Assets/Bullets'
        self.bullet_sprite = import_folder(path)

