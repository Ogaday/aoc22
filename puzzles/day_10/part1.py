from typing import Dict, List


def execute(register: Dict[str, int], instructions: List[str]) -> List[str]:
    cycles = []
    for instruction in instructions:
        if instruction == "noop":
            cycles.append(register["x"])
        else:
            value = int(instruction.split().pop(-1))
            cycles.append(register["x"])
            cycles.append(register["x"])
            register["x"] += value
    cycles.append(register["x"])
    return cycles


if __name__ == "__main__":
    register = {"x": 1}
    with open("inputs/day_10.txt") as f:
        instructions = [line.strip() for line in f.readlines()]
    cycles = execute(register={"x": 1}, instructions=instructions)
    print(cycles[19:220:40])
    s = slice(19, 220, 40)
    print(cycles[s])
    print(
        sum(
            (i + 1) * value
            for i, value in zip(range(s.start, s.stop, s.step), cycles[s])
        )
    )
    print(sum((i + 1) * value for i, value in list(enumerate(cycles))[19:220:40]))
