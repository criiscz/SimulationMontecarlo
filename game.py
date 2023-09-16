import random

from player import Player
from team import Team


def create_player(id, endurance, luck, gender):
    return Player(id, "female" if gender == 1 else "male", float(1 + (3 - 1) * luck), endurance)


def create_teams(name):
    players = [create_player(name + "_" + str(i), random.randrange(25, 46, 10), random.random(), random.randint(0, 1))
               for
               i in
               range(5)]
    return Team(players=players, name=name)


def get_point(launch, player):
    new_launch = int(100 * launch)
    if player.gender == "male":
        if new_launch <= 20:
            return 10
        elif 20 <= new_launch <= 53:
            return 9
        elif 53 <= new_launch <= 93:
            return 8
        elif 93 <= new_launch < 100:
            return 0
    elif player.gender == "female":
        if new_launch <= 30:
            return 10
        elif 30 <= new_launch <= 68:
            return 9
        elif 68 <= new_launch <= 95:
            return 8
        elif 95 <= new_launch <= 100:
            return 0


def launch_for_player(launch, player):
    player.launch()
    player.win_points(get_point(launch, player))


def assign_fatigue(team):
    fatigues = [1 if random.randint(0, 1) == 0 else 2 for _ in range(5)]
    for i in range(5):
        team.players[i].fatigue(fatigues[i])

    return team


def assign_luck(team):
    for player in team.players:
        lucky = float(1 + (3 - 1) * random.random())
        player.assign_luck(lucky)


def launch_lucky(team):
    lucky = random.random()
    team.global_score(get_point(lucky, team.lucky_player()))
    if team.lucky_player().extra == 0:
        team.lucky_player().extra = 1
    else:
        team.lucky_player().extra_launch()
    if team.lucky_player().extra >= 3:
        lucky = random.random()
        team.get_global_score(get_point(lucky, team.lucky_player()))


def play_round(team, launch):
    init = 0
    for player in team.players:
        count = -1
        for step in launch[init:count]:
            # print("count: ", count, "step: ", step, "player: ", player.id, "points: ", player.points, "endurance: ",
            #       player.endurance_round, "luck: ", player.luck)
            count += 1
            if player.endurance_round < 5:
                break
            launch_for_player(step, player)
        team.global_score(player.points)
        init = count + 1
    launch_lucky(team)
    team = assign_fatigue(team)

    return team


def solve_tie(team_1, team_2):
    while team_1.player_winner().points == team_2.player_winner().points:
        launch = random.random()
        launch2 = random.random()

        point_1 = get_point(launch, team_1.player_winner())
        point_2 = get_point(launch2, team_2.player_winner())
        team_1.player_winner().win_points(point_1)
        team_2.player_winner().win_points(point_2)


def solve_tie_finish(team_1, team_2):
    while team_1.player_winner().win == team_2.player_winner().win:
        launch = random.random()
        launch2 = random.random()
        point_1 = get_point(launch, team_1.player_winner())
        point_2 = get_point(launch2, team_2.player_winner())
        if point_1 > point_2:
            team_1.player_winner().win += 1
        elif point_1 < point_2:
            team_2.player_winner().win += 1


class Game:
    def __init__(self):
        self.team_one_history = []  # History of Team 1
        self.team_two_history = []  # History of Team 2
        self.male_total = 0  # Total male victories
        self.female_total = 0  # Total female victories
        self.genero_ganador_total = ""  # Total gender winner
        self.player_points_history = {}  # History of player points

    def init_play(self, team_one, team_two):
        global winner_round
        winner = {"player": Player(0, 0, 0, 0), "team": ""}  # Initialize winner
        male = 0  # Counter for male victories
        female = 0  # Counter for female victories
        player_points_history = {}  # History of player points by round
        self.player_points_history = {}  # History of player points

        # Repeat 10 rounds of the game
        for _ in range(10):

            team_one.new_round()  # Start round for Team 1
            team_two.new_round()  # Start round for Team 2

            # Calculate average launches for each team
            launch_1 = int(sum(player.endurance_round for player in team_one.players) / len(team_one.players))
            launch_2 = int(sum(player.endurance_round for player in team_two.players) / len(team_two.players))

            # Generate random launches for each team
            launch_r_1 = [random.random() for _ in range(launch_1)]
            launch_r_2 = [random.random() for _ in range(launch_2)]

            # Play the round for each team
            play_round(team_one, launch_r_1)
            play_round(team_two, launch_r_2)
            assign_luck(team_one)
            assign_luck(team_two)

            winner_1 = team_one.player_winner()  # Get winner of Team 1
            winner_2 = team_two.player_winner()  # Get winner of Team 2

            # Resolve tie in points between team winners
            if winner_1.points == winner_2.points:
                solve_tie(team_one, team_two)

            # Determine round winner
            if winner_1.points != winner_2.points:
                winner_round = team_one.player_winner_round() if winner_1.points > winner_2.points else team_two.player_winner_round()

            # Count victories by gender
            if winner_round.gender == "male":
                male += 1
            elif winner_round.gender == "female":
                female += 1

            # Add all player points to history by round
            for player in team_one.players:
                if player.id not in player_points_history:
                    player_points_history[player.id] = []
                player_points_history[player.id].append(player.points)
            for player in team_two.players:
                if player.id not in player_points_history:
                    player_points_history[player.id] = []
                player_points_history[player.id].append(player.points)

            launch_lucky(team_one)
            launch_lucky(team_two)

        # Add player points history to global history { player_id: total_points }
        for player_id, points in player_points_history.items():
            if player_id not in self.player_points_history:
                self.player_points_history[player_id] = []
            self.player_points_history[player_id].append(sum(points))

        # Resolve tie in final team victories
        if team_one.player_win().win == team_two.player_win().win:
            solve_tie_finish(team_one, team_two)

        # Determine final winner
        if team_one.player_win().win > team_two.player_win().win:
            winner = {"player": team_one.player_win(), "team": team_one.name}
        elif team_one.player_win().win < team_two.player_win().win:
            winner = {"player": team_two.player_win(), "team": team_two.name}

        self.team_one_history.append(team_one)  # Add Team 1 to history
        self.team_two_history.append(team_two)  # Add Team 2 to history

        lucky = {"player": Player(0, 0, 0, 0), "team": ""}  # Initialize lucky player
        if team_one.lucky_player_round().extra > team_two.lucky_player_round().extra:
            lucky = {"player": team_one.lucky_player_round(), "team": team_one.name}
        elif team_one.lucky_player_round().extra < team_two.lucky_player_round().extra:
            lucky = {"player": team_two.lucky_player_round(), "team": team_two.name}

        genero_ganador_ronda = "female" if female > male else "male"  # Determine round gender winner
        self.female_total += 1 if genero_ganador_ronda == "female" else 0  # Update female victories counter
        self.male_total += 1 if genero_ganador_ronda == "male" else 0  # Update male victories counter

        # Determine total gender winner
        self.genero_ganador_total = "female" if self.female_total > self.male_total else "male"

        return {
            "team_1": team_one,
            "team_2": team_two,
            "team_win": team_one if team_one.points > team_two.points else team_two,  # Winning team
            "winner": winner,  # Final winner
            "lucky": lucky,  # Lucky player
            "male": self.male_total,  # Total male victories
            "female": self.female_total,  # Total female victories
            "gender_winner": genero_ganador_ronda,  # Round gender winner
            "gender_winner_total": self.genero_ganador_total,  # Total gender winner
            "player_points_history": self.player_points_history  # Player points history
        }

    # Rest of the code unchanged, with comments in English.

    def restart_historial(self):
        self.team_one_history = []  # Reset Team 1 history
        self.team_two_history = []  # Reset Team 2 history
        self.male_total = 0  # Reset total male victories
        self.female_total = 0  # Reset total female victories

    def get_total_points(self):
        team_1_name = self.team_one_history[0].name if self.team_one_history else ""
        team_2_name = self.team_two_history[0].name if self.team_two_history else ""
        total_points_1 = sum(team.points for team in self.team_one_history)
        total_points_2 = sum(team.points for team in self.team_two_history)

        return {
            "male": self.male_total,
            "female": self.female_total,
            "team_1": team_1_name,
            "total_points_1": total_points_1,
            "team_2": team_2_name,
            "total_points_2": total_points_2,
        }
