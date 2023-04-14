# unclean file
import time


class Algo:
    pass

# refactor into class
def bfs(x, y, win, colors, x_lim, y_lim):
    visited = set()
    q = [(x, y)]
    switch = 0
    while q:
        # win.clear()
        color = colors[0]
        if switch % 2 == 0:
            color = colors[1]
        i, j = q.pop(0)
        visited.add((i, j))
        win.addstr(i, j, "*", color)
        for x_n in (-1, 0, 1):
            for y_n in (-1, 0, 1):
                if i + x_n < y_lim and j + y_n < x_lim:
                    if (x_n + i, y_n + j) not in visited:
                        q.append((x_n + i, y_n + j))

        switch += 1
        time.sleep(0.01)
        win.refresh()
