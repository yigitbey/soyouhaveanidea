#!/usr/bin/env python2
from collections import namedtuple

import curses
import locale


class EntityDetail(object):
    def __init__(self, entity, parent_window):
        self.window = parent_window.derwin(19, 0)
        self.window.border(0,0,0,0,0,0,0,0)
        self.window.addstr(entity.formatted)
        self.window.refresh()
        self.iwindow = self.window.derwin(2, 2)

        self.entity = entity

        fields = [
            ('initial_cost', "Initial Cost"),
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
    LIST_SIZE = 14

    def __init__(self, items, parent_window, which_menu="left"):
        self.which_menu = which_menu
        self.window = parent_window.derwin(1, 0)
        self.window.keypad(1)
        curses.noecho()
        curses.raw()

        self.position = 0
        self.items = items

        if self.which_menu == 'left':
            nothing = namedtuple("Nothing", 'message, action_str, article, formatted')
            nothing.message = "Nothing"
            nothing.action_str = "Do"
            nothing.article = ""
            nothing.formatted = "Nothing"
            self.items.insert(0, nothing)

        self.detailwindow = None

        code = locale.getpreferredencoding()
        self.arrow_up = (3*'\u2191').encode(code)
        self.arrow_down = (3*'\u2193').encode(code)

        self.first_item_index = self.position
        self.last_item_index = min(self.LIST_SIZE, len(self.items))

        self.next_window = None
        self.has_focus = False

        self.item_message = '{1.action_str} {1.article} {1.message}'

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

        if (self.position >= self.last_item_index) or (self.position < self.first_item_index):
            self.first_item_index += n
            self.last_item_index += n

        if self.detailwindow:
            self.detailwindow.delete()
        self.showdetail()

    @property
    def employees(self):
        return self.items[self.first_item_index: self.last_item_index]

    def showdetail(self):
        self.window.clear()
        if self.detailwindow:
            self.detailwindow.delete()
        if self.items[self.position].message != "Nothing":
            self.detailwindow = EntityDetail(self.items[self.position], self.window)

    # TODO: refactor this
    def select_mode(self, index):
        if self.has_focus:
            if self.first_item_index == 0 and index == self.position:
                mode = curses.A_REVERSE
            elif (self.position - self.first_item_index) == index:
                mode = curses.A_REVERSE
            elif (self.position + 1 == self.last_item_index) and (index == len(self.employees) - 1):
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL
        else:
            mode = curses.A_NORMAL

        return mode

    def init_display(self):
        self.window.clear()
        self.showdetail()

        self.update()

        self.window.refresh()
        curses.doupdate()

    def update(self):
        for index, item in enumerate(self.employees):
            mode = self.select_mode(index)

            try:
                if item.unlocked_age < 2:
                    mode = mode | curses.A_BOLD | curses.A_UNDERLINE
            except:
                pass

            if self.first_item_index > 0:
                self.window.addstr(0, 20, self.arrow_up)

            order = self.first_item_index + index + 1
            msg = self.item_message.format(order, item)
            self.window.addstr(1 + index, 1, msg, mode)

            if self.last_item_index < len(self.items):
                self.window.addstr(self.LIST_SIZE + 1, 20, self.arrow_down)

        self.window.refresh()
        curses.doupdate()

    def display(self):
        self.window.clear()
        self.showdetail()

        while True:
            self.has_focus = True
            self.next_window.has_focus = False

            self.window.refresh()
            curses.doupdate()

            self.update()

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                return self.position

            if key == curses.KEY_UP:
                if self.position == 0:
                    self.navigate(self.last_item_index)
                else:
                    self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

            elif key == curses.KEY_RIGHT or key == curses.KEY_LEFT:
                self.has_focus = False
                self.update()
                self.next_window.display()


class RightMenu(Menu):

    def action(self):
        self.items[self.position].fire()
        self.detailwindow.window.clear()
        self.window.clear()
        self.has_focus = False
        self.position = 0
        self.update()
        self.window.refresh()
        curses.doupdate()

    def display(self):
        self.window.clear()
        self.showdetail()

        while True:
            self.has_focus = True
            self.next_window.has_focus = False
            self.window.refresh()
            curses.doupdate()

            self.update()

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                self.action()
                return

            if key == curses.KEY_UP:
                if self.position == 0:
                    self.navigate(self.last_item_index)
                else:
                    self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

            elif key == curses.KEY_RIGHT or key == curses.KEY_LEFT:
                self.has_focus = False
                self.update()
                return


# TODO: scrolling this
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

                msg = '- %s\n   (Features: %s, Design: %s)' % (item, item.features, item.design_need)
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

