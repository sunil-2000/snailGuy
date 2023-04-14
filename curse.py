from curses import wrapper
import curses
import time

def main(stdscr):
    begin_x = 0
    begin_y = 0
    height = 100
    width = 100
    win = curses.newwin(height, width, begin_y, begin_x)
    y_lim, x_lim = curses.LINES - 1, curses.COLS - 1
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_YELLOW)

    def bfs(x, y):
        visited = set()
        q = [(x, y)]
        switch = 0

        while q:
            # win.clear()
            color = curses.color_pair(1)
            if switch % 2 == 0:
                color = curses.color_pair(2)
            i, j = q.pop(0)
            visited.add((i, j))
            win.addstr(i, j, "*", color)
            for x_n in (-1, 0, 1):
                for y_n in (-1, 0, 1):
                    if i + x_n < y_lim and j + y_n < x_lim:
                        if (x_n + i, y_n + j) not in visited:
                            q.append((x_n + i, y_n + j))

            switch += 1
            # time.sleep(0.01)
            win.refresh()

    bfs(y_lim // 2, x_lim // 2)
    stdscr.getch()


wrapper(main)
