import os, sys
# import path

sys.path.append(os.path.abspath('../model'))

from question import *
from field import *
from castle import *
from team import *
from item import *

class controller:
    def __init__(self, file_name_question='question.csv'):
        self.questions = Question.get_questions(file_name_question)
        self.teams = Team.get_teams_from_file()        
        self.castles = Castle.get_castles_from_file()
        self.fields = Field.get_fields_from_file()
    def join_team(self, player, team_id):
        for i in self.teams:
            if i.id == team_id:
                if i.add_member(player):
                    return True
                else:
                    return "max_players"
        return False
    def get_question_by_id(self, question_id): #0x0101
        for i in self.questions:
            if i.id == question_id:
                return i.get_question()
        return None, None

    def check_question_mine(self,mine_id, resource, team_id): #0x0201
        for i in self.fields:
            if i.id == mine_id:
                return i.is_solved(self, resource, team_id)

    def get_questionid_mine(self,mine_id, resource): #0x0201
        for i in self.fields:
            if i.id == mine_id:
                return i.get_question_id(resource)
        return False
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

    def get_question_mine(self, mine_id, resource):
        Id = self.get_questionid_mine(mine_id, resource)
        if Id == False:
            return None, None
        else:
            return self.get_question_by_id(Id)

    ### 0x0301 ###
    def check_answer_mine(self, mine_id, resource, team_id, answer):
        print("check")
        if self.check_question_mine(mine_id, resource, team_id):
            print("check1")
            return "is_solved"
        else:
            print("else")
            quesId = self.get_questionid_mine(mine_id, resource)
            if self.check_answer(self, answer, quesId):
                print("for")
                for i in self.fields:
                    if i.id == mine_id:
                        i.add_solver(resource, team_id)
                print("true")
                return True
            else:
                print("false")
                return False

    def check_castle(self, team_id, castle_id): #0x0501
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id:
                        if castle.is_blocked:
                            return "blocked"
                        if castle.owner_id == None:
                            return "empty_castle"
                        elif team_id == castle.owner_id:
                            return "our_castle"
                        else :
                            return "attack"
                return "not_found_castle"
        return "not_found_team"

    def check_weapon_attack(self, team_id, weapon):
        for i in self.teams():
            if i.id == team_id:
                return weapon in i.inventory and weapon in ITEM['attack'].keys()
        return "not_found_team"

    def attack_castle(self, team_id, castle_id):
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id: 
                        castle.attacked(team_id)
                        try:
                            if castle.is_attack_success(team.inventory[0]):
                                return True
                            else:
                                return False
                        except:
                            return False
                return "not_found_castle"
        return "not_found_team"

    def get_question_id_castle(self, castle_id):
        for castle in self.castles:
            if castle.id == castle_id: 
                return castle.question_i_i       
        return "not_found_castle"

        
    def answer_castles_success(self, team_id, castle_id):
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id: 
                        castle.owner_id = team_id
                        castle.block_time = 60
                        castle.is_blocked = True
                        castle.change_question((castle.question_id+3)%37)
                return "not_found_castle"
        return "not_found_castle"


    def get_team_resources(self):
        team_resources = []
        for i in self.teams:
            team_resources.append((i.id, i.resources["gold"], i.resources["iron"], i.resources["wood"], i.resources["stone"], i.inventory))        
        return team_resources

    def add_resource(self, team_id):
        for team in self.teams:
            if team.id == team_id:
                team.add_resource("gold", 10000)
                team.add_resource("iron", 10000)
                team.add_resource("stone", 10000)
                team.add_resource("wood", 10000)

control = controller()
control.add_resource(1)
print control.get_team_resources()
control.buy_item(1,'balista', 'attack')
control.buy_item(1,'stone', 'defence')
print control.get_team_resources()
print control.buy_item(2,'stone', 'defence')