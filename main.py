from game import Game
import ui

if __name__ == "__main__":
    print("So you have an idea")

    Game.init_game()

    while True:

        action = ui.cli(Game.objects, Game.entities, Game.used_resources)
        if action:
            o = action(Game.project)
            Game.objects.append(o)

        for o in Game.objects:
            o.turn()

        Game.used_resources.turn_count += 1

