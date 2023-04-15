import numpy as np

class Map:
    def __init__(self, y_lim, x_lim):
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.grid = [[0 for _ in range(x_lim)] for _ in range(y_lim)] # index by (y,x)
        self.grid[0] = [1] * x_lim
        self.grid[-1] = [1] * x_lim

        for row in self.grid:
            row[0] = 1
            row[-1] = 1

    def generate_boarder(self):
        board_coords = []
        for i in range(self.y_lim):
            board_coords.append((i, 0))
        for j in range(self.x_lim):
            board_coords.append((self.y_lim, j))
        for j in range(self.y_lim):
            board_coords.append((self.y_lim-j, self.x_lim))
        for j in range(self.x_lim):
            board_coords.append((0, self.x_lim-j))

        self.board_coords = board_coords

    def generate_obstacles(self, size=50):
        x_obs = np.random.randint(low=1, high=self.x_lim-1, size=size)
        y_obs = np.random.randint(low=1, high=self.y_lim-1, size=size)
        self.obstacles = [y_obs, x_obs]
        # update internal ds
        for y, x in zip(y_obs, x_obs):
            self.grid[y][x] = -1
    
    def generate_objective(self):
        x = np.random.randint(low=1, high=self.x_lim-1, size=1)
        y = np.random.randint(low=1, high=self.y_lim-1, size=1)

        while x in self.obstacles[1] and y in self.obstacles[0]:
          x = np.random.randint(low=1, high=self.x_lim-1, size=1)
          y = np.random.randint(low=1, high=self.y_lim-1, size=1)
        
        self.grid[y[0]][x[0]] = 2
        self.target = (y[0], x[0])
