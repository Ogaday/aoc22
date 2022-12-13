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


def draw(cycles):
    pixels = []
    for i, register in enumerate(cycles):
        position = i % 40
        if abs(register - position) <= 1:
            pixels.append("#")
        else:
            pixels.append(".")
    return pixels


if __name__ == "__main__":
    register = {"x": 1}
    with open("inputs/day_10.txt") as f:
        instructions = [line.strip() for line in f.readlines()]
    cycles = execute(register={"x": 1}, instructions=instructions)
    pixels = draw(cycles)
    for start, end in zip(range(0, 220, 40), range(40, 260, 40)):
        print("".join(pixels[start:end]))
