import sys
from dataclasses import dataclass  # noqa
from typing import *


PART1 = True


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


# FIXME: uncomment this if specific parsing is required
Item = str

# class Item(NamedTuple):
#     pass

# @dataclass
# class Item:
#     pass


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    # FIXME: edit this
    return s


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    result = len(data)

    return result


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
