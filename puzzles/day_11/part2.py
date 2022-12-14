from dataclasses import dataclass, field
from math import floor
from typing import Callable, List


class ModNumber(dict):
    def __init__(self, mapping=None, /, **kwargs):
        if mapping is None:
            mapping = {}
        mapping = {**mapping, **kwargs}
        mapping = {base: value % base for base, value in mapping.items()}
        super().__init__(mapping)

    def __add__(self, other) -> int:
        if isinstance(other, int):
            return ModNumber({base: (value + other) for base, value in self.items()})
        raise NotImplementedError()

    def __mul__(self, other) -> int:
        if isinstance(other, int):
            return ModNumber({base: (value * other) for base, value in self.items()})
        elif isinstance(other, ModNumber):
            return ModNumber(
                {base: (value * other[base]) for base, value in self.items()}
            )
        raise NotImplementedError()

    def is_divisible(self, by: int) -> bool:
        return self[by] == 0


@dataclass
class Monkey:
    items: List[ModNumber]
    operation: Callable = field(repr=False)
    test: Callable = field(repr=False)
    if_true: int
    if_false: int
    inspections: int = 0

    def inspect(self):
        item = self.items.pop(0)
        item = self.operation(item)
        if self.test(item):
            target = self.if_true
        else:
            target = self.if_false
        self.inspections += 1
        return target, item


ops = {
    "+": ModNumber.__add__,
    "*": ModNumber.__mul__,
}


def make_operation(description: str, ops: dict[str, Callable]) -> Callable:
    arg1, op, arg2 = description.split()[-3:]

    def operation(old):
        a, b = arg1, arg2
        if a == "old":
            a = old
        else:
            a = int(arg1)
        if b == "old":
            b = old
        else:
            b = int(arg2)

        return ops[op](a, b)

    operation.__doc__ = description
    return operation


def make_test(description: str):
    quotient = int(description.split()[-1])

    def test(item: int) -> bool:
        return item.is_divisible(quotient)

    return test


def make_monkeys(puzzle_input):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    monkeys = []
    for section in puzzle_input.split("\n\n"):
        rows = [row.strip() for row in section.split("\n")]
        starting_items = [
            ModNumber({prime: int(item.strip(",")) for prime in primes})
            for item in rows[1].split()[2:]
        ]
        operation = make_operation(rows[2], ops)
        test = make_test(rows[3])
        if_true = int(rows[4].split()[-1])
        if_false = int(rows[5].split()[-1])
        monkeys.append(
            Monkey(
                items=starting_items,
                operation=operation,
                test=test,
                if_true=if_true,
                if_false=if_false,
            )
        )
    return monkeys


def round(monkeys):
    for i, monkey in enumerate(monkeys):
        while monkey.items:
            target, item = monkey.inspect()
            monkeys[target].items.append(item)


if __name__ == "__main__":
    with open("inputs/day_11.txt") as f:
        puzzle = f.read()

    monkeys = make_monkeys(puzzle)
    for _ in range(10000):
        round(monkeys)

    top_two = sorted(monkeys, key=lambda m: m.inspections)[-2:]
    print(top_two[0].inspections * top_two[1].inspections)
