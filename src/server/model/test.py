import question, field, castle, team
print 1
ques = question.Question.get_questions("question.csv")
for i in ques:
    print i.id,i.content
    print i.choices
    print i.answer
print ques[35].get_question()
print ques[35].check_answer('3')

fields = field.Field.get_fields_from_file()
for i in fields:
	print "Field", i.id
	idq = int(i.get_question_id("wood"))
	print ques[idq].get_question()

castles = castle.Castle.get_castles_from_file()
for i in castles:
	print "Castle", i.id
	idq = int(i.question_id)
	print ques[idq].get_question()

teams = team.Team.get_teams_from_file()
for i in teams:
	print i.id, "Team", i.name