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
        return NotImplemented

    def __abs__(self):
        return Vector(x=abs(self.x), y=abs(self.y))


def covered(sensor, dist_to_beacon, row):
    freedon = dist_to_beacon - abs(sensor.y - row)
    return set(
        Vector(x, row) for x in range(sensor.x - freedon, sensor.x + freedon + 1)
    )


def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


if __name__ == "__main__":
    with open("inputs/day_15.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    coords = [[int(n) for n in re.findall("-{0,1}\d+", line)] for line in lines]

    connections = {Vector(sx, sy): Vector(bx, by) for sx, sy, bx, by in coords}
    seen = set()
    for sensor, beacon in connections.items():
        seen.update(covered(sensor, manhattan(sensor, beacon), 2000000))
    for beacon in connections.values():
        seen.discard(beacon)
    print(len(seen))
