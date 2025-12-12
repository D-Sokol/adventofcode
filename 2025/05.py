import sys
from dataclasses import dataclass  # noqa
from typing import *


PART1 = True


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


Item = int | tuple[int, int]



def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)
        else:
            return


def parse(s: str) -> Item:
    if '-' in s:
        i1, i2 = map(int, s.split('-', 1))
        return i1, i2
    return int(s)


def union(range1: tuple[int, int], range2: tuple[int, int]) -> tuple[int, int] | None:
    if range1[0] > range2[0]:
        range1, range2 = range2, range1

    if range2[0] > range1[1] + 1:
        return None

    return range1[0], max(range1[1], range2[1])


def optimize_db(db: list[tuple[int, int]]) -> list[tuple[int, int]]:
    db_collected = []
    for new_range in db:
        db_temp = []
        for exist_range in db_collected:
            if (combined_range := union(new_range, exist_range)) is not None:
                new_range = combined_range
            else:
                db_temp.append(exist_range)
        db_temp.append(new_range)
        db_collected = db_temp
    return db_collected



def main(in_stream: TextIO) -> Any:
    database: list[tuple[int, int]] = list(read_input(in_stream))

    database = optimize_db(database)

    if PART1:
        available: list[int] = list(read_input(in_stream))

        result = 0
        for item_id in available:
            for lo, hi in database:
                if lo <= item_id <= hi:
                    result += 1
                    break

        return result
    else:
        return sum(hi - lo + 1 for lo, hi in database)


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
