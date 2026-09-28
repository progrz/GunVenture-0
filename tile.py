import pygame
from support import import_cut_graphics

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_index):
        super().__init__(groups)
        self.import_sprite()
        self.image = self.tile_sprite[tile_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.display_surface = pygame.display.get_surface()
    
    def update(self):
        pass
    
    def import_sprite(self):
        self.tile_sprite = import_cut_graphics('Assets/terrain/terrain_tiles.png')

    # def update(self, ref_point):
    #     point = ref_point
    #     offset = pygame.math.Vector2(0, 0)
    #     offset.x = point.rect.centerx - self.display_surface.get_width()//2
    #     self.rect.topleft += offset

class backTile:
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.speed = 16
        pass

    def update(self):
        self.rect.x += self.speed

class ConstraintTile(pygame.sprite.Sprite):
    def __init__(self, size, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)
    
    def update(self):
        pass

class Crate(pygame.sprite.Sprite):
    def __init__(self, size, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("Assets/terrain/crate.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.rect.y += size - self.image.get_size()[1]