import sys
from dataclasses import dataclass  # noqa
from typing import *


PART1 = True


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


Item = Sequence[str]


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    return s


def free_neighbours(arr: Sequence[Sequence[str]], i: int, j: int) -> int:
    result = 0
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == dj == 0:
                continue
            ei, ej = i + di, j + dj
            if ei == -1 or ej == -1 \
                or ei >= len(arr) \
                or ej >= len(arr[ei]):
                    continue
            result += int(arr[ei][ej] == '@')
    return result


def main(in_stream: TextIO) -> Any:
    data: list[Sequence[str]]
    data2: list[Sequence[str]]

    data = list(read_input(in_stream))

    result = 0
    iter_result = -1
    while iter_result:
        iter_result = 0
        data2 = []
        for i, line in enumerate(data):
            line2: list[str] = []
            for j, char in enumerate(line):
                if char == "@" and free_neighbours(data, i, j) < 4:
                    iter_result += 1
                    line2.append(".")
                else:
                    line2.append(char)
            data2.append(line2)
        result += iter_result

        if PART1:
            break

    return result


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
