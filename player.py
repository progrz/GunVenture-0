import pygame
from support import import_folder
from settings import *
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # player
        self.import_sprite()
        self.frameIndex = 0
        self.frameSpeed = 0.15
        self.image = self.player_sprites['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)

        # state
        self.state = 'idle'
        self.isFacingRight = True
        self.isOnGround = False

        # move
        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.gravity = 0.98
        self.jumpForce = 16

        # atribut
        self.lives = 3
        self.invincible = False
        self.invincible_duration = 500
        self.hurt_ticks = 0

        # collision
        # self.collision_sprite = collision_sprite

    def import_sprite(self):
        # self.player_sprites = {'idle': [], 'run': [], 'jump':[], 'fall':[]}
        self.player_sprites = {'idle': [], 'run': [], 'jump':[]}

        for player_state in self.player_sprites.keys():    
            path = f'Assets/Player/{player_state}'
            self.player_sprites[player_state] = import_folder(path)
    
    def animate(self):
        self.frameIndex += self.frameSpeed
        animation = self.player_sprites[self.state]

        if self.frameIndex > len(animation):
            self.frameIndex = 0
        
        image = animation[int(self.frameIndex)]
        if self.isFacingRight:
            self.image = image
        else :
            flip_img = pygame.transform.flip(image, True, False)
            self.image = flip_img

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] :
            self.direction.x = 1
            self.isFacingRight = True
        elif keys[pygame.K_a] :
            self.direction.x = -1
            self.isFacingRight = False
        else :
            self.direction.x = 0
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.isOnGround == True:
            self.isOnGround = False
            self.direction.y = -self.jumpForce
    
    def downForce(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def setgetState(self):
        if self.direction.y < 0:
            self.state = 'jump'
        elif self.direction.y > 1:
            self.state = 'idle'         # harusnya 'fall' tapi malas bikin sprite lagi.
        else :
            if self.direction.x != 0:
                self.state = 'run'
            else:
                self.state = 'idle'

        return self.state
    
    def get_damage(self):
        if not self.invincible:
            self.invincible = True
            self.lives -= 1
            self.hurt_ticks = pygame.time.get_ticks()
    
    def invincibility_timer(self):
        if self.invincible:
            current_ticks = pygame.time.get_ticks()
            if current_ticks - self.hurt_ticks >= self.invincible_duration:
                self.invincible = False
    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0
    
    def update(self):
        self.input()
        self.setgetState()
        self.invincibility_timer()
        self.animate()
        # print(self.direction)