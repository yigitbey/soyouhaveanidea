from functools import partial

from nc import init_ui, printw, getstr, clear

import curses

windows = init_ui()
print0 = partial(printw, windows[0])
print1 = partial(printw, windows[1])
print2 = partial(printw, windows[2])
print3 = partial(printw, windows[3])
read = partial(getstr, windows[3])


def initproject(all_budget):
    print1("So you have an idea")
    print1("What's the name of the project?")

    name = str(read(), 'utf-8')

    budget = all_budget + 1

    clear(windows[1])

    while budget > all_budget:
        print1("You have $10000.")
        print1("Your daily personal expense is $5.")
        print1("How much budget do you want to allocate to your project?")
        budget = int(read())

    clear(windows[1])

    return name, budget


def print_project(project):
    clear(windows[0])
    print0(project.name, color=3)

    print0("Budget", end=": ")
    print0("$" + str(project.money), color=2)

    print0("Productivity", end=": ")
    print0("%" + str(int(project.productivity*100)), color=2)

    print0("Remaining Features", end=": ")
    print0(int(project.features), color=1)

    print0("Bugs", end=": ")
    print0(project.bugs, color=1)

    print0("Technical Dept", end=": ")
    print0(project.technical_debt, color=1)

    print0("Documentation", end=": ")
    print0(project.documentation, color=1)

    print0("Server Costs", end=": ")
    print0("$" + str(int(project.server_maintenance)), color=1)

    print0("Design Need", end=": ")
    print0(int(project.design_need), color=1)


def cli(objects, entities, used_resources):
    player = objects[0]
    project = objects[1]

    clear(windows[1])

    print1("Day {}".format(used_resources.turn_count))
    print1("Your Wallet: ${}".format(player.money))
    print_project(project)

    unlocked_entities = [entity for entity in entities if entity.unlocked and not entity.limit_reached()]
    limited_entities = [entity for entity in entities if entity.limit_reached()]

    print_limited(objects)
    action = multiple_choice("What do you do?", unlocked_entities)
    if not action:
        return None
    return action


def print_limited(entities):
    clear(windows[2])
    print2("You have:")
    for entity in entities:
        print2(entity.message)

    #print1("\n============")


def multiple_choice(question, choices):
    print1(question)

    for number, choice in enumerate(choices):
        print1("{} {} a {}".format(number, choice.action_str, choice.message))

    nothing_choice = number + 1
    print1("Enter: Do nothing.")

    answer = read(empty_ok=True)

    if answer == nothing_choice or not answer:
        return None
    else:
        answer = int(answer)
        if answer <= len(choices):
            return choices[int(answer)]
        else:
            return None


def win(project):
    print0(chr(27) + "[2J")
    print0("---------")
    print0("YOU WON")
    print0("---------")
    print0(project)
    print0("Score: {}".format(project.score))


def over(project):
    print0(chr(27) + "[2J")
    print0("---------")
    print0("GAME OVER")
    print0("---------")
    print0(project)
    print0("Score: {}".format(project.score))
