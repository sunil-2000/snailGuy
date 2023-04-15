from grid import Map
from functools import lru_cache

class Algo(Map):
    def __init__(self, y_lim, x_lim, start, n_obstacles=50):
        super().__init__(y_lim, x_lim)
        self.generate_boarder()
        self.generate_obstacles(size=n_obstacles)
        self.generate_objective()
        self.start = start
        self.path_seq = []

    @lru_cache(maxsize=None)
    def _dfs(self, y, x):
        """
        move constrained to following space: [1, y_lim-1]; [1, x_lim-1]
        """
        def obs_check(y, x):
            if self.grid[y][x] < 0 or self.grid[y][x] == 1: # obstacle or boarder
                return False
            return True 

        stack = [(y, x)]
        while stack:
            # print(stack)
            i, j = stack.pop(-1)
            self.path_seq.append((i,j))

            if self.grid[i][j] == 2:
               return True 
            self.grid[i][j] = -1
            # down
            if i + 1 <= self.y_lim - 1 and obs_check(i+1, j): 
              stack.append((i+1, j))
            # up
            if i - 1 >= 1 and obs_check(i-1, j):
              stack.append((i-1, j))
            # left
            if j - 1 >= 1 and obs_check(i, j-1):
              stack.append((i, j-1))
            # right
            if i + 1 <= self.x_lim -1 and obs_check(i, j+1):
              stack.append((i, j+1))
        return False

    def compute_path(self):
        self.reached = self._dfs(self.start[0], self.start[1])