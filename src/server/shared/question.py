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

