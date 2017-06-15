from item import ITEM
import csv 

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
        self.inventory = [None, None]

    def add_member(self, member):
        if len(self.members) >= 4:
            return False
        self.members.append(member)
        return True

    def add_resource(self, type, amount):
        self.resources[type] += amount

    def reduce_resource(self, type, amount):
        if self.resources[type] < amount:
            return False

        self.resources[type] -= amount

        return True

    def add_item(self, item_name):
        if item_name not in self.inventory:
            self.inventory.append(item_name)
            return True
        return False

    def is_enough(self, price):
        types = price.keys()

        is_enough = True

        for type in types:
            is_enough = (is_enough
                         and self.resources[type] >= price[type])

        return is_enough

    def is_have(self, item_name):
        return item_name in self.inventory

    def buy_item(self, type, item_name):
        if item_name not in ITEM[type].keys():
            return False

        price = ITEM[type][item_name]['resources']

        resource_types = price.keys()

        if not self.is_enough(price):
            return False

        for type, amount in price.items():
            self.reduce_resource(type, amount)
        # print "reduce resource"
        if item_name in ITEM['attack'].keys():
            # print "atk"
            try:      
                self.inventory[0] = item_name
                return True
            except:
                return "ERROR_append_item"
        else:
            # print "def"
            try:      
                self.inventory[1] = item_name
                return True
            except:
                return "ERROR_append_item"
 
    def use_item(self, item_name):
        if not item_name in self.inventory:
            return False

        self.inventory.remove(item_name)

        return True
   

    
    @staticmethod
    def get_teams_from_file(file_name='teams.csv'):
        teams = []

        with open(file_name) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for index, row in enumerate(csvreader):
                teams.append(Team(int(row[0]), row[1]))

        return teams