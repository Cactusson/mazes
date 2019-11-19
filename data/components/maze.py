import pygame as pg
import random

from . import data


def generate_maze(width, height):
    mx = width
    my = height  # width and height of the maze
    maze = [[1 for x in range(mx)] for y in range(my)]
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]  # 4 directions to move in the maze
    # start the maze from a random cell
    cx = random.randint(0, mx - 1)
    cy = random.randint(0, my - 1)
    maze[cy][cx] = 0
    stack = [(cx, cy, 0)]  # stack element: (x, y, direction)

    while len(stack) > 0:
        (cx, cy, cd) = stack[-1]
        # to prevent zigzags:
        # if changed direction in the last move then cannot change again
        if len(stack) > 2:
            if cd != stack[-2][2]:
                dirRange = [cd]
            else:
                dirRange = range(4)
        else:
            dirRange = range(4)

        # find a new cell to add
        nlst = []  # list of available neighbors
        for i in dirRange:
            nx = cx + dx[i]
            ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                if maze[ny][nx] == 1:
                    ctr = 0  # of occupied neighbors must be 1
                    for j in range(4):
                        ex = nx + dx[j]
                        ey = ny + dy[j]
                        if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                            if maze[ey][ex] == 0:
                                ctr += 1
                    if ctr == 1:
                        nlst.append(i)

        # if 1 or more neighbors available then randomly select one and move
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]
            cy += dy[ir]
            maze[cy][cx] = 0
            stack.append((cx, cy, ir))
        else:
            stack.pop()

    count_block = 0
    for row in maze:
        for elem in row:
            if elem == 1:
                count_block += 1

    blocks_to_delete = random.randint(count_block // 30, count_block // 20)
    for _ in range(blocks_to_delete):
        get_cell(maze, 0, 1)

    maze.insert(0, [1] * width)
    maze.append([1] * width)
    for row in maze:
        row.insert(0, 1)
        row.append(1)

    # print('Maze done')
    # for row in maze:
    #     print(row)
    return maze


def get_cell(maze, number_to, number_from=None):
    if number_from is None:
        number_from = 0
    while True:
        row = random.randint(0, len(maze) - 1)
        col = random.randint(0, len(maze) - 1)
        if maze[row][col] == number_from:
            maze[row][col] = number_to
            return row, col


class Maze:
    def __init__(self, width, height):
        self.start = (1, 1)
        self.finish = (width, height)
        while True:
            self.maze_map = generate_maze(width, height)
            if (self.maze_map[self.start[0]][self.start[1]] == 0
                    and self.maze_map[self.finish[0]][self.finish[1]] == 0):
                break
        self.cell_size = min(65, 1000 // (width + 2))
        self.topleft = (15, 15)
        # self.font_size = 20 - (width // 10) * 2

    def get_neighbors(self, cell):
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = [(cell[0] + row_offset, cell[1] + col_offset) for
                     (row_offset, col_offset) in offsets]
        return [cell for cell in neighbors
                if self.maze_map[cell[0]][cell[1]] == 0]

    def get_position_at(self, point):
        return (self.topleft[1] + self.cell_size * (point[1] + 0.5),
                self.topleft[0] + self.cell_size * (point[0] + 0.5))

    def get_cell_at(self, point):
        row = (point[0] - self.topleft[0]) // self.cell_size
        col = (point[1] - self.topleft[1]) // self.cell_size
        if (row < 1 or row > len(self.maze_map) - 2 or col < 1
                or col > len(self.maze_map) - 2):
            return None
        return col, row

    def draw(self, solver, surface):
        for row_num in range(len(self.maze_map)):
            for col_num in range(len(self.maze_map[row_num])):
                rect = pg.rect.Rect(0, 0, self.cell_size, self.cell_size)
                rect.topleft = (self.topleft[0] + col_num * self.cell_size,
                                self.topleft[1] + row_num * self.cell_size)
                if self.maze_map[row_num][col_num] == 1:
                    surface.fill(data.WALL_COLOR, rect)
                elif (row_num, col_num) in solver.path:
                    surface.fill(data.PATH_COLOR, rect)
                elif (row_num, col_num) in solver.get_frontier_cells():
                    surface.fill(data.FRONTIER_COLOR, rect)
                elif (row_num, col_num) in solver.visited:
                    surface.fill(data.VISITED_COLOR, rect)
                else:
                    surface.fill(data.EMPTY_COLOR, rect)
        # for label in solver.labels:
        #     label.draw(surface)
