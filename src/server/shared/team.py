class Team:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.members = []

    def add_member(self, member):
        if len(self.members) >= 4:
            return False

        self.members.append(member)

        return True
