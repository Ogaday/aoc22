from dataclasses import dataclass
from typing import Any


@dataclass
class Range:
    lower: int
    upper: int

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, int):
            return self.lower <= item <= self.upper
        if isinstance(item, Range):
            return self.lower <= item.lower and item.upper <= self.upper
        return NotImplemented

    @classmethod
    def from_puzzle(cls, spec: str) -> "Range":
        a, b = spec.split("-")
        return cls(int(a), int(b))


if __name__ == "__main__":
    with open("inputs/day_04.txt") as f:
        data = [row.strip().split(",") for row in f.readlines()]
    count = 0
    for spec1, spec2 in data:
        range1, range2 = Range.from_puzzle(spec1), Range.from_puzzle(spec2)
        if range1 in range2 or range2 in range1:
            count += 1
    print(count)
