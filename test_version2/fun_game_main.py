from cmath import atan
from pickle import TRUE

from numpy import source
import pygame
import fun_pyMapeditor
import fun_pygameboard
import fun_pyMain_title
import os
#__________________________________________________
class title(object):

    def title_evetn(self, screen):    
        cur_path = os.path.dirname(__file__)
        source_path = os.path.join(cur_path, "images")
        screen.fill([0,0,0])
        img_main = pygame.image.load(os.path.join(source_path, "test.png"))
        img_main = pygame.transform.scale(img_main, (1250, 800))
        screen.blit(img_main, (0,0))
        pygame.time.wait(10000)

def main():
    pygame.init()
    pygame.font.init()
    screen_w = 1250
    screen_h = 800
    screen_window = pygame.display.set_mode((screen_w, screen_h))
    ESC = False
    chapter = "main_title"
    #___________________________________________________
    chapter = "main_title"
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    while ESC == False:
        if chapter == "main_title":
            main_menu = fun_pyMain_title.main_title(screen_window)
            chapter = main_menu.main_event()
        elif chapter == "map":
            editor = fun_pyMapeditor.map_editor([1050,800],50,screen_window)
            chapter = editor.edit_event()
            del editor
        elif chapter == "game":
            game = fun_pygameboard.game_mother_board([1050,800],"maps/Map.txt",screen_window)
            chapter = game.game_event()  
        elif chapter == "quit":
            break
    pygame.quit()

if __name__ == "__main__":
	main()  