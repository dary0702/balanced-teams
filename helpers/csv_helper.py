import csv
from models.player import Player
from models.position import Position


def read_file(file) -> (list[Player], set[Player], set[Player]):
    result = list[Player]()
    with open(file) as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header.

        gks = set[Player]()
        fixeds = set[Player]()
        pivots = set[Player]()
        for row in reader:
            if row[4] == "1":  # is going
                name = row[0]
                rating = float(row[1])
                intensity = float(row[2])
                position = row[3]
                result.append(Player(name, rating, intensity, position))
                if position == Position.GK:
                    gks.add(name)
                if position == Position.Fixed:
                    fixeds.add(name)

    return (result, gks, fixeds)
