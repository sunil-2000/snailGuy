import numpy as np
import openai
from grid import Map
from functools import lru_cache
from private import sk

class Algo(Map):
    def __init__(self, y_lim, x_lim, start, n_obstacles=50, questions="question.txt"):
        super().__init__(y_lim, x_lim)
        openai.api_key = sk
        self.generate_boarder()
        self.generate_obstacles(size=n_obstacles)
        self.generate_objective()
        self.chat_start = (y_lim, 0)
        self.start = start
        self.path_seq = []

        with open(questions) as file:
          self.questions = [line.rstrip() for line in file]

        self.marked_questions = [False for _ in range(len(self.questions))]

        # divide 2D space into k partitions where each partition is a 2D space
        A = (y_lim * x_lim) // len(questions) # area of partition
        a_h, a_w = A // 9, 9
        self.q_map = [[-1 for _ in range(x_lim)] for _ in range(y_lim)]
        
        i, j = 0, 0
        for k in range(len(questions)):
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
              if self.q_map[i][j] < 0:
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
      q_idx = self.q_map[y][x]

      # plass call to GPT with input_q
      input_q = self.questions[q_idx]

      if self.marked_questions[q_idx]:
         return input_q, False

      # completion = f"{' '.join(['hello' for _ in range(20)])}"
      completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
           {"role": "user", "content": f"{input_q}"}
         ],
        max_tokens=50,
        temperature=1.5,
        stream=True
       )
      self.marked_questions[q_idx] = True
      return input_q, completion 

