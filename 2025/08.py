import sys
from dataclasses import dataclass  # noqa
from itertools import count
from typing import *


PART1 = False


def log(*args, **kwargs):
    # return
    return print(*args, file=sys.stderr, **kwargs)


@dataclass
class Item:
    x: int
    y: int
    z: int


def squared_distance(p1: Item, p2: Item) -> int:
    return (p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    x, y, z = map(int, s.split(","))
    return Item(x, y, z)


def connect_components(components: list[set[int]], i: int, j: int) -> None:
    components[i].add(j)
    replaced = components[j]
    components[i].update(replaced)
    for n, component in enumerate(components):
        if component is replaced:
            components[n] = components[i]


def sort_components(components: list[set[int]]) -> list[set[int]]:
    seen_ids = set()
    result = []
    for component in components:
        id_ = id(component)
        if id_ in seen_ids:
            continue
        seen_ids.add(id_)
        result.append(component)
    result.sort(key=len, reverse=True)
    return result


def is_connected(components: list[set[int]], i: int, j: int) -> bool:
    return j in components[i]


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    distances: Sequence[Sequence[int]] = [[squared_distance(p1, p2) for p2 in data] for p1 in data]
    sorted_distances: Sequence[list[tuple[int, int]]] = [
        sorted(
            (distance, j)
            for j, distance in enumerate(distances[i])
            if i != j
        )
        for i, point_distances in enumerate(distances)
    ]
    components: list[set[int]] = [
        {i} for i, _ in enumerate(data)
    ]

    for step in count(1):
        minimal: tuple[int, int, int] | None = None
        for i, sd in enumerate(sorted_distances):
            if not sd:
                continue
            dist, j = sd[0]
            if minimal is None or dist < minimal[0]:
                minimal = dist, i, j
        assert minimal is not None
        _, i, j = minimal
        connect_components(components, i, j)
        # remove used connection
        sorted_distances[i][:] = [(d, node) for (d, node) in sorted_distances[i] if node != j]
        sorted_distances[j][:] = [(d, node) for (d, node) in sorted_distances[j] if node != i]

        # for i, sd in enumerate(sorted_distances):
        #     while sd and is_connected(components, i, sd[0][1]):
        #         del sd[0]

        if PART1 and step == 1000:
            break

        if not PART1 and len(components[0]) == len(data):
            return data[i].x * data[j].x

        if step % 100 == 0:
            log(step, max(map(len, components)), "/", len(data))

    sorted_components = sort_components(components)
    log(sorted_components)
    assert len(sorted_components) >= 3
    c1, c2, c3, *_ = sorted_components
    return len(c1) * len(c2) * len(c3)


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)
