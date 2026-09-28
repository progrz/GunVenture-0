from support import *
import pygame

class Menu:
    def show(self):
        self.surface = pygame.display.get_surface()
        # title
        title_x = self.surface.get_width() / 2
        title_y = self.surface.get_height() / 4
        draw_title("GunVenture", 100, title_x, title_y, 2)
        
        # menu
        y_pos = self.surface.get_height() / 2
        self.playbtn = draw_text("Play", 100, 30, y_pos)
        self.tutobtn = draw_text("Tutorial", 100, 30, y_pos+100)
        self.credbtn = draw_text("Credits", 100, 30, y_pos+200)

        self.collisionCheck()
    
    def collisionCheck(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.playbtn.collidepoint(mouse_pos):
            self.background(self.playbtn)
            if getClick() == True:
                setState("select")
                setClick(False)
        if self.tutobtn.collidepoint(mouse_pos):
            self.background(self.tutobtn)
            if getClick() == True:
                setState("tutorial")
                setClick(False)
        if self.credbtn.collidepoint(mouse_pos):
            self.background(self.credbtn)
            if getClick() == True:
                setState("credit")
                setClick(False)
    
    def background(self, target):
        x = 2000
        y = target.height
        bg = pygame.Surface((x, y), pygame.SRCALPHA)
        bg.fill((35,46,64, 80))
        self.surface.blit(bg, (0, target.y))


class Credit:
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_BACKSPACE] :
            setState("Menu")

    def show(self):
        self.input()
        self.surface = pygame.display.get_surface()

        # title
        title_x = self.surface.get_width() / 2
        title_y = self.surface.get_height() / 10
        draw_title("CREDITS", 100, title_x, title_y)

        # team name
        x_pos = self.surface.get_width() / 2
        y_pos = self.surface.get_height() / 4
        draw_text1("192267", 40, x_pos - 110, y_pos)
        draw_text1("192271", 40, x_pos - 110, y_pos+100)
        draw_text1("192275", 40, x_pos - 110, y_pos+200)
        draw_text1("192282", 40, x_pos - 110, y_pos+300)
        draw_text1("192301", 40, x_pos - 110, y_pos+400)
        
        draw_text("Fadel Muhammad", 40, x_pos - 100, y_pos)
        draw_text("Dayu Purnama Salaki", 40, x_pos - 100, y_pos+100)
        draw_text("Ryan Agung Pramuditha", 40, x_pos - 100, y_pos+200)
        draw_text("Daan Pradana Riring", 40, x_pos - 100, y_pos+300)
        draw_text("Muh. Yusuf Zahir", 40, x_pos - 100, y_pos+400)

        # H-192267-Fadel Muhammad
        # H-192271-Dayu Purnama Salaki
        # H-192275-Ryan Agung Pramuditha
        # -192282-Daan Pradana Riring
        # G-192301-Muh. Yusuf Zahir