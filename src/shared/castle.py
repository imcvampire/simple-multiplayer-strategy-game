import item

class Castle:
    def __init__(self, id, question_id):
        self.id = id
        self.owner_id = null
        self.defence = 0
        self.is_blocked = false
        self.team_attacking = null
        self.block_time = 0
        self.question_id = question_id

    def change_def(self, item_id):
        if not (item_id >= 3 and item_id <= 5):
            return False

        self.defence = item[item_id]
        return True

    def is_attack_success(self, item_id):
        if not (item_id >= 0 and item_id <= 2):
            return False

        return self.defence <= item[item_id]

    def attacked(self, team_id):
        if self.is_blocked:
            return False

        self.is_blocked = True
        self.block_time = 60 * 5
        self.team_attacking = team_id

        return True

