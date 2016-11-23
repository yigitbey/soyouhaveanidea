from game import Game
from exceptions import *
import ui_nc as ui

def start_game():
    Game.init_game()
    over = False
    win = False

    while not (over or win):

        action = ui.cli(Game.objects, Game.entities, Game.used_resources)
        if action:
            o = action(Game.project)
            Game.objects.append(o)

        for o in Game.objects:
            try:
                o.turn()
            except NotEnoughFundsException:
                over = True
            except WinException:
                win = True

        Game.used_resources.turn_count += 1

    if over:
        ui.over(Game.project)

    if win:
        ui.win(Game.project)

if __name__ == "__main__":
    start_game()
