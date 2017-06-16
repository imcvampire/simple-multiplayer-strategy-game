import os, sys
# import path

sys.path.append(os.path.abspath('model'))
sys.path.append(os.path.abspath('../model'))

from question import *
from field import *
from castle import *
from team import *
from item import *

class controller:
    def __init__(self, file_name_question='controller/question.csv'):
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
                return i.is_solved(resource, team_id)

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
                return team.buy_item(type, itemname)
        return "not_found_team"

    def check_item_attack_team(self, team_id, itemname):
        for team in self.teams:
            if team.id == team_id:
                if len(team.inventory) == 0:
                    return True
                else:
                    if itemname == team.inventory[0]:
                        return "had_it"
                    if ITEM['attack'][itemname]['value'] > ITEM['attack'][team.inventory[0]]['value']:
                        return True
                    else:
                        return "you_had_best"

    def buy_attack(self, team_id, itemname):
        for team in self.teams:
            if team.id == team_id:
                result = self.check_item_attack_team(team_id, itemname)
                if result != True:
                    return result
                else:
                    return self.buy_item(team_id, itemname, 'attack')

    def check_item_defence(self, castle_id, itemname):
        for castle in self.castles:
            if castle.id == castle_id:
                if castle.defence == 0:
                    return True
                else:
                    if ITEM['defence'][itemname]['value'] > castle.defence:
                        return True
                    else: return "you_had_best"

    def buy_defense(self,team_id, castle_id, itemname): #0x0601
        for castle in self.castles:
            if castle.id == castle_id:
                if castle.owner_id == team_id:
                    result = self.check_item_defence(castle_id, itemname)
                    if result != True: return result
                    else:
                        result = self.buy_item(team_id, itemname, 'defence')
                        if result != True:
                            return result
                        else:
                            castle.defence = ITEM['defence'][itemname]['value']
                            return True
                else:
                    return "not_owner"
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
        if self.check_question_mine(mine_id, resource, team_id):
            return "is_solved"
        else:
            quesId = self.get_questionid_mine(mine_id, resource)
            if self.check_answer(answer, quesId):
                for i in self.fields:
                    if i.id == mine_id:
                        i.add_solver(resource, team_id)
                        return True
                return False
            else:
                return False

    def check_castle(self, team_id, castle_id): #0x0501
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id:
                        print ('1: {}'.format(castle.is_blocked))
                        if castle.is_blocked:
                            return "blocked"
                        elif castle.owner_id == None:
                            castle.set_block()
                            print ('2: {}'.format(castle.is_blocked))
                            return "empty_castle"
                        elif team_id == castle.owner_id:
                            return "our_castle"
                        else :
                            return True
                return "not_found_castle"
        return "not_found_team"

    def attack_castle(self, team_id, castle_id):
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id:
                        castle.set_block()
                        try:
                            itemattack = team.inventory[0]
                        except:
                            itemattack = None
                        try:
                            if castle.is_attack_success(itemattack):
                                castle.block_time += 60*5
                                castle.attacked(team_id)
                                return True
                            else:
                                castle.remove_block()
                                team.inventory = []
                                return False
                        except:
                            return "Error"
                return "not_found_castle"
        return "not_found_team"


    def team_attack(self, team_id, castle_id):
        result = self.check_castle(team_id, castle_id)
        if result != True:
            return result
        else:
            return self.attack_castle(team_id, castle_id)


    def check_weapon_attack(self, team_id, weapon):
        for i in self.teams():
            if i.id == team_id:
                return weapon in i.inventory and weapon in ITEM['attack'].keys()
        return "not_found_team"


    def get_questionid_castle(self, castle_id):
        for castle in self.castles:
            if castle.id == castle_id:
                return castle.question_id
        return "not_found_castle"

    def check_answer_castle(self, castle_id, answer):
        quesId = self.get_questionid_castle(castle_id)
        result = self.check_answer(answer, quesId)
        if result == True:
            return True
        else:
            for castle in self.castles:
                if castle.id == castle_id:
                    castle.remove_block()
                    return result
            return False

    def answer_castles_success(self, team_id, castle_id):
        for team in self.teams:
            if team.id == team_id:
                for castle in self.castles:
                    if castle.id == castle_id:
                        castle.change_owner(team_id)
                        castle.change_question()
                return "not_found_castle"
        return "not_found_castle"


    def getData(self):
        list_team = []
        for i in self.teams:
            list_team.append((i.id, i.resources["gold"], i.resources["iron"], i.resources["wood"], i.resources["stone"]))
        list_defend = []
        list_owner = []
        for castle in self.castles:
            list_defend.append(castle.defence)
            list_owner.append(castle.owner_id)
        return list_team, list_defend, list_owner

    def add_resource(self, team_id):
        for team in self.teams:
            if team.id == team_id:
                team.add_resource("gold", 10000)
                team.add_resource("iron", 10000)
                team.add_resource("stone", 10000)
                team.add_resource("wood", 10000)


#control = controller()
