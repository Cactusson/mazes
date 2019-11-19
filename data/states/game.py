import pygame as pg

from .. import prepare, state_machine
from ..components import data
from ..components.button import Button
from ..components.label import Label
from ..components.maze import Maze
from ..components.task import Task
from ..components.toggle_button import GroupButton, ToggleButton
from ..components.solver import AStar, BFS, DFS, Dijkstra


class Game(state_machine._State):
    def startup(self, persistant):
        self.tasks = pg.sprite.Group()
        self.solver = None
        self.create_buttons()
        self.generate_maze(10, 10)
        self.auto_step_active = False
        self.bg = self.create_bg()
        self.labels = self.create_labels()

    def generate_maze(self, width, height):
        self.maze = Maze(width, height)
        if not self.solver:
            self.solver = BFS(self.maze)
        else:
            self.solver = self.solver.__class__(self.maze)

    def create_buttons(self):
        button10 = Button('10x10', (1075, 100), self.generate_maze, 40, 10, 10)
        button20 = Button('20x20', (1200, 100), self.generate_maze, 40, 20, 20)
        button30 = Button('30x30', (1325, 100), self.generate_maze, 40, 30, 30)
        button40 = Button('40x40', (1450, 100), self.generate_maze, 40, 40, 40)
        dfs = GroupButton('DFS', (1075, 250), self.change_solver, 50, DFS)
        bfs = GroupButton('BFS', (1200, 250), self.change_solver, 50, BFS)
        dijkstra = GroupButton(
            'Dijkstra', (1325, 250), self.change_solver, 50, Dijkstra)
        astar = GroupButton('A*', (1500, 250), self.change_solver, 50, AStar)
        step = Button('STEP', (1150, 350), self.step, 75)
        fast = ToggleButton('FAST', (1350, 350), self.toggle_auto_step, 75)
        self.buttons = [button10, button20, button30, button40, dfs, bfs,
                        dijkstra, astar, step, fast]
        self.solver_buttons = [dfs, bfs, dijkstra, astar]
        bfs.activate()

    def create_bg(self):
        bg = pg.Surface(prepare.SCREEN_SIZE).convert()
        bg.fill(data.BG_COLOR)
        pg.draw.line(bg, pg.Color('black'), (1100, 165), (1525, 165), 2)
        pg.draw.line(bg, pg.Color('black'), (1100, 325), (1525, 325), 2)
        labels = self.create_labels()
        for label in labels:
            label.draw(bg)
        pg.draw.rect(bg, data.WALL_COLOR, (1125, 675, 35, 35))
        pg.draw.rect(bg, data.EMPTY_COLOR, (1125, 750, 35, 35))
        pg.draw.rect(bg, data.VISITED_COLOR, (1125, 825, 35, 35))
        pg.draw.rect(bg, data.FRONTIER_COLOR, (1125, 900, 35, 35))
        return bg

    def create_labels(self):
        maze = Label('Generate a maze:', 40, topleft=(1075, 50))
        algorithm = Label('Choose an algorithm:', 40, topleft=(1075, 200))
        legend = Label('Legend:', 40, topleft=(1075, 600))
        wall = Label('wall', 35, topleft=(1200, 675))
        empty = Label('empty (not visited)', 35, topleft=(1200, 750))
        visited = Label('visited', 35, topleft=(1200, 825))
        frontier = Label('frontier (about to visit)', 35, topleft=(1200, 900))
        return [maze, algorithm, legend, wall, empty, visited, frontier]

    def change_solver(self, solver):
        for button in self.solver_buttons:
            if solver not in button.args:
                button.deactivate()
        self.solver = solver(self.maze)

    def toggle_auto_step(self):
        self.auto_step_active = not self.auto_step_active
        if self.auto_step_active:
            self.tasks.add(Task(self.step, 50, -1))
        else:
            self.tasks.empty()

    def step(self):
        self.solver.step()

    def edit_maze(self, point):
        cell = self.maze.get_cell_at(point)
        if cell is None:
            return
        if self.maze.maze_map[cell[0]][cell[1]] == 0:
            self.maze.maze_map[cell[0]][cell[1]] = 1
        else:
            self.maze.maze_map[cell[0]][cell[1]] = 0

    def get_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in self.buttons:
                    button.click()
                self.edit_maze(event.pos)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                self.generate_maze(10, 10)
            elif event.key == pg.K_2:
                self.generate_maze(20, 20)
            elif event.key == pg.K_3:
                self.generate_maze(30, 30)
            elif event.key == pg.K_4:
                self.generate_maze(40, 40)
            elif event.key == pg.K_SPACE:
                self.solver.step()

    def draw(self, surface):
        surface.blit(self.bg, (0, 0))
        self.maze.draw(self.solver, surface)
        for button in self.buttons:
            button.draw(surface)

    def update(self, surface, dt):
        self.tasks.update(dt * 1000)
        for button in self.buttons:
            button.update()
        self.draw(surface)
