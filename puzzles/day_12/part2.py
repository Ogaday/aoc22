import string
import sys
from collections import namedtuple
from typing import Callable, Dict, List, Union
import numpy as np


class Vector(namedtuple("Vector", ["x", "y"])):
    def __add__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(x=self.x - other.x, y=self.y - other.y)


def next_steps(position: Vector, maze: np.array) -> Vector:
    steps = [Vector(0, 1), Vector(1, 0), Vector(0, -1), Vector(-1, 0)]
    for step in steps:
        new = position + step
        if (
            (0 <= new.x < maze.shape[0])
            and (0 <= new.y < maze.shape[1])
            and (maze[new] - maze[position] >= -1)
        ):
            yield new


def get_path_score(position: Vector, paths: Dict[Vector, Vector]):
    if paths[position] is None:
        return 0
    return 1 + get_path_score(paths[position], paths)


def bfs(start: Vector, maze: np.array) -> Dict:
    nodes = [start]
    paths = {start: None}
    while nodes:
        current = nodes.pop(0)
        for step in next_steps(current, maze):
            if step not in paths:
                paths[step] = current
                nodes.append(step)
    return paths


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    with open("inputs/day_12.txt") as f:
        maze = [list(row.strip()) for row in f.readlines()]
    height_map = {letter: i + 1 for i, letter in enumerate(string.ascii_lowercase)}
    new_maze = np.empty((len(maze), len(maze[0])))
    print(new_maze.shape)
    starts = []
    for i, row in enumerate(maze):
        for j, column in enumerate(row):
            if column == "S":
                start = Vector(i, j)
                starts.append(start)
                maze[i][j] = "a"
            if column == "E":
                target = Vector(i, j)
                maze[i][j] = "z"
            if column == "a":
                starts.append(Vector(i, j))
            new_maze[i, j] = height_map[maze[i][j]]
    paths = bfs(target, new_maze)
    print(min(get_path_score(start, paths) for start in starts if start in paths))
