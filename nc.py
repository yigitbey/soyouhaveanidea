from curses import wrapper, newwin, resize_term
import curses
from time import sleep

def init_ui():
    begin_x = 1; begin_y = 1
    height = 40; width = 120
    win = newwin(height, width, begin_y, begin_x)
    win.border(0,0,0,0,0,0,0,0)
    win.addstr("So You Have an Idea")
    win.refresh()

    left_win = win.subwin(height-5, 28, 2, 2)
    left_win.border(0,0,0,0,0,0,0,0)
    middle_win = win.subwin(height-5, 60, 2, 30)
    middle_win.border(0,0,0,0,0,0,0,0)
    right_win = win.subwin(height-5, 28, 2, 90)
    right_win.border(0,0,0,0,0,0,0,0)

    bottom_win = win.subwin(3, 116, 37, 2)
    bottom_win.border(0,0,0,0,0,0,0,0)

    left_win.refresh()
    middle_win.refresh()
    right_win.refresh()
    bottom_win.refresh()

    bottom_win.move(1,1)
    bottom_win.getkey()
    #win.refresh()

def main(stdscr):
    # Clear screen
    #resize_term(40,120)
    stdscr.clear()
    curses.start_color()

    init_ui()

    stdscr.refresh()


wrapper(main)
