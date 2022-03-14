import pygame 
import os
cur_path = os.path.dirname(__file__)
source_path = os.path.join(cur_path, "images")
#___________________________________________________
class pyImgTxt(object):
    x = 0
    y = 0
    myfont = None
    text = None
    font_size = 15
    text_surf = None
    text_rect = None
    text_color = [255,255,255]
    screen = None
    img = None
    
    def __init__(self, text, pos, font_size, text_color, img, img_size, screen):
        self.x, self.y = pos
        self.font_size = font_size
        self.text = text
        self.text_color = text_color
        self.img = pygame.image.load(os.path.join(source_path, img))
        self.img  = pygame.transform.scale(self.img, (img_size[0],img_size[1]))

        self.screen = screen
        self.myfont = pygame.font.SysFont("arial",self.font_size, True, False)


    def draw(self):        
        self.rect = self.img.get_rect()
        self.rect.center = [self.x, self.y]
        self.screen.blit(self.img, self.rect)
        self.text_surf = self.myfont.render(self.text, True, self.text_color)
        self.font_rect = self.text_surf.get_rect()
        self.font_rect.center = [self.x, self.y]
        self.screen.blit(self.text_surf, self.font_rect)

