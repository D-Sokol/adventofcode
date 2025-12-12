import sys
from dataclasses import dataclass  # noqa
from typing import *


PART1 = True


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


Item = tuple[int, int]


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            for term in line.split(","):
                yield parse(term)


def parse(s: str) -> Item:
    s1, s2 = map(int, s.split('-'))
    return s1, s2


def is_invalid(x: int) -> bool:
    s = str(x)
    l = len(s)
    if PART1:
        if l % 2 == 0 and s == s[l//2:] * 2:
            return True
    else:
        for subl in range(1, l):
            if l % subl == 0 and s == s[:subl] * (l // subl):
                return True

    return False

def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    result = 0
    for s1, s2 in data:
        for i in range(s1, s2 + 1):
            if is_invalid(i):
                result += i

    return result


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
