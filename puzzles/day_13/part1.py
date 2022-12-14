import json

from typing import List, Union


def compare(left: Union[List, str], right: Union[List, int]) -> bool:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return
        else:
            return left < right
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    else:
        for l, r in zip(left, right):
            res = compare(l, r)
            if res is not None:
                return res
        if len(right) == len(left):
            return
        else:
            return len(right) > len(left)


if __name__ == "__main__":
    with open("inputs/day_13.txt") as f:
        cases = f.read().split("\n\n")
    cases = [
        (json.loads(case.split()[0]), json.loads(case.split()[1])) for case in cases
    ]
    score = 0
    for i, (left, right) in enumerate(cases):
        score += (i + 1) * compare(left, right)
    print(score)
