def cli(objects, entities):
    player = objects[0]

    print("So you have an idea")
    print("Money: ${}".format((player.money)))

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
        print("{} Hire {}".format(number, choice.message))

    answer = int(input())
    return choices[answer]

