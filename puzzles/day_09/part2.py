from collections import namedtuple
from itertools import pairwise
from typing import Union


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


class Instruction:
    steps = {
        "R": Vector(0, 1),
        "U": Vector(1, 0),
        "D": Vector(-1, 0),
        "L": Vector(0, -1),
    }

    def __init__(self, direction: str, num: int):
        self.direction = direction
        self.num = num

    def __iter__(self):
        for _ in range(self.num):
            yield self.steps[self.direction]

    def __repr__(self):
        return f"Instruction(direction={self.direction}, num={self.num})"


def follow(head: Vector, tail: Vector) -> Vector:
    step = get_step(head, tail)
    return tail + step


def get_step(head: Vector, tail: Vector) -> Vector:
    diff = head - tail
    if abs(diff).x > 1 or abs(diff).y > 1:
        step = Vector(x=min(1, max(-1, diff.x)), y=min(1, max(-1, diff.y)))
    else:
        step = Vector(0, 0)
    return step


def plot(knots):
    min_x = min(knot.x for knot in knots)
    min_y = min(knot.y for knot in knots)
    offset = Vector(min_x, min_y)
    knots = [knot - offset for knot in knots]
    max_x = max(knot.x for knot in knots) + 1
    max_y = max(knot.y for knot in knots) + 1
    field = np.zeros((max_x, max_y)).astype("int").astype(str)
    for i, knot in enumerate(knots):
        i = i or "H"
        field[knot] = i
    return field


if __name__ == "__main__":
    with open("inputs/day_09.txt") as f:
        data = [line.strip().split() for line in f.readlines()]

    instructions = [Instruction(row[0], int(row[1])) for row in data]
    seen = set()
    knots = [Vector(0, 0) for _ in range(10)]

    for instruction in instructions:
        for step in instruction:
            knots[0] += step
            for first_i, second_i in pairwise(range(len(knots))):
                knots[second_i] = follow(knots[first_i], knots[second_i])
            seen.add(knots[-1])
    print(len(seen))
