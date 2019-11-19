import heapq

# from .label import Label


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


class Solver:
    def __init__(self, maze):
        self.maze = maze
        self.visited = {self.maze.start: None}
        self.path = []
        # self.counter = 1
        self.done = False
        # self.labels = [Label(str(self.counter), self.maze.font_size,
        #                center=(self.maze.get_position_at(self.maze.start)))]

    def get_frontier_cells(self):
        return self.frontier

    def build_path(self):
        self.done = True
        current_cell = self.maze.finish
        while current_cell != self.maze.start:
            self.path.append(current_cell)
            current_cell = self.visited[current_cell]
        self.path.append(self.maze.start)


class BFS(Solver):
    def __init__(self, maze):
        Solver.__init__(self, maze)
        self.frontier = [self.maze.start]

    def step(self):
        if self.done or not self.frontier:
            return
        current_cell = self.frontier.pop(0)
        if current_cell == self.maze.finish:
            self.build_path()
            return
        for next_cell in self.maze.get_neighbors(current_cell):
            if next_cell not in self.visited:
                self.frontier.append(next_cell)
                self.visited[next_cell] = current_cell
                # self.counter += 1
                # label = Label(str(self.counter), self.maze.font_size,
                #               center=(self.maze.get_position_at(next_cell)))
                # self.labels.append(label)


class Dijkstra(Solver):
    def __init__(self, maze):
        Solver.__init__(self, maze)
        self.cost_so_far = {self.maze.start: 0}
        self.frontier = PriorityQueue()
        self.frontier.put(self.maze.start, 0)

    def step(self):
        if self.done or not self.frontier:
            return
        current_cell = self.frontier.get()
        if current_cell == self.maze.finish:
            self.build_path()
            return
        for next_cell in self.maze.get_neighbors(current_cell):
            new_cost = self.cost_so_far[current_cell] + 1
            if (next_cell not in self.cost_so_far
                    or new_cost < self.cost_so_far[next_cell]):
                self.cost_so_far[next_cell] = new_cost
                self.visited[next_cell] = current_cell
                # self.counter += 1
                priority = new_cost
                self.frontier.put(next_cell, priority)
                # label = Label(str(self.counter), self.maze.font_size,
                #               center=(self.maze.get_position_at(next_cell)))
                # self.labels.append(label)

    def get_frontier_cells(self):
        return [cell for (_, cell) in self.frontier.elements]


class AStar(Dijkstra):
    def step(self):
        if self.done or not self.frontier:
            return
        current_cell = self.frontier.get()
        if current_cell == self.maze.finish:
            self.build_path()
            return
        for next_cell in self.maze.get_neighbors(current_cell):
            new_cost = self.cost_so_far[current_cell] + 1
            if (next_cell not in self.cost_so_far
                    or new_cost < self.cost_so_far[next_cell]):
                self.cost_so_far[next_cell] = new_cost
                self.visited[next_cell] = current_cell
                # self.counter += 1
                priority = new_cost + heuristic(self.maze.finish, next_cell)
                self.frontier.put(next_cell, priority)
                # label = Label(str(self.counter), self.maze.font_size,
                #               center=(self.maze.get_position_at(next_cell)))
                # self.labels.append(label)


class DFS(BFS):
    def step(self):
        if self.done or not self.frontier:
            return
        current_cell = self.frontier.pop()
        if current_cell == self.maze.finish:
            self.build_path()
            return
        for next_cell in self.maze.get_neighbors(current_cell):
            if next_cell not in self.visited:
                self.frontier.append(next_cell)
                self.visited[next_cell] = current_cell
                # self.counter += 1
                # label = Label(str(self.counter), self.maze.font_size,
                #               center=(self.maze.get_position_at(next_cell)))
                # self.labels.append(label)
