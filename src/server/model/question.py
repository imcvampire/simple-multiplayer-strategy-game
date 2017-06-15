import csv


class Question:
    def __init__(self, id, content, choice_1, choice_2, choice_3, choice_4, answer):
        self.id = id
        self.content = content
        self.choices = [
            choice_1,
            choice_2,
            choice_3,
            choice_4,
        ]
        self.answer = answer

    def check_answer(self, choice):
        return choice == self.answer

    def get_question(self):
        return self.content, self.choices

    @staticmethod
    def get_questions(file_name='questions.csv'):
        questions = []

        with open(file_name) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for index, row in enumerate(csvreader):
                questions.append(Question(int(row[0]),
                                          row[1],
                                          row[2],
                                          row[3],
                                          row[4],
                                          row[5],
                                          row[6]))

        return questions
