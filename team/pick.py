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

    # shuffle group so the pick order list is different every time
    for group in groups:
        shuffle(group)

    # concat all grouped items
    return list(chain.from_iterable(groups))


def get_best_order_formula(
    sorted_players: list[Player],
    order_formula: list[int],
    gks: set[str],
    fixeds: set[str],pivots: set[str],
) -> list[int]:
    best_order_formula_guess = _full_formula(order_formula)
    max_diff_best = sys.maxsize
    count = 0
    while count < MAX_TRIALS and max_diff_best > 0:
        shuffle(order_formula)
        full_formula = _full_formula(order_formula)
        pick_results = _find_teams(sorted_players, full_formula, gks, fixeds, pivots)
        if pick_results.max_diff <= max_diff_best:
            max_diff_best = pick_results.max_diff
            best_order_formula_guess = full_formula.copy()
        count += 1

    print("--------  Solution: --------\n")
    pick_results = _find_teams(sorted_players, best_order_formula_guess, gks, fixeds,pivots)

    _print_teams(
        pick_results.team1,
        pick_results.team2,
        pick_results.team3,
        pick_results.max_diff,
        pick_results.avgs,
    )
    return best_order_formula_guess


def _full_formula(order_formula: list[int]) -> list[int]:
    # captains order they are already shuffled before so is never the same
    return [1, 2, 3] + order_formula


def _find_teams(
    sorted_players: list[Player],
    order_formula: list[int],
    gks: set[str],
    fixeds: set[str],
    pivots: set[str],
) -> PickResults:
    team1 = _get_team_pick_by_order(sorted_players, order_formula, 1)
    team2 = _get_team_pick_by_order(sorted_players, order_formula, 2)
    team3 = _get_team_pick_by_order(sorted_players, order_formula, 3)

    if _is_not_valid_team(team1, team2, team3, gks, fixeds, pivots):
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
    _print_players(team1, 1, avgs[0])
    _print_players(team2, 2, avgs[1])
    _print_players(team3, 3, avgs[2])

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
) -> bool:
    gk_counts: tuple[int, int, int] = (0, 0, 0)
    fixed_team_counts: tuple[int, int, int] = (0, 0, 0)
    pivot_team_counts: tuple[int, int, int] = (0, 0, 0)

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

        if _has_minimum_player_per_position(fixed_team_counts):
            return True
        if _has_minimum_player_per_position(pivot_team_counts):
            return True

    return False


def _add_teams_count_by_position(
    from1: Player,
    from2: Player,
    from3: Player,
    player_in_position: set[str],
    team_counts: tuple[int, int, int],
) -> tuple[int, int, int]:
    if from1.name in player_in_position:
        team_counts[0] += 1

    if from2.name in player_in_position:
        team_counts[1] += 1

    if from3.name in player_in_position:
        team_counts[2] += 1

    return team_counts


def _has_minimum_player_per_position(position_team_count: tuple[int, int, int]) -> bool:
    """
    determines if a minimun of at least 1 player with this position per team is meet (fixed, pivot, wing)

    :param position_team_count: the count of the player with this position per team

    returs True is condition meet, False otherwise
    """
    if 0 in position_team_count and any(fixed > 1 for fixed in position_team_count):
        return
    return False


def _print_players(players: list[Player], team_number: int, team_rating: float) -> None:
    print(f"({team_rating}) - Team {team_number}")
    for player in players:
        print(f"({player.rating}) - {player.name} - {player.position}")

    print("\n")
