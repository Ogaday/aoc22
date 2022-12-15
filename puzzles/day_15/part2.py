import re
from collections import namedtuple
from typing import Dict, List, Union


class Vector(namedtuple("Vector", ["x", "y"])):
    def __gt__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x > other.x, y=self.y > other.y)

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x - other.x, y=self.y - other.y)

    def __mul__(self, other: Union[int, float]) -> "Vector":
        if isinstance(other, int) or isinstance(other, float):
            return Vector(x=self.x * other, y=self.y * other)
        if isinstance(other, Vector):
            return Vector(x=self.x * other.x, y=self.y * other.y)
        return NotImplemented

    def __abs__(self):
        return Vector(x=abs(self.x), y=abs(self.y))


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_border(sensor, distance_to_beacon, limit=4000000):
    bases = [Vector(1, 1), Vector(-1, 1), Vector(1, -1), Vector(-1, -1)]
    border = set()
    xs = range(distance_to_beacon)
    ys = range(distance_to_beacon, -1, -1)
    for x, y in zip(xs, ys):
        for base in bases:
            new = sensor + base * Vector(x, y)
            if 0 <= new.x <= limit and 0 <= new.y <= limit:
                border.add(new)

    return border


if __name__ == "__main__":
    with open("inputs/day_15.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    coords = [[int(n) for n in re.findall("-{0,1}\d+", line)] for line in lines]
    connections = {Vector(sx, sy): Vector(bx, by) for sx, sy, bx, by in coords}
    dists = {
        sensor: manhattan(sensor, beacon) for sensor, beacon in connections.items()
    }

    viable = set()
    print("Finding viable coordinates")
    for sensor in connections:
        viable |= get_border(sensor, dists[sensor] + 1)
    print(f"Found {len(viable)} viable candidates")
    print("Testing candidates")
    for position in viable:
        for sensor in connections:
            if manhattan(position, sensor) <= dists[sensor]:
                break
        else:
            break
    print(position)
    print(position.x * 4000000 + position.y)
