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

    def add_item(self, item_id):
        if item_id not in self.inventory:
            self.inventory.append(item_id)
            return True

        return False

    def buy_item(self, type, item_id):
        return None
