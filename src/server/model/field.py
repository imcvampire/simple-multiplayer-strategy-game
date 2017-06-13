from threading import Lock
from random import randint


class Field:
    def __init__(self, id, questionid1, questionid2, questionid3):
        self.id = id
        self.resources = {
            "iron": {
                "solvers": [],
                "question": questionid1,
            },

            "stone": {
                "solvers": [],
                "question": questionid2,
            },

            "wood": {
                "solvers": [],
                "question": questionid3,
            },
        }
        self.lock = Lock()

    def get_question_id(self, resource):
        return self.resources[resource]['question']

    def add_solver(self, resource, team_id):
        result = False

        with self.lock:
            if not (team_id in self.resources[resource]['solvers']):
                self.resources[resource]['solvers'].append(team_id)

                result = True

        return result

    def is_solved(self, resource, team_id):
        return team_id in self.resources[resource]['solvers']

    @staticmethod
    def create_field_list(n_fields=3, n_questions):
        fields = []

        for field_index in range(n_fields):
            fields.append(Field(field_index, randint(0, n_questions)))

        return fields

