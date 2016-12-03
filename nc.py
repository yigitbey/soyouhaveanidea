import os
import struct
from curses import wrapper, newwin, resize_term, beep, flash
import curses
from time import sleep

import fcntl

import termios
import sys


def get_term_size():
    # taken from http://dag.wieers.com/home-made/dstat/
    try:
        h, w = int(os.environ["LINES"]), int(os.environ["COLUMNS"])
    except KeyError:
        try:
            s = struct.pack('HHHH', 0, 0, 0, 0)
            x = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ,
                            s)
            h, w = struct.unpack('HHHH', x)[:2]
        except:
            h, w = 25, 80
    return h, w


def check_size():
    h, w = get_term_size()
    while h < 40 or w < 162:
        print(chr(27) + "[2J")
        print("Resize the window until 50x162")
        h, w = get_term_size()
        print("Current window size: {}x{}".format(h,w))

        sleep(0.2)


def init_ui():
    check_size()
    begin_x = 1
    begin_y = 1
    height = 40
    width = 160
    left_win_width = 28
    middle_win_width = 80
    right_win_width = width - left_win_width - middle_win_width - 4

    win = newwin(height, width, begin_y, begin_x)
    win.border(0, 0, 0, 0, 0, 0, 0, 0)
    win.addstr("So You Have an Idea")
    win.refresh()

    left_win = win.subwin(height-5, left_win_width, 2, 2)
    left_win.border(0, 0, 0, 0, 0, 0, 0, 0)
    left_win.refresh()
    left_win = left_win.derwin(height-7, left_win_width-2, 1, 1)

    middle_win = win.subwin(height-5, middle_win_width, 2, left_win_width+2)
    middle_win.border(0, 0, 0, 0, 0, 0, 0, 0)
    middle_win.refresh()
    middle_win = middle_win.derwin(height-7, middle_win_width-2, 1, 1)

    right_win = win.subwin(height-5, right_win_width, 2, left_win_width + middle_win_width + 2)
    right_win.border(0, 0, 0, 0, 0, 0, 0, 0)
    right_win.refresh()
    right_win = right_win.derwin(height-7, right_win_width-2, 1, 1)

    bottom_win = win.subwin(3, width-4, height-3, 2)
    bottom_win.border(0, 0, 0, 0, 0, 0, 0, 0)
    bottom_win.refresh()
    bottom_win = bottom_win.derwin(1, 114, 1, 1)

    left_win.refresh()
    middle_win.refresh()
    right_win.refresh()
    bottom_win.refresh()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    return left_win, middle_win, right_win, bottom_win, win


def printw(window, text="", end="\n", color=0):
    if not isinstance(text, str):
        text = repr(text)
    window.addstr(text + end, curses.color_pair(color))
    window.refresh()


def alert(window, text):
    y, x = window.getmaxyx()
    w, h = 50, 6
    alertb = window.subwin(h, w, int(y/2-h/2), int(x/2-w/2))
    alertb.border(0,0,0,0,0,0,0,0)
    alertb.refresh()
    alert = alertb.derwin(h-2, w-2, 1, 1)

    alert.addstr(text)
    alert.refresh()
    beep()
    flash()
    alert.getch()
    #getstr(alert, empty_ok=True)
    alert.erase()
    alertb.erase()

    return alert, alertb


def getstr(window, empty_ok=False):
    window.clear()
    window.move(0, 0)
    if empty_ok:
        response = window.getstr()
    else:
        response = b''
        while response == b'':
            response = window.getstr()
    window.clear()
    window.refresh()
    window.move(0, 0)
    return response


def clear(window):
    window.clear()
    window.refresh()


def main(stdscr):

    stdscr.clear()
    curses.start_color()

    stdscr.refresh()


wrapper(main)
