import pygame 
#___________________________________________________
class Button(object):
    x = 0
    y = 0
    w = 125
    h = 50
    rect = None
    myfont = None
    text = None
    font_size = 15
    text_surf = None
    text_rect = None
    text_color = [255,255,255]
    button_color = [0,0,0]
    screen = None
    name = None

    def __init__(self, text, pos, size, font_size, text_color, button_color, screen, name):
        self.x, self.y = pos
        self.w, self.h = size
        self.font_size = font_size
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.screen = screen
        self.name = name

        self.rect = pygame.draw.rect(self.screen, self.button_color, [self.x,self.y,self.w,self.h],5)
        self.myfont = pygame.font.SysFont("arial",self.font_size, True, False)
        self.text_surf = self.myfont.render(self.text, True, self.text_color)
        self.font_rect = self.text_surf.get_rect()
        self.font_rect.center = self.rect.center

    def draw(self):
        pygame.draw.rect(self.screen, self.button_color, [self.x,self.y,self.w,self.h])
        pygame.draw.rect(self.screen, [0,0,0], [self.x,self.y,self.w,self.h], 5)
        self.screen.blit(self.text_surf, self.font_rect)

    def check(self, event):
        mouse = pygame.mouse.get_pos()
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            pygame.draw.rect(self.screen, [120,120,120], [self.x,self.y,self.w,self.h])
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, [0,125,0], [self.x,self.y,self.w,self.h], 5)
                return self.name
        self.screen.blit(self.text_surf, self.font_rect)
        return None

