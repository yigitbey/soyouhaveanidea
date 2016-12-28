from copy import deepcopy

from game import Game, Project
from exceptions import *
import ui

SPEED = 10


def start_game():
    Game.init_game()
    over = False
    win = False

    while not (over or win):
        action = ui.cli(Game.objects, Game.entities, Game.used_resources, Game.project.turn_events, Game.last_state)
        Game.last_state = deepcopy(Game.project)
        if action:
            o = action(Game.project)
            Game.objects.append(o)

        for o in Game.objects:
            if isinstance(o, Project):
                continue
            try:
                o.turn()
            except NotEnoughFundsException:
                over = True
            except WinException:
                win = True

        try:
            Game.project.turn()
        except NotEnoughFundsException:
            over = True
        except WinException:
            win = True

        Game.used_resources.turn_count += 1

        ui.wait_anim(int(10/SPEED))

    player = Game.objects[0]

    if over:
        ui.over(Game.project, player)

    if win:
        ui.win(Game.project, player)

if __name__ == "__main__":
    start_game()

