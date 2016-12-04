#!/usr/bin/env python2
from collections import namedtuple

import curses
from curses import panel


class EntityDetail(object):
    def __init__(self, entity, parent_window):
        self.window = parent_window.derwin(18, 0)
        self.window.border(0,0,0,0,0,0,0,0)
        self.window.addstr(entity.formatted)
        self.window.refresh()
        self.iwindow = self.window.derwin(2, 2)

        self.entity = entity

        fields = [('initial_cost', "Initial Cost"),
                ('cost', "Monthly Cost"),
                ('productivity_modifier', "Productivity Modifier")
                ]

        for field in fields:
            if getattr(entity, field[0]) != 0:
                self.iwindow.addstr("{}: {}\n".format(field[1], getattr(entity, field[0])))

        if entity.increases:
            self.iwindow.addstr("Increases:\n")
            for key, value in entity.increases.items():
                if value != 0:
                    self.iwindow.addstr("   {}: {}\n".format(key, value))
        if entity.decreases:
            self.iwindow.addstr("Decreases:\n")
            for key, value in entity.decreases.items():
                if value != 0:
                    self.iwindow.addstr("   {}: {}\n".format(key, value))

        for field in entity.detail_fields:
            value = getattr(entity, field[0])
            self.iwindow.addstr(field[1].format(value)+"\n")

        self.iwindow.refresh()

    def delete(self):
        try:
            self.window.clear()
            self.iwindow.clear()
            del self.window
            del self.iwindow
            del self

        except:
            pass


class Menu(object):

    def __init__(self, items, parent_window):
        self.window = parent_window.derwin(1, 0)
        self.window.keypad(1)
        curses.noecho()
        curses.raw()

        self.position = len(items)
        self.items = items

        nothing = namedtuple("Nothing", 'message, action_str')
        nothing.message = "Nothing"
        nothing.action_str = "Do"
        self.detailwindow = None

        self.items.append(nothing)

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

        if self.detailwindow:
            self.detailwindow.delete()
        self.showdetail()

    def showdetail(self):
        if self.detailwindow:
           self.detailwindow.delete()
        if self.position != len(self.items)-1:
            self.detailwindow = EntityDetail(self.items[self.position], self.window)

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


class IdeaMenu(object):

    def __init__(self, items, parent_window):
        self.window = parent_window.derwin(1, 0)
        self.window.keypad(1)
        curses.noecho()
        curses.raw()

        self.position = 0
        self.items = items

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

                msg = '%s. %s\n   (Features: %s, Design: %s)' % (index, item, item.features, item.design_need)
                self.window.addstr(1+index*2, 2, msg, mode)

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
