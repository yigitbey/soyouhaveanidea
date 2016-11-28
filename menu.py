#!/usr/bin/env python2
from collections import namedtuple

import curses
from curses import panel

class Menu(object):

    def __init__(self, items, parent_window):
        self.window = parent_window.derwin(3,0)
        self.window.keypad(1)
        curses.noecho()
        curses.raw()

        self.position = len(items)
        self.items = items

        nothing = namedtuple("Nothing", 'message, action_str')
        nothing.message = "Nothing"
        nothing.action_str = "Do"

        self.items.append(nothing)

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.window.clear()
        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                   mode = curses.A_REVERSE
                else:
                   mode = curses.A_NORMAL

                msg = '%d. %s a %s' % (index, item.action_str, item.message)
                self.window.addstr(1+index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
               if self.position == len(self.items)-1:
                   return None
               else:
                   return self.position

            if key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        curses.doupdate()

class MyApp(object):

    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        items = []
        nothing = namedtuple("Nothing", 'message', 'action_str')
        nothing.message = "Nothing"
        nothing.action_str = "Do"
        items.append(nothing)
        items.append(nothing)

        main_menu = Menu(items, self.screen)
        main_menu.display()

if __name__ == '__main__':
    curses.wrapper(MyApp)
