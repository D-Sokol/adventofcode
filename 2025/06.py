import sys
import operator
from dataclasses import dataclass  # noqa
from functools import reduce
from typing import *


PART1 = True


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


Item = list[int] | list[str]


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    ls = s.split()
    assert ls
    if ls[0] in {"*", "+"}:
        return ls
    return list(map(int, ls))


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    numbers = data[:-1]
    operations = data[-1]

    result = 0
    for i, op_char in enumerate(operations):
        fn = operator.add if op_char == '+' else operator.mul
        item = reduce(fn, [n[i] for n in numbers])
        result += item

    return result


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
