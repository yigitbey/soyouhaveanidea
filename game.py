import ui
from entity import Entity
from resource import Resource, UsedResources


class Person(Entity):
    limit = -1
    cost = 0
    formatted = "Person"
    drains_from = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def turn(self):
        super().turn()
        self.drains_from.trade(self, 'money', self.cost)


class Developer(Person):
    limit = -1
    formatted = "Developer"
    cost = 0
    action_str = "Hire"
    inventory = {'money': 0}

    introduces = {}
    develops = {}

    def turn(self):
        super().turn()
        for key, value in self.introduces.items():
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key + value)

        for key, value in self.develops.items():
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key - value)

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drains_from = project


class StudentDeveloper(Developer):
    limit = -1
    formatted = "Student Developer"
    cost = 0

    introduces = {
        "bugs": 2,
        "technical_debt": 3,
    }
    develops = {
        "features": 1,
        "documentation": -1,
    }


class ShittyDeveloper(Developer):
    limit = -1
    formatted = "Shitty Developer"
    cost = 5

    introduces = {
        "bugs": 1,
        "technical_debt": 4,
    }
    develops = {"features": 2}


class MediocreDeveloper(Developer):
    limit = -1
    formatted = "Mediocre Developer"
    cost = 10

    introduces = {
        "bugs": 1,
        "technical_debt": 3,
        "documentation": 1
    }
    develops = {
        "features": 3,
    }


class SeniorDeveloper(Developer):
    limit = -1
    formatted = "Senior Developer"
    cost = 20

    introduces = {
        "bugs": 1,
        "technical_debt": 1,
        "documentation": 6
    }
    develops = {
        "features": 6,
    }


class GeniusDeveloper(Developer):
    limit = 1
    formatted = "Genius Developer"
    cost = 100

    introduces = {
        "bugs": 1,
        "technical_debt": 0,
        "documentation": 10
    }
    develops = {
        "features": 10,
    }


class Project(Entity):
    name = "Project 1"
    limit = 1
    unlocked = True
    bugs = 0
    features = 1000
    technical_debt = 0
    documentation = 0
    server_maintenance = 0
    action_str = "Start"
    formatted = "Project"
    unlocks_entities = [StudentDeveloper, ShittyDeveloper, MediocreDeveloper, SeniorDeveloper, GeniusDeveloper]

    introduces = {
        'features': 2
    }

    def turn(self):
        super().turn()
        for key, value in self.introduces.items():
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key + value)

    def __repr__(self):
        return "{}: Budget: ${}, Remaining Features: {}, Bugs: {}, Technical Debt: {}, Documentation: {}, Server Costs: {}".format(
            self.name,
            self.money,
            self.features,
            self.bugs,
            self.technical_debt,
            self.documentation,
            self.server_maintenance
        )


class Boss(Person):
    limit = 1
    formatted = "Boss"
    cost = 0
    unlocked = True
    unlocks_entities = [Project]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drains_from = self


class Game(object):

    @classmethod
    def init_game(cls):
        cls.used_resources = UsedResources()

        initial_player_inventory = {
            'money': 10000,
        }
        initial_player_drain = {
            'money': 5
        }
        initial_player_replenish = {}

        player = Boss(
            inventory=initial_player_inventory,
            draining=initial_player_drain,
            replenishing=initial_player_replenish,
        )

        project_name, budget = ui.initproject(player.inventory['money'])

        cls.project = Project()
        cls.project.name = project_name
        player.trade(cls.project, 'money', budget)

        cls.objects.append(player)
        cls.objects.append(cls.project)
        player.project = cls.project

    objects = []
    used_resources = None
    project = None

    entities = [Boss, StudentDeveloper, ShittyDeveloper, MediocreDeveloper, SeniorDeveloper, GeniusDeveloper]
