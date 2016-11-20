import ui
from entity import Entity
from resource import Resource, UsedResources
from exceptions import *


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Event(Entity):
    productivity_modifier = 0
    initial_cost = 0
    formatted = "Event"
    action_str = "Organize"
    drains = {}

    def __init__(self, project,*args, **kwargs):
        super().__init__(*args, **kwargs)
        project.productivity += self.productivity_modifier / 100
        project.money -= self.initial_cost


class TeamEvent(Event):
    productivity_modifier = 10
    initial_cost = 1000
    formatted = "Team Event (Productivity: +{}, Initial Cost: {})".format(productivity_modifier, initial_cost)

    unlocked = False


class Person(Entity):
    limit = -1
    cost = 0
    formatted = "Person"
    action_str = "Hire"
    drains_from = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def turn(self):
        super().turn()
        self.drains_from.trade(self, 'money', self.cost)


class ProjectEmployee(Person):
    formatted = "Employee"

    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drains_from = project


class Developer(ProjectEmployee):
    limit = -1
    formatted = "Developer"
    cost = 0
    action_str = "Hire"
    inventory = {'money': 0}
    productivity_drop = 0
    introduces = {}
    develops = {}

    def turn(self):
        super().turn()
        for key, value in self.introduces.items():
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key + value)

        for key, value in self.develops.items():
            value *= Game.project.productivity
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key - value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Game.project.productivity *= (1 - self.productivity_drop)
        self.introduces['server_maintenance'] = self.develops['features'] / 10


class CoffeeMachine(Entity):
    limit = -1
    formatted = "Coffee Machine ☕"
    action_str = "Buy"
    initial_cost = 0
    productivity_modifier = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Game.project.money -= self.initial_cost
        Game.project.productivity += self.productivity_modifier / 100


class ShittyCoffeeMachine(CoffeeMachine):
    limit = 1
    cost = 2
    initial_cost = 10
    productivity_modifier = 2

    formatted = u"Shitty Coffee Machine ☕(Productivity: +{}, Initial Cost: {})".format(productivity_modifier, initial_cost)


class GoodCoffeeMachine(CoffeeMachine):
    limit = 1
    formatted = "Good Coffee Machine ☕"
    cost = 4
    initial_cost = 25
    productivity_modifier = 5


class ArtisanCoffeeMachine(CoffeeMachine):
    limit = 1
    formatted = "Artisan Coffee Machine ☕"
    cost = 10
    initial_cost = 100
    productivity_modifier = 10


class Designer(ProjectEmployee):
    limit = -1
    formatted = "Designer"
    cost = 0
    productivity_drop = 0.1
    action_str = "Hire"
    inventory = {'money': 0}

    introduces = {}
    drops = {}

    def turn(self):
        super().turn()
        for key, value in self.drops.items():
            value *= Game.project.productivity
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key - value)


class StudentDesigner(Designer):
    formatted = "Student Designer"
    cost = 0
    drops = {'design_need': 4}


class ShittyDesigner(Designer):
    formatted = "Shitty Designer 💩"
    cost = 5
    drops = {'design_need': 6}

    unlocks_entities = [ShittyCoffeeMachine]


class MediocreDesigner(Designer):
    formatted = "Mediocre Designer"
    cost = 10
    drops = {'design_need': 8}

    unlocks_entities = [GoodCoffeeMachine]


class SeniorDesigner(Designer):
    formatted = "Senior Designer"
    cost = 20
    drops = {'design_need': 12}

    unlocks_entities = [ArtisanCoffeeMachine]


class ProjectManager(ProjectEmployee):
    limit = 1
    formatted = "Project Manager"
    cost = 10

    introduces = {
        'design_need': 5
    }
    drops = {
        "features": 15
    }
    unlocks_entities = [Designer, ShittyDesigner, MediocreDesigner, SeniorDesigner, TeamEvent]

    def turn(self):
        super().turn()
        for key, value in self.introduces.items():
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key + value)
        for key, value in self.drops.items():
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key - value)


class StudentDeveloper(Developer):
    limit = -1
    formatted = "Student Developer 👦"
    cost = 0
    productivity_drop = 0.2

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
    formatted = u"Shitty Developer 💩"
    cost = 5
    productivity_drop = 0.15

    introduces = {
        "bugs": 1,
        "technical_debt": 4,
    }
    develops = {"features": 2}


class MediocreDeveloper(Developer):
    limit = -1
    formatted = "Mediocre Developer 👱"
    cost = 10
    productivity_drop = 0.10

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
    formatted = "Senior Developer 👴"
    cost = 20
    productivity_drop = 0.05

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
    formatted = "Genius Developer 🕵"
    cost = 100
    productivity_drop = 0

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
    initial_features = features
    technical_debt = 0
    documentation = 0
    server_maintenance = 0
    productivity = 1
    design_need = 0
    action_str = "Start"
    formatted = "Project"
    unlocks_entities = [StudentDeveloper, ShittyDeveloper, MediocreDeveloper, SeniorDeveloper, GeniusDeveloper]

    introduces = {
        'features': 5,
        'design_need': 5
    }

    @property
    def score(self):
        score = ((self.features * -1 / 2) - self.bugs - self.technical_debt + self.documentation * 3 - self.server_maintenance - self.design_need + self.money) * self.productivity
        return score

    def turn(self):
        super().turn()
        for key, value in self.introduces.items():
            project_key = getattr(Game.project, key)
            setattr(Game.project, key, project_key + value)

        if Game.project.features/Game.project.initial_features <= 0.9:
            ProjectManager.unlock()

        if Game.project.money <= 0:
            raise NotEnoughFundsException

        if Game.project.features <= 0:
            raise WinException


    def __repr__(self):
        return (bcolors.FAIL + "{}" + bcolors.ENDC +
                ": Budget: " + bcolors.OKGREEN + "${}" + bcolors.ENDC +
                ", Productivity:" + bcolors.OKGREEN + "%{}" + bcolors.ENDC +
                ", Remaining Features:" + bcolors.OKGREEN + "{}" + bcolors.ENDC +
                ", Bugs: " + bcolors.OKGREEN + "${}" + bcolors.ENDC +
                ", Technical Debt: " + bcolors.OKGREEN + "{}" + bcolors.ENDC +
                ", Documentation: " + bcolors.OKGREEN + "{}" + bcolors.ENDC +
                ", Server Costs: " + bcolors.OKGREEN + "${}" + bcolors.ENDC +
                ", Design Need: " + bcolors.OKGREEN + "{}" + bcolors.ENDC ).format(
            self.name,
            self.money,
            int(self.productivity*100),
            int(self.features),
            self.bugs,
            self.technical_debt,
            self.documentation,
            int(self.server_maintenance),
            int(self.design_need),
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

    def turn(self):
        super().turn()

        if self.money <= 0:
            raise NotEnoughFundsException


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

    entities = [Boss, StudentDeveloper, ShittyDeveloper, MediocreDeveloper, SeniorDeveloper, GeniusDeveloper,
                MediocreDesigner, StudentDesigner, ShittyDesigner, SeniorDesigner, ProjectManager,
                ShittyCoffeeMachine, GoodCoffeeMachine, ArtisanCoffeeMachine, TeamEvent
                ]
