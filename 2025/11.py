import sys
from dataclasses import dataclass  # noqa
from typing import *

PART1 = False


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


Item = tuple[str, list[str]]


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    src, *dsts = s.split()
    src = src.strip(':')
    return src, dsts


class MultiInt:
    values: tuple[int, int, int, int]

    def __init__(self, v: Any = 0):
        if isinstance(v, MultiInt):
            self.values = v.values
        elif isinstance(v, int):
            self.values = v, 0, 0, 0
        elif isinstance(v, tuple):
            assert all(isinstance(x, int) for x in v) and len(v) == 4
            self.values = cast(tuple[int, int, int, int], v)
        else:
            raise ValueError

    def __add__(self, other):
        other = MultiInt(other)
        vs = cast(tuple[int, int, int, int], tuple(v1 + v2 for v1, v2 in zip(self.values, other.values)))
        return MultiInt(vs)

    def advance_fft(self) -> None:
        a, b, c, d = self.values
        self.values = 0, 0, a + c, b + d

    def advance_dac(self) -> None:
        a, b, c, d = self.values
        self.values = 0, a + b, 0, c + d

    def __str__(self) -> str:
        return f"MInt({self.values})"


def main(in_stream: TextIO) -> int:
    target = "you" if PART1 else "svr"

    data = list(read_input(in_stream))
    graph = dict(data)

    n_paths: dict[str, MultiInt] = {"out": MultiInt(1)}
    while True:
        # This cycle may be optimized by tracking recently added nodes and precomputed src for them
        for src, dsts in graph.items():
            if src in n_paths:
                continue

            if all(dst in n_paths for dst in dsts):
                s = sum((n_paths[dst] for dst in dsts), MultiInt(0))
                if src == "fft":
                    s.advance_fft()
                elif src == "dac":
                    s.advance_dac()

                if src == target:
                    return sum(s.values) if PART1 else s.values[-1]

                n_paths[src] = s

        # Infinite cycle happens if target is unreachable or there are cycle and therefore answer is also infinite.
        # I ignore these cases.


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
