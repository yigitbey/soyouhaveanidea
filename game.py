import ui


class Resource(object):
    def __init__(self):
        pass


class EntityMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        clss = type.__new__(cls, clsname, superclasses, attributedict)
        clss.message = "{} (${} monthly)".format(attributedict['formatted'], attributedict['wage'])
        return clss


class Entity(object, metaclass=EntityMeta):
    current_amount = 0
    limit = -1
    unlocked = False
    unlocks_entities = []
    locks_entities = []
    wage = 0
    formatted = "Entity"

    def __init__(self, unlocked=False, inventory={}, draining={}, replenishing={}):

        if self.__class__.limit >= 0:
            if self.__class__.current_amount < self.__class__.limit:
                self.inventory = inventory
                self.draining = draining
                self.replenishing = replenishing
                self.__class__.unlocked = unlocked
                self.__class__.current_amount += 1
                self.__class__.unlocks()
                self.__class__.locks()
            else:
                raise Entity.TooManyEntitiesException("No limit for {}".format(self.__class__.__name__))

    def drain(self, **kwargs):
        for key, value in kwargs.items():
            self.inventory[key] += value

    def replenish(self, **kwargs):
        for key, value in kwargs.items():
            self.inventory[key] -= value

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


class StudentDeveloper(Developer):
    limit = -1
    formatted = "Student Developer"
    wage = 0


class ShittyDeveloper(Developer):
    limit = -1
    formatted = "Shitty Developer"
    wage = 5


class MediocreDeveloper(Developer):
    limit = -1
    formatted = "Mediocre Developer"
    wage = 10


class Boss(Person):
    limit = 1
    formatted = "Boss"
    wage = 0
    unlocks_entities = [StudentDeveloper, ShittyDeveloper, MediocreDeveloper]


def init_game():
    initial_player_inventory = {
        'money': 10000,
    }
    initial_player_drain = {
        'money': 5
    }
    initial_player_replenish = {}

    player = Boss(
        unlocked=True,
        inventory=initial_player_inventory,
        draining=initial_player_drain,
        replenishing=initial_player_replenish,
    )
    global objects
    objects.append(player)

objects = []
entities = [Boss, StudentDeveloper, ShittyDeveloper, MediocreDeveloper]

if __name__ == "__main__":

    init_game()
    while True:

        action = ui.cli(objects, entities)
        objects.append(action)

