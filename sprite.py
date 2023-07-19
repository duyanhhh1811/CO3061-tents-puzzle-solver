import pygame
from pygame.locals import *
from UIsetting import *

pygame.font.init()

class Title(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TITLESIZE, TITLESIZE), pygame.SRCALPHA)
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        
        self.draw_content()
        
    def draw_content(self):
        if self.text == "0":
            self.image.fill(CELL_COLOR)
        elif self.text == "1":
            self.image.fill(TREE_COLOR)
            image_ = pygame.image.load("images/tree.png").convert_alpha()
            image_scaled = pygame.transform.scale(image_, (TITLESIZE, TITLESIZE))
            self.image.blit(image_scaled, (0, 0))
        elif self.text == "2":
            self.image.fill(TENT_COLOR)
            image_ = pygame.image.load("images/tent.png").convert_alpha()
            image_scaled = pygame.transform.scale(image_, (TITLESIZE, TITLESIZE))
            self.image.blit(image_scaled, (0, 0))
        else:
            self.font = pygame.font.Font("blomberg-font/Blomberg-8MKKZ.otf", 35)
            font_surface = self.font.render(str(self.text), True, TEXT_COLOR)
            self.image.fill(CELL_COLOR)
            self.font_size = self.font.size(str(self.text))
            draw_x = (TITLESIZE / 2) - self.font_size[0] / 2
            draw_y = (TITLESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))

    
    def update(self):
        self.rect.x = self.x * TITLESIZE
        self.rect.y = self.y * TITLESIZE
    
    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
    
class UIElement:
    def __init__(self, x, y, text, text_color = F2A1C1):
        self.x = x
        self.y = y
        self.text = text
        self.text_color = text_color
        
    def draw(self, screen):
        font = pygame.font.Font("blomberg-font/Blomberg-8MKKZ.otf", 20)
        
        text = font.render(self.text, True, self.text_color)
        
        text_x = self.x
        text_y = self.y
        
        screen.blit(text, (text_x, text_y))
    
    def set_text_for_testcase(self, n):
        text = "Testcase #" + str(n)
        
        text_color = F291A3 + self.text_color[3:]
        
        self.text = text
        self.text_color = text_color
    
    def set_text_for_level(self, level):
        text = "Level: " + str(level)
        
        text_color = F291A3 + self.text_color[3:]
        
        self.text = text
        self.text_color = text_color

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.text = text
        self.text_color = text_color
        
    def draw(self, screen):
       # pygame.draw.rect(screen, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font("blomberg-font/Blomberg-8MKKZ.otf", 30)
        text = font.render(self.text, True, self.text_color)
        self.font_size = font.size(self.text)
        draw_x = self.x + (self.width / 2) - self.font_size[0] / 2
        draw_y = self.y + (self.height / 2) - self.font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))
    
    def click(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height