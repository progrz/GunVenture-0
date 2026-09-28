from level import Level
from menu import *
from levelSelect import LevelSelect
from support import draw_copyright, SCREEN_HEIGHT, SCREEN_WIDTH, getState, setState

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.start_level = 1
        self.max_level = 1
        self.levelSelect = LevelSelect(self.start_level, self.max_level, self.screen, self.create_level)
        self.menu = Menu()
        self.credit = Credit()
        self.count = 0

    def create_level(self, selected_level):
        self.level = Level(self.screen, selected_level, self.create_levelSelect)
        setState("level")

    def create_levelSelect(self, current_level, new_max_level, cleared):
        if new_max_level > self.max_level and cleared:
            self.max_level = new_max_level
        if current_level - 1 == 0:
            current_level = 1
        self.levelSelect = LevelSelect(current_level, self.max_level, self.screen, self.create_level)
        setState("select")

    def load(self):
        if getState() == "select":
            self.levelSelect.show()
        elif getState() == "level":
            self.level.run()
        elif getState() == "tutorial":
            self.menu.show()
        elif getState() == "credit":
            self.credit.show()
        else:
            self.menu.show()

            draw_copyright("GunVenture dev v0.0.1", 15, SCREEN_WIDTH, SCREEN_HEIGHT-15, 5)
            draw_copyright("Copyright 2022 - 2023 | UNIVERSITAS DIPA MAKASSAR", 10, SCREEN_WIDTH, SCREEN_HEIGHT, 5)
