from grid import Map
from functools import lru_cache
import numpy as np

class Algo(Map):
    def __init__(self, y_lim, x_lim, start, n_obstacles=50, questions=[]):
        super().__init__(y_lim, x_lim)
        self.generate_boarder()
        self.generate_obstacles(size=n_obstacles)
        self.generate_objective()
        self.chat_start = (y_lim, 0)
        self.start = start
        self.path_seq = []

        self.questions = questions
        
        # divide 2D space into k partitions where each partition is a 2D space
        A = (y_lim * x_lim) // len(questions) # area of partition
        a_h, a_w = 2, A // 2
        self.q_map = [[-1 for _ in range(x_lim)] for _ in range(y_lim)]
        
        i, j = 0, 0
        for k in range(len(questions)):
          print(i)
          for y in range(i, i + a_h+1, 1): # i, j, upper-left expand partition each iter
            for x in range(j, j + a_w+1, 1):
              if y < y_lim and  x < x_lim:
                self.q_map[y][x] = k
          if j + a_w <= x_lim:
             j += a_w  
          else:
             i += a_h
             j = 0

        for i in range(y_lim):
           for j in range(x_lim):
              if self.q_map < 0:
                 choice = np.random.randint(low=0, high=len(questions))
                 self.q_map[i][j] = choice
        
        # permute questions
        self.questions = np.random.permutation(self.questions)

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
    
    def converse(self, i):
       y, x = self.path_seq[i]
       print(self.y_lim, self.x_lim)
       print(y, x, (y * self.x_lim) + (x % self.x_lim))
       q_idx = (y * self.x_lim + (x % self.x_lim)) % len(self.questions)
       input_q = self.questions[q_idx]
       print(input_q)
       # plass call to GPT with input_q

       pass

algo = Algo(13, 17, n_obstacles=1, start=(1,1), questions=['1' for i in range(20)])
algo.compute_path()
# for i in range(len(algo.path_seq)):
#   algo.converse(i)

