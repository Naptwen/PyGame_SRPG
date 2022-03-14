import numpy as np
import copy


def merge(map, map_size, paint, img, img_map):
    img_map = copy.deepcopy(img_map)
    for i in range(0, map_size[0]):
        for j in range(0, map_size[1]):
            if map[i][j] == paint:
                left = False
                right = False
                up = False
                down = False
                if i - 1 >= 0:
                    if map[i - 1, j] == paint:
                        left = True
                if j - 1 >= 0:
                    if map[i, j - 1] == paint:
                        up = True
                if i + 1 < map_size[0]:
                    if map[i + 1, j] == paint:
                        right = True
                if j + 1 < map_size[1]:
                    if map[i, j + 1] == paint:
                        down = True
                direction = [left, right, up, down]
                if direction == [0, 0, 0, 0]:  # none
                    img_map[i][j] = img[0]
                elif direction == [1, 0, 0, 0]:  # left
                    img_map[i][j] = img[1]
                elif direction == [0, 1, 0, 0]:  # right
                    img_map[i][j] = img[2]
                elif direction == [0, 0, 1, 0]:  # up
                    img_map[i][j] = img[3]
                elif direction == [0, 0, 0, 1]:  # down
                    img_map[i][j] = img[4]
                elif direction == [1, 1, 0, 0]:  # -
                    img_map[i][j] = img[5]
                elif direction == [0, 0, 1, 1]:  # |
                    img_map[i][j] = img[6]
                elif direction == [1, 0, 1, 0]:  # ┛
                    img_map[i][j] = img[7]
                elif direction == [1, 0, 0, 1]:  # ┓
                    img_map[i][j] = img[8]
                elif direction == [0, 1, 1, 0]:  # ┗
                    img_map[i][j] = img[9]
                elif direction == [0, 1, 0, 1]:  # ┏
                    img_map[i][j] = img[10]
                elif direction == [1, 1, 1, 0]:  # ┻
                    img_map[i][j] = img[11]
                elif direction == [1, 1, 0, 1]:  # ┳
                    img_map[i][j] = img[12]
                elif direction == [1, 0, 1, 1]:  # ┨
                    img_map[i][j] = img[13]
                elif direction == [0, 1, 1, 1]:  # ┝
                    img_map[i][j] = img[14]
                elif direction == [1, 1, 1, 1]:  # ╋
                    img_map[i][j] = img[15]
    return img_map


def painting(tile_map, tile_map_size, cell_pos, bucket, paint):
    if bucket == False:
        tile_map[cell_pos[0]][cell_pos[1]] = paint
    else:
        if tile_map[cell_pos[0]][cell_pos[1]] != paint:
            open_list = []
            open_list.append([cell_pos[0], cell_pos[1]])
            orin_paint = tile_map[cell_pos[0]][cell_pos[1]]
            while open_list:
                temp = open_list.pop()
                tile_map[temp[0]][temp[1]] = paint
                if temp[0] - 1 >= 0:
                    if tile_map[temp[0] - 1, temp[1]] == orin_paint:
                        open_list.append([temp[0] - 1, temp[1]])
                if temp[1] - 1 >= 0:
                    if tile_map[temp[0], temp[1] - 1] == orin_paint:
                        open_list.append([temp[0], temp[1] - 1])
                if temp[0] + 1 < tile_map_size[0]:
                    if tile_map[temp[0] + 1, temp[1]] == orin_paint:
                        open_list.append([temp[0] + 1, temp[1]])
                if temp[1] + 1 < tile_map_size[1]:
                    if tile_map[temp[0], temp[1] + 1] == orin_paint:
                        open_list.append([temp[0], temp[1] + 1])


class NODE(object):
    pos = []
    neigh = []
    price = -1  # -1 means no prcie marked
    parent = -1  # -1 means no parent node marked
    dis = 1  # the connection between nodes
    check = False  # for checking
    obstacle = False
    block = False
    type = None
    status = None


class Cell_Table:
    rows = 0
    cols = 0
    node_table = []

    def __init__(self, cols, rows):
        for j in range(0, rows):
            for i in range(0, cols):
                __node = NODE()
                __node.pos = [i, j]
                __node.neigh = []
                if j - 1 >= 0:
                    __node.neigh.append((j - 1) * cols + i)
                if j + 1 < rows:
                    __node.neigh.append((j + 1) * cols + i)
                if i - 1 >= 0:
                    __node.neigh.append(j * cols + (i - 1))
                if i + 1 < cols:
                    __node.neigh.append(j * cols + (i + 1))
                __node.dis = 1
                __node.price = -1
                __node.parent = -1
                __node.check = False
                __node.obstacle = False
                self.node_table.append(__node)
        self.rows = rows
        self.cols = cols

    def giveCell(self, cell):
        if cell:
            if len(self.node_table) > self.cols * cell[1] + cell[0] >= 0:
                return self.node_table[self.cols * cell[1] + cell[0]]
        return None
    # return 2D array list

    def Astar(self, start, end):
        self.clearCell()
        que = []
        start_index = self.cols * start[1] + start[0]  # convert coordinates in index
        end_index = self.cols * end[1] + end[0]  # convert coordinates in index
        if end[1] > self.rows or end[0] > self.cols or start[1] > self.rows or start[0] > self.cols or end[1] < 0 or end[0] < 0 or start[1] < 0 or start[0] < 0:
            return []
        else:
            que.append(start_index)
            # finding connected nodes
            trial = 0
            find = False
            _set = False
            if self.node_table[end_index].block:
                self.node_table[end_index].block = False
                _set = True
            while len(que) > 0:
                trial = trial + 1
                parent = que.pop(0)  # pop the first index
                if parent == end_index:
                    find = True
                    break
                # find the neighbor indices
                neigh = self.node_table[parent].neigh
                for child in neigh:
                    # total price
                    new_price = self.node_table[child].dis + \
                        self.node_table[parent].price
                    # if price is less than given
                    if self.node_table[child].price == -1 or new_price < self.node_table[child].price:
                        # change price
                        self.node_table[child].price = new_price
                        # change its parent
                        self.node_table[child].parent = parent
                    if self.node_table[child].check is False and self.node_table[child].obstacle is False \
                        and self.node_table[child].block is False:
                        que.append(child)
                    self.node_table[child].check = True
            if _set:  # get back the block status
                self.node_table[end_index].block = True
            if find is True:
                way_list = []
                back = end_index
                way_list.append(self.node_table[back].pos)
                while back != start_index:  # until end at the start_index
                    back = self.node_table[back].parent
                    # node list of optimazation path in coordinates
                    way_list.append(self.node_table[back].pos)
                reverse_list = []
                if _set and way_list:  # since the end is block, erase the end point
                    way_list.pop(0)
                for way in way_list[::-1]:
                    reverse_list.append(way)
                return reverse_list
            else:
                return []

    def DEEP(self, start, end):
        self.clearCell()
        start_index = self.cols * start[1] + start[0]  # convert coordinates in index
        end_index = self.cols * end[1] + end[0]  # convert coordinates in index
        if end[1] > self.rows or end[0] > self.cols or start[1] > self.rows or start[0] > self.cols or end[1] < 0 or end[0] < 0 or start[1] < 0 or start[0] < 0:
            return []     
        else:
            self.node_table[start_index].price = 99999999999999999999
            close_que = []
            que = []
            que.append(start_index)
            while que:
                parent = que.pop(0)
                if parent == end_index:
                    if self.node_table[parent].obstacle == False and self.node_table[parent].block == False:
                        close_que.append(self.node_table[parent].pos)
                    break
                neigh = self.node_table[parent].neigh
                open_que = {}
                for child in neigh:
                    if self.node_table[child].obstacle == False and self.node_table[child].block == False\
                        and self.node_table[child].price == -1 and not(child == start_index):
                        dis = (self.node_table[child].pos[0] - self.node_table[end_index].pos[0])**2\
                            + (self.node_table[child].pos[1] - self.node_table[end_index].pos[1])**2
                        self.node_table[child].price = dis
                        if self.node_table[child].price < self.node_table[parent].price:
                            open_que[self.node_table[child].price] = child
                if bool(open_que) :
                    min = next(iter(open_que)) 
                    for k, v in open_que.items():
                        if min > k:
                            min = k
                    que.append(open_que[min])
                    close_que.append(open_que[k])
        return_list = []
        for temp in close_que:
            return_list.append(self.node_table[temp].pos)
        return return_list

    def range(self, start, shape, range):
        self.clearCell()
        que = []
        if shape == "circle":
            open_list = []
            start_index = self.cols * start[1] + start[0]
            start_cell = self.node_table[start_index]
            open_list.append(start_cell)
            while open_list:
                start_cell = open_list.pop(0)
                start_cell.check = True
                neigh = start_cell.neigh
                for ng in neigh:
                    temp = self.node_table[ng]
                    if temp.check == False and temp.obstacle == False:
                        start_index = self.cols * \
                            start_cell.pos[1] + start_cell.pos[0]
                        temp.parent = start_index
                        temp.dis += self.node_table[start_index].dis
                        temp.check = True
                        if temp.dis <= range + 1:
                            open_list.append(temp)
                            que.append(temp.pos)
        else:
            for node in self.node_table:
                if (node.pos[0] - start[0])**2 + (node.pos[1] - start[1])**2 < range**2:
                    que.append(node.pos)
        return que

    def checkObstacle(self, x, y):
        index = self.cols * y + x
        return self.node_table[index].obstacle

    def setObstacle(self, bool, x, y):
        index = self.cols * y + x
        self.node_table[index].obstacle = bool

    def swap_cell(self, A_pos, B_pos):
        A = self.cols * A_pos[1] + A_pos[0]
        B = self.cols * B_pos[1] + B_pos[0]
        pA = self.node_table[A]
        pB = self.node_table[B]
        temp_block = copy.deepcopy(pA.block)
        temp_type = copy.deepcopy(pA.type)
        temp_status = copy.deepcopy(pA.status)
        pA.block = copy.deepcopy(pB.block)
        pA.type = copy.deepcopy(pB.type)
        pA.status = copy.deepcopy(pB.status)
        pB.block = copy.deepcopy(temp_block)
        pB.type = copy.deepcopy(temp_type)
        pB.status = copy.deepcopy(temp_status)

    def resetCell(self):
        for node in self.node_table:
            node.price = -1
            node.parent = -1
            node.dis = 1
            node.status = None
            node.check = False
            node.obstacle = False
            node.type = None
            node.block = False

    def clearCell(self):
        for node in self.node_table:
            node.price = -1
            node.parent = -1
            node.dis = 1
            node.check = False
            node.status = None
