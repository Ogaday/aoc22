from collections import namedtuple
from itertools import pairwise
from typing import Any, List


class Vector(namedtuple("Vector", ["x", "y"])):
    def __add__(self, other: Any) -> "Vector":
        if isinstance(other, Vector):
            return Vector(x=self.x + other.x, y=self.y + other.y)
        elif isinstance(other, int):
            return Vector(x=self.x + other, y=self.y + other)
        return NotImplemented

    def __sub__(self, other: Any) -> "Vector":
        if isinstance(other, Vector):
            return Vector(x=self.x - other.x, y=self.y - other.y)
        elif isinstance(other, int):
            return Vector(x=self.x + other, y=self.y + other)
        return NotImplemented

    def __mul__(self, other: Any) -> "Vector":
        if isinstance(other, Vector):
            return Vector(x=self.x * other.x, y=self.y * other.y)
        elif isinstance(other, int):
            return Vector(x=self.x * other, y=self.y * other)
        return NotImplemented

    def unit_step(self) -> "Vector":
        return Vector(min(1, max(self.x, -1)), min(1, max(self.y, -1)))


def parse_walls(rows: List[str]) -> List[List[Vector]]:
    return [
        [
            Vector(int(coord.split(",")[0]), int(coord.split(",")[1]))
            for coord in row.split(" -> ")
        ]
        for row in data
    ]


if __name__ == "__main__":
    with open("inputs/day_14.txt") as f:
        data = [line.strip() for line in f.readlines()]

    walls = parse_walls(data)

    seen = set()
    for wall in walls:
        for start, stop in pairwise(wall):
            step = (stop - start).unit_step()
            position = start
            while position != stop:
                seen.add(position)
                position += step
            seen.add(stop)

    max_depth = max([coord.y for coord in seen])

    steps = [Vector(0, 1), Vector(-1, 1), Vector(1, 1)]
    sand_counter = 0
    while True:
        sand = Vector(500, 0)
        moved = False
        while sand.y < max_depth:
            for step in steps:
                if sand + step not in seen:
                    sand += step
                    break
            else:
                seen.add(sand)
                sand_counter += 1
                break
        else:
            break
        continue
    print(sand_counter)
