import pygame
import os
import fun_pytxtInput
import fun_pygameboard
import fun_pyImgBtn
import fun_pyMap
import fun_pytxt
import fun_pyBtn
import numpy as np
import copy


class map_editor(object):
    screen = None
    screen_size = [0,0]
    icon_size = [50, 50]
    btn_list = []
    btn_list2 = []

    bucket = False
    back_img = None
    cur_mode = None
    map_pos = [0, 0]
    map_screen_size = [0,0]

    cell_size = 50
    cell_pos = [0, 0]

    tile_map_size = []
    tile_map = []    
    obj_map = []
    img_map = []
    char_map = []
    etc_map = []

    #values for set cell in map 
    tile_library = {"grass1": 1, "dirt1": 2, "ice1": 3, "rock1": 4}
    obj_library = {"tree1": 1, "water1": 2, "wall1": 3, "shovel": 0}
    img_library = {1: np.arange(1, 17), 2: np.arange(17, 33), 3: np.arange(33, 49)}
    unit_library = {"orc1": 1, "ogr1": 2, "troll1": 3, "cancle": 0}
    etc_library = {"mission1": 1, "mission2" : 2, "mission_cancle": 0}
    #file names for load images
    tile_txt_list = ["grass1.png", "dirt1.png", "ice1.png", "rock1.png"]
    unit_txt_list = ["orc1.png", "ogr1.png", "troll1.png", "Footman.png", "Archer.png", "Peasant.png"]
    obj_txt_list = ["tree1.png", "water1.png", "wall1.png"]
    etc_txt_list = ["mission1.png", "mission2.png", "mission_cancle.png"]
    #save image files for drawing on map
    tile_img_list = {}
    obj_img_list = {}
    unit_img_list = {}
    etc_img_list = {}

    mouse_pos = [0, 0]

    def __init__(self, map_screen_size, cell_size, screen):
        self.screen = screen
        info = pygame.display.Info()
        self.screen_size = [info.current_w, info.current_h]
        self.map_pos = [0, 0]
        self.map_screen_size = map_screen_size
        self.btn_size = [self.screen_size[0] - self.map_screen_size[0], 50]
        self.btn_list = []
        self.btn_list2 = []
        self.cell_size = cell_size
        self.tile_map_size = [map_screen_size[0] //
                              self.cell_size, map_screen_size[1]//self.cell_size]
        self.tile_map = np.zeros(
            [self.tile_map_size[0], self.tile_map_size[1]])
        self.obj_map = copy.deepcopy(self.tile_map)
        self.img_map = copy.deepcopy(self.tile_map)
        self.char_map = copy.deepcopy(self.tile_map)
        self.etc_map = copy.deepcopy(self.tile_map)
        # ------------------tile-----------------------
        cur_path = os.path.dirname(__file__)
        source_path = os.path.join(cur_path, "images")
        btn1 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "grass1.png", self.screen, "grass1")
        btn2 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "dirt1.png", self.screen, "dirt1")
        btn3 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "ice1.png", self.screen, "ice1")
        btn4 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "rock1.png", self.screen, "rock1")
        self.tile_img_list = {}
        for i, img in enumerate(self.tile_txt_list):
            temp = pygame.image.load(os.path.join(source_path, img)).convert()
            temp = pygame.transform.scale(
                temp, (self.cell_size, self.cell_size))
            self.tile_img_list[i + 1] = temp
        # ------------------obj-----------------------
        self.obj_img_list = {}
        for i, img in enumerate(self.obj_txt_list):
            temp = pygame.image.load(os.path.join(source_path, img)).convert()
            for j in range(0, 16):
                sprite_img = temp.subsurface([52 * j, 0, 52, 52])
                sprite_img = pygame.transform.scale(
                    sprite_img, (self.cell_size, self.cell_size))
                self.obj_img_list[16 * i + j + 1] = sprite_img
        btn5 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "tree_icon.png", self.screen, "tree1")
        btn6 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "water_icon.png", self.screen, "water1")
        btn7 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "wall1_icon.png", self.screen, "wall1")
        btn8 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "shovel.png", self.screen, "shovel")
        # ------------------enemy-----------------------
        btn9 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "character/orc1.png", self.screen, "orc1")
        btn10 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "character/ogr1.png", self.screen, "ogr1")
        btn11 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "character/troll1.png", self.screen, "troll1")
        btn12 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size,"cancle.png", self.screen, "cancle")
        self.unit_img_list = {}
        for i, img in enumerate(self.unit_txt_list):
            temp = pygame.image.load(os.path.join(
                source_path,  "character/" + img)).convert()
            temp = pygame.transform.scale(
                temp, (self.cell_size, self.cell_size))
            self.unit_img_list[i + 1] = temp
        # -----------------mission-----------------------
        btn13 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "mission/mission1.png", self.screen, "mission1")
        btn14 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "mission/mission2.png", self.screen, "mission2")
        btn15 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "mission/mission_cancle.png", self.screen, "mission_cancle")
        self.etc_img_list = {}
        for i, img in enumerate(self.etc_txt_list):
            temp = pygame.image.load(os.path.join(
                source_path,  "mission/" + img)).convert()
            temp = pygame.transform.scale(
                temp, (self.cell_size, self.cell_size))
            self.etc_img_list[i + 1] = temp
        # ------------------other option-----------------------
        btn16 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "save.png", self.screen, "save")
        btn17 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "load.png", self.screen, "load")
        btn18 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "bucket.png", self.screen, "bucket")
        btn19 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "brush.png", self.screen, "brush")
        btn20 = fun_pyImgBtn.pyImgBtn(
            [0, 0], self.icon_size, "exit.png", self.screen, "exit")
        # -----------------map text input---------------------
        btn21 = fun_pytxtInput.pytxtInput("", [0, 0], self.icon_size, 15, [0, 0, 0], [
                                          255, 255, 255], [207, 214, 219], self.screen, True, "table_cols")
        btn22 = fun_pytxt.pytxt("cols", [0, 0], 20, [
                                0, 0, 0], self.screen, "cols")
        btn23 = fun_pytxtInput.pytxtInput("", [0, 0], self.icon_size, 15, [0, 0, 0], [
                                          255, 255, 255], [207, 214, 219], self.screen, True, "table_rows")
        btn24 = fun_pytxt.pytxt("rows", [0, 0], 20, [
                                0, 0, 0], self.screen, "rows")
        btn25 = fun_pyBtn.Button("GENERATE", [0, 0], [0, 0], 20, [0, 0, 0], [
                                 180, 180, 180], [236, 239, 241], self.screen, "generate")
        # -----------------btn list---------------------
        self.btn_list.append(btn1)
        self.btn_list.append(btn2)
        self.btn_list.append(btn3)
        self.btn_list.append(btn4)
        self.btn_list.append(btn5)
        self.btn_list.append(btn6)
        self.btn_list.append(btn7)
        self.btn_list.append(btn8)
        self.btn_list.append(btn9)
        self.btn_list.append(btn10)
        self.btn_list.append(btn11)
        self.btn_list.append(btn12)
        self.btn_list.append(btn13)
        self.btn_list.append(btn14)
        self.btn_list.append(btn15)
        self.btn_list.append(btn16)
        self.btn_list.append(btn17)
        self.btn_list.append(btn18)
        self.btn_list.append(btn19)
        self.btn_list.append(btn20)
        self.btn_list2.append(btn21)
        self.btn_list2.append(btn22)
        self.btn_list2.append(btn23)
        self.btn_list2.append(btn24)
        self.btn_list2.append(btn25)

    def screen_move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.map_pos[0] += 10
        elif keys[pygame.K_d]:
            self.map_pos[0] -= 10
        elif keys[pygame.K_w]:
            self.map_pos[1] += 10
        elif keys[pygame.K_s]:
            self.map_pos[1] -= 10
        mouse_pos = pygame.mouse.get_pos()
        speed = 20
        if mouse_pos[0] == self.screen_size[0] - 1:
            self.map_pos[0] -= speed
            if mouse_pos[1] == self.screen_size[1] - 1:
                self.map_pos[1] -= speed
            elif mouse_pos[1] == 0:
                self.map_pos[1] += speed
        elif mouse_pos[0] == 0:
            self.map_pos[0] += speed
            if mouse_pos[1] == self.screen_size[1] - 1:
                self.map_pos[1] -= speed
            elif mouse_pos[1] == 0:
                self.map_pos[1] += speed
        elif mouse_pos[1] == self.screen_size[1] - 1:
            self.map_pos[1] -= speed
            if mouse_pos[0] == self.screen_size[0] - 1:
                self.map_pos[0] -= speed
            elif mouse_pos[0] == 0:
                self.map_pos[0] += speed
        elif mouse_pos[1] == 0:
            self.map_pos[1] += speed
            if mouse_pos[0] == self.screen_size[0] - 1:
                self.map_pos[0] -= speed
            elif mouse_pos[0] == 0:
                self.map_pos[0] += speed

        w = self.tile_map_size[0] * self.cell_size
        h = self.tile_map_size[1] * self.cell_size
        if w >= self.map_screen_size[0]:
            if  self.map_pos[0] <= -w + self.map_screen_size[0] :
                self.map_pos[0] = -w + self.map_screen_size[0]
            elif self.map_pos[0] >= 0:
                self.map_pos[0] = 0
        else:
            if self.map_pos[0] >= self.map_screen_size[0] - w :
                self.map_pos[0] = self.map_screen_size[0] - w
            elif self.map_pos[0] <= 0:
                self.map_pos[0] = 0
        if h >= self.map_screen_size[1]:
            if  self.map_pos[1] <= -h + self.map_screen_size[1] :
                self.map_pos[1] = -h + self.map_screen_size[1]
            elif self.map_pos[1] >= 0:
                self.map_pos[1] = 0
        else:
            if self.map_pos[1] >= self.map_screen_size[1] - h :
                self.map_pos[1] = self.map_screen_size[1] - h
            elif self.map_pos[1] <= 0:
                self.map_pos[1] = 0

    def edit_event(self):
        # --------text box----------------------------------
        while True:
            self.screen.fill((0, 0, 0))
            self.screen_move()
            for event in pygame.event.get():
                self.mouse_pos = pygame.mouse.get_pos()
                self.cell_pos = [(self.mouse_pos[0] - self.map_pos[0])//self.cell_size,
                                 (self.mouse_pos[1] - self.map_pos[1])//self.cell_size]
                if event.type == pygame.QUIT:
                    return "quit"
                elif self.tile_map_size[0] > self.cell_pos[0] >= 0\
                        and self.tile_map_size[1] > self.cell_pos[1] >= 0\
                        and self.map_screen_size[0] > self.mouse_pos[0] >= 0\
                        and self.map_screen_size[1] > self.mouse_pos[1] >= 0\
                        and event.type == pygame.MOUSEBUTTONDOWN\
                        and self.cur_mode != None:
                        if self.cur_mode in self.tile_library:
                            fun_pygameboard.fun_pyCell.painting(
                                self.tile_map, self.tile_map_size, self.cell_pos, self.bucket, self.tile_library[self.cur_mode])
                        elif self.cur_mode in self.obj_library:
                            fun_pygameboard.fun_pyCell.painting(
                                self.obj_map, self.tile_map_size, self.cell_pos, self.bucket, self.obj_library[self.cur_mode])
                        elif self.cur_mode in self.unit_library:
                            fun_pygameboard.fun_pyCell.painting(
                                self.char_map, self.tile_map_size, self.cell_pos, self.bucket, self.unit_library[self.cur_mode])
                        elif self.cur_mode in self.etc_library:
                            fun_pygameboard.fun_pyCell.painting(
                                self.etc_map, self.tile_map_size, self.cell_pos, self.bucket, self.etc_library[self.cur_mode])
                for btn in self.btn_list:
                    name = btn.check(event, self.mouse_pos)
                    if name is not None:
                        self.cur_mode = name
                        break
                for btn in self.btn_list2:
                    name = btn.check(event, self.mouse_pos)
                    if name is not None:
                        self.cur_mode = name
                        break
                if self.cur_mode == "bucket":
                    self.bucket = True
                elif self.cur_mode == "brush":
                    self.bucket = False
                elif self.cur_mode == "save":
                    fun_pyMap.map_txt_export(
                        "maps/Map.txt", self.tile_map_size, self.tile_map, self.obj_map, self.img_map, self.char_map, self.etc_map)
                    self.cur_mode = ""
                elif self.cur_mode == "load":
                    [self.tile_map_size, self.tile_map, self.obj_map, self.img_map,
                        self.char_map, self.etc_map] = fun_pyMap.map_txt_import("maps/Map.txt")
                    self.cur_mode = None
                elif self.cur_mode == "generate":
                    if int(self.btn_list2[0].text) > 0 and int(self.btn_list2[2].text) :
                        self.map_pos = [0,0]
                        self.tile_map_size = [int(self.btn_list2[0].text), int(self.btn_list2[2].text)]
                        self.tile_map = np.zeros(
                            [self.tile_map_size[0], self.tile_map_size[1]])
                        self.obj_map = copy.deepcopy(self.tile_map)
                        self.img_map = copy.deepcopy(self.tile_map)
                        self.char_map = copy.deepcopy(self.img_map)
                        self.etc_map = copy.deepcopy(self.img_map)
                        self.cur_mode = None
                elif self.cur_mode == "exit":
                    return "game"
            self.draw()
            pygame.time.Clock().tick(60)

    def draw(self):
        self.screen.fill([0, 0, 0])
        # -------------------draw object---------------------------
        self.img_map = np.zeros([self.tile_map_size[0], self.tile_map_size[1]])
        for obj in range(1, 4):
            indices = range(16 * (obj - 1) + 1, 16 * (obj - 1) + 17)
            self.img_map = fun_pygameboard.fun_pyCell.merge(
                self.obj_map, self.tile_map_size, obj, indices, self.img_map)
        # -------------------draw enemy---------------------------
        for j in range(0, self.tile_map_size[1]):
            for i in range(0, self.tile_map_size[0]):
                paint = int(self.tile_map[i][j])
                if paint > 0:
                    self.screen.blit(self.tile_img_list[paint],
                                     [self.map_pos[0] + i * self.cell_size, self.map_pos[1] + j * self.cell_size])
                paint = int(self.img_map[i][j])
                if paint > 0:
                    self.screen.blit(self.obj_img_list[paint],
                                    [self.map_pos[0] + i * self.cell_size, self.map_pos[1] + j * self.cell_size])
                paint = int(self.char_map[i][j])
                if paint > 0:
                    self.screen.blit(self.unit_img_list[paint],
                                    [self.map_pos[0] + i * self.cell_size, self.map_pos[1] + j * self.cell_size])
                paint = int(self.etc_map[i][j])
                if paint > 0:
                    s = pygame.Surface([self.cell_size, self.cell_size])
                    s.set_alpha(100)
                    if paint == 1:
                        s.fill([0,255,0])
                    elif paint == 2:
                        s.fill([218,165,32])
                    self.screen.blit(
                    s, (self.map_pos[0] + i * self.cell_size,
                            self.map_pos[1] + j * self.cell_size))
        # -----------------draw mouse cursor----------------------------------
        if self.tile_map_size[0] > self.cell_pos[0] >= 0\
                        and self.tile_map_size[1] > self.cell_pos[1] >= 0:
                    pygame.draw.rect(self.screen, [255, 255, 255], [
                        self.map_pos[0] + self.cell_pos[0] * self.cell_size,
                        self.map_pos[1] + self.cell_pos[1] * self.cell_size,
                        self.cell_size, self.cell_size], 5)
        pygame.draw.rect(self.screen, [50, 150, 255], [
                        self.map_pos[0], self.map_pos[1],
                        self.cell_size * self.tile_map_size[0], self.cell_size * self.tile_map_size[1]], 5)
        # -------------------draw UI distinguish line---------------------------
        pygame.draw.rect(self.screen, [255, 255, 225], [
                         self.map_screen_size[0], 0, 200, self.map_screen_size[1]])
        pygame.draw.line(self.screen, [255, 255, 255], [self.map_screen_size[0], 0], [
                         self.map_screen_size[0], self.map_screen_size[1]], 5)
        #------------------draw mini map-------------------------------------
        mini_window = [self.map_screen_size[0], 500]
        mini_map_size= [200, 200]
        mini_size = min(mini_map_size[0]//self.tile_map_size[0], mini_map_size[1]//self.tile_map_size[1])
        mini_cell= [mini_size, mini_size]
        pygame.draw.rect(self.screen,[0,0,0], [mini_window[0], mini_window[1], mini_map_size[0], mini_map_size[1]])
        for j in range(0, self.tile_map_size[1]):
            for i in range(0, self.tile_map_size[0]):
                paint = int(self.tile_map[i][j])
                if paint == 0:
                    pygame.draw.rect(self.screen,[0,0,0],
                    [mini_window[0] + i * mini_cell[0], mini_window[1] + j * mini_cell[1], mini_cell[0], mini_cell[1]])
                elif paint > 0:
                    temp = pygame.transform.scale(
                            self.tile_img_list[paint], (mini_cell[0],mini_cell[1]))
                    self.screen.blit(temp,
                                        [mini_window[0] + i * mini_cell[0], mini_window[1] + j * mini_cell[1]])
                paint = int(self.img_map[i][j])
                if paint > 0:
                    temp = pygame.transform.scale(
                            self.obj_img_list[paint], (mini_cell[0],mini_cell[1]))
                    self.screen.blit(temp,
                                        [mini_window[0] + i * mini_cell[0], mini_window[1] + j * mini_cell[1]])
                paint = int(self.char_map[i][j])
                if paint > 0:
                    pygame.draw.rect(self.screen,[255,125,0],
                    [mini_window[0] + i * mini_cell[0], mini_window[1] + j * mini_cell[1], mini_cell[0], mini_cell[1]])
                paint = int(self.etc_map[i][j])
                if paint > 0:
                    s = pygame.Surface([mini_cell[0], mini_cell[1]])
                    s.set_alpha(100)
                    if paint == 1:
                        s.fill([0,255,0])
                    elif paint == 2:
                        s.fill([218,165,32])
                    self.screen.blit(s, [mini_window[0] + i * mini_cell[0], mini_window[1] + j * mini_cell[1]])
        x =  self.map_pos[0] * self.tile_map_size[0] * mini_size/self.map_screen_size[0]
        y =  self.map_pos[1] * self.tile_map_size[1] * mini_size/self.map_screen_size[1]
        w =  self.map_screen_size[0] * self.tile_map_size[0] * mini_size/(self.tile_map_size[0] * self.cell_size)
        h =  self.map_screen_size[1] * self.tile_map_size[1] * mini_size/(self.tile_map_size[1] * self.cell_size) 
        pygame.draw.rect(self.screen,[255,255,255], 
                    [mini_window[0] - x, mini_window[1] - y, w, h], 2)
         # -------------------draw btn---------------------------
        for i, btn in enumerate(self.btn_list):
            j = i//4
            k = i % 4
            rect = [self.map_screen_size[0] + k * self.btn_size[0]/4,
                    j * self.btn_size[0]/4,
                    self.btn_size[0]/4,
                    self.btn_size[0]/4]
            btn.x, btn.y, btn.w, btn.h = rect
            btn.draw(self.mouse_pos)
            if self.cur_mode == btn.name:
                pygame.draw.rect(self.screen, [255, 0, 0], rect, 5)
        # --------panting for selecting---------------------
        if self.bucket == True:
            rect_size = [self.btn_list[14].x, self.btn_list[14].y,
                         self.btn_list[14].w, self.btn_list[14].h]
            pygame.draw.rect(self.screen, [0, 255, 255], rect_size, 5)
        else:
            rect_size = [self.btn_list[15].x, self.btn_list[15].y,
                         self.btn_list[15].w, self.btn_list[15].h]
            pygame.draw.rect(self.screen, [0, 255, 255], rect_size, 5)
        # -------------------draw btn for input-------------------------------
        for i, btn in enumerate(self.btn_list2):
            j = i//2
            k = i % 2
            rect = [self.map_screen_size[0] + k * self.btn_size[0]/2,
                    300 + j * self.btn_size[1]/2,
                    self.btn_size[0]/2 - 2,
                    self.btn_size[1]/2 - 2]
            btn.x, btn.y, btn.w, btn.h = rect
            if j > 1:
                btn.w = self.btn_size[0]
                btn.h = 50
            btn.draw(self.mouse_pos)
        pygame.display.flip()
