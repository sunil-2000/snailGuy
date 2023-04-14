import numpy as np

class Map:
    def __init__(self, x_lim, y_lim):
        self.x_lim = x_lim; self.y_lim = y_lim
    
    def generate_boarder(self):
        board_coords = []
        for i in range(self.y_lim+1):
            board_coords.append((i, 0))
        for j in range(self.x_lim+1):
            board_coords.append((self.y_lim, j))
        for j in range(self.y_lim+1):
            board_coords.append((self.y_lim-j, self.x_lim))
        for j in range(self.x_lim+1):
            board_coords.append((0, self.x_lim-j))

        return board_coords

    def generate_obstacles(self, size=50):
        x_obs = np.random.randint(0, self.x_lim-1, size=size)
        y_obs = np.random.randint(0, self.y_lim-1, size=size)
        self.x_obs = x_obs
        self.y_obs = y_obs
        return [y_obs, x_obs]
    
    def generate_objective(self):
        assert self.x_obs and self.y_obs # defined
        
        x = np.random.randint(0, self.x_lim-1, size=1)
        y = np.random.randint(0, self.y_lim-1, size=1)
        
        while x in self.x_obs and y in self.y_obs:
          x = np.random.randint(0, self.x_lim-1, size=1)
          y = np.random.randint(0, self.y_lim-1, size=1)
        
        self.x_tr = x
        self.y_tr = y
        return y, x
    