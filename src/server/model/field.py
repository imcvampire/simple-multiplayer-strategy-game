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

    def get_question_id(self, resource):
        return self.resources[resource]['question']

    def add_solver(self, resource, team_id):
        if team_id in self.resources[resource]['solvers']:
            return False
        self.resources[resource]['solvers'].append(team_id)
        return True

    def is_solved(self, resource, team_id):
        return team_id in self.resources[resource]['solvers']

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
