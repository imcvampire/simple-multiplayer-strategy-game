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
        self.questions = Question.get_questions()
        self.teams = Team.get_teams_from_file()
        self.castles = Castle.get_castles_from_file()
        self.fields = Field.get_fields_from_file()
    def join_team(self, player, team_id):
        for i in self.teams:
            print i.id
            if i.id == team_id:
                print 1
                if i.add_member(player):
                    return True
                else:
                    return "max_players"
        return False
    def get_question_by_id(self, question_id): #0x0101
        for i in self.questions:
            if i.id == question_id:
                return i.get_question()
        return None

    def check_question_mine(self,mine_id, resource, team_id): #0x0201
        for i in self.fields:
            if i.id == mine_id:
                return i.is_solved(self, resource, team_id)

    def get_question_mine(self,mine_id, resource, team_id): #0x0201
        for i in self.fields:
            if i.id == mine_id:
                return i.get_question_id(resource)
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
                        elif team_id == castle.owner_id:
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


    def check_castle(self, team_id, castle_id): #0x0501
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id:
                        if castle.is_blocked:
                            return "blocked"
                        if castle.owner_id == None or castle.defence == 0:
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

    def attack_castle(self, team_id, castle_idgi, item_attack):
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id: 
                        castle.attacked(team_id)
                        if castle.is_attack_success(item_attack):
                            castle.defence = 0
                            return True
                        else:
                            return False

                return "not_found_castle"
        return "not_found_castle"
        
        
    def answer_castles_success(self, team_id, castle_id):
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id: 
                        castle.owner_id = team_id
                        castle.block_time = 60
                        castle.is_blocked = True

                return "not_found_castle"
        return "not_found_castle"


    def get_team_resources(self):
        team_resources = []
        for i in self.teams:
            team_resources.append((i.id, i.resources, i.inventory))
        
        return team_resources
