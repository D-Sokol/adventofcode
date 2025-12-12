import sys
from dataclasses import dataclass  # noqa
from typing import *  # noqa


PART1 = False


def log(*args, **kwargs):
    # return
    return print(*args, file=sys.stderr, **kwargs)


Item = tuple[int, int]


def read_input(in_stream: TextIO) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    c1, c2 = map(int, s.split(','))
    return c1, c2


def inverse_x(items: list[Item]) -> list[Item]:
    return [(-x, y) for x, y in items]

def inverse_y(items: list[Item]) -> list[Item]:
    return [(x, -y) for x, y in items]

def inverse_xy(items: list[Item]) -> list[Item]:
    return [(-x, -y) for x, y in items]


def get_top_left_candidates(items: list[Item], strict: bool = True) -> list[Item]:
    result: list[Item] = []
    items.sort()
    last_x: int | None = None
    minimal_y: int | None = None
    for x, y in items:
        if x == last_x:
            continue
        if minimal_y is None or y < minimal_y or (not strict and y == minimal_y):
            minimal_y = y
            result.append((x, y))

    return result


def get_area(c1: Item, c2: Item) -> int:
    width = abs(c1[0] - c2[0]) + 1
    height = abs(c1[1] - c2[1]) + 1
    return width * height


def make_clockwise_from_top(items: list[Item]) -> list[Item]:
    assert len(items) >= 2
    # Line definitely goes to the right and to the down from this point
    top_left = min(items)
    start_index = items.index(top_left)
    items = items[start_index:] + items[:start_index]
    next_point = items[1]
    if next_point[0] == top_left[0]:
        assert next_point[1] > top_left[1]
        return items
    else:
        assert next_point[1] == top_left[1]
        assert next_point[0] > top_left[0]
        return items[::-1]


def _angle_type(c1: Item, c2: Item, c3: Item) -> tuple[bool, bool, bool] | None:
    if c1[0] == c2[0] == c3[0]:
        return None
    if c1[1] == c2[1] == c3[1]:
        return None

    is_left = c2[1] > c1[1] or c2[1] > c3[1]
    is_top = c2[0] < c1[0] or c2[0] < c3[0]

    v1 = (c2[0] - c1[0], c2[1] - c1[1])
    v2 = (c2[0] - c3[0], c2[1] - c3[1])
    is_inner = v1[0] * v2[1] - v1[1] * v2[0] < 0

    return is_left, is_top, is_inner


def ranges_intersects(r1: tuple[int, int], r2: tuple[int, int]) -> bool:
    return r1[0] <= r2[1] and r2[0] <= r1[1]


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


def minmax(*args: int) -> tuple[int, int]:
    return min(args), max(args)


class RectPolygon:
    values: dict[tuple[int, int], list[tuple[int, int]]]

    def __init__(self, points: list[Item]):
        xs = sorted({x for x, y in points})
        assert len(xs) >= 2
        x_ranges = [(xs[0] - 1_000_000, xs[0] - 1)]
        for x, x_next in zip(xs, xs[1:]):
            x_ranges.append((x, x))
            if x_next > x + 1:
                x_ranges.append((x+1, x_next-1))
        x_ranges.append((xs[-1], xs[-1]))
        x_ranges.append((xs[-1] + 1, xs[-1] + 1_000_000))

        horizontals: list[tuple[int, tuple[int, int]]] = []
        verticals: list[tuple[int, tuple[int, int]]] = []
        for p1, p2 in zip(points, points[1:] + points[:1]):
            if p1[0] == p2[0]:
                # Horizontal
                horizontals.append((p1[0], minmax(p1[1], p2[1])))
            else:
                assert p1[1] == p2[1]
                verticals.append((p1[1], minmax(p1[0], p2[0])))

        ys: dict[tuple[int, int], set[int]] = {xr: set() for xr in x_ranges}
        for y, (x_min, x_max) in verticals:
            for xr in x_ranges:
                # Intersection only in x_min intentionally excluded
                if xr[0] >= x_max or xr[1] < x_min:
                    continue
                ys[xr].add(y)

        self.values = {}
        for xr, y_values in ys.items():
            assert len(y_values) % 2 == 0
            ys_sorted = sorted(y_values)
            self.values[xr] = [(ys_sorted[i], ys_sorted[i+1]) for i in range(0, len(ys_sorted), 2)]

        for x, (y_min, y_max) in horizontals:
            self.values[(x, x)].append((y_min, y_max))

        self.values = {
            k: optimize_db(v) for k, v in self.values.items()
        }

    def contains(self, rect: tuple[Item, Item]) -> bool:
        x0, x1 = sorted(p[0] for p in rect)
        y0, y1 = sorted(p[1] for p in rect)

        for (x_min, x_max), y_ranges in self.values.items():
            if x_min > x1 or x_max < x0:
                continue
            for y_min, y_max in y_ranges:
                if y_min > y1 or y_max < y0:
                    continue
                if y_min <= y0 and y1 <= y_max:
                    break
                else:
                    return False
        return True


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    if PART1:
        top_left_candidates = get_top_left_candidates(data)
        top_right_candidates = inverse_y(get_top_left_candidates(inverse_y(data)))
        bottom_left_candidates = inverse_x(get_top_left_candidates(inverse_x(data)))
        bottom_right_candidates = inverse_xy(get_top_left_candidates(inverse_xy(data)))

        best_area = max(
            max(get_area(c1, c2) for c1 in top_left_candidates for c2 in bottom_right_candidates),
            max(get_area(c1, c2) for c1 in top_right_candidates for c2 in bottom_left_candidates),
        )
    else:
        data = make_clockwise_from_top(data)  # FIXME: not required
        poly = RectPolygon(data)
        # log("Poly", poly.values)
        best_area = -1
        for i, c1 in enumerate(data):
            for c2 in data[i+1:]:
                area = get_area(c1, c2)
                if area <= best_area:
                    continue

                if not poly.contains((c1, c2)):
                    # log("no update", area, c1, c2)
                    continue

                log("update", area, c1, c2)
                best_area = area

    assert best_area > 0
    return best_area


if __name__ == '__main__':
    output = main(sys.stdin)
    print(output)