from threading import Lock
from random import randint
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
        self.lock = Lock()

    def change_def(self, item_name):
        result = None

        with self.lock:
            if item_name not in list(ITEM['defence'].keys()):
                result = False
            else:
                self.defence = ITEM['defence'][item_name]
                result = True

        return result

    def change_question(self, question_id):
        self.question_id = question_id

    def is_attack_success(self, item_name):
        result = None

        with self.lock:
            if item_name not in list(ITEM['attack'].keys()):
                result = False
            else:
                result = self.defence <= ITEM['attack'][item_name]['value']

        return result

    def attacked(self, team_id):
        result = None

        with self.lock:
            if self.is_blocked:
                result = False
            else:
                self.is_blocked = True
                self.block_time = 60 * 5
                self.team_attacking = team_id

                result = True

        return result

    def change_owner(self, team_id):
        result = None

        with self.lock:
            if self.owner_id == team_id:
                result = False
            else:
                self.owner_id = team_id
                self.gold_delay = 30

                result = True

        return result

    def reduce_gold_delay(self):
        is_have_resource = False

        with self.lock:
            self.gold_delay -= 1

            if self.gold_delay == -1:
                self.gold_delay = 30
                is_have_resource = True

        return True

    @staticmethod
    def create_castle_list(n_castles=3, n_questions):
        castles = []

        for i in range(n_castles):
            castles.append(Castle(i, randint(0, n_questions)))

        return castles
