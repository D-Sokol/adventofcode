#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--easy', action='store_true', dest="easy")
group.add_argument('--hard', action='store_false', dest="easy", default=False)
args = parser.parse_args()
EASY = args.easy


data = []
for line in sys.stdin:
    line = line.strip()
    # line = int(line)
    data.append(line)


def extra_item(r: str) -> str:
  n = len(r) // 2
  r1, r2 = r[:n], r[n:]
  item, = set(r1) & set(r2)
  return item


def common_item(r1, r2, r3) -> str:
  item, = set(r1) & set(r2) & set(r3)
  return item


def score(item: str) -> str:
  assert len(item) == 1
  if item.islower():
    return ord(item) - ord("a") + 1
  else:
    return ord(item) - ord("A") + 27

# Some computations
if EASY:
  result = sum(
    score(extra_item(r))
    for r in data
  )
else:
  assert len(data) % 3 == 0
  data = [data[i:i+3] for i in range(0, len(data), 3)]
  result = sum(
    score(common_item(*r123))
    for r123 in data
  )


print(result)

