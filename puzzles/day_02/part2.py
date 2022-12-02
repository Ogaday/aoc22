from typing import Any


class Move:
    score = 0

    def __add__(self, other: Any) -> int:
        if isinstance(other, int):
            return self.score + other
        if isinstance(other, Move):
            return self.score + other.score
        return NotImplemented

    def __radd__(self, other: int) -> int:
        return self.__add__(other)

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self))

    def __repr__(self) -> str:
        return f"{type(self)}"


class Scissors(Move):
    score = 3

    def __lt__(self, other: Move) -> bool:
        return isinstance(other, Rock)

    def __gt__(self, other: Move) -> bool:
        return isinstance(other, Paper)


class Paper(Move):
    score = 2

    def __lt__(self, other: Move) -> bool:
        return isinstance(other, Scissors)

    def __gt__(self, other: Move) -> bool:
        return isinstance(other, Rock)


class Rock(Move):
    score = 1

    def __lt__(self, other: Move) -> bool:
        return isinstance(other, Paper)

    def __gt__(self, other: Move) -> bool:
        return isinstance(other, Scissors)


def score(their_move, my_move):
    if their_move > my_move:
        score = 0
    elif their_move == my_move:
        score = 3
    else:
        score = 6
    return score


RPS = (Rock(), Paper(), Scissors())


def get_move(their_move: Move, strategy: str):
    """
    Return your move
    """
    # Draw
    if strategy == "Y":
        return their_move
    # Lose
    if strategy == "X":
        for move in RPS:
            if move < their_move:
                return move
    # Win
    if strategy == "Z":
        for move in RPS:
            if move > their_move:
                return move
    raise Exception()


move_table = {
    "A": Rock(),
    "B": Paper(),
    "C": Scissors(),
}


if __name__ == "__main__":
    with open("inputs/day_02.txt") as f:
        data = [row.split() for row in f.readlines()]
    games = [
        (move_table[their_move], get_move(move_table[their_move], strategy))
        for their_move, strategy in data
    ]
    print(sum([score(their_move, my_move) + my_move for their_move, my_move in games]))
