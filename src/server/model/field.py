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
        """Return question's id
        :param resource: a type of resource
        :return question_id: this resource's question's id
        """
        return self.resources[resource]['question']

    def add_solver(self, resource, team_id):
        """Add a team to list of solver
        :param resource: a type of resource
        :param team_id: team's id
        :return result
        """
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
        """Check whether a team is solved a field's resource"""
        return len(list(filter(lambda x: x['team_id'] == team_id,
                               self.resources[resource]['solvers']))) == 1

    def get_solvers(self, resource):
        """Return a list of solvers of one kind resource"""
        solvers = []

        with self.lock:
            solvers = self.resources[resource]['solvers']

        return solvers

    def reduce_time(self, resource):
        """Reduce resource's timer"""
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
                fields.append(Field(int(row[0]),
                                          int(row[1]),
                                          int(row[2]),
                                          int(row[3])))
        return fields
