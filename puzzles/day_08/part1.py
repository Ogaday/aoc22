import numpy as np


def reflect(forest) -> np.array:
    return forest[:, ::-1]


def rolling_hidden(forest) -> np.array:
    hidden = np.ones(forest.shape).astype(bool)
    rolling_max = -1 * np.ones((forest.shape[0]))
    for col in range(forest.shape[1]):
        hidden[:, col] &= rolling_max >= forest[:, col]
        rolling_max = forest[:, : col + 1].max(axis=1)
    return hidden


if __name__ == "__main__":
    with open("inputs/day_08.txt") as f:
        data = [[int(i) for i in row.strip()] for row in f.readlines()]
    forest = np.array(data)
    hidden_ltr = rolling_hidden(forest)
    hidden_rtl = reflect(rolling_hidden(reflect(forest)))
    hidden_ttb = np.transpose(rolling_hidden(np.transpose(forest)))
    hidden_btt = np.transpose(reflect(rolling_hidden(reflect(np.transpose(forest)))))
    hidden = hidden_ltr & hidden_rtl & hidden_ttb & hidden_btt
    print(
        forest.shape[0] * forest.shape[1]
        - (hidden_ltr & hidden_rtl & hidden_ttb & hidden_btt).sum()
    )
