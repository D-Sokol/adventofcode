import sys
from dataclasses import dataclass  # noqa
from functools import partial
from typing import *


PART1 = True


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


Item = str


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    return s


def _argmax(s: str, offset: int = 0) -> tuple[int, str]:
    c = max(s)
    return s.index(c) + offset, c


def find_max(s: str, n_characters: int) -> str:
    if len(s) < n_characters:
        raise ValueError

    result = []
    start_pos = 0
    for i in range(n_characters):
        # this many last characters cannot be used at this iteration
        untouchable = n_characters - i - 1
        # `:-0` does not remove prefix of size 0, so we must provide None instead
        limit = -untouchable if untouchable != 0 else None

        pos, char = _argmax(s[start_pos:limit], offset=start_pos)
        result.append(char)
        start_pos = pos + 1

    return "".join(result)


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    n_batteries = 2 if PART1 else 12
    result = sum(map(int, map(partial(find_max, n=n_batteries), data)))

    return result


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
