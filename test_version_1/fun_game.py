from cmath import atan
from pickle import TRUE

from numpy import source
import pygame
import fun_pyscreen

#__________________________________________________
pygame.init()
pygame.font.init()
screen_w = 1200
screen_h = 600
screen_window = pygame.display.set_mode((screen_w, screen_h))
FPS = 60
ESC = False
clock = pygame.time.Clock()
chapter = "main_title"
screen_1 = fun_pyscreen.main_title(screen_window)
screen_2 = fun_pyscreen.main_menu(screen_window)
screen_3 = fun_pyscreen.game_menu(screen_window)
screen_4 = fun_pyscreen.map_menu(screen_window,[1000, 600])
screen_5 = fun_pyscreen.shop_menu(screen_window)
#___________________________________________________
chapter = "main_title"

while ESC == False:
    event = pygame.event.poll()
    if chapter == "main_title":
        screen_1.display()
        chapter = screen_1.key_handler(event)
    elif chapter == "main_menu":
        screen_2.display()
        chapter = screen_2.key_handler(event)
    elif chapter == "game_menu":
        screen_3.display()
        chapter = screen_3.key_handler(event)
    elif chapter == "map_menu":
        screen_4.display()
        chapter = screen_4.key_handler(event)    
    elif chapter == "shop_menu":
        screen_5.display()
        chapter = screen_5.key_handler(event)   
    elif chapter == "reset":
        print("RESET")
        screen_1.__init__(screen_window)
        screen_2.__init__(screen_window)
        screen_3.__init__(screen_window)
        screen_4.__init__(screen_window,[1000,600])
        screen_5.__init__(screen_window)
        chapter = "main_menu" 
    elif chapter == "quit":
        pygame.quit()
        break
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()