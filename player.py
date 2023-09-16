class Player:
    def __init__(self, id, gender, luck, endurance):
        self.id = id
        self.gender = gender
        self.luck = luck
        self.endurance = endurance
        self.experience = 10
        self.endurance_round = endurance
        self.endurance_previous_round = endurance
        self.points = 0
        self.extra = 0
        self.win = 0
        self.player_total_points = 0
        self.expert_launch = 0
        self.expert_launch_bool = False

    def launch(self):
        if self.experience >= 9 and not self.expert_launch_bool:
            self.expert_launch = 2
            self.expert_launch_bool = True
        if self.expert_launch > 0:
            self.expert_launch -= 1
            self.endurance_round -= 1
        if self.expert_launch == 0:
            self.expert_launch_bool = False
            self.endurance_round -= 5

    def win_points(self, point_launch):
        self.points += point_launch

    def finish_round(self):
        self.points = 0
        self.endurance_round = self.endurance

    def win_round(self):
        self.win += 1
        self.experience += 3

    def assign_luck(self, luck):
        self.luck = luck

    def fatigue(self, fatigue):
        self.endurance_round = self.endurance_previous_round - fatigue
        self.endurance_previous_round = self.endurance_round

    def restart_endurance(self):
        self.endurance_round = self.endurance
        self.endurance_previous_round = self.endurance

    def extra_launch(self):
        if self.extra != 0:
            self.extra -= 1
        else:
            self.extra = 0
