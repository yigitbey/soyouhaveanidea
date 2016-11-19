def initproject(all_budget):
    print("What's the name of the project?")
    name = input()

    budget = all_budget + 1
    while budget > all_budget:
        print("How much budget do you want to allocate to your project?")
        budget = int(input())

    return name, budget


def cli(objects, entities, used_resources):
    player = objects[0]
    project = objects[1]

    print("Day {}".format(used_resources.turn_count))
    print("Your Wallet: ${}".format(player.money))
    print(project)

    unlocked_entities = [entity for entity in entities if entity.unlocked and not entity.limit_reached()]
    limited_entities = [entity for entity in entities if entity.limit_reached()]

    print_limited(objects)
    action = multiple_choice("What do you do?", unlocked_entities)
    return action


def print_limited(entities):
    print("You have:")
    for entity in entities:
        print(entity.message, end=", ")

    print("\n============")


def multiple_choice(question, choices):
    print(question)

    for number, choice in enumerate(choices):
        print("{} {} a {}".format(number, choice.action_str, choice.message))

    nothing_choice = number + 1
    print("{} Do nothing.".format(nothing_choice))

    answer = int(input())

    print()
    print()

    if answer == nothing_choice:
        return None
    else:
        return choices[answer]

