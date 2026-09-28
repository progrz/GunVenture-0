import pygame
from settings import *
from support import import_folder
from random import choice, randint

class Sky:
	def __init__(self,horizon):
		self.top = pygame.image.load('Assets/Decoration/Sky/sky_top.png').convert()
		self.bottom = pygame.image.load('Assets/Decoration/Sky/sky_bottom.png').convert()
		self.middle = pygame.image.load('Assets/Decoration/Sky/sky_middle.png').convert()
		self.horizon = horizon

		# stretch 
		self.top = pygame.transform.scale(self.top,(SCREEN_WIDTH,TILE_SIZE))
		self.bottom = pygame.transform.scale(self.bottom,(SCREEN_WIDTH,TILE_SIZE))
		self.middle = pygame.transform.scale(self.middle,(SCREEN_WIDTH,TILE_SIZE))

	def draw(self,surface):
		for row in range(VERTICAL_HEIGHT):
			y = row * TILE_SIZE
			if row < self.horizon:
				surface.blit(self.top,(0,y))
			elif row == self.horizon:
				surface.blit(self.middle,(0,y))
			else:
				surface.blit(self.bottom,(0,y))
