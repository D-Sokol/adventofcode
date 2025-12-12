import sys
from dataclasses import dataclass  # noqa
from typing import *


PART1 = True


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


@dataclass
class Region:
    width: int
    height: int
    n_presents: list[int]

Shape = list[str]

@dataclass
class Item:
    regions: list[Region]
    shapes: list[Shape]


def read_input(in_stream) -> Item:
    region_blocks = False
    regions: list[Region] = []
    shapes: list[Shape] = []
    current_shape: Shape = []

    for line in in_stream:
        line = line.strip().removesuffix(":")
        if not line:
            continue

        if region_blocks:
            regions.append(parse(line))
        elif line.isdigit():
            if current_shape:
                shapes.append(current_shape)
                current_shape = []
        elif 'x' in line:
            region_blocks = True
            regions.append(parse(line))
            if current_shape:
                shapes.append(current_shape)
                current_shape = []
        else:
            current_shape.append(line)

    assert not current_shape
    return Item(regions=regions, shapes=shapes)


def parse(s: str) -> Region:
    shape, presents_s = s.split(':')
    width, height = map(int, shape.split("x"))
    presents = list(map(int, presents_s.split()))
    return Region(width=width, height=height, n_presents=presents)


def shape_size(shape: Shape) -> int:
    return sum(
        line.count("#")
        for line in shape
    )


# THIS IS EFFING SOLVES THE FIRST PART KURWA
def region_minimal_required_size(shape_sizes: list[int], region: Region) -> bool:
    actual_size = region.height * region.width
    required_size = sum(size * n for size, n in zip(shape_sizes, region.n_presents))
    return actual_size >= required_size


def main(in_stream: TextIO) -> Any:
    data = read_input(in_stream)

    shape_sizes = list(map(shape_size, data.shapes))

    if PART1:
        result = sum(
            region_minimal_required_size(shape_sizes, region)
            for region in data.regions
        )
    else:
        result = "Congratulations"

    return result


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
