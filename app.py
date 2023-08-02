import pandas as pd
from team.pick import find_teams, print_teams, get_best_order_formula, get_shuffled_groups


def pick_teams(order_formula):
    # 1 - get the list of players
    df = pd.read_csv('players.csv')

    # 2 - get the players attending
    df = df.loc[df['is_going'] == 1]

    # 3- groups players by same rating and  sort order of the groups
    groups = get_shuffled_groups(df)

    # 4 - appends all the groups into one list,
    df = pd.concat(groups)

    # 5 - sort from best to low rating players,  (drop=True) removes indexes from csv and add new ones
    df = df.sort_values(by='rating', ascending=False).reset_index(drop=True)

    # 6 - gets the best possible order formula if possible
    total = len(df)
    if total < 15:
        print(f'--------  Not enough players:  {total} --------\n')
    else:
        is_full = total == 18
        if is_full:
            order_formula.extend([2, 3, 1])
        best_order_formula = get_best_order_formula(df, order_formula)

        print('--------  Solution: --------\n')
        team1, team2, team3, max_diff = find_teams(best_order_formula, df)
        print_teams(team1, team2, team3, max_diff)

        if not is_full:
            print('\n--------  Remaining: --------')
            # print all the players that dont fit (ex 17 - 15 = 2) print last 2 players
            # remove is going column axis number (0 for rows and 1 for columns.)
            last_ones = df.tail(n=len(df) - 15).drop('is_going', axis=1)
            print(last_ones.to_string(index=False))


order_formula = [
    1, 2, 3,
    3, 2, 1,
    2, 3, 1,
    1, 2, 3,
    3, 2, 1
]
pick_teams(order_formula)
