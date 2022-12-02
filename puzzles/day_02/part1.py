from typing import Union


class Move:
    score = 0

    def __add__(self, other: Union["Move", int]) -> int:
        if isinstance(other, int):
            return self.score + other
        return self.score + other.score

    def __radd__(self, other: int) -> int:
        return self.score + other

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self))

    def __repr__(self) -> str:
        return f"{type(self)}"


class Scizzors(Move):
    score = 3

    def __lt__(self, other: Move) -> bool:
        return isinstance(other, Rock)

    def __gt__(self, other: Move) -> bool:
        return isinstance(other, Paper)


class Paper(Move):
    score = 2

    def __lt__(self, other: Move) -> bool:
        return isinstance(other, Scizzors)

    def __gt__(self, other: Move) -> bool:
        return isinstance(other, Rock)


class Rock(Move):
    score = 1

    def __lt__(self, other: Move) -> bool:
        return isinstance(other, Paper)

    def __gt__(self, other: Move) -> bool:
        return isinstance(other, Scizzors)


def score(their_move, my_move):
    if their_move > my_move:
        score = 0
    elif their_move == my_move:
        score = 3
    else:
        score = 6
    return score


move_table = {
    "A": Rock(),
    "B": Paper(),
    "C": Scizzors(),
    "X": Rock(),
    "Y": Paper(),
    "Z": Scizzors(),
}


if __name__ == "__main__":
    with open("inputs/day_02.txt") as f:
        games = [
            tuple(map(lambda item: move_table[item], row.split()))
            for row in f.readlines()
        ]
    print(sum([score(their_move, my_move) + my_move for their_move, my_move in games]))
