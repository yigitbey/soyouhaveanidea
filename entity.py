import copy
from exceptions import *

class EntityMeta(type):
    def __new__(mcs, clsname, superclasses, attributedict):
        clss = type.__new__(mcs, clsname, superclasses, attributedict)
        if 'cost' in attributedict:
            clss.message = "{} (${} monthly)".format(attributedict['formatted'], attributedict['cost'])
        else:
            clss.message = "{}".format(attributedict['formatted'])
        return clss


class Entity(object, metaclass=EntityMeta):
    current_amount = 0
    initial_cost = 0
    limit = -1
    unlocked = False
    age = 0
    unlocked_age = 0
    unlocks_entities = []
    locks_entities = []
    cost = 0
    formatted = "Entity"
    drains = {}
    replenishes = {}
    inventory = {'money': 0}
    project = None
    increases = {}
    decreases = {}
    productivity_modifier = 0
    detail_fields = []
    article = "a"

    def __init__(self, project=None, inventory=inventory, draining=drains, replenishing=replenishes):

        if self.__class__.limit >= 0:
            if self.__class__.current_amount >= self.__class__.limit:
                raise TooManyEntitiesException("No limit for {}".format(self.__class__.__name__))

        self.inventory = copy.deepcopy(inventory)
        self.draining = copy.deepcopy(draining)
        self.replenishing = copy.deepcopy(replenishing)
        self.project = project
        self.__class__.current_amount += 1
        self.__class__.unlocks()
        self.__class__.locks()

    def __repr__(self):
        return self.__class__.__name__

    def trade(self, to_entity, item, value):
        item1 = getattr(self, item)
        item2 = getattr(to_entity, item)
        setattr(self, item, item1-value)
        setattr(to_entity, item, item2+value)

    def turn(self):
        self.drain()
        self.replenish()
        self.age += 1

    def drain(self):
        for key, value in self.draining.items():
            self.inventory[key] -= value

    def replenish(self):
        for key, value in self.replenishing.items():
            self.inventory[key] += value

    @property
    def money(self):
        return self.inventory['money']

    @money.setter
    def money(self, value):
        self.inventory['money'] = value

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

    def fire(self):
        pass

