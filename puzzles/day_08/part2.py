from enum import Enum
from collections import namedtuple

import numpy as np


class Vector(namedtuple("Vector", ["x", "y"])):
    def __add__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def strictly_gte(self, other: "Vector") -> bool:
        return (self.x >= other.x) and (self.y >= other.y)

    def strictly_gt(self, other: "Vector") -> bool:
        return (self.x > other.x) and (self.y > other.y)


class Compass(Enum):
    N = Vector(1, 0)
    E = Vector(0, 1)
    S = Vector(-1, 0)
    W = Vector(0, -1)


def line_of_sight(position: Vector, step: Vector, forest: np.array) -> int:
    origin = Vector(0, 0)
    extent = Vector(*forest.shape)
    height = forest[position]
    position += step
    score = 0
    while position.strictly_gte(origin) and extent.strictly_gt(position):
        score += 1
        if forest[position] >= height:
            break
        position += step
    return score


if __name__ == "__main__":
    with open("inputs/day_08.txt") as f:
        data = [[int(i) for i in row.strip()] for row in f.readlines()]
    forest = np.array(data)

    scores = {
        Compass.N: np.empty(forest.shape),
        Compass.E: np.empty(forest.shape),
        Compass.S: np.empty(forest.shape),
        Compass.W: np.empty(forest.shape),
    }
    for bearing, score_arr in scores.items():
        for i in range(forest.shape[0]):
            for j in range(forest.shape[1]):
                score_arr[i, j] = line_of_sight(
                    position=Vector(i, j), step=bearing.value, forest=forest
                )
    total_score = (
        scores[Compass.N] * scores[Compass.E] * scores[Compass.S] * scores[Compass.W]
    )
    print(total_score.max())
    print(forest)
