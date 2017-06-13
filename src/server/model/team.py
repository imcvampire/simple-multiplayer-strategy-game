from threading import Lock
from item import ITEM


class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.members = []
        self.resources = {
            "gold": 0,
            "iron": 0,
            "stone": 0,
            "wood": 0,
        }
        self.inventory = []
        self.lock = Lock()

    def add_member(self, member):
        if len(self.members) >= 4:
            return False

        self.members.append(member)

        return True

    def add_resource(self, type, amount):
        with self.lock:
            self.resources[type] += amount

    def __reduce_resource(self, type, amount):
        if self.resources[type] >= amount:
            self.resources[type] -= amount

            return True

        return False

    def __add_item(self, item_name):
        if item_name not in self.inventory:
            self.inventory.append(item_name)
            return True

        return False

    def __is_enough(self, price):
        types = price.keys()

        is_enough = True

        for type in types:
            is_enough = (is_enough
                         and self.resources[type] >= price[type])

        return is_enough

    def is_have(self, item_name):
        # Thread safe
        return item_name in self.inventory

    def buy_item(self, type, item_name):
        if item_name not in ITEM[type].keys():
            return False

        price = ITEM[type][item_name]['resources']

        resource_types = price.keys()

        result = False

        with self.lock:
            if not self.__is_enough(price):
                return False

            for type, amount in price.items():
                self.__reduce_resource(type, amount)

            result = self.__add_item(item_name)

        return result

    def use_item(self, item_name):
        result = False

        with self.lock:
            if item_name in self.inventory:
                self.inventory.remove(item_name)

                result = True

        return result

