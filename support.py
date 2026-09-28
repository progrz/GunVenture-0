from os import walk
from csv import reader
import pygame
from settings import *

def import_folder(path):
    sprite_list = []

    for _, __, img_file in walk(path):
        for img in img_file:
            f_path = f"{path}/{img}"
            load_img = pygame.image.load(f_path).convert_alpha()
            sprite_list.append(load_img)
    
    return sprite_list

# def import_folder1(path):

#     for _, files, __ in walk(path):
#         for file in files:
#             print(file)

def import_csv_layout(path):
	terrain_map = []
	with open(path) as map:
		level = reader(map,delimiter = ',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map

def import_cut_graphics(path):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
	tile_num_y = int(surface.get_size()[1] / TILE_SIZE)

	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * TILE_SIZE
			y = row * TILE_SIZE
			new_surf = pygame.Surface((TILE_SIZE,TILE_SIZE), flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0),pygame.Rect(x,y,TILE_SIZE,TILE_SIZE))
			cut_tiles.append(new_surf)

	return cut_tiles

CLICKED = False

def setClick(bool):
	global CLICKED 
	CLICKED = bool

def getClick():
	return CLICKED

STATE = "Menu"

def setState(bool):
	global STATE 
	STATE = bool

def getState():
	return STATE



type = ["editundo", "ka1", "light_pixel-7", "BACKTO1982", "Minecraftia", "pixelmix", "04B_30__"]
def draw_text(text, size, x, y, var=0):
	surface = pygame.display.get_surface()
	font = pygame.font.Font(f"Assets/Fonts/{type[var]}.ttf", size) # ka1 BACKTO1982 editundo
	text_display = font.render(text, 1, "#FFFFFF")
	text_rect = text_display.get_rect()
	text_rect.topleft = (x, y)
	surface.blit(text_display, text_rect)

	return text_rect

def draw_text1(text, size, x, y, var=0):
	surface = pygame.display.get_surface()
	font = pygame.font.Font(f"Assets/Fonts/{type[var]}.ttf", size) # ka1 BACKTO1982 editundo
	text_display = font.render(text, 1, "#FFFFFF")
	text_rect = text_display.get_rect()
	text_rect.topright = (x, y)
	surface.blit(text_display, text_rect)

	return text_display

def draw_title(text, size, x, y, var=0):
	surface = pygame.display.get_surface()
	font = pygame.font.Font(f"Assets/Fonts/{type[var]}.ttf", size) # ka1 BACKTO1982 editundo
	text_display = font.render(text, 1, "#FFFFFF")
	text_rect = text_display.get_rect()
	text_rect.center = (x, y)
	surface.blit(text_display, text_rect)

def draw_copyright(text, size, x, y, var=0):
	surface = pygame.display.get_surface()
	font = pygame.font.Font(f"Assets/Fonts/{type[var]}.ttf", size) # ka1 BACKTO1982 editundo
	text_display = font.render(text, 1, "#FFFFFF")
	text_rect = text_display.get_rect()
	text_rect.bottomright = (x, y)
	surface.blit(text_display, text_rect)

# import_folder('Assets/Player/particle/dust/run')
# import_folder1('Assets/Player')
# import_cut_graphics('Assets/terrain/terrain_tiles.png')
