from helpers.csv_helper import read_file
from models.player import Player
from team.pick import get_best_order_formula, get_players_order_by_rating, print_players


def pick_teams(
    players: list[Player],
    gks: set[str],
    fixeds: set[str],
    pivots: set[str],
    base_count: int,
):
    order_formula = [1, 2, 3, 3, 2, 1, 2, 3, 1, 1, 2, 3, 3, 2, 1]
    total = len(players)
    if total < 15:
        print(f"--------  Not enough players:  {total} --------\n")
    else:
        is_full = total == 18
        if is_full:
            order_formula.extend([2, 3, 1])

        sorted_players = get_players_order_by_rating(players)

        get_best_order_formula(
            sorted_players, order_formula, gks, fixeds, pivots, base_count
        )

        # print all the players that dont fit (ex 17 - 15 = 2) print last 2
        if not is_full and total > 15:
            print("\n--------  Remaining: --------")
            length = len(sorted_players)
            remaining = length - 15
            last_ones = sorted_players[length - remaining :]
            print_players(last_ones, 0, 0)


file = "players.csv"
(players, gks, fixeds, pivots, base_count) = read_file(file)
pick_teams(players, gks, fixeds, pivots, base_count)
