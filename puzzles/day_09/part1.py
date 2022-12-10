from collections import namedtuple
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


if __name__ == "__main__":
    with open("inputs/day_09.txt") as f:
        data = [line.strip().split() for line in f.readlines()]

    seen = set()
    head = Vector(0, 0)
    tail = Vector(0, 0)

    instructions = [Instruction(row[0], int(row[1])) for row in data]
    for instruction in instructions:
        for step in instruction:
            head += step
            tail = follow(head, tail)
            seen.add(tail)
    print(len(seen))
