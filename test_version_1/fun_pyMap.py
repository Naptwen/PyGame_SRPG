import fun_pyCell
import numpy as np
import fun_pyCharacter
import copy

enemy = { 
        1:fun_pyCharacter.character("orc1",5,1,2,1,1,1,3,1,"orc1.png","orc1.png","enemy"),\
        2:fun_pyCharacter.character("ogr1",7,2,3,1,1,1,3,1,"ogr1.png","org1.png","enemy"),\
        3:fun_pyCharacter.character("troll1",4,2,2,0,1,1,4,2,"troll1.png","troll1.png","enemy")}

def map2cell(cols, rows, tile_map, obj_map, enemy_map):
    table =  fun_pyCell.Cell_Table(cols, rows)
    for j in range(0,table.rows):
        for i in range(0,table.cols):
            index = table.cols * j + i
            if tile_map[i][j] == 0 or obj_map[i][j] != 0:
                table.node_table[index].obstacle = True
                if obj_map[i][j] == 1:
                    table.node_table[index].block = True
            temp = enemy_map[i][j]
            if temp > 0:
                table.node_table[index].type = copy.deepcopy(enemy[temp])
                table.node_table[index].block = True
    return table

def map_txt_import(txt):
    file = open(txt, "r")
    line = file.readline()
    data = line.split(",")
    tile_size = [int(data[0]), int(data[1])]
    tile_map = np.zeros(tile_size)
    obj_map = np.zeros(tile_size)
    img_map = np.zeros(tile_size)
    enemy_map = np.zeros(tile_size)
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
        j += 1
        if not line:
            break
    file.close()
    return [tile_size, tile_map, obj_map, img_map, enemy_map]

def map_txt_export(txt, tile_map_size, tile_map, obj_map, img_map, enemy_map):
    file = open(txt, "w")
    file.write(str(tile_map_size[0]) + str(",") + str(tile_map_size[1]) + str("\n"))
    for j in range(0, tile_map_size[1]):
        for i in range(0, tile_map_size[0]):
            txt = str(int(tile_map[i][j])) + ":" + str(int(obj_map[i][j])) + ":" + str(int(img_map[i][j]))+ ":" + str(int(enemy_map[i][j]))
            file.write(txt)
            if i is not tile_map_size[0]-1:
                file.write(",")
        if j is not tile_map_size[1]-1:
            file.write("\n")
    file.close()