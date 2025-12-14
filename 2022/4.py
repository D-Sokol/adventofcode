#!/usr/bin/env python3
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--easy', action='store_true', dest="easy")
group.add_argument('--hard', action='store_false', dest="easy", default=False)
args = parser.parse_args()
EASY = args.easy


def parse_pair(s):
  r1, r2 = s.strip().split(",")
  r1 = tuple(map(int, r1.split("-")))
  r2 = tuple(map(int, r2.split("-")))
  return r1, r2


def is_contained(r1, r2) -> bool:
  return r1[0] >= r2[0] and r1[1] <= r2[1]


def is_overlap(r1, r2):
  return not (r1[0] > r2[1] or r1[1] < r2[0])


data = []
for line in sys.stdin:
    r = parse_pair(line)
    data.append(r)


# Some computations
result = sum(
  is_contained(r1, r2) or is_contained(r2, r1) if EASY else is_overlap(r1, r2)
  for r1, r2 in data
)

print(result)

