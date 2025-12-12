import sys
from dataclasses import dataclass  # noqa
from typing import *


PART1 = False


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


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    assert data
    assert data[0].count("S") == 1
    position = data[0].index("S")
    beams = {position: 1}

    splits = 0
    for row in data[1:]:
        next_beams = {}
        for beam, multiplicity in beams.items():
            if row[beam] == '.':
                next_beams[beam] = next_beams.get(beam, 0) + multiplicity
            elif row[beam] == '^':
                splits += 1
                if beam - 1 >= 0:
                    next_beams[beam - 1] = next_beams.get(beam - 1, 0) + multiplicity
                if beam + 1 < len(row):
                    next_beams[beam + 1] = next_beams.get(beam + 1, 0) + multiplicity
            else:
                raise ValueError(row[beam])

        beams = next_beams

    return splits if PART1 else sum(beams.values())


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)


# >= 385854758324