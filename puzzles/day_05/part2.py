import string
from dataclasses import dataclass
from itertools import zip_longest
from typing import Dict, List


@dataclass
class Instruction:
    source: str
    dest: str
    number: int

    @classmethod
    def from_string(cls, string: str):
        number, source, dest = string.split()[1::2]
        return cls(source=source, dest=dest, number=int(number))


class CargoWorks:
    def __init__(self, stack_labels: List[str]):
        self.stacks: Dict[str, List[str]] = {label: [] for label in stack_labels}

    def add_items(self, row: str):
        for crate, stack in zip(row, self.stacks.values()):
            if crate in string.ascii_letters:
                stack.append(crate)

    def apply(self, instr: Instruction):
        new_stack: List[str] = []
        for _ in range(instr.number):
            new_stack.insert(0, self.stacks[instr.source].pop(-1))
        self.stacks[instr.dest].extend(new_stack)

    def heads(self) -> List[str]:
        return [stack.pop(-1) if stack else " " for stack in self.stacks.values()]

    def __repr__(self) -> str:
        return f"CargoWorks(stack_labels={tuple(self.stacks.keys())})"

    def __str__(self) -> str:
        parts = []
        for row in reversed(list(zip_longest(*self.stacks.values()))):
            parts.append(
                " ".join(
                    [f"[{crate}]" if crate is not None else "   " for crate in row]
                )
            )
        parts.append(" " + "   ".join(self.stacks.keys()) + " ")
        return "\n".join(parts)


if __name__ == "__main__":
    with open("inputs/day_05.txt") as f:
        data = f.read()
    stacks_data, instructions_data = data.split("\n\n")
    rows = [row[1::4] for row in stacks_data.split("\n")[:-1]]
    stack_labels = stacks_data.split("\n")[-1].split()
    instructions = [
        Instruction.from_string(row)
        for row in instructions_data.strip("\n").split("\n")
    ]

    cw = CargoWorks(stack_labels=stack_labels)
    for row in reversed(rows):
        cw.add_items(row)

    for instruction in instructions:
        cw.apply(instruction)

    print(cw)
    print("".join(cw.heads()))
