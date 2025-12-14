#!/usr/bin/env python3
import fileinput

# If True, this script solves the first part of the puzzle, the second one otherwise.
EASY = True
# If True, example from the puzzle condition is used as input.
TEST = False
DAY = 1

INPUT_FILE = f'{DAY}{"t" if TEST else ""}.txt'


all_sums = []
current_sum = 0
for line in fileinput.input(INPUT_FILE):
    line = line.strip()
    if not line:
        all_sums.append(current_sum)
        current_sum = 0
        continue
    current_sum += int(line)

all_sums.append(current_sum)

all_sums.sort()
print(sum(all_sums[-3:]))

