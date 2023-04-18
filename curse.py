from curses import wrapper
import curses
import time
from algo import Algo

def game_init(win, algo, refresh_fn):
  # boarder
  boarder = algo.board_coords
  for (y, x) in boarder:
    win.addstr(y, x, "+", curses.color_pair(2))
    refresh_fn()

  # obstacles
  obstacles = algo.obstacles
  for y, x in zip(obstacles[0], obstacles[1]):
    win.addstr(y, x, "&", curses.color_pair(3))
    refresh_fn()
  
  # target coord
  y_t, x_t = algo.target
  win.addstr(y_t, x_t, "$", curses.color_pair(5))
  refresh_fn()

def gpt_conversation(win, algo, refresh_fn, question, completion):
  boarder_offset = 2
  y_chat, x_chat = algo.y_lim + boarder_offset, 1
  question = f"[userA]: {question}"
  refresh_fn()
  win.addstr(y_chat, x_chat, question)

  response = f"[userB]: "
  win.addstr(y_chat + boarder_offset, x_chat, response)
  refresh_fn()

  y_chat += boarder_offset
  x_chat += len(response)
  switch = 0
  for chunk in completion:
    if 'content' in chunk['choices'][0]['delta']: # grab token to write
      s = chunk['choices'][0]['delta']['content']

      win.addstr(y_chat, x_chat, s)
      refresh_fn()

      if x_chat + len(s) < algo.x_lim:
        x_chat += len(s)
      else:
        y_chat += 1; x_chat = 1

      time.sleep(0.1)
      switch += 1

def game_loop(win, algo, refresh_fn):
  
  obstacles = algo.obstacles
  y_tar, x_tar = algo.target

  i = 0
  while i < len(algo.path_seq):
    # refresh obstacle colors
    color_obs = curses.color_pair(3)
    if i % 2 == 0:
      color_obs = curses.color_pair(4)
    for y, x in zip(obstacles[0], obstacles[1]):
      win.addstr(y, x, "&", color_obs)
      refresh_fn()

    # refresh target colors 
    color_tar = curses.color_pair(5)
    if i % 10 == 0:
      color_tar = curses.color_pair(6)
    win.addstr(y_tar, x_tar, "$", color_tar)
    refresh_fn()

    # update game positions
    y, x = algo.path_seq[i]
    win.addstr(y, x, ".", curses.color_pair(1))
    refresh_fn()
    
    # talk to GPT, pause path-finding, output completion    
    question, completion = algo.converse(i)
    if completion:
      # clear chat window
      win.addstr(algo.y_lim + 2, 1, '')
      refresh_fn()
      win.clrtobot()
      refresh_fn()
      gpt_conversation(win, algo, refresh_fn, question, completion)

    i+=1
    time.sleep(1)

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
  curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK) # player
  curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_YELLOW) # boarder
  curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE) # obstacle
  curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED) # obstacle
  curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK) # target 
  curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN) # target 
  curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW) # player

  algo = Algo(y_lim//2, x_lim, start=(y_lim//4,x_lim//2))
  algo.compute_path()
  game_init(win, algo, refresh)
  game_loop(win, algo, refresh)

  stdscr.getch()

wrapper(main)
