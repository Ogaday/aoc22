from collections import Counter
from dataclasses import dataclass, field
from functools import cache, reduce
from typing import Callable, List

from tqdm import tqdm


class Factors(Counter):
    def __repr__(self):
        return f"Factors({dict(self.items())})"

    def __add__(self, other) -> "Factors":
        if isinstance(other, Factors):
            common_factors = Factors(self & other)
            return common_factors * Factors.from_int(
                int(self / common_factors) + int(other / common_factors)
            )
        raise NotImplementedError()

    def __mul__(self, other) -> "Factors":
        if isinstance(other, Factors):
            return Factors(super().__add__(other))
        raise NotImplementedError()

    def __truediv__(self, other) -> "Factors":
        if isinstance(other, Factors):
            return Factors(super().__sub__(other))
        raise NotImplementedError()

    def __int__(self):
        return reduce(
            int.__mul__, [factor**power for factor, power in self.items()], 1
        )

    @classmethod
    @cache
    def from_int(cls, n: int) -> "Factors":
        for i in range(2, n // 2 + 1):
            if n % i == 0:
                # found a factor
                return cls({i: 1}) * cls.from_int(int(n / i))
        else:
            return cls({n: 1})


@dataclass
class Monkey:
    items: List[Factors]
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
    "+": Factors.__add__,
    "*": Factors.__mul__,
}


def make_operation(description: str, ops: dict[str, Callable]) -> Callable:
    arg1, op, arg2 = description.split()[-3:]
    if arg1 != "old":
        arg1 = Factors.from_int(int(arg1))
    if arg2 != "old":
        arg2 = Factors.from_int(int(arg2))

    def operation(old):
        a, b = arg1, arg2
        if a == "old":
            a = old
        if b == "old":
            b = old

        return ops[op](a, b)

    operation.__doc__ = description
    return operation


def make_test(description: str):
    quotient = int(description.split()[-1])

    def test(item: Factors) -> bool:
        return item[quotient] > 0

    return test


def make_monkeys(puzzle_input):
    monkeys = []
    for section in puzzle_input.split("\n\n"):
        rows = [row.strip() for row in section.split("\n")]
        starting_items = [
            Factors.from_int(int(item.strip(","))) for item in rows[1].split()[2:]
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
    with open("inputs/day_11_.txt") as f:
        puzzle = f.read()

    monkeys = make_monkeys(puzzle)
    for monkey in monkeys:
        print(monkey)
    for _ in range(10000):
        round(monkeys)

    top_two = sorted(monkeys, key=lambda m: m.inspections)[-2:]
    print(top_two[0].inspections * top_two[1].inspections)
