from functools import partial
import logging

from nc import init_ui, printw, getstr, clear, alert
from menu import Menu
from idea import Idea

windows = init_ui()
print0 = partial(printw, windows[0])
print1 = partial(printw, windows[1])
print2 = partial(printw, windows[2])
print3 = partial(printw, windows[3])
read = partial(getstr, windows[3])


def list_ideas(count):
    ideas = []
    for i in range(count):
        idea = Idea()
        ideas.append(idea)
        print1("{}. {}".format(i, idea))
        print1("Features:{} Design:{}".format(idea.features, idea.design_need))
        print1("-----")

    return ideas


def initproject(all_budget):
    print1("Choose your idea:")
    print1("")
    ideas = list_ideas(10)
    idea = ideas[int(read())]
    clear(windows[1])

    idea_pitch = " ".join(idea.pitch.split(" ")[1:])
    print1("So you have an idea, you are going to build {}".format(idea_pitch))
    print1("What's the name of the project?")

    name = str(read(), 'utf-8')

    budget = all_budget + 1

    clear(windows[1])

    while budget > all_budget:
        print1("You have $10000.")
        print1("Your daily personal expense is $25.")
        print1("How much budget do you want to allocate to your project?")
        budget = int(read())

    clear(windows[1])

    return name, budget, idea


def print_project(project):
    clear(windows[0])
    print0(project.name, color=4)
    print0(project.pitch)

    print0("Budget", end=": ")
    print0("$" + str(project.money), color=2)

    print0("Productivity", end=": ")
    print0("%" + str(int(project.productivity*100)), color=2)

    print0("Remaining Features", end=": ")
    print0(int(project.features), color=1)

    print0("Bugs", end=": ")
    print0(project.bugs, color=1)

    print0("Technical Debt", end=": ")
    print0(project.technical_debt, color=1)

    print0("Documentation", end=": ")
    print0(project.documentation, color=1)

    print0("Server Costs", end=": ")
    print0("$" + str(int(project.server_maintenance)), color=1)

    print0("Design Need", end=": ")
    print0(int(project.design_need), color=1)


def cli(objects, entities, used_resources, turn_events):
    player = objects[0]
    project = objects[1]

    logger = logging.getLogger('soyu')
    logger.debug(turn_events)
    for event in turn_events:
        a, b = alert(windows[4], str(event))
        del a
        del b
    project.turn_events = []

    clear(windows[1])

    print1("Day {}".format(used_resources.turn_count))
    print1("Your Wallet: ${} Your shares: %{}".format(player.money, player.shares))
    print_project(project)

    unlocked_entities = [entity for entity in entities if entity.unlocked and not entity.limit_reached()]
    limited_entities = [entity for entity in entities if entity.limit_reached()]

    print_limited(objects)
    action = select("What do you do?", unlocked_entities)

    if not action:
        return None
    return action


def print_limited(entities):
    clear(windows[2])
    print2("You have:")
    entities = {x.message: x for x in entities}.values()
    for entity in entities:
        print2("{}x {}".format(entity.current_amount, entity.message))


def select(question, choices):
    print1(question)
    answer_menu = Menu(choices, windows[1])
    answer = answer_menu.display()
    try:
        answer = int(answer)
    except (ValueError, TypeError):
        answer = False

    if not answer:
        return None
    else:
        if answer <= len(choices) - 1 :
            return choices[int(answer)]
        else:
            return None

def win(project):
    clear(windows[1])
    print1("---------")
    print1("YOU WON")
    print1("---------")
    print1("Score: {}".format(project.score))
    windows[1].getch()


def over(project):
    clear(windows[1])
    print1("---------")
    print1("GAME OVER")
    print1("---------")
    print1("Score: {}".format(project.score))
    windows[1].getch()
