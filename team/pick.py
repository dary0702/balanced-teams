import sys
from random import shuffle
from itertools import groupby, chain
from statistics import mean
from models.pick_results import PickResults
from models.player import Player


MAX_TRIALS = 50000


def get_players_order_by_rating(assisting_players: list[Player]) -> list[Player]:
    # assisting_players has to be sorted before groupby
    sorted_players = sorted(
        assisting_players, key=lambda player: player.rating, reverse=True
    )

    groups = [
        list(group)
        for _, group in groupby(sorted_players, key=lambda player: player.rating)
    ]

    # concat all grouped items
    return list(chain.from_iterable(groups))


def get_best_order_formula(
    sorted_players: list[Player],
    order_formula: list[int],
    gks: set[str],
    fixeds: set[str],
    pivots: set[str],
    base_count: int,
) -> list[int]:
    best_order_formula_guess = order_formula.copy()
    all_formulas = [best_order_formula_guess]
    max_diff_best = sys.maxsize
    count = 0
    while count < MAX_TRIALS:
        shuffle(order_formula)
        pick_results = _find_teams(
            sorted_players, order_formula, gks, fixeds, pivots, base_count
        )
        if pick_results.max_diff <= max_diff_best:
            best_order_formula_guess = order_formula.copy()
            if pick_results.max_diff < max_diff_best:
                max_diff_best = pick_results.max_diff
                all_formulas = [best_order_formula_guess]
            else:
                all_formulas.append(best_order_formula_guess)

        count += 1

    print("--------  Solution: --------\n")
    shuffle(all_formulas)
    pick_results = _find_teams(
        sorted_players, all_formulas[0], gks, fixeds, pivots, base_count
    )

    _print_teams(
        pick_results.team1,
        pick_results.team2,
        pick_results.team3,
        pick_results.max_diff,
        pick_results.avgs,
    )

    return all_formulas


def _find_teams(
    sorted_players: list[Player],
    order_formula: list[int],
    gks: set[str],
    fixeds: set[str],
    pivots: set[str],
    base_count: int,
) -> PickResults:
    team1 = _get_team_pick_by_order(sorted_players, order_formula, 1)
    team2 = _get_team_pick_by_order(sorted_players, order_formula, 2)
    team3 = _get_team_pick_by_order(sorted_players, order_formula, 3)

    if _is_not_valid_team(team1, team2, team3, gks, fixeds, pivots, base_count):
        return PickResults([], [], [], sys.maxsize, [])

    avgs = [mean(map(lambda x: x.rating, x)) for x in [team1, team2, team3]]
    max_diff = max(avgs) - min(avgs)

    return PickResults(team1, team2, team3, max_diff, avgs)


def _print_teams(
    team1: list[Player],
    team2: list[Player],
    team3: list[Player],
    max_diff: float,
    avgs: list[float],
) -> None:
    print_players(team1, 1, avgs[0])
    print_players(team2, 2, avgs[1])
    print_players(team3, 3, avgs[2])

    print("Diff best vs worst team: {:.2f}".format(max_diff))


def _get_team_pick_by_order(
    sorted_players: list[Player], order_formula: list[int], position
) -> list[Player]:
    team_indexes = [
        index for index, value in enumerate(order_formula) if value == position
    ]

    return [sorted_players[i] for i in team_indexes]


def _is_not_valid_team(
    team1: list[Player],
    team2: list[Player],
    team3: list[Player],
    gks: set[str],
    fixeds: set[str],
    pivots: set[str],
    base_count: int,
) -> bool:
    gk_counts: list[int] = [0, 0, 0]
    fixed_team_counts: list[int] = [0, 0, 0]
    pivot_team_counts: list[int] = [0, 0, 0]
    base_team_counts: list[int] = [0, 0, 0]

    for from1, from2, from3 in zip(team1, team2, team3):
        # not more than 1 gk per team
        if from1.name in gks:
            gk_counts[0] += 1
            if gk_counts[0] > 1:
                return True

        if from2.name in gks:
            gk_counts[1] += 1
            if gk_counts[1] > 1:
                return True

        if from3.name in gks:
            gk_counts[2] += 1
            if gk_counts[2] > 1:
                return True

        _add_teams_count_by_position(from1, from2, from3, fixeds, fixed_team_counts)

        _add_teams_count_by_position(from1, from2, from3, pivots, pivot_team_counts)

        _add_is_base_count(from1, from2, from3, base_team_counts)

        if _has_minimum_player_per_position(fixed_team_counts):
            return True
        if _has_minimum_player_per_position(pivot_team_counts):
            return True

    if base_count % 3 == 0:
        if not all(x == base_team_counts[0] for x in base_team_counts):
            return True

    return False


def _add_teams_count_by_position(
    from1: Player,
    from2: Player,
    from3: Player,
    player_in_position: set[str],
    team_counts: list[int],
):
    if from1.name in player_in_position:
        team_counts[0] += 1

    if from2.name in player_in_position:
        team_counts[1] += 1

    if from3.name in player_in_position:
        team_counts[2] += 1


def _add_is_base_count(
    from1: Player,
    from2: Player,
    from3: Player,
    team_counts: list[int],
):
    if from1.is_base == True:
        team_counts[0] += 1

    if from2.is_base:
        team_counts[1] += 1

    if from3.is_base:
        team_counts[2] += 1


def _has_minimum_player_per_position(position_team_count: list[int]) -> bool:
    """
    determines if a minimun of at least 1 player with this position per team is meet (fixed, pivot, wing)

    :param position_team_count: the count of the player with this position per team

    returs True is condition meet, False otherwise
    """
    if 0 in position_team_count and any(fixed > 1 for fixed in position_team_count):
        return True
    return False


def print_players(players: list[Player], team_number: int, team_rating: float) -> None:
    if not team_number == 0:
        print(f"({team_rating}) - Team {team_number}")
    for player in players:
        player_to_print = f"({player.rating}) - {player.name} - {player.position}"
        print(
            player_to_print
            if not player.is_base
            else player_to_print + "                                       - Base"
        )

    print("\n")
