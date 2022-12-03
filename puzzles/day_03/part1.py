import string

if __name__ == "__main__":
    with open("inputs/day_03.txt") as f:
        print(
            sum(
                [
                    string.ascii_letters.index(
                        (
                            set(pack[: len(pack) // 2]) & set(pack[len(pack) // 2 :])
                        ).pop()
                    )
                    + 1
                    for pack in f.readlines()
                ]
            )
        )
