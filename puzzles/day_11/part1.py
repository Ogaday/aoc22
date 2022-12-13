from dataclasses import dataclass, field
from math import floor
from typing import Callable, List


@dataclass
class Monkey:
    items: List[int]
    operation: Callable = field(repr=False)
    test: Callable = field(repr=False)
    if_true: int
    if_false: int
    inspections: int = 0

    def inspect(self):
        item = self.items.pop(0)
        print(f"  Monkey inspects and item with a worry level of {item}")
        item = self.operation(item)
        print(f"    Worry level increases to {item}")
        item = int(floor(item / 3))
        print(f"    Monkey gets bored with item. Worry level is divided by 3 to {item}")
        if self.test(item):
            target = self.if_true
            print("    Test passed")
        else:
            print("    Test failed")
            target = self.if_false
        print(f"    Item with worry level {item} if thrown to monkey {target}")
        self.inspections += 1
        return target, item


ops = {
    "+": int.__add__,
    "*": int.__mul__,
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
        return item % quotient == 0

    return test


def make_monkeys(puzzle_input):
    monkeys = []
    for section in puzzle_input.split("\n\n"):
        rows = [row.strip() for row in section.split("\n")]
        starting_items = [int(item.strip(",")) for item in rows[1].split()[2:]]
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
        print(f"Monkey {i}:")
        while monkey.items:
            target, item = monkey.inspect()
            monkeys[target].items.append(item)


if __name__ == "__main__":
    with open("inputs/day_11.txt") as f:
        puzzle = f.read()

    monkeys = make_monkeys(puzzle)
    for _ in range(20):
        round(monkeys)

    top_two = sorted(monkeys, key=lambda m: m.inspections)[-2:]
    print(top_two)
    print(top_two[0].inspections * top_two[1].inspections)
