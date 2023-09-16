import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

from game import Game, create_teams


def send_team(team):
    players = [{'id': player.id, 'luck': player.luck, 'gender': player.gender,
                'points_total': player.player_total_points, 'experience': player.experience} for player in
               team.players]
    return {'name': team.name, 'players': players, "points": team.points}


def print_final_points(final_points):
    # Convertir los datos en una lista de listas para tabulate
    table_data = []
    for item in final_points:
        row = ["Game:" + str(item['Game'])]
        for player_num in range(5):
            player_key = f'team_1_{player_num}'
            row.append(f'T1P{player_num}:{item["Points"][player_key][0]}')
        for player_num in range(5):
            player_key = f'team_2_{player_num}'
            row.append(f'T2P{player_num}:{item["Points"][player_key][0]}')
        table_data.append(row)

    # Definir encabezados de la tabla
    headers = ['Game'] + [f'T1 P{i}' for i in range(5)] + [f'T2 P{i}' for i in range(5)]

    # Imprimir la tabla en la consola
    print(tabulate(table_data, headers, tablefmt='grid'))


def print_team_data(title, team_data, final_points):
    print(f'Team Name: {team_data["name"]} ---- {title}')
    print('Players:')
    players_data = []
    for player in team_data["players"]:
        player_id = player["id"]
        # Buscar los puntos totales del jugador en final_points
        player_points = [item["Points"][player_id][0] for item in final_points]
        total_points = sum(player_points)
        players_data.append([player["id"], player["luck"], player["gender"], total_points, player["experience"]])
    headers = ["ID", "Luck", "Gender", "Points Total", "Experience"]
    print(tabulate(players_data, headers, tablefmt='grid'))
    print(f'Total Points: {team_data["points"]}\n')


class GameSimulator:

    def __init__(self):
        self.play = Game()
        self.team_1_history = []
        self.team_2_history = []
        self.male_total = 0
        self.female_total = 0
        self.name_count = 0

    def create_team(self):
        self.name_count = self.name_count + 1
        str_name = "team_" + str(self.name_count)
        team = create_teams(name=str_name)
        players = [{'id': player.id, 'endurance': player.endurance, 'luck': player.luck,
                    'gender': player.gender, 'experience': player.experience} for player in team.players]
        # pprint({'name': team.name, 'players': players})
        df = pd.DataFrame(players)
        print("Team: " + team.name)

        # Print the DataFrame as a table
        print(tabulate(df, headers='keys', tablefmt='psql'))

        return team, players

    def play_round(self, team_1, team_2, iterations):
        global resultss
        final_points = []
        while iterations > 0:
            resultss = self.play.init_play(team_1, team_2)
            iterations -= 1
            iteration_results = {
                "Player luckiest in iteration": {
                    'iteration': iterations,
                    'id': resultss["lucky"]["player"].id,
                    'luck': resultss["lucky"]["player"].luck,
                    'gender': resultss["lucky"]["player"].gender,
                    'points': resultss["lucky"]["player"].points,
                    'extra': resultss["lucky"]["player"].extra,
                    "team": resultss["lucky"]["team"]
                },
                "Gender winner": resultss["gender_winner"]
            }
            final_points.append({
                'Game': iterations,
                'Points': resultss["player_points_history"],
            })

            print(tabulate(iteration_results.items(), tablefmt='grid'))

        final_results = {
            "Team One": send_team(resultss["team_1"]),
            "Team Two": send_team(resultss["team_2"]),
            "Team Winner": send_team(resultss["team_win"]),
            "Individual Winner": {
                'id': resultss["winner"]["player"].id,
                'Luck': resultss["winner"]["player"].luck,
                'Gender': resultss["winner"]["player"].gender,
                'Points': resultss["winner"]["player"].points,
                "Team": resultss["winner"]["team"]
            },
            "Female": resultss["female"],
            "Male": resultss["male"],
            "Gender with more total wins": resultss["gender_winner_total"],
            "Final Points": final_points,
            # "player_points_history": resultss["player_points_history"],
        }
        print_team_data("Team One", final_results["Team One"], final_points)
        print_team_data("Team Two", final_results["Team Two"], final_points)
        print_team_data("Team Winner", final_results["Team Winner"], final_points)
        print_final_points(final_points)
        data = self.total()
        table_data = [
            ['Male', data['male']],
            ['Female', data['female']],
            ['Total Points Team 1', data['total_points_1']],
            ['Total Points Team 2', data['total_points_2']]
        ]

        # Imprimir la tabla en la consola
        headers = ['Category', 'Value']
        print(tabulate(table_data, headers, tablefmt='grid'))
        self.play.restart_historial()
        return final_results

    def total(self):
        return self.play.get_total_points()

    def simulate(self):
        team_1, _ = self.create_team()
        team_2, _ = self.create_team()
        iterations = int(input("Input the number of iterations: "))
        result = self.play_round(team_1, team_2, iterations)
        return result


def create_scatter_plot(final_points):
    # Datos
    games = [item['Game'] for item in final_points]
    players = [f'team_1_{i}' for i in range(5)]
    players2 = [f'team_2_{i}' for i in range(5)]
    players.extend(players2)

    plt.figure(figsize=(10, 6))

    for player in players:
        player_points = [item['Points'][player][0] for item in final_points]
        plt.scatter(games, player_points, label=player)

    plt.title('Puntos de Jugadores por Juego')
    plt.xlabel('Juego')
    plt.ylabel('Puntos')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def create_line_plot(final_points):
    # Datos
    games = [item['Game'] for item in final_points]
    players = [f'team_1_{i}' for i in range(5)]  # Jugadores del equipo 1 (ajusta según tus datos)
    players2 = [f'team_2_{i}' for i in range(5)]  # Jugadores del equipo 1 (ajusta según tus datos)
    players.extend(players2)

    # Crear una gráfica separada para cada jugador
    for player in players:
        player_points = [item['Points'][player][0] for item in final_points]

        # Crear la gráfica
        plt.figure(figsize=(10, 6))
        plt.plot(games, player_points, label=player, marker='o')

        # Personalizar la gráfica
        plt.title(f'Puntos de {player} por Juego')
        plt.xlabel('Juego')
        plt.ylabel('Puntos')
        plt.legend()
        plt.grid(True)

        # Mostrar la gráfica
        plt.show()


if __name__ == "__main__":
    simulator = GameSimulator()
    results = simulator.simulate()
    final_points = results["Final Points"]

    # Crear y mostrar la gráfica de puntos de los jugadores
    create_scatter_plot(final_points)
    create_line_plot(final_points)
