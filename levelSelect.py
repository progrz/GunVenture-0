from support import *
from level_data import levels
import pygame

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, index, status, groups, icon_speed):
        super().__init__(groups)
        self.image = pygame.image.load('Assets/terrain/terrain_select.png').convert_alpha()
        if status == 'unlocked':
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(70)
        self.rect = self.image.get_rect(center=pos)

        self.level_index = index
        self.pos = pos

        # self.detect_zone = pygame.Rect(self.rect.centerx - icon_speed/2, self.rect.centery - icon_speed/2, icon_speed, icon_speed)
        self.detect_zone = pygame.Rect(self.rect.centerx, self.rect.centery, 1, 1)

    def draw_level_num(self):
        x = self.pos[0]
        y = self.pos[1] - self.image.get_size()[1] / 2 - 30
        text = "Stage " + self.level_index
        draw_title(text, 40, x, y, 0)

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.pos = pos
        self.image = pygame.image.load('Assets/head.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def update(self):
        self.rect.center = self.pos

class LevelSelect:
    def __init__(self, start_level, max_level, surface, create_level):
        self.surface = surface
        self.current_level = start_level - 1
        self.max_level = max_level
        self.create_level = create_level

        self.moving = False
        self.move_direction = pygame.math.Vector2(0,0)
        self.speed = 8

        self.setupNode()
        self.setupIcon()

    def setupNode(self):
        self.nodes = pygame.sprite.Group()

        for index, node_data in enumerate(levels.values()):
            if index < self.max_level:
                Node(node_data['pos'], node_data['content'], 'unlocked', self.nodes, self.speed)
            else:
                Node(node_data['pos'], node_data['content'], 'locked', self.nodes, self.speed)
    
    def setupIcon(self):
        self.icon = pygame.sprite.GroupSingle()
        Icon(self.nodes.sprites()[self.current_level].rect.center, self.icon)
    
    def updateIcon(self):
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.move_direction * self.speed
            target = self.nodes.sprites()[self.current_level]
            if target.detect_zone.colliderect(self.icon.sprite.rect):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0,0)
                self.icon.sprite.pos = target.pos

    def draw_path(self):
        pos = [node['pos'] for index, node in enumerate(levels.values()) if index < self.max_level]
        if pos.__len__() > 1:
            pygame.draw.lines(self.surface, '#9BABD7', False, pos, 10)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_d] and self.current_level + 1 < self.max_level:
                self.move_direction = self.get_movement("next")
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_a] and self.current_level > 0:
                self.move_direction = self.get_movement("back")
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_s]:
                self.create_level(self.current_level+1)
            
            elif keys[pygame.K_BACKSPACE]:
                setState("Menu")
    
    def get_movement(self, direction):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if direction == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)
        return (end - start).normalize()
    
    def nodes_num_draw(self):
        for node in self.nodes.sprites():
            node.draw_level_num()

    def show(self):
        self.input()
        self.updateIcon()
        self.icon.update()
        
        draw_title("STAGE SELECT", 60, 600, 40)
        draw_title("Press S to Select", 20, 600, SCREEN_HEIGHT - 50)
        self.draw_path()
        self.nodes.draw(self.surface)
        self.nodes_num_draw()
        self.icon.draw(self.surface)
