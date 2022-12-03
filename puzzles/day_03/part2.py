import string

if __name__ == "__main__":
    with open("inputs/day_03.txt") as f:
        packs = [pack.strip() for pack in f.readlines()]
    print(
        sum(
            [
                string.ascii_letters.index((set(pack1) & set(pack2) & set(pack3)).pop())
                + 1
                for pack1, pack2, pack3 in zip(packs[::3], packs[1::3], packs[2::3])
            ]
        )
    )
