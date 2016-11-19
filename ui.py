def cli(objects, entities):
    player = objects[0]
    project = objects[1]

    print("Money: ${}".format((player.money)))
    print(project)

    unlocked_entities = [entity for entity in entities if entity.unlocked and not entity.limit_reached()]
    limited_entities = [entity for entity in entities if entity.limit_reached()]

    print_limited(objects)
    action = multiple_choice("What do you do?", unlocked_entities)
    return action


def print_limited(entities):
    print("You have:")
    for entity in entities:
        print(entity.message)
    print("============")


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

