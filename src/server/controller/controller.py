from src.server.model.question import *
from src.server.model.field import *
from src.server.model.castle import *
from src.server.model.team import *
from src.server.model.item import *

class controller:
    def __init__(self, file_name_question='question.csv'):
        self.questions = Question.get_questions(file_name_question)
        self.teams = []
        self.teams.append(Team('team1', "Red"))
        self.teams.append(Team('team2', "Yealow"))
        self.teams.append(Team('team3', "Blue"))
        self.castles = []
        self.castles.append(Castle(1,1))
        self.castles.append(Castle(2,2))
        self.castles.append(Castle(3,3))
        self.fields = []
        self.fields.append(Field(1,4,5,6))
        self.fields.append(Field(2,7,8,9))
        self.fields.append(Field(3,10,11,12))
    def join_team(self, player, team_id):
        for i in self.teams:
            if i.id == team_id:
                if i.add_member(player):
                    return True
                else :
                    return "max_players"
        return False
    def get_question_by_id(self, question_id): #0x0101
        for i in self.questions:
            if i.id == question_id:
                return i.get_question()
        return None

    def send_question_mine(self,mine_id, resource, team_id): #0x0201
        for i in self.fields:
            if i.id == mine_id:
                if i.is_solved(self, resource, team_id):
                    return "team_solved"
                else :
                    return i.get_question()

    def check_answer(self, answer, question_id): #0x0301
        for i in self.questions:
            if i.id == question_id:
                return i.check_answer(answer)
        return "Not_found_question"



    def buy_item(self, team_id, itemname, type): #0x0401
        for team in self.teams:
            if team.id == team_id:
                if team.is_have(itemname):
                    return "already_have"
                else:
                    if team.is_enough(ITEM[type][itemname]['resources']):
                        return team.buy_item(type, itemname)
                        
                    else:
                        return "not_enough_resource"
        return "not_found_team"

    def check_castle(self, team_id, castle_id): #0x0501
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id:
                        if castle.is_blocked:
                            return "blocked"
                        if castle.owner_id == None: 
                            return "empty_castle"
                        else if team_id == castle.owner_id:
                            return "our_castle"
                        else :
                            return "attack"
                return "not_found_castle"
        return "not_found_team"

    def set_defense(self,team_id, castle_id, itemname): #0x0601
        for team in self.teams:
            if team.id == team_id:
                if not team.is_have(itemname):
                    if self.buy_item(team_id, itemname,'defence') != True:
                        return "cant_set_defense"


                for castle in self.castles:
                    if castle.id == castle_id:
                        if team.use_item(itemname):
                            if castle.change_def(itemname):
                                return True
                            else :
                                return False
                return "not_found_castle"
        return "not_found_team"





     


