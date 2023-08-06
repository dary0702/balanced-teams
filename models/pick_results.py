from models.player import Player


class PickResults:
    def __init__(
        self,
        team1: list[Player],
        team2: list[Player],
        team3: list[Player],
        max_diff: float,
        avgs: list[float],
    ):
        self.team1 = team1
        self.team2 = team2
        self.team3 = team3
        self.max_diff = max_diff
        self.avgs = avgs
