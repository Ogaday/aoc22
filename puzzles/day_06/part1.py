from collections import deque
from collections.abc import Iterable, Iterator


class NoResultFoundError(Exception):
    """
    Unable to find puzzle solution.
    """


def sliding_window(iterable: Iterable, n: int) -> Iterator[deque]:
    window: deque = deque(maxlen=n)
    for item in iterable:
        window.append(item)
        yield window


def find_marker(puzzle: str, n: int) -> int:
    for i, quadruple in enumerate(sliding_window(puzzle, n)):
        if len(set(quadruple)) == n:
            break
    else:
        raise NoResultFoundError("Reached end of input without finding solution")
    return i + 1


if __name__ == "__main__":
    with open("inputs/day_06.txt") as f:
        data = f.read().strip()
    print(find_marker(data, n=4))
