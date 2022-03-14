import pygame
import os
import fun_pyBtn
import fun_pygameboard
import fun_pyImgBtn
import fun_pyMap
import fun_pytxt
import numpy as np
import copy
#___________________________________________________
cur_path = os.path.dirname(__file__)
source_path = os.path.join(cur_path, "images")
#___________________________________________________
class main_title:
    img_main = None
    screen_window = None

    def __init__(self, screen):
        self.screen_window = screen
        img_main = pygame.image.load(os.path.join(source_path, "test.png"))
        img_main = pygame.transform.scale(img_main, (1200,600))
        self.img_main = img_main

    def display(self):    
        self.screen_window.blit(self.img_main, (0,0))
        
    def key_handler(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            print("move to main menu")
            return "main_menu"
        return "main_title"
#___________________________________________________
class main_menu:
    screen_window = None
    btn1 = None
    btn2 = None
    btn3 = None
    back_img = None
    def __init__(self, screen):
        self.screen_window = screen
        self.btn1 = fun_pyBtn.Button("GAME",[1000,0],[200,100],20,[0,0,0],[100,100,100], self.screen_window, "GAME")
        self.btn2 = fun_pyBtn.Button("SHOP",[1000,100],[200,100],20,[0,0,0],[100,100,100], self.screen_window, "SHOP")
        self.btn3 = fun_pyBtn.Button("MAP",[1000,200],[200,100],20,[0,0,0],[100,100,100], self.screen_window, "MAP")
        self.back_img = pygame.image.load(os.path.join(source_path, "main_menu.jpg"))
        self.back_img = pygame.transform.scale(self.back_img, (1000,600))

    def display(self):    
        self.screen_window.fill([255,255,255])
        self.screen_window.blit(self.back_img, (0,0))
        self.btn1.draw()
        self.btn2.draw()
        self.btn3.draw()

    def key_handler(self, event):    
        if self.btn1.check(event) is not None:
            print("moving to map view")
            return "game_menu"
        elif self.btn2.check(event)is not None:
            print("moving to shop view")
            return "shop_menu"
        elif self.btn3.check(event)is not None:
            print("moving to map view")
            return "map_menu"
        if event.type == pygame.QUIT:
            return "quit"
        return "main_menu"
#___________________________________________________
class game_menu:
    screen_window = None
    game1 = None
    tile_size = 50
    def __init__(self, screen):
        self.screen_window = screen
        self.game1 = fun_pygameboard.game_mother_board([1000,600],self.tile_size, screen)

    def display(self):    
        self.screen_window.fill([255,255,255])

    def key_handler(self,event):
        return self.game1.event(event)  
#___________________________________________________
class map_menu:
    screen_window = None
    icon_size = [50, 50]
    btn_list = []

    bucket = False
    back_img = None
    cur_mode = None
    map_size = None
    
    tile_map = []
    tile_map_size = []
    tile_size = 50
    tile_image = []
    tile_library = {"grass1" : 1, "dirt1" : 2, "ice1" : 3, "rock1" : 4}

    obj_map = []
    obj_map_size = []
    obj_image = []
    obj_library = {"tree1" : 1, "water1" : 2, "shovel" : 0}
    img_map = []
    img_map_size = []
    img_library = {1 : np.arange(1,17), 2 : np.arange(17,33)}
    enemy_map_size = []
    enenmy_map = []
    enemy_img = []
    enemy_library = {"orc1" : 1, "ogr1": 2, "troll1" : 3, "cancle" : 0}

    def __init__(self, screen, size):
        self.screen_window = screen       
        self.map_size = size
        self.tile_map_size = [size[0]//self.tile_size, size[1]//self.tile_size]
        self.tile_map = np.zeros([self.tile_map_size[0], self.tile_map_size[1]])
        self.obj_map_size = copy.deepcopy(self.tile_map_size)
        self.obj_map = copy.deepcopy(self.tile_map)
        self.img_map_size = copy.deepcopy(self.obj_map_size)
        self.img_map = np.zeros([self.tile_map_size[0], self.tile_map_size[1]])
        self.enemy_map_size = copy.deepcopy(self.img_map_size)
        self.enenmy_map = copy.deepcopy(self.img_map)
        w, h = self.icon_size
        #------------------tile-----------------------
        btn1 = fun_pyImgBtn.pyImgBtn([1000,           0],self.icon_size,"grass1.png", self.screen_window, "grass1")
        btn2 = fun_pyImgBtn.pyImgBtn([1000 + w,       0],self.icon_size,"dirt1.png", self.screen_window, "dirt1")
        btn3 = fun_pyImgBtn.pyImgBtn([1000 + w * 2,   0],self.icon_size,"ice1.png", self.screen_window, "ice1")
        btn4 = fun_pyImgBtn.pyImgBtn([1000 + w * 3,   0],self.icon_size,"rock1.png", self.screen_window, "rock1")
        self.tile_image.append(pygame.image.load(os.path.join(source_path, "grass1.png")))
        self.tile_image.append(pygame.image.load(os.path.join(source_path, "dirt1.png")))
        self.tile_image.append(pygame.image.load(os.path.join(source_path, "ice1.png")))
        self.tile_image.append(pygame.image.load(os.path.join(source_path, "rock1.png")))
        self.tile_image = [pygame.transform.scale(temp, (self.tile_size,self.tile_size)) for temp in self.tile_image]
        #------------------obj-----------------------
        btn5 = fun_pyImgBtn.pyImgBtn([1000,   h],self.icon_size,"tree_icon.png", self.screen_window, "tree1")
        btn6 = fun_pyImgBtn.pyImgBtn([1000 + w,h],self.icon_size,"water_icon.png", self.screen_window, "water1")
        btn9 = fun_pyImgBtn.pyImgBtn([1000 + w * 3, h],self.icon_size,"shovel.png", self.screen_window, "shovel")
        img = pygame.image.load(os.path.join(source_path, "tree1.png")).convert()
        img2 = pygame.image.load(os.path.join(source_path, "water1.png")).convert()
        for i in range(0,16):    
            sprite_img = img.subsurface([52 * i, 0, 52,52])
            self.obj_image.append(sprite_img)
        for i in range(0,16):    
            sprite_img = img2.subsurface([52 * i, 0, 52,52])
            self.obj_image.append(sprite_img)
        self.obj_image= [pygame.transform.scale(temp, (self.tile_size,self.tile_size)) for temp in self.obj_image]
        #------------------enemy-----------------------
        btn20 = fun_pyImgBtn.pyImgBtn([1000,        h * 4],self.icon_size,"orc1.png", self.screen_window, "orc1")
        btn22 = fun_pyImgBtn.pyImgBtn([1000 + w,    h * 4],self.icon_size,"ogr1.png", self.screen_window, "ogr1")     
        btn23 = fun_pyImgBtn.pyImgBtn([1000 + w * 2,h * 4],self.icon_size,"troll1.png", self.screen_window, "troll1")    
        btn21 = fun_pyImgBtn.pyImgBtn([1000,        h * 5],self.icon_size,"cancle.png", self.screen_window, "cancle")
        img3 = pygame.image.load(os.path.join(source_path, "orc1.png"))
        img4 = pygame.image.load(os.path.join(source_path, "ogr1.png"))
        img5 = pygame.image.load(os.path.join(source_path, "troll1.png"))
        self.enemy_img.append(img3)
        self.enemy_img.append(img4)
        self.enemy_img.append(img5)
        self.enemy_img = [pygame.transform.scale(temp, (self.tile_size,self.tile_size)) for temp in self.enemy_img]
        #------------------other option-----------------------
        btn10 = fun_pyImgBtn.pyImgBtn([1000        ,500],self.icon_size,"save.png", self.screen_window, "save")
        btn11 = fun_pyImgBtn.pyImgBtn([1000 + w    ,500],self.icon_size,"load.png", self.screen_window, "load")
        btn12 = fun_pyImgBtn.pyImgBtn([1000 + w * 2,500],self.icon_size,"bucket.png", self.screen_window, "bucket")
        btn13 = fun_pyImgBtn.pyImgBtn([1000 + w * 3,500],self.icon_size,"brush.png", self.screen_window, "brush")
        btn14 = fun_pyBtn.Button("EXIT",[1000,    500 + h],[200,50],15,[0,0,0],[100,100,100],self.screen_window, "exit")
        #-----------------btn list---------------------
        self.btn_list.append(btn1)
        self.btn_list.append(btn2)
        self.btn_list.append(btn3)
        self.btn_list.append(btn4)
        self.btn_list.append(btn5)
        self.btn_list.append(btn6)
        self.btn_list.append(btn9)
        self.btn_list.append(btn20) 
        self.btn_list.append(btn22)
        self.btn_list.append(btn23)
        self.btn_list.append(btn21)
        self.btn_list.append(btn10)
        self.btn_list.append(btn11)
        self.btn_list.append(btn12)
        self.btn_list.append(btn13)
        self.btn_list.append(btn14)

    def display(self):    
        self.screen_window.fill([0,0,0])
        pygame.draw.rect(self.screen_window,[150,75,0],[1000,0,200,600])
        pygame.draw.line(self.screen_window,[125,125,125], [1000,0], [1000,600], 2)
        #--------frame for selecting---------------------      
        w, h = self.icon_size
        if self.bucket == True: 
            pygame.draw.rect(self.screen_window,[255,0,0],[1000 + w * 2,500,w,h], 5)  
        else:
            pygame.draw.rect(self.screen_window,[255,0,0],[1000 + w * 3,500,w,h], 5)   
        for btn in self.btn_list:
            btn.draw()
            if self.cur_mode == btn.name:
                pygame.draw.rect(self.screen_window, [255,0,0], [btn.x,btn.y,btn.w,btn.h], 5)
        #-------------------draw tile map---------------------------  
        for j in range(0, self.tile_map_size[1]):
            for i in range(0, self.tile_map_size[0]):
                paint = int(self.tile_map[i][j])
                if paint > 0:
                    self.screen_window.blit(self.tile_image[paint - 1], [i * self.tile_size, j * self.tile_size])
        #-------------------draw object---------------------------          
        self.img_map = np.zeros([self.tile_map_size[0], self.tile_map_size[1]])              
        for obj in [1,2]:
            indices = self.img_library[obj]
            self.img_map = fun_pygameboard.fun_pyCell.merge(self.obj_map, self.obj_map_size, obj, indices, self.img_map)  
        for j in range(0, self.tile_map_size[1]):
            for i in range(0, self.tile_map_size[0]):
                paint = int(self.img_map[i][j])
                if paint > 0:
                    self.screen_window.blit(self.obj_image[paint - 1], [i * self.tile_size, j * self.tile_size])
        #-------------------draw enemy---------------------------
        for j in range(0, self.tile_map_size[1]):
            for i in range(0, self.tile_map_size[0]):
                paint = int(self.enenmy_map[i][j])
                if paint > 0:
                    self.screen_window.blit(self.enemy_img[paint - 1], [i * self.tile_size, j * self.tile_size])  

    def key_handler(self,event):
        mouse_pos = pygame.mouse.get_pos()
        cell_pos = [mouse_pos[0]//self.tile_size , mouse_pos[1]//self.tile_size] 
        
        if event.type == pygame.QUIT:
            return "quit"
        elif self.tile_map_size[0] > cell_pos[0] >= 0 and self.tile_map_size[1] > cell_pos[1] >= 0:
            pygame.draw.rect(self.screen_window, [200,212,0],\
                [cell_pos[0] * self.tile_size, cell_pos[1] * self.tile_size, self.tile_size, self.tile_size],5)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cur_mode != None:
                    if self.cur_mode in self.tile_library:
                        fun_pygameboard.fun_pyCell.painting(self.tile_map, self.tile_map_size, cell_pos, self.bucket, self.tile_library[self.cur_mode])
                    elif self.cur_mode in self.obj_library:
                        fun_pygameboard.fun_pyCell.painting(self.obj_map, self.obj_map_size, cell_pos, self.bucket, self.obj_library[self.cur_mode])  
                    elif self.cur_mode in self.enemy_library:
                        fun_pygameboard.fun_pyCell.painting(self.enenmy_map, self.enemy_map_size, cell_pos, self.bucket, self.enemy_library[self.cur_mode])  
        for btn in self.btn_list:
            name = btn.check(event)
            if name is not None:
                self.cur_mode = name
                break
        if self.cur_mode == "bucket":
            self.bucket = True
        elif self.cur_mode == "brush":
            self.bucket = False
        elif self.cur_mode == "save": 
            self.cur_mode = ""
            fun_pyMap.map_txt_export("Map.txt",self.tile_map_size,self.tile_map,self.obj_map, self.img_map, self.enenmy_map)
        elif self.cur_mode == "load":
            self.cur_mode = ""
            [self.tile_map_size, self.tile_map, self.obj_map, self.img_map, self.enenmy_map] =  fun_pyMap.map_txt_import("Map.txt")
        elif self.cur_mode == "exit":
            self.cur_mode = ""
            return "reset"
        return "map_menu"
#___________________________________________________
class shop_menu:
    screen_window = None
    icon_size = [100,100]
    btn_list = []
    cur_mode = ""
    money = 0
    army = []
    def __init__(self, screen):
        self.money = 1000
        self.screen_window = screen
        img_main = pygame.image.load(os.path.join(source_path, "shop.jpg"))
        img_main = pygame.transform.scale(img_main, (800,600))
        gold = pygame.image.load(os.path.join(source_path, "gold.png"))
        gold = pygame.transform.scale(gold, (50,50))
        self.img_main = img_main
        self.gold = gold

        btn1 = fun_pyImgBtn.pyImgBtn([1000,0],self.icon_size,"c1.png", self.screen_window, "c1")
        btn2 = fun_pyImgBtn.pyImgBtn([1100,0],self.icon_size,"c2.png", self.screen_window, "c2")
        btn10 = fun_pyImgBtn.pyImgBtn([1000,500],self.icon_size,"cancle.png", self.screen_window, "cancle")
        btn11 = fun_pyBtn.Button("SAVE",[1100,500],[100,50],20,[0,0,0],[100,100,100], self.screen_window, "SAVE")
        btn12 = fun_pyBtn.Button("LOAD",[1100,550],[100,50],20,[0,0,0],[100,100,100], self.screen_window, "LOAD")
        self.btn_list.append(btn1)
        self.btn_list.append(btn2)
        self.btn_list.append(btn10)
        self.btn_list.append(btn11)
        self.btn_list.append(btn12)
        self.cur_mode = ""

    def army_txt_import(self, txt):
        file = open(txt, "r")
        temp = file.read().splitlines()
        self.army = []
        self.money = int(temp[0])
        for i in range(1, len(temp)):
            self.army.append(str(temp[i]))
        file.close()

    def army_txt_export(self, txt):
        file = open(txt, "w")
        file.write(str(self.money) + "\n")
        for temp in self.army:
            file.write(str(temp) + "\n")
        file.close()

    def display(self):    
        self.screen_window.fill([0,0,0])
        self.screen_window.blit(self.img_main, (0,0))
        self.screen_window.blit(self.gold, (1000,400))
        for btn in self.btn_list:
            btn.draw()
            if self.cur_mode == btn.name:
                pygame.draw.rect(self.screen_window, [255,0,0], [btn.x,btn.y,btn.w,btn.h], 5)
        temp = fun_pytxt.pyText(str(self.money),[1060,400],15, [255,255,255], self.screen_window)
        temp.draw()
        for i, temp in enumerate(self.army):
            j = i // 4
            i = i % 4
            if temp == "c1":
                temp = fun_pyImgBtn.pyImgBtn([850 + i * 25, 0 + j * 25],[25,25],"c1.png", self.screen_window, "c1")
                temp.draw()
            elif temp == "c2":
                temp = fun_pyImgBtn.pyImgBtn([850+ i * 25, 0 + j * 25],[25,25],"c2.png", self.screen_window, "c2")
                temp.draw()
        

    def key_handler(self, event):
        for btn in self.btn_list:
                name = btn.check(event)
                if name is not None:
                    self.cur_mode = name
                    break
        if self.cur_mode == "c1" and self.money >= 100:
            print("buy c1")
            self.money -= 100
            self.army.append("c1")
            self.cur_mode = []
        elif self.cur_mode == "c2" and self.money >= 200:
            print("buy c2")
            self.money -= 200
            self.army.append("c2")
            self.cur_mode = []
        elif self.cur_mode == "cancle":
            self.cur_mode = []
            return "main_menu"
        elif self.cur_mode == "SAVE":
            self.army_txt_export("save.txt")
            self.cur_mode = []
        elif self.cur_mode == "LOAD":
            self.army_txt_import("save.txt")
            self.cur_mode = []
        if event.type == pygame.QUIT:
            return "quit"
        return "shop_menu"