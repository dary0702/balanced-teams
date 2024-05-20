import csv
from models.player import Player
from models.position import Position


def read_file(file) -> (list[Player], set[Player], set[Player], set[Player], int):
    result = list[Player]()
    with open(file) as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header.

        base_count = 0
        gks = set[Player]()
        fixeds = set[Player]()
        pivots = set[Player]()
        for row in reader:
            if row[5] == "1":  # is going
                name = row[0]
                rating = float(row[1])
                intensity = float(row[2])
                position = row[3]
                is_base = row[4] == "1"
                result.append(Player(name, rating, intensity, position, is_base))
                if is_base:
                    base_count += 1
                if position == Position.GK:
                    gks.add(name)
                if position == Position.Fixed:
                    fixeds.add(name)
                if position == Position.Pivot:
                    pivots.add(name)

    return (result, gks, fixeds, pivots, base_count)
