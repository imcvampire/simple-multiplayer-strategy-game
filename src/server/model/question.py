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
    def get_questions_from_file(file_name='questions.csv'):
        questions = []

        with open(file_name) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for index, row in enumerate(csvreader):
                questions.append(Question(index,
                                          row[1],
                                          row[2],
                                          row[3],
                                          row[4],
                                          row[5],
                                          row[6]))

        return questions

class ListQuestion:
    def __init__(self):
        self.questions = []

    def get_questions(self, file_name='questions.csv'):
        
        with open(file_name) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')

            for index, row in enumerate(csvreader):
                self.questions.append(Question(index,
                                          row[1],
                                          row[2],
                                          row[3],
                                          row[4],
                                          row[5],
                                          row[6]))

    def printListQuestion(self):
        for i in self.questions:
            print i.id
            print i.content
            print 1, i.choices[0]
            print 2, i.choices[1]
            print 3, i.choices[2]
            print 4, i.choices[3]
            print "Answer:", i.answer
            print 
    
    def get_question_by_id(self, id):
        for i in self.questions:
            if i.id == id:
                return i.get_question()
        return None
    
    def check_answer_by_id(self, id, choice):
        for i in self.questions:
            if i.id == id:
                return i.check_answer(choice)
        return "Not found!"
