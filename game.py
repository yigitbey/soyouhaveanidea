import ui


class Resource(object):
    def __init__(self):
        pass


class EntityMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        clss = type.__new__(cls, clsname, superclasses, attributedict)
        if 'wage' in attributedict:
            clss.message = "{} (${} monthly)".format(attributedict['formatted'], attributedict['wage'])
        else:
            clss.message = "{}".format(attributedict['formatted'])
        return clss


class Entity(object, metaclass=EntityMeta):
    current_amount = 0
    limit = -1
    unlocked = False
    unlocks_entities = []
    locks_entities = []
    wage = 0
    formatted = "Entity"
    drains = {}
    replenishes = {}

    def __init__(self, inventory={}, draining=drains, replenishing=replenishes):

        if self.__class__.limit >= 0:
            if self.__class__.current_amount < self.__class__.limit:
                self.inventory = inventory
                self.draining = draining
                self.replenishing = replenishing
                self.__class__.current_amount += 1
                self.__class__.unlocks()
                self.__class__.locks()
            else:
                raise Entity.TooManyEntitiesException("No limit for {}".format(self.__class__.__name__))

    def trade(self, entity, item, value):
        item1 = getattr(self, item)
        item2 = getattr(entity, item)
        item1 -= value
        item2 += value

    def turn(self):
        self.drain()
        self.replenish()

    def drain(self):
        for key, value in self.draining.items():
            self.inventory[key] -= value

    def replenish(self):
        for key, value in self.replenishing.items():
            self.inventory[key] += value

    @classmethod
    def unlocks(cls):
        for entity in cls.unlocks_entities:
            entity.unlock()

    @classmethod
    def locks(cls):
        for entity in cls.locks_entities:
            entity.lock()

    @classmethod
    def unlock(cls):
        cls.unlocked = True

    @classmethod
    def lock(cls):
        cls.unlocked = False

    @classmethod
    def limit_reached(cls):
        if cls.limit >= 0:
            if cls.current_amount >= cls.limit:
                return True

        return False


    class TooManyEntitiesException(Exception):
        pass


class Person(Entity):
    limit = -1
    wage = 0
    formatted = "Person"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def money(self):
        return self.inventory['money']

    @money.setter
    def money(self, value):
        self.inventory['money'] = value


class Developer(Person):
    limit = -1
    formatted = "Developer"
    wage = 0
    action_str = "Hire"

    introduces = {}
    develops = {}

    def turn(self):
        super().turn()
        for key, value in self.introduces.items():
            project_key = getattr(project, key)
            setattr(project, key, project_key + value)

        for key, value in self.develops.items():
            project_key = getattr(project, key)
            setattr(project, key, project_key - value)


class StudentDeveloper(Developer):
    limit = 3
    formatted = "Student Developer"
    wage = 0

    introduces = {"bugs": 10}
    develops = {"features": 5}


class ShittyDeveloper(Developer):
    limit = -1
    formatted = "Shitty Developer"
    wage = 5


class MediocreDeveloper(Developer):
    limit = -1
    formatted = "Mediocre Developer"
    wage = 10


class Project(Entity):
    limit = 1
    unlocked = True
    bugs = 0
    features = 1000
    technical_debt = 0
    server_maintenance = 0
    action_str = "Start"
    formatted = "Project"
    unlocks_entities = [StudentDeveloper, ShittyDeveloper, MediocreDeveloper]

    def __repr__(self):
        return "Remaining Features: {}, Bugs: {}, Technical Debt: {}, Server Costs: {}".format(
            self.features,
            self.bugs,
            self.technical_debt,
            self.server_maintenance
        )


class Boss(Person):
    limit = 1
    formatted = "Boss"
    wage = 0
    unlocked = True
    unlocks_entities = [Project]


class UsedResources(object):
    def __init__(self):
        self.money = 0
        self.turn_count = 0


def init_game():
    global used_resources
    used_resources = UsedResources()
    global project
    project = Project()

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
    global objects
    objects.append(player)
    objects.append(project)

objects = []
used_resources = None
project = None

entities = [Boss, StudentDeveloper, ShittyDeveloper, MediocreDeveloper]

if __name__ == "__main__":
    print("So you have an idea")
    init_game()

    while True:

        action = ui.cli(objects, entities)
        if action:
            objects.append(action())

        for o in objects:
            o.turn()

