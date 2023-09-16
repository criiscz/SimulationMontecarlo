from operator import attrgetter


class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.points = 0

    def win_round(self):
        self.points += 1

    def sort_by_luck(self):
        self.players.sort(key=lambda player: player.luck, reverse=True)

    def sort_by_points(self):
        self.players.sort(key=lambda player: player.points, reverse=True)

    def global_score(self, individual):
        self.points += individual

    def lucky_player(self):
        return max(self.players, key=attrgetter('luck'))

    def lucky_player_round(self):
        return max(self.players, key=attrgetter('extra'))

    def finish_game(self):
        self.points = 0
        for player in self.players:
            player.restart_endurance()
            player.expert_launch = 0
            player.points = 0
            player.win = 0
            player.expert_launch_bool = False

    def player_winner_round(self):
        winner = max(self.players, key=attrgetter('points'))
        winner.win_round()
        return winner

    def player_winner(self):
        return max(self.players, key=attrgetter('points'))

    def new_round(self):
        for player in self.players:
            player.finish_round()

    def player_win(self):
        return max(self.players, key=attrgetter('win'))
