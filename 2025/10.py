import sys
from dataclasses import dataclass  # noqa
from typing import *

import numpy as np
from scipy.optimize import linprog


PART1 = False


def log(*args, **kwargs):
    return print(*args, file=sys.stderr, **kwargs)


@dataclass
class Item:
    target: int
    buttons: set[int]
    # n_bits: int
    raw_buttons: set[tuple[int, ...]]

    joltage: list[int]

    @property
    def n_bits(self) -> int:
        return len(self.joltage)


def read_input(in_stream) -> Iterator[Item]:
    for line in in_stream:
        line = line.strip()
        if line:
            yield parse(line)


def parse(s: str) -> Item:
    buttons_s: list[str]
    target_s, *buttons_s, joltage_s = s.split()
    target_s = target_s.removeprefix("[").removesuffix("]")
    target = 0
    for char in reversed(target_s):
        target <<= 1
        target += (char == "#")

    buttons = set()
    raw_buttons = set()
    for button_s in buttons_s:
        button = 0
        raw_button = []
        button_s = button_s.removeprefix("(").removesuffix(")")
        for index in map(int, button_s.split(",")):
            raw_button.append(index)
            button += 1 << index
        buttons.add(button)
        raw_buttons.add(tuple(raw_button))

    joltage_s = joltage_s.removeprefix("{").removesuffix("}")
    joltage = list(map(int, joltage_s.split(",")))
    assert len(target_s) == len(joltage)

    return Item(target=target, buttons=buttons, joltage=joltage, raw_buttons=raw_buttons)


def solve_machine_1(machine: Item) -> int:
    seen = {0}
    history: list[tuple[int, int]] = [(0, 0)]
    for value, step in history:
        seen.add(value)
        for button in machine.buttons:
            next_value = value ^ button
            if next_value == machine.target:
                log("solved in", step+1)
                return step + 1
            elif next_value in seen:
                continue
            history.append((next_value, step + 1))
            seen.add(next_value)

    raise ValueError("Unreachable")


State = tuple[int, ...]
Indexes = tuple[int, ...]


def is_failed(machine: Item, state: State) -> bool:
    for curr, desired in zip(state, machine.joltage):
        if curr > desired:
            return True
    return False


def max_presses(machine: Item, state: State, button: Indexes) -> int:
    n_left = min(
        machine.joltage[index] - state[index]
        for index in button
    )
    return max(0, n_left)


def apply_button(button: Indexes, state: State, times: int = 1) -> State:
    state = list(state)
    for index in button:
        state[index] += times
    return tuple(state)


def solve_machine_2(machine: Item, initial: State | None = None) -> int:
    n_b = len(machine.raw_buttons)
    n_i = len(machine.joltage)
    conditions = np.zeros((n_i, n_b), dtype=int)
    for i, button in enumerate(machine.raw_buttons):
        for index in button:
            conditions[index, i] = 1

    solution = linprog(
        c=np.ones(n_b, dtype=int),
        A_eq=conditions,
        b_eq=machine.joltage,
        integrality=1,  # only integer values
    )
    return solution.x.sum()


def main(in_stream: TextIO) -> Any:
    data = list(read_input(in_stream))

    solve_machine = solve_machine_1 if PART1 else solve_machine_2
    result = sum(map(solve_machine, data))

    return result


if __name__ == '__main__':
    output = main(sys.stdin)

    print(output)
