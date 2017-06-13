import question
# print 1
ques = question.Question.get_questions_from_file("question.csv")
# for i in ques:
#     print i.id,i.content
#     print i.choices
#     print i.answer
print ques[35].get_question()
print ques[35].check_answer('3')
# listQues = question.ListQuestion()
# listQues.get_questions("question.csv")
# listQues.printListQuestion()
# print listQues.get_question_by_id(35)
# print listQues.check_answer_by_id(35, 3)
# print listQues.check_answer_by_id(35, 2)
