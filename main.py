from game import Game
from exceptions import *
import ui

if __name__ == "__main__":
    print("So you have an idea")

    Game.init_game()
    over = False

    while not over:

        action = ui.cli(Game.objects, Game.entities, Game.used_resources)
        if action:
            o = action(Game.project)
            Game.objects.append(o)

        for o in Game.objects:
            try:
                o.turn()
            except NotEnoughFundsException:
                over = True

        Game.used_resources.turn_count += 1

    print("XXXXXXXXX")
    print("GAME OVER")
    print("XXXXXXXXX")
    print(Game.project)
    print("Score: {}".format(Game.project.score))
