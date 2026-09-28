import pygame
from settings import *
from support import import_csv_layout, setClick, getClick, setState, draw_title
from tile import *
from player import Player
from enemies import *
from weapon import *
from decoration import *
from level_data import levels
from ui import UI

class Level:
    def __init__(self, surface, selected_level, create_levelSelect):
        self.display_surface = surface
        self.selected_level = selected_level
        self.create_levelSelect = create_levelSelect
        level_data = levels[selected_level]
        level_content = level_data['content']
        self.new_max = level_data['unlock']

        # self.visible_sprite = CameraGroup() #sprite static
        # self.active_sprite = pygame.sprite.Group() #sprite yang harus selalu di-update
        # self.collision_sprite = pygame.sprite.Group() #sprite collider

        self.terrain_sprite = pygame.sprite.Group()      # menyimpan terrain
        self.crate_sprite = pygame.sprite.Group()        # menyimpan crate
        self.camera = CameraGroup()                      # semua yang tersimpan diperlihatkan ke layar
        self.player_sprite = pygame.sprite.GroupSingle() # sprite player
        self.constraint_sprite = pygame.sprite.Group()   # sprite constraint
        self.enemies_sprite = pygame.sprite.Group()      # sprite musuh
        self.bullets_sprite = pygame.sprite.Group()      # sprite bullets

        setClick(False)
        self.running = True
        self.spaced = False

        # terrain
        self.setupLevel(level_content, "terrain")
        # constraints
        self.setupLevel(level_content, "constraints")
        # crates
        self.setupLevel(level_content, "crate")
        # enemies
        self.setupLevel(level_content, "enemies")
        # player
        self.setupLevel(level_content, "player")

        self.ammo = 6

        # bg sprite
        self.sky = Sky(7)

    def setupLevel(self, level, type):
        path = f'levels/{level}/_{type}.csv'
        tiles = import_csv_layout(path)

        for row_index, row in enumerate(tiles):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if col != '-1' :
                    if type == 'terrain':
                        Tile((x, y), [self.terrain_sprite, self.camera], int(col))
                    if type == 'constraints':
                        ConstraintTile(TILE_SIZE, (x,y) , [self.constraint_sprite])
                    if type == 'crate':
                        Crate(TILE_SIZE, (x,y) , [self.crate_sprite, self.camera])
                    if type == 'player':
                        self.start_pos = pygame.math.Vector2(x, y)
                        self.player = Player((x,y), [self.player_sprite, self.camera])
                    if type == 'enemies':
                        self.enemy = Enemy((x,y), [self.enemies_sprite, self.camera])
    
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_BACKSPACE] and self.running:
            setState("select")
        if keys[pygame.K_BACKSLASH] and self.running:
            self.create_levelSelect(self.selected_level, self.new_max, True)
        if keys[pygame.K_SPACE] and not self.running:
            self.spaced = True
        
        click = getClick()
        if click and self.ammo > 0 and self.running:
            self.create_bullet()
    
    def borderCheck(self):
        if self.player.rect.centery > SCREEN_HEIGHT:
            self.player.rect.topleft = self.start_pos
            self.player.lives -= 1
    
    def check_cleared(self):
        if self.player.lives < 1:
            self.running = False
            self.isCleared = False
        else:
            if len(self.enemies_sprite) == 0:
                self.running = False
                self.isCleared = True
    
    def level_check(self):
        x = SCREEN_WIDTH
        y = SCREEN_HEIGHT
        bg = pygame.Surface((x, y), pygame.SRCALPHA)
        bg.fill((35,46,64, 80))
        self.display_surface.blit(bg, (0, 0))

        if self.isCleared:
            text = "STAGE CLEARED"
        else:
            text = "GAME OVER"
        
        if self.ammo == 0:
            cause = "OUT OF AMMO"
        elif self.player.lives == 0:
            cause = "NO MORE LIVES"
        else:
            cause = ""

        draw_title(text, 90, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 2)
        draw_title(cause, 30, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 90)
        draw_title("PRESS SPACE TO CONTINUE", 20, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 200)
        if self.spaced:
            self.create_levelSelect(self.selected_level, self.new_max, self.isCleared)

    def toUI(self):
        self.camera.dataUI(self.ammo, self.player.lives)
    
    def run(self):
        self.check_cleared()
        self.borderCheck()
        self.input()

        if self.running:
            # data ke UI
            self.toUI()

            # level tiles and player update
            self.sky.draw(self.display_surface)
            self.enemies_sprite.update()
            self.player_sprite.update()
            self.bullets_sprite.update()
            self.camera.draw(self.player)

            # collision
            self.horizontal_collision()
            self.vertical_collision()
            self.enemy_collision_reverse()
            self.bullet_collision()
            self.enemy_player_collision()
        
        else:
            self.level_check()

    # collision
    def horizontal_collision(self):
        # move
        self.player.rect.x += self.player.direction.x * self.player.speed
        collideable = self.terrain_sprite.sprites() + self.crate_sprite.sprites()

        for tile in collideable:
            # horizontal
            if tile.rect.colliderect(self.player.rect):
                if self.player.direction.x < 0 :
                    self.player.rect.left = tile.rect.right
                if self.player.direction.x > 0 :
                    self.player.rect.right = tile.rect.left

    def vertical_collision(self):
        # move
        self.player.downForce()
        collideable = self.terrain_sprite.sprites() + self.crate_sprite.sprites()

        for tile in collideable:
            # vertical
            if tile.rect.colliderect(self.player.rect):
                if self.player.direction.y < 0 :
                    self.player.direction.y = 0
                    self.player.rect.top = tile.rect.bottom
                if self.player.direction.y > 0 :
                    self.player.rect.bottom = tile.rect.top
                    self.player.direction.y = 0
                    self.player.isOnGround = True
        
        # anti mid-air jump
        if self.player.isOnGround and self.player.direction.y != 0 :
            self.player.isOnGround = False
            # pass

    def create_bullet(self):
        ref_point = self.player
        if ref_point.isFacingRight:
            posX = ref_point.rect.right
            direction = 1
        else:
            posX = ref_point.rect.left
            direction = -1
        posY = ref_point.rect.centery
        Bullet(posX, posY, direction, [self.camera, self.bullets_sprite])
        self.ammo -= 1
        setClick(False)

    def bullet_collision(self):
        collideable = self.terrain_sprite.sprites() + self.crate_sprite.sprites() + self.enemies_sprite.sprites()

        for bullet in self.bullets_sprite.sprites():
            for enemy in self.enemies_sprite.sprites():
                if pygame.sprite.spritecollide(enemy, self.bullets_sprite, False):
                    enemy.kill()
                    ammo = randint(0, 1)
                    if self.ammo + ammo > 6:
                        self.ammo = 6
                    else:
                        self.ammo += ammo
            if pygame.sprite.spritecollide(bullet, collideable, False):
                bullet.kill()
        # bullet penghancur massal
        # for bullet in self.bullets_sprite.sprites():
        #     pygame.sprite.spritecollide(bullet, (self.terrain_sprite), True)

    def enemy_collision_reverse(self):
        for enemy in self.enemies_sprite.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprite, False):
                enemy.reverse()
    
    def enemy_player_collision(self):
        for enemy in self.enemies_sprite.sprites():
            if enemy.rect.colliderect(self.player.rect):
                self.player.get_damage()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # ui
        self.ui = UI(self.display_surface)

        # camera setup
        self.offset = pygame.math.Vector2()

        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def draw(self, player):
        
        # ui
        self.ui.show_lives()
        self.ui.show_ammo()

        self.offset.x = player.rect.centerx - self.half_w
        # self.offset.y = player.rect.centery - self.half_h
        self.offset.y = 0

        for sprite in self.sprites():
            off_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, off_pos)
            
            # center of player
            # pew pew mutar mutar, malas.
            # if hasattr(sprite, 'speed'):
            #     precise = pygame.math.Vector2()
            #     precise.x = sprite.image.get_width() + 15
            #     precise.y = sprite.image.get_height()/2

            #     center = off_pos + precise
            #     pygame.draw.circle(self.display_surface, (243,79,79), center, 8)
    
    def dataUI(self, ammo, lives):
        self.ui.set_ammo(ammo)
        self.ui.set_lives(lives)
