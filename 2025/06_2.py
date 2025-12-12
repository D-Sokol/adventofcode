import sys
import operator
from dataclasses import dataclass  # noqa
from functools import reduce
from typing import *


PART1 = False


@dataclass
class Item:
    op: str
    numbers: list[int]


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


def read_input(in_stream) -> Iterator[Item]:
    lines = []
    for line in in_stream:
        line = line.rstrip("\n")
        if line:
            lines.append(line)

    assert lines
    num_lines = lines[:-1]
    op_line = lines[-1]

    assert num_lines
    op: str | None = None
    numbers = []
    for i, op_char in enumerate(op_line):
        if not op and op_char != ' ':
            op = op_char

        number = "".join(line[i] for line in num_lines).replace(" ", "")
        if number:
            numbers.append(int(number))
        else:
            assert op
            yield Item(op, numbers)
            op = None
            numbers = []

    if op and numbers:
        yield Item(op, numbers)


def solve(item: Item) -> int:
    fn = operator.add if item.op == '+' else operator.mul
    result = reduce(fn, item.numbers)
    return result


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    log(data)

    return sum(map(solve, data))


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
