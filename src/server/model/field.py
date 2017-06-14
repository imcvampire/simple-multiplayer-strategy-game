from threading import Lock
from random import randint
import csv

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
                self.resources[resource]['solvers'].append({
                    'team_id': team_id,
                    'time': 30,
                })

                result = True

        return result

    def is_solved(self, resource, team_id):
        return len(list(filter(lambda: x: x['team_id'] == team_id,
                               self.resources[resource]['solvers']))) == 1

    def get_solvers(self, resource):
        solvers = []

        with self.lock:
            solvers = self.resources[resource]['solvers']

        return solvers

    def reduce_time(self, resource):
        teams_have_resource = []

        with self.lock:
            solvers = self.resources[resource]['sovlers']

            for solver in solvers:
                solver['time'] -= 1
                if solver['time'] == -1:
                    solver['time'] = 30
                    teams_have_resource.append(solver['team_id'])

        return teams_have_resource

    @staticmethod
    def get_fields_from_file(file_name='fields.csv'):
        fields = []

        with open(file_name) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for index, row in enumerate(csvreader):
                fields.append(Field(row[0],
                                          row[1],
                                          row[2],
                                          row[3]))

        return fields
