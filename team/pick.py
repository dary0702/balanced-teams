import sys
import random


def find_teams(order_formula, df):
    team1 = _get_team_pick_order(df, order_formula, 1)
    team2 = _get_team_pick_order(df, order_formula, 2)
    team3 = _get_team_pick_order(df, order_formula, 3)

    avgs = [x["rating"].mean() for x in [team1, team2, team3]]
    max_diff = max(avgs) - min(avgs)
    return team1, team2, team3, max_diff


def print_teams(team1, team2, team3, max_diff):
    for x in [team1, team2, team3]:
        x["aux"] = "(" + x["rating"].astype(str) + ")" + " - " + x["player"]

    _print_players(team1.aux.values, 1, team1['rating'].mean())
    _print_players(team2.aux.values, 2, team2['rating'].mean())
    _print_players(team3.aux.values, 3, team3['rating'].mean())

    print('Diff best vs worst team: {:.2f}'.format(max_diff))


def get_best_order_formula(df, order_formula):
    new_order_formula_guess = order_formula.copy()
    best_order_formula_guess = order_formula.copy()
    max_diff_best = sys.maxsize
    max_trials = 5000
    count = 0
    while count < max_trials and max_diff_best > 0:
        random.shuffle(new_order_formula_guess)
        _, _, _, max_diff = find_teams(new_order_formula_guess, df)
        if max_diff <= max_diff_best:
            max_diff_best = max_diff
            best_order_formula_guess = new_order_formula_guess.copy()
        count += 1
    return best_order_formula_guess


def get_shuffled_groups(df):
    groups = [df for _, df in df.groupby('rating')]
    random.shuffle(groups)
    return groups


def _print_players(players, team_number, team_rating):
    print(f"({team_rating}) - Team {team_number}")
    for player in players:
        print(player)

    print('\n')


def _get_team_pick_order(df, order_formula, position):
    team_indexes = [index for index, value in enumerate(
        order_formula) if value == position]

    return df.loc[team_indexes]
