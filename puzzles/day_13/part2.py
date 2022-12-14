import json
from functools import cmp_to_key
from typing import List, Union


def compare(left: Union[List, str], right: Union[List, int]) -> bool:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        elif left < right:
            return -1
        else:
            return 1
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    else:
        for l, r in zip(left, right):
            res = compare(l, r)
            if res != 0:
                return res
        if len(right) == len(left):
            return 0
        elif len(right) > len(left):
            return -1
        else:
            return 1


if __name__ == "__main__":
    with open("inputs/day_13.txt") as f:
        cases = [json.loads(case.strip()) for case in f.readlines() if case.strip()]
    two = [[2]]
    six = [[6]]
    cases.append(two)
    cases.append(six)
    res = sorted(cases, key=cmp_to_key(compare))
    print((res.index(two) + 1) * (res.index(six) + 1))
