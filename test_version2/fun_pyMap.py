import fun_pyCell
import fun_pyMap
import numpy as np
import fun_pyCharacter
import copy
import os

enemy = { 
        1:fun_pyCharacter.character("orc1",5,1,2,1,1,1,3,1,"orc1.png","orc1.png","enemy", "FOX"),\
        2:fun_pyCharacter.character("ogr1",7,2,3,1,1,1,3,1,"ogr1.png","org1.png","enemy", "FOX"),\
        3:fun_pyCharacter.character("troll1",4,2,2,0,1,1,4,2,"troll1.png","troll1.png","enemy", "FOX")}

troop = {
        "Footman":fun_pyCharacter.character("Footman",5,1,2,1,1,1,3,1,"c1.png","c1.png","troop", "FOX"),\
        "Archer":fun_pyCharacter.character("Archer",5,1,2,1,2,1,3,2,"c2.png","c2.png","troop", "FOX"),\
        "Peasant":fun_pyCharacter.character("Peasant",4,2,1,0,1,1,3,1,"c3.png","c3.png","troop", "FOX")}

def army_txt_import(txt):
    file = open(txt, "r")
    temp = file.read().splitlines()
    army = []
    money = int(temp[0])
    for i in range(1, len(temp)):
        army.append(str(temp[i]))
    file.close()
    army.sort()
    return [money, army]

def army_txt_export(txt, army, money):
    file = open(txt, "w")
    file.write(str(money) + "\n")
    for temp in army:
        file.write(str(temp) + "\n")
    file.close()

def map_load_for_game(map_name):
    tile_map = []
    obj_map = []
    img_map = []
    enemy_map = []
    etc_map = []
    [tile_map_size, tile_map, obj_map,
    img_map, enemy_map, etc_map] = fun_pyMap.map_txt_import(map_name)
    table = fun_pyMap.map2cell(
        tile_map_size[0], tile_map_size[1], tile_map, obj_map, enemy_map, etc_map)
    return tile_map, img_map, table

def map2cell(cols, rows, tile_map, obj_map, enemy_map, etc_map):
    table = fun_pyCell.Cell_Table(cols, rows)
    for j in range(0,table.rows):
        for i in range(0,table.cols):
            index = table.cols * j + i
            if tile_map[i][j] == 0 or obj_map[i][j] != 0:
                table.node_table[index].obstacle = True
                if obj_map[i][j] == 1:
                    table.node_table[index].block = True
            if etc_map[i][j] == 1:
                table.node_table[index].status = "deploy"
            elif etc_map[i][j] == 2:
                table.node_table[index].status = "goal"
            temp = enemy_map[i][j]
            if temp > 0:
                table.node_table[index].type = copy.deepcopy(enemy[temp])
                table.node_table[index].block = True
    return table

def map_txt_import(txt):
    cur_path = os.path.dirname(__file__)
    source_path = os.path.join(cur_path, txt)
    file = open(source_path, "r")
    line = file.readline()
    data = line.split(",")
    tile_size = [int(data[0]), int(data[1])]
    tile_map = np.zeros(tile_size)
    obj_map = np.zeros(tile_size)
    img_map = np.zeros(tile_size)
    enemy_map = np.zeros(tile_size)
    etc_map = np.zeros(tile_size)
    j = 0
    while True:
        line = file.readline()
        data = line.split(",")
        if line == "":
            break
        for i, txt in enumerate(data):
            data2 = txt.split(":")
            tile_map[i][j] = int(data2[0])
            obj_map[i][j] = int(data2[1])
            img_map[i][j] = int(data2[2])
            enemy_map[i][j] = int(data2[3])
            etc_map[i][j] = int(data2[4])
        j += 1
        if not line:
            break
    file.close()
    return [tile_size, tile_map, obj_map, img_map, enemy_map, etc_map]

def map_txt_export(txt, tile_map_size, tile_map, obj_map, img_map, enemy_map, etc_map):
    cur_path = os.path.dirname(__file__)
    source_path = os.path.join(cur_path, txt)
    file = open(source_path, "w")
    file.write(str(tile_map_size[0]) + str(",") + str(tile_map_size[1]) + str("\n"))
    for j in range(0, tile_map_size[1]):
        for i in range(0, tile_map_size[0]):
            txt = str(int(tile_map[i][j])) + ":" + str(int(obj_map[i][j])) + ":"\
                 + str(int(img_map[i][j]))+ ":" + str(int(enemy_map[i][j])) + ":" + str(int(etc_map[i][j]))
            file.write(txt)
            if i is not tile_map_size[0]-1:
                file.write(",")
        if j is not tile_map_size[1]-1:
            file.write("\n")
    file.close()