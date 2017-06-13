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

    def get_question_id(self, resource):
        return self.resources[resource].question.get_question()

    def add_solver(self, resource, team_id):
        if team_id in self.resources[resource].solvers:
            return False

        self.resources[resource].solvers.append(team_id)

        return True

    def is_solved(self, resource, team_id):
        return team_id in self.resources[resource].solvers

