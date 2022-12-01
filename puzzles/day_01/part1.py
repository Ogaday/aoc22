if __name__ == "__main__":
    with open("inputs/day_01.txt") as f:
        data = f.read()

    packs = [
        [int(val) for val in row.split("\n")] for row in data.strip("\n").split("\n\n")
    ]

    print(max(sum(pack) for pack in packs))
