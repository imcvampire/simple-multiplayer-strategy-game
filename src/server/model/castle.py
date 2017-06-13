from item import ITEM


class Castle:
    def __init__(self, id, question_id):
        self.id = id
        self.owner_id = None
        self.defence = 0
        self.is_blocked = False
        self.team_attacking = None
        self.block_time = 0
        self.question_id = question_id
        self.gold_delay = 0

    def change_def(self, item_name):
        if item_name not in list(ITEM['defence'].keys()):
            return False

        self.defence = ITEM['defence'][item_name]
        return True

    def is_attack_success(self, item_name):
        if item_name not in list(ITEM['attack'].keys()):
            return False

        return self.defence <= ITEM['attack'][item_name]['value']

    def attacked(self, team_id):
        if self.is_blocked:
            return False

        self.is_blocked = True
        self.block_time = 60 * 5
        self.team_attacking = team_id

        return True

    def change_owner(self, team_id):
        if self.owner_id == team_id:
            return False

        self.owner_id = team_id
        self.gold_delay = 30

    def reduce_gold_delay(self):
        self.gold_delay -= 1

        if self.gold_delay == 0:
            self.gold_delay = 30

