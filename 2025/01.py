import sys
from dataclasses import dataclass  # noqa
from typing import *

PART1 = False

@dataclass
class Item:
    dist: int
    left: bool


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    left = s.startswith("L")
    dist = int(s[1:])
    return Item(dist=dist, left=left)


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    pos = 50
    result = 0
    for item in data:
        if PART1:
            pos += item.dist * (-1 if item.left else 1)
            if pos % 100 == 0:
                result += 1
        else:
            diff = (-1 if item.left else 1)
            for _ in range(item.dist):
                pos += diff
                if pos % 100 == 0:
                    result += 1

    return result


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
