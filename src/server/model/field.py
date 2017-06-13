from threading import Lock


class Field:
    def __init__(self, id, questions):
        self.id = id
        self.resources = {
            "iron": {
                "solvers": [],
                "question": questions[0],
            },

            "stone": {
                "solvers": [],
                "question": questions[1],
            },

            "wood": {
                "solvers": [],
                "question": questions[2],
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

