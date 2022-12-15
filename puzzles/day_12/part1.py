import string
import sys
from collections import namedtuple
from typing import Dict, List, Union
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
        if (0 <= new.x < maze.shape[0]) and (0 <= new.y < maze.shape[1]) and (maze[new] - maze[position] <= 1):
            yield new


def get_path_score(position: Vector, paths: Dict[Vector, Vector]):
    if paths[position] is None:
        return 0
    return 1 + get_path_score(paths[position], paths)


def find_path(position, target, maze, paths) -> Dict[Vector, Vector]:
    cont = False
    for new_pos in next_steps(position, maze):
        if new_pos not in paths:
            paths[new_pos] = position
            cont = True
        elif get_path_score(position=position, paths=paths) + 1 < get_path_score(position=new_pos, paths=paths):
            paths[new_pos] = position
            cont = True

        if new_pos != target and cont:
            find_path(new_pos, target, maze, paths)

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    with open("inputs/day_12.txt") as f:
        maze = [list(row.strip()) for row in f.readlines()]
    height_map = {letter: i + 1 for i, letter in enumerate(string.ascii_lowercase)}
    new_maze = np.empty((len(maze), len(maze[0])))
    print(new_maze.shape)
    for i, row in enumerate(maze):
        for j, column in enumerate(row):
            if column == "S":
                start = Vector(i, j)
                maze[i][j] = 'a'
            if column == "E":
                target = Vector(i, j)
                maze[i][j] = 'z'
            new_maze[i, j] = height_map[maze[i][j]]
    paths = {start: None}
    find_path(start, target, new_maze, paths)
    print(get_path_score(target, paths))
