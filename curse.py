from curses import wrapper
import curses
import time
from grid import Map

global_attrs = {}

def game_init(win, x_lim, y_lim, refresh_fn):
  screen_map = Map(x_lim, y_lim)
  
  # boarder
  boarder = screen_map.generate_boarder()
  for (y, x) in boarder:
    win.addstr(y, x, "+", curses.color_pair(2))
    refresh_fn()

  # obstacles
  obstacles = screen_map.generate_obstacles()
  global_attrs['obstacles'] = obstacles
  for y, x in zip(obstacles[0], obstacles[1]):
    win.addstr(y, x, "&", curses.color_pair(3))
    refresh_fn()


def game_loop(win ,refresh_fn):
  
  obstacles = global_attrs['obstacles']
  switch = 0

  while True:
    # refresh obstacle colors
    color = curses.color_pair(3)
    if switch % 2 == 0:
      color = curses.color_pair(4)

    for y, x in zip(obstacles[0], obstacles[1]):
      win.addstr(y, x, "&", color)
      refresh_fn()
    switch+=1


def main(stdscr):

  def refresh():
    stdscr.refresh()
    win.refresh()

  begin_x = 0
  begin_y = 0
  height = 500
  width = 500
  win = curses.newwin(height, width, begin_y, begin_x)
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(True)

  y_lim, x_lim = curses.LINES - 1, curses.COLS - 1
  curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_GREEN)
  curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_YELLOW)
  curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
  curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
  
  # init board
  game_init(win, x_lim, y_lim, refresh)
  game_loop(win, refresh)

  # path find

  stdscr.getch()


wrapper(main)
