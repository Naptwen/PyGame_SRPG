from asyncio import all_tasks
from pydoc import cli, text
from shutil import move
import os

import pygame
import copy
import numpy as np

import fun_pyCell
import fun_pyBtn
import fun_pyMap
import fun_pytxt
import fun_pyImgTxt
import fun_pyCharacter

# return index


def find_list(ele, list):
    for i, sub in enumerate(list):
        if ele == sub:
            return i
    return -1
# ___________________________________________________


class game_mother_board:
    table = None
    cols, rows = [0, 0]
    screen = None
    path = []
    deploy = True
    phase = "deploy"
    cell_size = 50
    table_size = [1000, 600]
    click_cell_pos = []
    cur_cell_pos = []
    Ai_who = []
    Ai_target = []
    team_A = []
    team_B = []

    deployzone = [0, 3, 0, 10]

    image_list = []
    btn_list = []
    btn2_list = []

    damage_txt = None
    skull_image = None
    turn_image = None
    tile_image = []
    obj_image = []

    tile_map    = []
    obj_map     = []
    img_map     = []
    enemy_map   = []

    def __init__(self, table_size, cell_size, screen):
        self.deploy = True
        self.cols, self.rows = table_size[0]//cell_size, table_size[1]//cell_size
        self.table_size = table_size
        self.cell_size = cell_size
        self.table = fun_pyCell.Cell_Table(self.cols, self.rows)
        self.screen = screen
        self.damage_txt = fun_pyImgTxt.pyImgTxt(
            "", [0, 0], 20, [0, 0, 0], "wow.png", [100, 100], self.screen)
        w, h = pygame.display.get_surface().get_size()
        self.mission_fail = fun_pyImgTxt.pyImgTxt(
            "MISSION FAILED", [w/2, h/2], 100, [255, 255, 255], "mission_fail.png", [w, h], self.screen)
        self.mission_success = fun_pyImgTxt.pyImgTxt(
            "MISSION COMPLETE", [w/2, h/2], 100, [255, 255, 255], "mission_suc.jpg", [w, h], self.screen)
        btn1 = fun_pyBtn.Button("MOVING",   [1000, 0], [200, 50], 15, [
                                0, 0, 0],   [100, 100, 100], screen, "MOVE")
        btn2 = fun_pyBtn.Button("ATTACK",   [1000, 50], [200, 50], 15, [
                                0, 0, 0],   [100, 100, 100], screen, "ATTACK")
        btn3 = fun_pyBtn.Button("AUTO",     [1000, 100], [200, 50], 15, [
                                0, 0, 0],   [100, 100, 100], screen, "AUTO")
        btn4 = fun_pyBtn.Button("TURN END", [1000, 150], [200, 50], 15, [
                                0, 0, 0],   [100, 100, 100], screen, "TURN END")
        btn7 = fun_pyBtn.Button("FINISH",   [1000, 0], [200, 50], 15, [
                                0, 0, 0],   [100, 100, 100], screen, "FINISH")
        btn8 = fun_pyBtn.Button("LOAD_MAP", [1000, 50], [200, 50], 15, [
                                0, 0, 0],   [100, 100, 100], screen, "MAP LOAD")
        self.turn_image = fun_pyImgTxt.pyImgTxt("", [self.screen.get_size(
        )[0]/2, self.screen.get_size()[1]/2], 35, [255, 255, 255], "banner.png", [500, 200], self.screen)
        self.image_loader()
        self.btn_list.append(btn1)
        self.btn_list.append(btn2)
        self.btn_list.append(btn3)
        self.btn_list.append(btn4)
        self.btn2_list.append(btn7)
        self.btn2_list.append(btn8)

    def image_loader(self):
        cur_path = os.path.dirname(__file__)
        source_path = os.path.join(cur_path, "images")
        temp = pygame.image.load(os.path.join(source_path, "c1.png"))
        temp = pygame.transform.scale(temp, (self.cell_size, self.cell_size))
        self.image_list.append(temp)

        img3 = pygame.image.load(os.path.join(source_path, "orc1.png"))
        img4 = pygame.image.load(os.path.join(source_path, "ogr1.png"))
        img5 = pygame.image.load(os.path.join(source_path, "troll1.png"))
        self.image_list.append(img3)
        self.image_list.append(img4)
        self.image_list.append(img5)
        self.image_list = [pygame.transform.scale(temp, (self.cell_size,self.cell_size)) for temp in self.image_list]

        self.skull_image = pygame.image.load(
            os.path.join(source_path, "skull.png"))
        self.skull_image = pygame.transform.scale(
            self.skull_image, (self.cell_size, self.cell_size))

        self.tile_map = np.zeros([self.table.cols, self.table.rows], dtype=int)
        self.obj_map = np.zeros([self.table.cols, self.table.rows], dtype=int)
        self.img_map = np.zeros([self.table.cols, self.table.rows], dtype=int)
        self.enemy_map = np.zeros([self.table.cols, self.table.rows], dtype=int)
        self.map_img()

        print("[GAME] : Deployment Phase")
        self.phase = "deploy"
        self.turn_image.text = "DEPLOYMENT TURN"

    def map_img(self):
        cur_path = os.path.dirname(__file__)
        source_path = os.path.join(cur_path, "images")
        self.tile_image.append(pygame.image.load(
            os.path.join(source_path, "dark.png")))
        self.tile_image.append(pygame.image.load(
            os.path.join(source_path, "grass1.png")))
        self.tile_image.append(pygame.image.load(
            os.path.join(source_path, "dirt1.png")))
        self.tile_image.append(pygame.image.load(
            os.path.join(source_path, "ice1.png")))
        self.tile_image.append(pygame.image.load(
            os.path.join(source_path, "rock1.png")))
        self.tile_image = [pygame.transform.scale(
            temp, (self.cell_size, self.cell_size)) for temp in self.tile_image]
        self.obj_image.append(pygame.image.load(
            os.path.join(source_path, "none.png")))
        img = pygame.image.load(os.path.join(
            source_path, "tree1.png")).convert()
        img2 = pygame.image.load(os.path.join(
            source_path, "water1.png")).convert()
        for i in range(0, 16):
            sprite_img = img.subsurface([52 * i, 0, 52, 52])
            self.obj_image.append(sprite_img)
        for i in range(0, 16):
            sprite_img = img2.subsurface([52 * i, 0, 52, 52])
            self.obj_image.append(sprite_img)
        self.obj_image = [pygame.transform.scale(
            temp, (self.cell_size, self.cell_size)) for temp in self.obj_image]
        self.ttxt = fun_pytxt.pyText(
            "", [1000, 400], 15, [0, 0, 0], self.screen)

    def map_draw(self):
        for j in range(0, self.table.rows):
            for i in range(0, self.table.cols):
                tile = int(self.tile_map[i][j])
                paint = int(self.img_map[i][j])
                self.screen.blit(self.tile_image[tile], [
                                 i * self.cell_size, j * self.cell_size])
                self.screen.blit(self.obj_image[paint], [
                                 i * self.cell_size, j * self.cell_size])

    def phase_check(self):
        if self.phase == "MOVE":
            self.move_event()
        elif self.phase == "ATTACK":
            self.attack_event()
        elif self.phase == "AUTO":
            self.Ai_event("troop", "enemy")        
        elif self.phase == "TURN END":
            self.trun_end_event()
            self.phase = "ENEMY"
        elif self.phase == "ENEMY":
            self.Ai_event("enemy", "troop")
            for cell in self.table.node_table:
                if cell.type is not None and cell.type.tag == "enemy":
                    cell.type.phase_end()
        elif self.phase == "LOSE":
            self.table.resetCell()
            return "reset"
        elif self.phase == "WIN" :
            self.table.resetCell()
            return "reset"
        return "game_menu"

    def event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        cell_pos = [mouse_pos[0]//self.cell_size, mouse_pos[1]//self.cell_size]
        if event.type == pygame.QUIT:
            return "quit"
        if self.deploy == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.deploy_event(cell_pos, 0, 3, 0, self.table.rows)
            for btn in self.btn2_list:
                temp = btn.check(event)
                if temp is not None:
                    self.phase = temp
                    print("[GAME] : " + str(self.phase))
                    break
            if self.phase == "MAP LOAD":
                print("[GAME] : Load")
                [self.tile_map_size, self.tile_map, self.obj_map, self.img_map,
                    self.enemy_map] = fun_pyMap.map_txt_import("Map.txt")
                self.table = fun_pyMap.map2cell(
                    self.tile_map_size[0], self.tile_map_size[1], self.tile_map, self.obj_map, self.enemy_map)
                self.phase = "deploy"
                print(self.phase)
            elif self.phase == "FINISH":
                self.deploy = False
        else:
            for btn in self.btn_list:
                temp = btn.check(event)
                if temp is not None:
                    self.path = []
                    self.phase = temp
                    self.turn_image.text = temp
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                temp = self.table.giveCell(cell_pos)
                if temp is not None:
                    self.click_cell_pos = cell_pos
                    if self.phase == "MOVE" and temp.type is not None and temp.type.tag == "troop":
                        self.cur_cell_pos = cell_pos
                        self.path = []
                    elif self.phase == "ATTACK" and temp.type is not None and temp.type.tag == "troop" and self.cur_cell_pos == []:
                        self.cur_cell_pos = cell_pos
                        self.path = []
                    elif self.phase == "ATTACK" and find_list(self.click_cell_pos, self.path) < 0:
                        print("[GAME] : ATTACK cancle")
                        self.cur_cell_pos = []
                    print("[GAME] : click[" + str(self.click_cell_pos) +
                          "] cur[" + str(self.cur_cell_pos))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("[GAME] : ESC")
                self.phase = ""
                self.path = []
                self.click_cell_pos = []
                self.cur_cell_pos = []
        pygame.event.pump()
        self.draw()
        return self.phase_check()

    def deploy_event(self, click_cell_pos, min_x, max_x, min_y, max_y):
        if self.table.cols > click_cell_pos[0] >= 0 and self.table.rows > click_cell_pos[1] >= 0 and max_x > click_cell_pos[0] >= min_x and max_y > click_cell_pos[1] >= min_y:
            index = self.table.cols * click_cell_pos[1] + click_cell_pos[0]
            if self.table.node_table[index].obstacle == False and self.table.node_table[index].block == False:
                print(self.table.node_table[index].type)
                print(self.table.node_table[index].block)
                self.table.node_table[index].block = True
                temp = fun_pyCharacter.character(
                    "c1", 5, 1, 2, 1, 3, 3, 5, 1, "c1.png", "c1_face.png", "troop")
                self.table.node_table[index].type = copy.deepcopy(temp)
                print("[GAME] : deployed" + str(self.table.node_table[index].pos) +
                      " Type : " + self.table.node_table[index].type.name)

    def move_event(self):
        if self.cur_cell_pos:
            mouse_pos = pygame.mouse.get_pos()
            cell_pos = [mouse_pos[0]//self.cell_size,
                        mouse_pos[1]//self.cell_size]
            start = self.table.giveCell(self.cur_cell_pos)
            end = self.table.giveCell(cell_pos)
            if start is not None and end is not None and end.obstacle is False and end.block is False:
                self.path = self.table.Astar(self.cur_cell_pos, cell_pos)
        if self.path:
            start = copy.deepcopy(self.table.giveCell(self.cur_cell_pos))
            num = find_list(self.click_cell_pos, self.path)
            step = copy.deepcopy(start.type.mov)
            if step >= num > 0:
                for i in range(1, num + 1):
                    self.table.swap_cell(self.cur_cell_pos, self.path[i])
                    self.cur_cell_pos = self.path[i]
                    self.draw()
                    pygame.time.wait(10)
                    step -= 1
                character = self.table.giveCell(self.cur_cell_pos)
                character.type.mov = step
                self.click_cell_pos = []
                self.path = []
                print("[GAME] : MOVE action done")

    def attack_event(self):
        if self.cur_cell_pos:
            temp = self.table.giveCell(self.cur_cell_pos)
            if temp.type.tag == "troop":
                self.path = self.table.range(
                    self.cur_cell_pos, "circle", temp.type.ran)
            if self.click_cell_pos and find_list(self.click_cell_pos, self.path) >= 0 and not self.click_cell_pos == self.cur_cell_pos:
                temp = self.table.giveCell(self.click_cell_pos)
                temp2 = self.table.giveCell(self.cur_cell_pos)
                if temp.type is not None and temp2.type is not None and temp2.type.hit > 0:
                    self.hit_event(temp, temp2)
                self.click_cell_pos = []

    def death_check_event(self):
        if not self.deploy:
            troop = 0
            enemy = 0
            for node in self.table.node_table:
                if node.type is not None:
                    if node.type.die_check():
                        node.type = None
                        node.block = False
                        self.screen.blit(self.skull_image, [
                                        node.pos[0] * self.cell_size, node.pos[1] * self.cell_size])
                        pygame.time.wait(1000)
                    elif node.type.tag == "troop":
                        troop += 1
                    elif node.type.tag == "enemy":
                        enemy += 1
            if troop == 0:
                print("MISSION FAILED")
                self.mission_fail.draw()
                pygame.time.wait(2000)
                self.phase = "LOSE"
            elif enemy == 0:
                print("MISSION SUCCESS")
                self.mission_success.draw()
                pygame.time.wait(2000)
                self.phase = "WIN"

    def trun_end_event(self):
        self.Ai_event("enemy", "troop")
        for cell in self.table.node_table:
            if cell.type is not None and cell.type.tag == "troop":
                cell.type.phase_end()
        self.path = []
        self.cur_cell_pos = []
        self.click_cell_pos = []
        self.phase = []

    def Ai_turn_draw(self, current, target):
        if current:
            pygame.draw.rect(self.screen, [255, 255, 255], [
                current[0] * self.cell_size, current[1] * self.cell_size, self.cell_size, self.cell_size], 5)
            if target:
                pygame.draw.rect(self.screen, [200, 212, 0], [
                    target[0] * self.cell_size, target[1] * self.cell_size, self.cell_size, self.cell_size], 5)
    # if target is in range return the target cell if not return None
    def Ai_attack(self, cell, Ai_b):
        ATTACK_path = self.table.range(cell.pos, "circle", cell.type.ran)
        que = {}
        for cell2 in self.table.node_table:
            if cell2.type is not None and cell2.type.tag == Ai_b and find_list(cell2.pos, ATTACK_path) > -1:
                percent = cell2.type.hp/cell2.type.max_hp
                que[percent] = cell2
        if bool(que) :
            min = next(iter(que))
            for k, v in que.items():
                if min > k:
                    min = k
            return que[min]
        return None

    def Ai_mov(self, cell, path_info, Ai_b):  # reference
        step = copy.deepcopy(cell.type.mov)
        self.Ai_target = path_info[1].pos
        for i in range(1, len(path_info[2])):
            if step <= 0 or self.Ai_attack(cell, Ai_b):
                break
            self.table.swap_cell(cell.pos, path_info[2][i])
            cell = self.table.giveCell(path_info[2][i])
            self.Ai_who = cell.pos
            self.draw()
            pygame.time.wait(50)
            step -= 1
        cell.type.mov = step
        self.table.node_table[self.table.cols *
                              cell.pos[1] + cell.pos[0]] = copy.copy(cell)
        return cell

    def Ai_event(self, Ai_a, Ai_b):
        print("-----------------------------")
        print("[GAME] : AI Working")
        for cell in self.table.node_table:
            if cell.type is not None and cell.type.tag == Ai_a:
                self.Ai_who = cell.pos
                print("[GAME] : AI " + str(self.Ai_who))
                if cell.type.mov > 0:
                    target = [-1, None, []]
                    dis = -1
                    enemy_path = []
                    for cell2 in self.table.node_table:
                        if cell2.type is not None and cell2.type.tag == Ai_b:
                            enemy_path = self.table.Astar(
                                cell.pos, cell2.pos)
                            if enemy_path and (dis > len(enemy_path) or dis == -1):
                                target = [dis, cell2, enemy_path]
                                dis = len(enemy_path)
                    if target[2]:
                        cell = self.Ai_mov(cell, target, Ai_b)
                        print("[GAME] : ASTAR" + str(cell.pos))
                    else:
                        for cell2 in self.table.node_table:
                            if cell2.type is not None and cell2.type.tag == Ai_b:
                                enemy_path = self.table.DEEP(
                                    cell.pos, cell2.pos)
                            if enemy_path and (dis > len(enemy_path) or dis == -1):
                                target = [dis, cell2, enemy_path]
                                dis = len(enemy_path)
                        if target[2]:
                            cell = self.Ai_mov(cell, target, Ai_b)
                            print("[GAME] : DEEP" + str(cell.pos))
                target = self.Ai_attack(cell, Ai_b)
                self.hit_event(target, cell)
        print("-----------------------------")
        self.Ai_who = []
        self.Ai_target = []
        self.phase = ""

    def hit_event(self, target, attacker):
        if target is not None and attacker.type.hit > 0:
            print("[GAME] : ATTACK")
            attacker.type.hit -= 1
            result = attacker.type.attack(target.type)
            txt = "MISS"
            txt_pos = [target.pos[0] * self.cell_size,
                        target.pos[1] * self.cell_size]
            if result[0] == 2:
                txt = "CRI" + "-" + str(result[1])
            elif result[0] == 1:
                txt = "-" + str(result[1])
            self.damage_txt.text = txt
            self.damage_txt.x, self.damage_txt.y = txt_pos
            attacker.type.mov = 0
            self.draw()

    def path_draw(self):
        if self.path:
            if self.phase == "MOVE" and self.cur_cell_pos:
                temp = self.table.giveCell(self.cur_cell_pos)
                if temp.type is not None and temp.type.tag is "troop":
                    step = copy.deepcopy(temp.type.mov)
                    for way in self.path:
                        s = pygame.Surface([self.cell_size, self.cell_size])
                        s.set_alpha(100)
                        if step >= 0:
                            s.fill([100, 225, 0])
                            step -= 1
                        else:
                            s.fill([255, 0, 0])
                        self.screen.blit(
                            s, (way[0] * self.cell_size, way[1] * self.cell_size))
            elif self.phase == "ATTACK" and self.cur_cell_pos:
                temp = self.table.giveCell(self.cur_cell_pos)
                for way in self.path:
                    s = pygame.Surface([self.cell_size, self.cell_size])
                    s.set_alpha(100)
                    if temp.type.hit > 0:
                        s.fill([0, 225, 0])
                        if self.table.giveCell(way).type is not None:
                            s.fill([0, 0, 255])
                    else:
                        s.fill([255, 0, 0])
                    self.screen.blit(
                        s, (way[0] * self.cell_size, way[1] * self.cell_size))

    def unit_draw(self):
        for cell in self.table.node_table:
            if cell.type is not None:
                if cell.type.name == "c1":
                    self.screen.blit(self.image_list[0], [
                                     cell.pos[0] * self.cell_size, cell.pos[1] * self.cell_size])
                elif cell.type.name == "orc1":
                    self.screen.blit(self.image_list[1], [
                                     cell.pos[0] * self.cell_size, cell.pos[1] * self.cell_size])
                elif cell.type.name == "ogr1":
                    self.screen.blit(self.image_list[2], [
                                     cell.pos[0] * self.cell_size, cell.pos[1] * self.cell_size])
                elif cell.type.name == "troll1":
                    self.screen.blit(self.image_list[3], [
                                     cell.pos[0] * self.cell_size, cell.pos[1] * self.cell_size])
                if cell.type.mov <= 0 and cell.type.hit <= 0:
                    s = pygame.Surface([self.cell_size, self.cell_size])
                    s.set_alpha(100)
                    s.fill([0, 0, 0])                    
                    self.screen.blit(s, (cell.pos[0] * self.cell_size, cell.pos[1] * self.cell_size))
                x = cell.pos[0] * self.cell_size
                y = cell.pos[1] * self.cell_size + self.cell_size*3/4
                pygame.draw.rect(self.screen, [0, 0, 0], [
                                 cell.pos[0] * self.cell_size, cell.pos[1] * self.cell_size, self.cell_size, self.cell_size], 2)
                pygame.draw.rect(self.screen, [0, 0, 0], [
                                 x, y, self.cell_size, self.cell_size/4])
                pygame.draw.rect(self.screen, [255, 0, 0], [
                                 x, y, cell.type.hp/cell.type.max_hp * self.cell_size, self.cell_size/4])
                pygame.draw.rect(self.screen, [0, 0, 0], [
                                 x, y, self.cell_size, self.cell_size/4], 2)

    def mouse_draw(self):
        mouse = pygame.mouse.get_pos()
        if self.table_size[0] > mouse[0] > 0 and self.table_size[1] > mouse[1] > 0:
            mouse = [mouse[0] // self.cell_size, mouse[1] // self.cell_size]
            mouse = [mouse[0] * self.cell_size, mouse[1] * self.cell_size]
            pygame.draw.rect(self.screen, [255, 255, 255], [
                             mouse[0], mouse[1], self.cell_size, self.cell_size], 5)

    def information_draw(self):
        if self.click_cell_pos:
            temp = self.table.giveCell(self.click_cell_pos)
            if temp.type is not None:
                txt = "Name : " + str(temp.type.name) \
                    + "\n hp : " + str(temp.type.hp) + "/" + str(temp.type.max_hp)\
                    + "\n hit : " + str(temp.type.hit) + "/" + str(temp.type.max_hit)\
                    + "\n atk : " + str(temp.type.atk) + "\n dep : " + str(temp.type.dep)\
                    + "\n spd : " + str(temp.type.spd) + "\n luk: " + str(temp.type.luk)\
                    + "\n mov : " + str(temp.type.mov) + "/" + str(temp.type.max_mov)\
                    + "\n ran" + str(temp.type.ran)
                self.ttxt.text = txt
            self.ttxt.draw()

    def draw(self):
        self.map_draw()
        if self.deploy == True:
            s = pygame.Surface([self.cell_size * 3, 600])
            s.set_alpha(150)
            s.fill([255, 69, 0])
            self.screen.blit(s, (0, 0))
            for btn in self.btn2_list:
                btn.draw()
                if self.phase == btn.name:
                    pygame.draw.rect(self.screen, [255, 0, 0], [
                                     btn.x, btn.y, btn.w, btn.h], 5)
        else:
            for btn in self.btn_list:
                btn.draw()
                if self.phase == btn.name:
                    pygame.draw.rect(self.screen, [255, 0, 0], [
                                     btn.x, btn.y, btn.w, btn.h], 5)
        self.unit_draw()
        self.Ai_turn_draw(self.Ai_who, self.Ai_target)
        self.path_draw()
        self.mouse_draw()
        self.information_draw()
        if self.cur_cell_pos:
            pygame.draw.rect(self.screen, [200, 215, 0], [self.cur_cell_pos[0] * self.cell_size,
                             self.cur_cell_pos[1] * self.cell_size, self.cell_size, self.cell_size], 5)
        if self.damage_txt.text is not "":
            self.damage_txt.draw()
            pygame.display.flip()
            pygame.time.wait(500)
            self.damage_txt.text = ""
        if self.turn_image.text is not "":
            self.turn_image.draw()
            pygame.time.wait(100)
            self.turn_image.text = ""
        self.death_check_event()
        pygame.display.flip()
