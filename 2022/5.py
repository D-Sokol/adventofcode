#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--easy', action='store_true', dest="easy")
group.add_argument('--hard', action='store_false', dest="easy", default=False)
args = parser.parse_args()
EASY = args.easy


stdin = iter(sys.stdin)
stacks = []
for line in stdin:
  if not line.strip().startswith('['):
    break

  line = line[1::4]
  if len(line) > len(stacks):
    stacks.extend([] for _ in range(len(line) - len(stacks)))

  for stack, item in zip(stacks, line):
    if item != ' ':
      stack.append(item)

# reverse all lines
for stack in stacks:
  stack[:] = stack[::-1]


# Ignore two lines
next(stdin)
# next(stdin)

for line in stdin:
  _, count, _, src, _, dest = line.split()
  count, src, dest = map(int, (count, src, dest))
  src -= 1
  dest -= 1

  assert len(stacks[src]) >= count
  items = stacks[src][-count:]
  if EASY:
    items = items[::-1]
  del stacks[src][-count:]
  stacks[dest].extend(items)

# Some computations
result = "".join(
  stack[-1]
  for stack in stacks
)

print(result)

